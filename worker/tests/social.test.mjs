import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import { socialAdmin, validateDraft, runScheduler, processJob } from '../src/social/index.js';
import { seal, unseal } from '../src/social/crypto.js';
import { startOAuth, finishOAuth } from '../src/social/oauth.js';
import worker from '../src/index.js';
import catalog from '../src/social/catalog.json' with { type:'json' };

// Real SQLite constraints and UPDATE ... RETURNING semantics behind D1's small interface.
function database() {
  const sqlite=new DatabaseSync(':memory:');
  sqlite.exec(readFileSync(new URL('../migrations/0001_social.sql',import.meta.url),'utf8'));
  function prepare(sql) {
    const statement=sqlite.prepare(sql);let args=[];
    const api={bind(...values){args=values;return api;},async first(){return statement.get(...args)||null;},
      async all(){return {results:statement.all(...args)};},async run(){const result=statement.run(...args);return {meta:{changes:result.changes}};}};
    return api;
  }
  return {prepare,async batch(statements){sqlite.exec('BEGIN');try{const result=[];for(const s of statements)result.push(await s.run());sqlite.exec('COMMIT');return result;}catch(e){sqlite.exec('ROLLBACK');throw e;}},sqlite};
}
function env() { return {DB:database(),ADMIN_KEY:'test-admin',ALLOWED_ORIGINS:'https://depriver.tech',SITE_URL:'https://depriver.tech',SOCIAL_API_URL:'https://api.example.test',SOCIAL_TOKEN_KEY:btoa('x'.repeat(32)),SOCIAL_PUBLISHING_ENABLED:'true',LINKEDIN_API_VERSION:'202605',INSTAGRAM_API_VERSION:'v25.0',LINKEDIN_CLIENT_ID:'test-client',LINKEDIN_CLIENT_SECRET:'secret'}; }
const source=catalog.find(p=>Date.parse(p.date)<Date.now()&&p.media.length);
const body=(extra={})=>({slug:source.slug,platform:'linkedin',caption:'A useful article\n'+source.url,scheduled_at:new Date(Date.now()+3600000).toISOString(),media:[],...extra});
const json=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json'}});
async function admin(e,path='',data,method=data===undefined?'GET':'POST') {
  return socialAdmin(new Request('https://api.example.test/admin/social'+path,{method,headers:{'Content-Type':'application/json'},...(data===undefined?{}:{body:JSON.stringify(data)})}),e,json);
}
async function account(e,platform='linkedin') {
  await e.DB.prepare('INSERT INTO social_accounts VALUES(?,?,?,?,?,?)').bind(platform,'person-1','Test owner',await seal('private-test-token',e,platform),new Date(Date.now()+86400000).toISOString(),new Date().toISOString()).run();
}
async function scheduled(e,platform='linkedin') {
  await account(e,platform);
  const result=await admin(e,'/jobs',body({platform,media:platform==='instagram'?[source.poster.url]:[]}));
  assert.equal(result.status,201);const {id}=await result.json();
  assert.equal((await admin(e,`/jobs/${id}/schedule`,{})).status,200);
  await e.DB.prepare('UPDATE social_settings SET enabled=1').run();
  await e.DB.prepare('UPDATE social_jobs SET scheduled_at=? WHERE id=?').bind(new Date(Date.now()-1000).toISOString(),id).run();
  return id;
}
const job=(e,id)=>e.DB.prepare('SELECT * FROM social_jobs WHERE id=?').bind(id).first();
const live=()=>new Response(null,{status:200,headers:{'Content-Type':'image/jpeg'}});

test('tokens are authenticated, encrypted and bound to their platform',async()=>{
  const e=env();const value=await seal('secret',e,'linkedin');assert.ok(!value.includes('secret'));
  assert.equal(await unseal(value,e,'linkedin'),'secret');
  await assert.rejects(unseal(value,e,'instagram'));
  await assert.rejects(unseal(value,{...e,SOCIAL_TOKEN_KEY:btoa('y'.repeat(32))},'linkedin'));
});
test('admin endpoint rejects anonymous and foreign-origin requests',async()=>{
  const e=env();
  const response=await worker.fetch(new Request('https://api.example.test/admin/social'),e,{});assert.equal(response.status,401);
  const denied=await worker.fetch(new Request('https://api.example.test/admin/social',{headers:{Authorization:'Bearer test-admin',Origin:'https://evil.test'}}),e,{});assert.equal(denied.status,403);
});
test('catalog and account API excludes credentials',async()=>{
  const e=env();await account(e);
  const response=await admin(e);const text=await response.text();
  assert.ok(!text.includes('private-test-token'));assert.ok(!text.includes('"token"'));assert.ok(text.includes(source.title));
});
test('publisher key unlocks social tools but cannot access moderation',async()=>{
  const e={...env(),PUBLISHER_KEY:'publisher-only'};
  const headers={Authorization:'Bearer publisher-only'};
  assert.equal((await worker.fetch(new Request('https://api.example.test/admin/social',{headers}),e,{})).status,200);
  assert.equal((await worker.fetch(new Request('https://api.example.test/admin/comments',{headers}),e,{})).status,401);
});
test('draft validation rejects foreign media, too many slides, invalid dates and long captions',()=>{
  assert.throws(()=>validateDraft(body({platform:'instagram',media:['https://evil.test/file.jpg']}),source));
  assert.throws(()=>validateDraft(body({platform:'instagram',media:Array(11).fill(source.poster.url)}),source));
  assert.throws(()=>validateDraft(body({scheduled_at:'invalid'}),source));
  assert.throws(()=>validateDraft(body({scheduled_at:'2000-01-01'}),source));
  assert.throws(()=>validateDraft(body({caption:'x'.repeat(3001)}),source));
  assert.throws(()=>validateDraft(body(),undefined));
});
test('duplicate drafts cannot create repeated posts',async()=>{
  const e=env();assert.equal((await admin(e,'/jobs',body())).status,201);assert.equal((await admin(e,'/jobs',body())).status,409);
});
test('scheduling requires authorization lasting beyond publication and disallows TikTok',async()=>{
  const e=env();const {id}=await (await admin(e,'/jobs',body())).json();
  assert.equal((await admin(e,`/jobs/${id}/schedule`,{})).status,400);
  await account(e);await e.DB.prepare('UPDATE social_accounts SET expires_at=?').bind(new Date(Date.now()+1000).toISOString()).run();
  assert.equal((await admin(e,`/jobs/${id}/schedule`,{})).status,400);
  const {id:tiktok}=await (await admin(e,'/jobs',body({platform:'tiktok'}))).json();
  assert.equal((await job(e,tiktok)).status,'handoff');assert.equal((await admin(e,`/jobs/${tiktok}/schedule`,{})).status,400);
});
test('scheduled captions are immutable until unscheduled',async()=>{
  const e=env(),id=await scheduled(e);
  assert.equal((await admin(e,`/jobs/${id}/save`,body({caption:'changed'}))).status,400);
  assert.equal((await admin(e,`/jobs/${id}/cancel`,{})).status,200);
  assert.equal((await admin(e,`/jobs/${id}/save`,body({caption:'changed'}))).status,200);
});
test('pausing and deployment gate prevent any publishing',async t=>{
  const e=env(),id=await scheduled(e);t.mock.method(globalThis,'fetch',()=>{throw new Error('must not fetch');});
  e.SOCIAL_PUBLISHING_ENABLED='false';await runScheduler(e);assert.equal((await job(e,id)).status,'scheduled');
  e.SOCIAL_PUBLISHING_ENABLED='true';await e.DB.prepare('UPDATE social_settings SET enabled=0').run();await runScheduler(e);assert.equal((await job(e,id)).status,'scheduled');
});
test('concurrent scheduler attempts claim a job only once and persist provider ID',async t=>{
  const e=env(),id=await scheduled(e);let published=0;
  t.mock.method(globalThis,'fetch',async(url,options)=>{
    if(options.method==='HEAD')return live();published++;return new Response(null,{status:201,headers:{'x-restli-id':'urn:li:share:123'}});
  });
  await Promise.all([processJob(id,e),processJob(id,e)]);
  assert.equal(published,1);assert.equal((await job(e,id)).status,'published');assert.equal((await job(e,id)).external_id,'urn:li:share:123');
  await runScheduler(e);assert.equal(published,1);
});
test('unpublished website and media postpone publishing without posting',async t=>{
  const e=env(),id=await scheduled(e);let writes=0;
  t.mock.method(globalThis,'fetch',async(url,options)=>{if(options.method!=='HEAD')writes++;return new Response(null,{status:404});});
  await processJob(id,e);const j=await job(e,id);assert.equal(j.status,'scheduled');assert.ok(j.next_attempt_at);assert.equal(writes,0);
});
test('Instagram image must be reachable JPEG before creating a container',async t=>{
  const e=env(),id=await scheduled(e,'instagram');let writes=0;
  t.mock.method(globalThis,'fetch',async(url,options)=>{if(options.method!=='HEAD')writes++;return new Response(null,{status:200,headers:{'Content-Type':String(url).endsWith('.jpg')?'image/webp':'text/html'}});});
  await processJob(id,e);assert.equal((await job(e,id)).status,'scheduled');assert.equal(writes,0);
});
test('expired or changed account cannot receive a scheduled post',async t=>{
  const e=env(),id=await scheduled(e);await e.DB.prepare("UPDATE social_accounts SET account_id='other-person'").run();
  t.mock.method(globalThis,'fetch',()=>{throw new Error('must not fetch');});await processJob(id,e);assert.equal((await job(e,id)).status,'failed');
});
test('uncertain publish is held for review and never automatically retried',async t=>{
  const e=env(),id=await scheduled(e);let writes=0;
  t.mock.method(globalThis,'fetch',async(url,options)=>{if(options.method==='HEAD')return live();writes++;throw new Error('network lost after send');});
  await processJob(id,e);assert.equal((await job(e,id)).status,'review');await runScheduler(e);assert.equal(writes,1);
  assert.equal((await admin(e,`/jobs/${id}/save`,body())).status,400);
  assert.equal((await admin(e,`/jobs/${id}/resolve`,{outcome:'not_published'})).status,400);
  assert.equal((await admin(e,`/jobs/${id}/resolve`,{outcome:'not_published',confirmed:true})).status,200);
});
test('crashed attempts are held for review',async()=>{
  const e=env(),id=await scheduled(e);await e.DB.prepare("UPDATE social_jobs SET status='processing',updated_at='2020-01-01T00:00:00.000Z' WHERE id=?").bind(id).run();
  await runScheduler(e);assert.equal((await job(e,id)).status,'review');
});
test('Instagram persists containers between processing polls',async t=>{
  const e=env(),id=await scheduled(e,'instagram');let creates=0,publishes=0,polls=0;
  t.mock.method(globalThis,'fetch',async(url,options={})=>{
    if(options.method==='HEAD')return live();
    if(String(url).endsWith('/media')){creates++;return json({id:'container-1'});}
    if(String(url).includes('fields=status_code')){polls++;return json({status_code:polls===1?'IN_PROGRESS':'FINISHED'});}
    if(String(url).endsWith('/media_publish')){publishes++;return json({id:'post-1'});}
    return json({permalink:'https://www.instagram.com/p/example/'});
  });
  await processJob(id,e);assert.equal((await job(e,id)).status,'scheduled');assert.equal((await job(e,id)).container_id,'container-1');
  await e.DB.prepare('UPDATE social_jobs SET next_attempt_at=NULL WHERE id=?').bind(id).run();await processJob(id,e);
  assert.equal(creates,1);assert.equal(publishes,1);assert.equal((await job(e,id)).status,'published');
});
test('disconnect returns scheduled posts to draft',async()=>{
  const e=env(),id=await scheduled(e);assert.equal((await admin(e,'/accounts/linkedin',undefined,'DELETE')).status,200);assert.equal((await job(e,id)).status,'draft');
});
test('OAuth state is single use and invalid state never exchanges a code',async t=>{
  const e=env();let exchanges=0;
  t.mock.method(globalThis,'fetch',async(url)=>{exchanges++;return String(url).includes('userinfo')?json({sub:'member',name:'Owner'}):json({access_token:'new-token',expires_in:3600});});
  const {url}=await startOAuth('linkedin',e);const state=new URL(url).searchParams.get('state');
  const request=new Request(`https://api.example.test/social/oauth/linkedin/callback?state=${state}&code=test`);
  assert.match((await finishOAuth(request,e)).headers.get('location'),/connection=linkedin/);assert.equal(exchanges,2);
  assert.match((await finishOAuth(request,e)).headers.get('location'),/connection=failed/);assert.equal(exchanges,2);
  const acct=await e.DB.prepare('SELECT * FROM social_accounts').first();assert.equal(await unseal(acct.token,e,'linkedin'),'new-token');
});
test('expired OAuth state is rejected',async t=>{
  const e=env();const {url}=await startOAuth('linkedin',e);const state=new URL(url).searchParams.get('state');
  await e.DB.prepare("UPDATE social_oauth SET expires_at='2020-01-01'").run();
  t.mock.method(globalThis,'fetch',()=>{throw new Error('must not exchange');});
  const response=await finishOAuth(new Request(`https://api.example.test/social/oauth/linkedin/callback?state=${state}&code=test`),e);assert.match(response.headers.get('location'),/connection=failed/);
});
