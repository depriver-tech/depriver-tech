import catalog from './catalog.json' with { type:'json' };
import { configured, startOAuth } from './oauth.js';
import { ProviderError, publishInstagram, publishLinkedin } from './providers.js';

export { finishOAuth } from './oauth.js';
const now = () => new Date().toISOString();
const platforms = ['instagram','linkedin','tiktok'];
const editable = ['draft','failed','cancelled','handoff'];
const requireValue = (condition, message) => { if (!condition) throw new Error(message); };
const changes = result => Number(result.meta?.changes || 0);
const event = (env,id,action,detail='') => env.DB.prepare('INSERT INTO social_events(job_id,action,detail,created_at) VALUES(?,?,?,?)').bind(id,action,detail,now());

export function validateDraft(body, source) {
  requireValue(source, 'Article is no longer eligible for publishing.');
  requireValue(platforms.includes(body.platform), 'Choose a supported platform.');
  const caption = String(body.caption || '').trim();
  requireValue(caption.length > 0 && [...caption].length <= (body.platform === 'instagram' ? 2200 : 3000), 'Caption is empty or exceeds the platform limit.');
  const time = new Date(body.scheduled_at);
  requireValue(Number.isFinite(time.valueOf()), 'Choose a valid date and time.');
  requireValue(time.valueOf() >= Date.parse(source.date), 'Schedule this after the article publication date.');
  const requested = body.platform === 'instagram' ? body.media : [];
  requireValue(Array.isArray(requested), 'Choose the images to publish.');
  if (body.platform === 'instagram') requireValue(requested.length >= 1 && requested.length <= 10, 'Choose 1–10 images. Longer carousels need an edited selection or a single poster.');
  const allowed = [...source.media, source.poster];
  const media = requested.map(url => {
    const item = allowed.find(m=>m.url === url);
    requireValue(item, 'Only images belonging to this article can be published.');
    return { url:item.url, alt:item.alt };
  });
  requireValue(new Set(requested).size === requested.length,'Remove duplicate images.');
  return { caption, scheduled_at:time.toISOString(), media };
}

export async function socialAdmin(request, env, json) {
  const url = new URL(request.url);
  const path = url.pathname.split('/').filter(Boolean).slice(2);
  const [resource,id,action] = path;
  const method = request.method;
  try {
    if (!resource && method === 'GET') {
      const settings = await env.DB.prepare('SELECT enabled FROM social_settings WHERE id=1').first();
      const accounts = (await env.DB.prepare('SELECT platform,account_id,label,expires_at,connected_at FROM social_accounts').all()).results;
      const jobs = (await env.DB.prepare('SELECT * FROM social_jobs ORDER BY scheduled_at DESC LIMIT 500').all()).results;
      return json({ enabled:!!settings?.enabled, deployEnabled:env.SOCIAL_PUBLISHING_ENABLED === 'true',
        accounts, jobs:jobs.map(j=>({...j,media:JSON.parse(j.media)})), catalog,
        connections:Object.fromEntries(['instagram','linkedin'].map(p=>[p,configured(p,env)])) });
    }
    if (resource === 'settings' && method === 'POST') {
      const body = await request.json();
      requireValue(typeof body.enabled === 'boolean','Expected enabled true or false.');
      requireValue(!body.enabled || env.SOCIAL_PUBLISHING_ENABLED === 'true','Publishing must first be enabled in the deployment configuration.');
      await env.DB.batch([env.DB.prepare('UPDATE social_settings SET enabled=? WHERE id=1').bind(body.enabled ? 1 : 0),event(env,'system',body.enabled?'resumed':'paused')]);
      return json({ ok:true });
    }
    if (resource === 'connect' && method === 'POST') return json(await startOAuth(id,env));
    if (resource === 'accounts' && method === 'DELETE' && ['instagram','linkedin'].includes(id)) {
      await env.DB.batch([env.DB.prepare('DELETE FROM social_accounts WHERE platform=?').bind(id),
        env.DB.prepare("UPDATE social_jobs SET status='draft',error='Account disconnected; reconnect and schedule again.',updated_at=? WHERE platform=? AND status='scheduled'").bind(now(),id),event(env,'system','disconnected',id)]);
      return json({ ok:true });
    }
    if (resource === 'jobs' && !id && method === 'POST') {
      const body = await request.json();
      const source = catalog.find(p=>p.slug === body.slug);
      const draft = validateDraft(body,source);
      const existing = await env.DB.prepare('SELECT id,status FROM social_jobs WHERE source_slug=? AND platform=?').bind(body.slug,body.platform).first();
      if (existing) return json({ error:'This article already has a post for this platform. Open it in the queue.', id:existing.id },409);
      const jobId = crypto.randomUUID();
      const timestamp = now();
      await env.DB.batch([env.DB.prepare(`INSERT INTO social_jobs(id,source_slug,platform,title,caption,source_url,media,scheduled_at,status,created_at,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)`).bind(jobId,source.slug,body.platform,source.title,draft.caption,source.url,JSON.stringify(draft.media),draft.scheduled_at,body.platform === 'tiktok'?'handoff':'draft',timestamp,timestamp), event(env,jobId,'created')]);
      return json({ id:jobId },201);
    }
    if (resource === 'jobs' && id && action === 'events' && method === 'GET') {
      return json({ events:(await env.DB.prepare('SELECT * FROM social_events WHERE job_id=? ORDER BY id DESC LIMIT 100').bind(id).all()).results });
    }
    if (resource === 'jobs' && id && method === 'POST') {
      const job = await env.DB.prepare('SELECT * FROM social_jobs WHERE id=?').bind(id).first();
      if (!job) return json({ error:'Post not found.' },404);
      const body = await request.json();
      const source = catalog.find(p=>p.slug === job.source_slug);
      if (action === 'save') {
        requireValue(editable.includes(job.status),'Unschedule this post before editing it.');
        const draft = validateDraft({...body,platform:job.platform},source);
        const result = await env.DB.prepare(`UPDATE social_jobs SET caption=?,media=?,scheduled_at=?,status=?,container_id=NULL,error=NULL,attempts=0,next_attempt_at=NULL,updated_at=? WHERE id=? AND status IN ('draft','failed','cancelled','handoff')`)
          .bind(draft.caption,JSON.stringify(draft.media),draft.scheduled_at,job.platform === 'tiktok'?'handoff':'draft',now(),id).run();
        requireValue(changes(result),'Post changed while you were editing; reload it.');
      } else if (action === 'schedule') {
        requireValue(job.platform !== 'tiktok','TikTok requires manual publishing.');
        validateDraft({...job,media:JSON.parse(job.media).map(m=>m.url)},source);
        requireValue(Date.parse(job.scheduled_at)>Date.now(),'Choose a future publishing time.');
        const account = await env.DB.prepare('SELECT * FROM social_accounts WHERE platform=?').bind(job.platform).first();
        requireValue(account && Date.parse(account.expires_at)>Date.parse(job.scheduled_at)+60000,'Connect an account whose authorization lasts beyond the scheduled time.');
        const result = await env.DB.prepare("UPDATE social_jobs SET status='scheduled',account_id=?,error=NULL,attempts=0,next_attempt_at=NULL,updated_at=? WHERE id=? AND status='draft'").bind(account.account_id,now(),id).run();
        requireValue(changes(result),'Save this post as a draft before scheduling.');
      } else if (action === 'cancel') {
        const result = await env.DB.prepare("UPDATE social_jobs SET status='draft',updated_at=? WHERE id=? AND status='scheduled'").bind(now(),id).run();
        requireValue(changes(result),'Only a scheduled post can be unscheduled. It may already be processing.');
      } else if (action === 'resolve') {
        requireValue(['review','handoff'].includes(job.status),'Only a post needing review or handoff can be resolved.');
        requireValue(['published','not_published'].includes(body.outcome),'Choose whether the post exists on your account.');
        if (body.outcome === 'not_published') requireValue(body.confirmed === true,'Confirm you checked the account before retrying.');
        let externalUrl = null;
        if (body.outcome === 'published') {
          const link = new URL(body.url);
          const hosts = { instagram:['instagram.com','www.instagram.com'], linkedin:['linkedin.com','www.linkedin.com'], tiktok:['tiktok.com','www.tiktok.com'] };
          requireValue(link.protocol === 'https:' && hosts[job.platform].includes(link.hostname) && !link.username && !link.password,'Enter the published post URL on the correct platform.');
          externalUrl = link.href;
        }
        const result = await env.DB.prepare("UPDATE social_jobs SET status=?,external_url=?,container_id=NULL,error=NULL,updated_at=? WHERE id=? AND status IN ('review','handoff')")
          .bind(body.outcome === 'published'?'published':job.platform==='tiktok'?'handoff':'draft',externalUrl,now(),id).run();
        requireValue(changes(result),'Post changed; reload it.');
      } else return json({ error:'Unknown action.' },404);
      await event(env,id,action).run();
      return json({ ok:true });
    }
    return json({ error:'Not found.' },404);
  } catch (error) {
    // Errors from our validation are safe; don't return D1 exceptions or OAuth/provider details.
    const safe = error.constructor === Error && !/D1|SQLITE|SQL|UNIQUE|constraint/i.test(error.message);
    return json({ error:safe ? error.message : 'The request could not be completed. Reload and check the setup.' },400);
  }
}

export async function runScheduler(env) {
  if (env.SOCIAL_PUBLISHING_ENABLED !== 'true') return;
  const settings = await env.DB.prepare('SELECT enabled FROM social_settings WHERE id=1').first();
  if (!settings?.enabled) return;
  const timestamp = now();
  // Never retry a crashed attempt blindly: its provider request may already have succeeded.
  await env.DB.prepare("UPDATE social_jobs SET status='review',error='Worker stopped during publishing. Check the social account before retrying.',updated_at=? WHERE status='processing' AND updated_at<?")
    .bind(timestamp,new Date(Date.now()-15*60000).toISOString()).run();
  const { results } = await env.DB.prepare("SELECT id FROM social_jobs WHERE status='scheduled' AND scheduled_at<=? AND (next_attempt_at IS NULL OR next_attempt_at<=?) ORDER BY scheduled_at LIMIT 1").bind(timestamp,timestamp).all();
  for (const row of results) await processJob(row.id,env);
}

export async function processJob(id, env) {
  const settings = await env.DB.prepare('SELECT enabled FROM social_settings WHERE id=1').first();
  if (env.SOCIAL_PUBLISHING_ENABLED !== 'true' || !settings?.enabled) return;
  const job = await env.DB.prepare("UPDATE social_jobs SET status='processing',attempts=attempts+1,updated_at=? WHERE id=? AND status='scheduled' AND scheduled_at<=? AND (next_attempt_at IS NULL OR next_attempt_at<=?) RETURNING *")
    .bind(now(),id,now(),now()).first();
  if (!job) return;
  let publishStarted = false;
  try {
    const source = catalog.find(p=>p.slug === job.source_slug);
    validateDraft({...job,media:JSON.parse(job.media).map(m=>m.url)},source);
    const account = await env.DB.prepare('SELECT * FROM social_accounts WHERE platform=?').bind(job.platform).first();
    if (!account || account.account_id !== job.account_id || Date.parse(account.expires_at)<=Date.now()+60000) throw new ProviderError('Account changed, disconnected or expired. Reconnect and schedule again.');
    let live;
    try { live = await fetch(job.source_url,{ method:'HEAD',redirect:'manual',signal:AbortSignal.timeout(15000) }); }
    catch { throw new ProviderError('Website is unavailable. Waiting before publishing.',{retryable:true}); }
    if (live.status !== 200) throw new ProviderError('Article is not live yet. Waiting for website deployment.',{retryable:true});
    for (const item of JSON.parse(job.media)) {
      let response;
      try { response = await fetch(item.url,{method:'HEAD',redirect:'manual',signal:AbortSignal.timeout(15000)}); }
      catch { throw new ProviderError('Image is temporarily unavailable.',{retryable:true}); }
      if (response.status !== 200 || !response.headers.get('content-type')?.includes('image/jpeg')) throw new ProviderError('Publishing JPEG is not available yet. Waiting for website deployment.',{retryable:true});
    }
    const beforePublish = async () => {
      const [active,current] = await Promise.all([
        env.DB.prepare('SELECT enabled FROM social_settings WHERE id=1').first(),
        env.DB.prepare('SELECT account_id FROM social_accounts WHERE platform=?').bind(job.platform).first(),
      ]);
      if (!active?.enabled || current?.account_id !== job.account_id) throw new ProviderError('Publishing paused or account disconnected before submission.');
      await event(env,id,'submitting').run();
      publishStarted = true;
    };
    const result = job.platform === 'instagram' ? await publishInstagram(job,account,env,beforePublish) : await publishLinkedin(job,account,env,beforePublish);
    if (result.waiting) {
      if (job.attempts >= 12) throw new ProviderError('Instagram processing took too long. Check the account and media.');
      await env.DB.prepare("UPDATE social_jobs SET status='scheduled',next_attempt_at=?,updated_at=? WHERE id=? AND status='processing'")
        .bind(new Date(Date.now()+5*60000).toISOString(),now(),id).run();
      return;
    }
    await env.DB.batch([env.DB.prepare("UPDATE social_jobs SET status='published',external_id=?,external_url=?,error=NULL,updated_at=? WHERE id=? AND status='processing'").bind(result.id,result.url,now(),id),event(env,id,'published',result.id)]);
  } catch (error) {
    const uncertain = error instanceof ProviderError ? error.uncertain : publishStarted;
    const retry = !uncertain && error instanceof ProviderError && error.retryable && job.attempts < 12;
    const status = uncertain ? 'review' : retry ? 'scheduled' : 'failed';
    const message = error instanceof ProviderError ? error.message : 'Publishing could not complete. Check the configuration and account.';
    await env.DB.batch([env.DB.prepare("UPDATE social_jobs SET status=?,error=?,next_attempt_at=?,updated_at=? WHERE id=? AND status='processing'")
      .bind(status,message,retry?new Date(Date.now()+Math.min(60,5*job.attempts)*60000).toISOString():null,now(),id),event(env,id,status,message)]);
  }
}
