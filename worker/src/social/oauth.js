import { api, instagramBase } from './providers.js';
import { seal } from './crypto.js';

export const platforms = ['instagram','linkedin'];
export function configured(platform, env) {
  const prefix = platform.toUpperCase();
  return !!(env[`${prefix}_CLIENT_ID`] && env[`${prefix}_CLIENT_SECRET`] && env.SOCIAL_TOKEN_KEY && env.SOCIAL_API_URL && env[`${prefix}_API_VERSION`]);
}
const callback = (platform, env) => `${env.SOCIAL_API_URL.replace(/\/$/,'')}/social/oauth/${platform}/callback`;

export async function startOAuth(platform, env) {
  if (!platforms.includes(platform) || !configured(platform, env)) throw new Error('This connection needs developer-app setup first. See the setup guide.');
  const state = crypto.randomUUID() + crypto.randomUUID();
  const expires = new Date(Date.now()+600000).toISOString();
  await env.DB.prepare('DELETE FROM social_oauth WHERE expires_at < ?').bind(new Date().toISOString()).run();
  await env.DB.prepare('INSERT INTO social_oauth(state,platform,expires_at) VALUES(?,?,?)').bind(state,platform,expires).run();
  const url = new URL(platform === 'linkedin' ? 'https://www.linkedin.com/oauth/v2/authorization' : 'https://www.instagram.com/oauth/authorize');
  url.search = new URLSearchParams({ client_id:env[`${platform.toUpperCase()}_CLIENT_ID`], redirect_uri:callback(platform,env), response_type:'code', state,
    scope:platform === 'linkedin' ? 'openid profile w_member_social' : 'instagram_business_basic,instagram_business_content_publish',
    ...(platform === 'instagram' ? { enable_fb_login:'0', force_authentication:'1' } : {}),
  }).toString();
  return { url:url.href };
}

export async function finishOAuth(request, env) {
  const url = new URL(request.url);
  const platform = url.pathname.split('/')[3];
  const target = new URL('/publisher/', env.SITE_URL || 'https://depriver.tech');
  target.searchParams.set('connection', 'failed');
  try {
    if (!platforms.includes(platform) || !configured(platform,env)) throw new Error('configuration');
    const state = url.searchParams.get('state') || '';
    const row = await env.DB.prepare('DELETE FROM social_oauth WHERE state=? AND platform=? AND expires_at>? RETURNING state')
      .bind(state, platform, new Date().toISOString()).first();
    if (!row || url.searchParams.has('error') || !url.searchParams.get('code')) throw new Error('authorization');
    const code = url.searchParams.get('code');
    const prefix = platform.toUpperCase();
    const values = { client_id:env[`${prefix}_CLIENT_ID`], client_secret:env[`${prefix}_CLIENT_SECRET`], grant_type:'authorization_code', redirect_uri:callback(platform,env), code };
    let token, expires, accountId, label;
    if (platform === 'linkedin') {
      const { body } = await api('https://www.linkedin.com/oauth/v2/accessToken', { method:'POST', body:new URLSearchParams(values) });
      token = body.access_token; expires = body.expires_in;
      const { body:user } = await api('https://api.linkedin.com/v2/userinfo', { headers:{ Authorization:`Bearer ${token}` } });
      accountId = user.sub; label = user.name || 'LinkedIn profile';
    } else {
      const form = new FormData();
      for (const [k,v] of Object.entries(values)) form.append(k,v);
      const { body:short } = await api('https://api.instagram.com/oauth/access_token', { method:'POST', body:form });
      const first = short.data?.[0] || short;
      const exchange = new URL('https://graph.instagram.com/access_token');
      exchange.search = new URLSearchParams({ grant_type:'ig_exchange_token', client_secret:env.INSTAGRAM_CLIENT_SECRET, access_token:first.access_token });
      const { body:long } = await api(exchange.href);
      token = long.access_token; expires = long.expires_in;
      const { body:user } = await api(`${instagramBase(env)}/me?fields=user_id,username`, { headers:{ Authorization:`Bearer ${token}` } });
      accountId = user.user_id || first.user_id; label = user.username;
    }
    if (!token || !accountId || !Number.isFinite(Number(expires)) || Number(expires) <= 0) throw new Error('Invalid account response');
    const now = new Date().toISOString();
    const encrypted = await seal(token,env,platform);
    await env.DB.prepare(`INSERT INTO social_accounts(platform,account_id,label,token,expires_at,connected_at) VALUES(?,?,?,?,?,?)
      ON CONFLICT(platform) DO UPDATE SET account_id=excluded.account_id,label=excluded.label,token=excluded.token,expires_at=excluded.expires_at,connected_at=excluded.connected_at`)
      .bind(platform,String(accountId),label || platform,encrypted,new Date(Date.now()+Number(expires)*1000).toISOString(),now).run();
    target.searchParams.set('connection', platform);
  } catch {
    // Codes, tokens and raw provider errors are deliberately not logged or returned.
  }
  return new Response(null,{ status:303, headers:{ Location:target.href, 'Cache-Control':'no-store', 'Referrer-Policy':'no-referrer' } });
}
