// llms-full.txt: the complete public profile, story and posts as plain text.
// Also the knowledge base for viora, the on-site assistant (viora cloud reads this file when it re-indexes).
import type { APIRoute } from "astro";
import { livePosts } from "../lib/posts";
import { chapters, services, outside, dreams, lessons, contact } from "../data/story";

// a post's own headings sit under the post title (### …), so each section stays with its post for AI readers
const nest = (md: string) => md.replace(/^(#{1,4}) /gm, (_, h: string) => "#".repeat(h.length + 2) + " ");

export const GET: APIRoute = async () => {
  const posts = await livePosts();
  const text = `# Privatus Cosmas: full profile

Name: Privatus Cosmas (online: @_depriver, depriver)
Role: Software Engineer & Digital Innovator
Location: Mbeya, Tanzania (originally from Kitwe village, Kyerwa District, Kagera)
Education: Diploma in Computer Science, Mbeya University of Science and Technology (MUST), joined October 2023, graduated 2026. Now enrolled in the Bachelor of Computer Science programme at MUST, first year, first semester, academic year 2026/2027. Secondary: Kaisho Secondary School (Division I). Earlier: Katoke Seminary.
Languages: English, Swahili
Website: https://depriver.tech
Contact: WhatsApp/phone ${contact.phone} · Instagram ${contact.instagramHref} · GitHub ${contact.githubHref}

## What he does (services)
${services.map((s) => `- ${s.title}: ${s.body}`).join("\n")}

Skills and tools mentioned on the site: Python, JavaScript, React, Flutter, Django, AWS, cloud, DevOps, AI and automation, data dashboards, computer hardware and repairs, video and photography.

## Life beyond code
${outside.join(", ")}.

## His story
${chapters.map((c) => `### ${c.year}: ${c.title} ${c.accent} (${c.when}, ${c.place})\n${c.body.join("\n\n")}`).join("\n\n")}

### Today
He works full time as a Software Engineer & Digital Innovator in Mbeya, building web and mobile apps, business systems and data tools.

## Lessons he shares
${lessons.map((l) => `- ${l.title}: ${l.body}`).join("\n")}

## Goals and dreams
${dreams.map((d) => `- ${d.group}: ${d.items.join("; ")}`).join("\n")}

## Blog posts
${posts.map((p) => `### ${p.data.title}\nhttps://depriver.tech/blog/${p.id}/ · ${p.data.date.toISOString().slice(0, 10)}\n${p.data.description}\n${p.data.slides.length ? "Slides:\n" + p.data.slides.map((s, i) => `${i + 1}. ${s}`).join("\n") + "\n" : ""}${nest((p.body ?? "").trim())}`).join("\n\n")}
`;
  return new Response(text, { headers: { "Content-Type": "text/plain; charset=utf-8" } });
};
