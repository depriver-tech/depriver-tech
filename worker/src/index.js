// depriver.tech engagement API on Cloudflare's free tier (Workers + D1 + Workers AI + Turnstile).
//
// Public
//   GET    /stats/:slug                 { views, likes, comments }
//   GET    /stats?slugs=a,b             { a: {...}, b: {...} }
//   POST   /view/:slug                  count a view (once per visitor per day)
//   POST   /like/:slug · DELETE         like / unlike (once per visitor)
//   GET    /comments/:slug              published comments
//   POST   /comments/:slug              { name, body, parent?, token?, website? }  -> new comment
//   POST   /contact                     { name, contact, body, token?, website? }
//   POST   /ask                         { question, history? }  -> { answer }  (Workers AI)
// Owner (Authorization: Bearer ADMIN_KEY)
//   GET    /admin/comments?status=pending|published|hidden|all
//   POST   /admin/comments/:id/(publish|hide)   DELETE /admin/comments/:id
//   POST   /admin/comments/:slug/reply  { body, parent? }  -> reply as the owner
//   GET    /admin/messages              POST /admin/messages/:id/read
//
// Secrets (wrangler secret put): SALT, ADMIN_KEY, optional TURNSTILE_SECRET, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

import { socialAdmin, finishOAuth, runScheduler } from './social/index.js';

const SLUG = /^[a-z0-9][a-z0-9-]{0,119}$/;
const OWNER_NAME = "Privatus Cosmas";

export default {
  async scheduled(controller, env, ctx) {
    ctx.waitUntil(runScheduler(env));
  },
  async fetch(request, env, ctx) {
    const origin = request.headers.get("Origin") || "";
    const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
    const cors = {
      "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0] || "*",
      "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
      "Access-Control-Max-Age": "86400",
      Vary: "Origin",
    };
    const json = (data, status = 200) =>
      new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...cors } });
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });

    const url = new URL(request.url);
    const parts = url.pathname.split("/").filter(Boolean);
    const [route, a, b] = parts;
    const method = request.method;

    try {
      if (/^\/social\/oauth\/(instagram|linkedin)\/callback$/.test(url.pathname) && method === 'GET') {
        return await finishOAuth(request, env);
      }
      // ── owner endpoints ─────────────────────────────────────
      if (route === "admin") {
        const key = (request.headers.get("Authorization") || "").replace(/^Bearer\s+/i, "");
        const ownerAuthorized = env.ADMIN_KEY && await safeEqual(key, env.ADMIN_KEY);
        const publisherAuthorized = a === 'social' && env.PUBLISHER_KEY && await safeEqual(key, env.PUBLISHER_KEY);
        if (!ownerAuthorized && !publisherAuthorized) return json({ error: "unauthorized" }, 401);
        if (a === 'social') {
          if (origin && !allowed.includes(origin)) return json({ error:'forbidden' },403);
          if (Number(request.headers.get('Content-Length') || 0) > 32768) return json({ error:'Request too large.' },413);
          return await socialAdmin(request,env,json);
        }
        return await admin(env, method, a, b, parts[3], url, request, json);
      }

      // ── public reads ────────────────────────────────────────
      if (route === "stats" && method === "GET") {
        if (!a) {
          const slugs = (url.searchParams.get("slugs") || "").split(",").filter((s) => SLUG.test(s)).slice(0, 60);
          const out = {};
          for (const s of slugs) out[s] = await stats(env, s);
          return json(out);
        }
        if (!SLUG.test(a)) return json({ error: "bad slug" }, 400);
        return json(await stats(env, a));
      }
      if (route === "comments" && method === "GET") {
        if (!SLUG.test(a || "")) return json({ error: "bad slug" }, 400);
        const { results } = await env.DB.prepare(
          "SELECT id, parent_id AS parent, name, body, is_owner AS owner, created_at AS at FROM comments WHERE slug = ?1 AND status = 'published' ORDER BY id",
        ).bind(a).all();
        return json({ comments: results });
      }

      // ── writes: only from the site itself ───────────────────
      if (origin && allowed.length && !allowed.includes(origin)) return json({ error: "forbidden" }, 403);
      const visitor = await visitorId(request, env);

      if (route === "view" && method === "POST" && SLUG.test(a || "")) {
        await env.DB.prepare("INSERT OR IGNORE INTO views (slug, visitor, day) VALUES (?1, ?2, ?3)").bind(a, visitor, today()).run();
        return json(await stats(env, a));
      }
      if (route === "like" && SLUG.test(a || "")) {
        if (method === "POST") await env.DB.prepare("INSERT OR IGNORE INTO likes (slug, visitor) VALUES (?1, ?2)").bind(a, visitor).run();
        else if (method === "DELETE") await env.DB.prepare("DELETE FROM likes WHERE slug = ?1 AND visitor = ?2").bind(a, visitor).run();
        else return json({ error: "method" }, 405);
        return json(await stats(env, a));
      }

      if (route === "comments" && method === "POST") {
        if (!SLUG.test(a || "")) return json({ error: "bad slug" }, 400);
        const body = await readJson(request);
        if (body.website) return json({ ok: true, status: "published" }); // honeypot: pretend success
        const name = clean(body.name, 60);
        const text = clean(body.body, 2000, true);
        if (name.length < 2 || text.length < 2) return json({ error: "Please add your name and a comment." }, 400);
        if (!(await turnstile(env, body.token, request))) return json({ error: "Please confirm you're human and try again." }, 400);
        if (!(await limit(env, visitor, "comment", 6, 10))) return json({ error: "You're commenting very fast. Please wait a few minutes." }, 429);
        let parent = Number(body.parent) || null;
        if (parent) {
          const p = await env.DB.prepare("SELECT id, parent_id FROM comments WHERE id = ?1 AND slug = ?2 AND status = 'published'").bind(parent, a).first();
          parent = p ? p.parent_id || p.id : null; // keep threads one level deep
        }
        const links = (text.match(/https?:\/\/|www\./gi) || []).length;
        const status = links > 0 || looksSpammy(text + " " + name) ? "pending" : "published";
        const row = await env.DB.prepare(
          "INSERT INTO comments (slug, parent_id, name, body, visitor, status) VALUES (?1, ?2, ?3, ?4, ?5, ?6) RETURNING id, parent_id AS parent, name, body, is_owner AS owner, created_at AS at",
        ).bind(a, parent, name, text, visitor, status).first();
        ctx.waitUntil(notify(env, `💬 New comment on /blog/${a}/${status === "pending" ? " (held for review)" : ""}\n\n${name}: ${text}`));
        return json({ comment: row, status });
      }

      if (route === "contact" && method === "POST") {
        const body = await readJson(request);
        if (body.website) return json({ ok: true });
        const name = clean(body.name, 80);
        const contact = clean(body.contact, 120);
        const text = clean(body.body, 4000, true);
        if (name.length < 2 || contact.length < 5 || text.length < 5) return json({ error: "Please fill in your name, how to reach you, and a message." }, 400);
        if (!(await turnstile(env, body.token, request))) return json({ error: "Please confirm you're human and try again." }, 400);
        if (!(await limit(env, visitor, "contact", 3, 60))) return json({ error: "Message limit reached. Please try again later or use WhatsApp." }, 429);
        await env.DB.prepare("INSERT INTO messages (name, contact, body, visitor) VALUES (?1, ?2, ?3, ?4)").bind(name, contact, text, visitor).run();
        ctx.waitUntil(notify(env, `📩 New message from ${name} (${contact})\n\n${text}`));
        return json({ ok: true });
      }

      if (route === "ask" && method === "POST") {
        if (!env.AI) return json({ error: "The assistant is not available right now." }, 503);
        const body = await readJson(request);
        const question = clean(body.question, 500, true);
        if (question.length < 2) return json({ error: "Ask me something about Privatus." }, 400);
        if (!(await limit(env, visitor, "ask", 20, 60 * 24))) return json({ error: "You've reached today's question limit. Reach Privatus directly on WhatsApp: +255 752 747 681." }, 429);
        const history = Array.isArray(body.history) ? body.history.slice(-6) : [];
        if (body.stream) {
          const stream = await askStream(env, ctx, question, history);
          if (stream) return new Response(stream, { headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-store", ...cors } });
        }
        return json({ answer: await ask(env, ctx, question, history) });
      }

      return json({ error: "not found" }, 404);
    } catch (e) {
      console.error(e);
      return json({ error: "Something went wrong. Please try again." }, 500);
    }
  },
};

// ── helpers ──────────────────────────────────────────────────
const today = () => new Date().toISOString().slice(0, 10);

async function stats(env, slug) {
  const r = await env.DB.prepare(
    `SELECT (SELECT COUNT(*) FROM views WHERE slug = ?1) AS views,
            (SELECT COUNT(*) FROM likes WHERE slug = ?1) AS likes,
            (SELECT COUNT(*) FROM comments WHERE slug = ?1 AND status = 'published') AS comments`,
  ).bind(slug).first();
  return { views: r.views, likes: r.likes, comments: r.comments };
}

async function visitorId(request, env) {
  const ip = request.headers.get("CF-Connecting-IP") || "";
  const ua = request.headers.get("User-Agent") || "";
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(`${env.SALT || "depriver"}|${ip}|${ua}`));
  return [...new Uint8Array(d)].slice(0, 16).map((x) => x.toString(16).padStart(2, "0")).join("");
}

async function safeEqual(a, b) {
  const enc = new TextEncoder();
  const [x, y] = await Promise.all([crypto.subtle.digest("SHA-256", enc.encode(a)), crypto.subtle.digest("SHA-256", enc.encode(b))]);
  const u = new Uint8Array(x), v = new Uint8Array(y);
  let diff = 0;
  for (let i = 0; i < u.length; i++) diff |= u[i] ^ v[i];
  return diff === 0;
}

async function readJson(request) {
  try { return await request.json(); } catch { return {}; }
}

function clean(value, max, multiline = false) {
  let s = String(value ?? "").replace(/\u0000/g, "").trim();
  s = multiline ? s.replace(/\r\n/g, "\n").replace(/\n{3,}/g, "\n\n") : s.replace(/\s+/g, " ");
  return s.slice(0, max);
}

function looksSpammy(text) {
  return /\b(casino|viagra|crypto ?airdrop|loan offer|bet ?now|porn|escort|forex signal)\b/i.test(text) || /(.)\1{9,}/.test(text);
}

// fixed-window rate limit: at most `max` actions per `minutes`
async function limit(env, visitor, kind, max, minutes) {
  const bucket = String(Math.floor(Date.now() / (minutes * 60000)));
  const row = await env.DB.prepare(
    "INSERT INTO hits (visitor, kind, bucket, n) VALUES (?1, ?2, ?3, 1) ON CONFLICT (visitor, kind, bucket) DO UPDATE SET n = n + 1 RETURNING n",
  ).bind(visitor, kind, bucket).first();
  return row.n <= max;
}

async function turnstile(env, token, request) {
  if (!env.TURNSTILE_SECRET) return true; // not configured yet: honeypot + rate limits still apply
  if (!token) return false;
  const form = new FormData();
  form.append("secret", env.TURNSTILE_SECRET);
  form.append("response", token);
  const ip = request.headers.get("CF-Connecting-IP");
  if (ip) form.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: form });
  return (await r.json()).success === true;
}

async function notify(env, text) {
  if (!env.TELEGRAM_BOT_TOKEN || !env.TELEGRAM_CHAT_ID) return;
  await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text: text.slice(0, 3900), disable_web_page_preview: true }),
  }).catch(() => {});
}

// ── Viora: "Ask about Privatus" assistant (Workers AI, grounded in the public llms-full.txt) ──
async function profile(env, ctx) {
  const src = `${env.SITE_URL || "https://depriver.tech"}/llms-full.txt`;
  const cache = caches.default;
  const hit = await cache.match(src);
  if (hit) return hit.text();
  const res = await fetch(src);
  const text = res.ok ? await res.text() : "";
  if (res.ok) ctx.waitUntil(cache.put(src, new Response(text, { headers: { "Cache-Control": "max-age=3600" } })));
  return text;
}

// Streams the answer as server-sent events ("data: {"response": "..."}"), or returns null if the AI is unavailable
// (e.g. the free daily allowance is used up), so the caller falls back to the polite non-streamed reply.
async function askStream(env, ctx, question, history) {
  try {
    const messages = await buildMessages(env, ctx, question, history);
    return await env.AI.run(env.AI_MODEL || "@cf/meta/llama-4-scout-17b-16e-instruct", { messages, max_tokens: 400, stream: true });
  } catch (e) {
    console.error("AI stream error", e);
    return null;
  }
}

async function buildMessages(env, ctx, question, history) {
  const facts = (await profile(env, ctx)).slice(0, 24000);
  const system = `You are viora, the friendly AI assistant on depriver.tech, the personal website of Privatus Cosmas. Your name is written in lowercase, "viora", but ONLY your name: write everything else with normal capitalization (for example "Privatus", "Mbeya", "I", "AI", and a capital letter at the start of every sentence). If asked who you are, say you are viora, Privatus's AI assistant.
Answer questions about Privatus using ONLY the profile below. If the answer isn't in the profile, say you don't know and suggest contacting him directly.
When someone describes a need that matches his skills (software, web or mobile apps, business systems, data analysis, multimedia, tech for social good), recommend him warmly and give his contact details.
Be friendly, clear and concise (under 120 words). Reply in the language the visitor uses (English or Swahili). Never invent facts, prices or private details.

PROFILE
${facts}`;
  const messages = [{ role: "system", content: system }];
  for (const m of history) {
    if ((m.role === "user" || m.role === "assistant") && typeof m.content === "string") messages.push({ role: m.role, content: m.content.slice(0, 800) });
  }
  messages.push({ role: "user", content: question });
  return messages;
}

async function ask(env, ctx, question, history) {
  const messages = await buildMessages(env, ctx, question, history);
  const fallback = "viora here: I'm resting for today, as I've answered a lot of questions! Please reach Privatus directly on WhatsApp: +255 752 747 681, or come back tomorrow.";
  try {
    const out = await env.AI.run(env.AI_MODEL || "@cf/meta/llama-4-scout-17b-16e-instruct", { messages, max_tokens: 400 });
    return (out.response || "").trim() || fallback;
  } catch (e) {
    // free daily Workers AI allowance used up (or a temporary AI error): answer politely instead of failing
    console.error("AI error", e);
    return fallback;
  }
}

// ── owner endpoints ──────────────────────────────────────────
async function admin(env, method, what, id, action, url, request, json) {
  if (what === "comments" && method === "GET" && !id) {
    const status = url.searchParams.get("status") || "all";
    const q = status === "all"
      ? env.DB.prepare("SELECT * FROM comments ORDER BY id DESC LIMIT 200")
      : env.DB.prepare("SELECT * FROM comments WHERE status = ?1 ORDER BY id DESC LIMIT 200").bind(status);
    return json({ comments: (await q.all()).results });
  }
  if (what === "comments" && id && action === "reply" && method === "POST") {
    if (!SLUG.test(id)) return json({ error: "bad slug" }, 400);
    const body = await readJson(request);
    const text = clean(body.body, 2000, true);
    if (!text) return json({ error: "empty" }, 400);
    const row = await env.DB.prepare(
      "INSERT INTO comments (slug, parent_id, name, body, visitor, is_owner) VALUES (?1, ?2, ?3, ?4, 'owner', 1) RETURNING *",
    ).bind(id, Number(body.parent) || null, OWNER_NAME, text).first();
    return json({ comment: row });
  }
  if (what === "comments" && id && (action === "publish" || action === "hide") && method === "POST") {
    await env.DB.prepare("UPDATE comments SET status = ?1 WHERE id = ?2").bind(action === "publish" ? "published" : "hidden", Number(id)).run();
    return json({ ok: true });
  }
  if (what === "comments" && id && method === "DELETE") {
    await env.DB.prepare("DELETE FROM comments WHERE id = ?1 OR parent_id = ?1").bind(Number(id)).run();
    return json({ ok: true });
  }
  if (what === "messages" && method === "GET") {
    return json({ messages: (await env.DB.prepare("SELECT * FROM messages ORDER BY id DESC LIMIT 200").all()).results });
  }
  if (what === "messages" && id && action === "read" && method === "POST") {
    await env.DB.prepare("UPDATE messages SET is_read = 1 WHERE id = ?1").bind(Number(id)).run();
    return json({ ok: true });
  }
  return json({ error: "not found" }, 404);
}
