import { unseal } from './crypto.js';

export class ProviderError extends Error {
  constructor(message, { uncertain = false, retryable = false } = {}) {
    super(message); this.uncertain = uncertain; this.retryable = retryable;
  }
}
// Never expose provider response bodies or request URLs: either may contain tokens.
export async function api(url, options = {}, publishing = false) {
  let response;
  try { response = await fetch(url, { ...options, redirect:'error', signal:AbortSignal.timeout(20000) }); }
  catch { throw new ProviderError(publishing ? 'Publish response was not received. Check the account before retrying.' : 'Platform connection timed out.', { uncertain:publishing, retryable:!publishing }); }
  if (!response.ok) {
    throw new ProviderError(`Platform returned HTTP ${response.status}. ${response.status === 401 || response.status === 403 ? 'Reconnect the account and check publishing permissions.' : 'Check the account and try again.'}`, {
      uncertain:publishing && response.status >= 500,
      retryable:!publishing && (response.status === 429 || response.status >= 500),
    });
  }
  let body = {};
  try { const text = await response.text(); body = text ? JSON.parse(text) : {}; }
  catch { throw new ProviderError('Platform returned an unreadable response.', { uncertain:publishing, retryable:!publishing }); }
  return { body, response };
}

export function instagramBase(env) {
  if (!/^v\d+\.0$/.test(env.INSTAGRAM_API_VERSION || '')) throw new ProviderError('Set a supported Instagram API version before publishing.');
  return `https://graph.instagram.com/${env.INSTAGRAM_API_VERSION}`;
}
const bearer = token => ({ Authorization:`Bearer ${token}` });

export async function publishLinkedin(job, account, env, beforePublish) {
  if (!/^\d{6}$/.test(env.LINKEDIN_API_VERSION || '')) throw new ProviderError('Set a supported LinkedIn API version before publishing.');
  const token = await unseal(account.token, env, 'linkedin');
  await beforePublish();
  const { response } = await api('https://api.linkedin.com/rest/posts', {
    method:'POST', headers:{ ...bearer(token), 'Content-Type':'application/json', 'LinkedIn-Version':env.LINKEDIN_API_VERSION, 'X-Restli-Protocol-Version':'2.0.0' },
    body:JSON.stringify({ author:`urn:li:person:${account.account_id}`, commentary:job.caption,
      visibility:'PUBLIC', distribution:{ feedDistribution:'MAIN_FEED', targetEntities:[], thirdPartyDistributionChannels:[] },
      lifecycleState:'PUBLISHED', isReshareDisabledByAuthor:false }),
  }, true);
  const id = response.headers.get('x-restli-id');
  if (!id) throw new ProviderError('LinkedIn accepted the post without a post ID. Check your profile.', { uncertain:true });
  return { id, url:`https://www.linkedin.com/feed/update/${encodeURIComponent(id)}/` };
}

export async function publishInstagram(job, account, env, beforePublish) {
  const token = await unseal(account.token, env, 'instagram');
  const base = instagramBase(env);
  const post = async (path, values, publishing = false) => (await api(`${base}/${path}`, {
    method:'POST', headers:bearer(token), body:new URLSearchParams(values),
  }, publishing)).body;
  const media = JSON.parse(job.media);
  let container = job.container_id;
  if (!container) {
    const children = [];
    for (const item of media) {
      const body = await post(`${account.account_id}/media`, { image_url:item.url,
        ...(media.length > 1 ? { is_carousel_item:'true' } : { caption:job.caption }), alt_text:item.alt || job.title });
      if (!body.id) throw new ProviderError('Instagram did not return a media container.');
      children.push(body.id);
    }
    container = children[0];
    if (children.length > 1) {
      const body = await post(`${account.account_id}/media`, { media_type:'CAROUSEL', children:children.join(','), caption:job.caption });
      container = body.id;
    }
    if (!container) throw new ProviderError('Instagram did not return a carousel container.');
    await env.DB.prepare('UPDATE social_jobs SET container_id=? WHERE id=?').bind(container,job.id).run();
  }
  const { body:status } = await api(`${base}/${container}?fields=status_code`, { headers:bearer(token) });
  if (status.status_code === 'PUBLISHED') throw new ProviderError('Instagram reports this container already published. Check the account.', { uncertain:true });
  if (status.status_code === 'IN_PROGRESS') return { waiting:true };
  if (status.status_code !== 'FINISHED') throw new ProviderError('Instagram media processing failed or expired. Recreate the draft after checking your account.');
  await beforePublish();
  const published = await post(`${account.account_id}/media_publish`, { creation_id:container }, true);
  if (!published.id) throw new ProviderError('Instagram accepted the post without a media ID. Check the account.', { uncertain:true });
  // A missing permalink must not turn a confirmed post into a retry.
  let url = null;
  try { url = (await api(`${base}/${published.id}?fields=permalink`, { headers:bearer(token) })).body.permalink || null; } catch {}
  return { id:String(published.id), url };
}
