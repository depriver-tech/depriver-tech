export {};
type Media = { url:string; preview?:string; alt:string };
type Article = { slug:string; title:string; description:string; date:string; url:string; caption:string; media:Media[]; poster:Media };
type Job = { id:string; source_slug:string; source_url:string; platform:string; title:string; caption:string; media:Media[]; scheduled_at:string; status:string; error?:string; external_url?:string };
type Account = { platform:string; label:string; expires_at:string };
type Studio = { catalog:Article[]; jobs:Job[]; accounts:Account[]; enabled:boolean; deployEnabled:boolean; connections:Record<string,boolean> };
const el = <T extends HTMLElement = HTMLElement>(id:string) => document.getElementById(id) as T;
const esc = (s:unknown) => String(s ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));
const label = (p:string) => (({instagram:'Instagram',linkedin:'LinkedIn',tiktok:'TikTok'} as Record<string,string>)[p] || p);
const date = (s:string) => new Intl.DateTimeFormat('en-GB',{timeZone:'Africa/Dar_es_Salaam',day:'numeric',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'}).format(new Date(s));
const localTime = (s:string) => new Date(Date.parse(s)+3*3600000).toISOString().slice(0,16);
const status = (s:string) => `<span class="badge ${esc(s)}">${esc(s === 'review' ? 'Check account' : s)}</span>`;
let key = '';
let data:Studio;
let article:Article;
let job:Job|undefined;
let view = 'library';
let busy = false;
const dialog = el<HTMLDialogElement>('editor');
const platform = el<HTMLSelectElement>('platform');
const caption = el<HTMLTextAreaElement>('caption');
const schedule = el<HTMLInputElement>('schedule');
const notice = (message:string) => { el('notice').textContent = message; };

async function call(path='',body?:unknown,method=body === undefined?'GET':'POST') {
  const requestKey = key;
  const response = await fetch(`${el('publisher').dataset.api}/admin/social${path}`,{
    method, headers:{Authorization:`Bearer ${key}`,'Content-Type':'application/json'},
    ...(body === undefined ? {} : {body:JSON.stringify(body)}), signal:AbortSignal.timeout(30000),
  });
  let value:any;
  try { value = await response.json(); } catch { throw new Error('The publishing service returned an unreadable response.'); }
  if (key !== requestKey) throw new Error('Studio locked. Unlock it to continue.');
  if (response.status === 401) { lock(); throw new Error('Your admin key was not accepted.'); }
  if (!response.ok) throw new Error(value.error || 'The request could not be completed.');
  return value;
}

function lock() {
  key=''; data=undefined as any; job=undefined;
  dialog.close();
  el<HTMLFormElement>('unlock').reset();
  el('workspace').hidden=true; el('login').hidden=false; el('lock').hidden=true;
  ['library','queue','calendar','accounts','stats','media-options','events','preview-caption','editor-title'].forEach(id=>el(id).replaceChildren());
  caption.value=''; el<HTMLImageElement>('preview-image').removeAttribute('src');
}
async function load() {
  data = await call();
  render();
}
function render() {
  const count = (states:string[]) => data.jobs.filter(j=>states.includes(j.status)).length;
  el('stats').innerHTML = [[data.catalog.length,'Stories in library'],[count(['scheduled']),'Scheduled'],[count(['published']),'Published'],[count(['failed','review','handoff']),'Need your attention']]
    .map(([n,s])=>`<div class="stat"><strong>${n}</strong><span>${s}</span></div>`).join('');
  el('engine-state').textContent = !data.deployEnabled ? 'Setup mode · live posting disabled' : data.enabled ? 'Automatic publishing is on' : 'Publishing is paused';
  const toggle = el<HTMLButtonElement>('toggle-engine');
  toggle.textContent=data.enabled?'Pause publishing':'Resume publishing'; toggle.disabled=!data.deployEnabled;
  renderLibrary(); renderQueue(); renderCalendar(); renderAccounts();
  showView(view);
}
function showView(next:string) {
  view=next;
  ['library','queue','calendar','accounts'].forEach(v=>el(`${v}-view`).hidden=v!==view);
  document.querySelectorAll<HTMLButtonElement>('[data-view]').forEach(b=>{
    if(b.dataset.view===view)b.setAttribute('aria-current','page'); else b.removeAttribute('aria-current');
  });
}
function renderLibrary() {
  const query=el<HTMLInputElement>('search').value.toLowerCase();
  const articles=data.catalog.filter(p=>(p.title+' '+p.description).toLowerCase().includes(query))
    .sort((a,b)=> {
      const af=Date.parse(a.date)>=Date.now(),bf=Date.parse(b.date)>=Date.now();
      if(af!==bf)return af?-1:1;
      return af?Date.parse(a.date)-Date.parse(b.date):Date.parse(b.date)-Date.parse(a.date);
    });
  el('library').innerHTML=articles.map(p=>`<article class="card"><img class="card-image" src="${esc(p.media[0]?.preview || p.poster.preview)}" alt="" loading="lazy"/><div class="card-body"><div class="card-meta"><span>${Date.parse(p.date)>Date.now()?'Upcoming article':'Publication date passed'}</span><span>${p.media.length} slides</span></div><h3>${esc(p.title)}</h3><p>${esc(date(p.date))} EAT</p><p>${esc(p.description)}</p><button data-prepare="${esc(p.slug)}">Prepare a post ↗</button></div></article>`).join('') || '<div class="empty">No articles match your search.</div>';
}
function row(j:Job) {
  return `<article class="row"><div>${status(j.status)} <span class="muted">${label(j.platform)}</span><h3>${esc(j.title)}</h3><p>${esc(date(j.scheduled_at))} EAT</p>${j.error?`<p class="error">${esc(j.error)}</p>`:''}${j.external_url?`<p><a href="${esc(j.external_url)}" target="_blank" rel="noopener noreferrer">View published post ↗</a></p>`:''}</div><button data-job="${esc(j.id)}">Open post ↗</button></article>`;
}
function renderQueue() {
  const filter=el<HTMLSelectElement>('status-filter').value;
  const jobs=data.jobs.filter(j=>filter==='all'||j.status===filter).sort((a,b)=>Date.parse(a.scheduled_at)-Date.parse(b.scheduled_at));
  el('queue').innerHTML=jobs.map(row).join('')||'<div class="empty">No posts here yet. Start with an article in your content library.</div>';
}
function renderCalendar() {
  const jobs=data.jobs.filter(j=>['scheduled','processing','published'].includes(j.status)).sort((a,b)=>Date.parse(a.scheduled_at)-Date.parse(b.scheduled_at));
  let day='';
  el('calendar').innerHTML=jobs.map(j=>{
    const next=localTime(j.scheduled_at).slice(0,10);
    const heading=day!==next?`<h3 class="calendar-date">${esc(date(j.scheduled_at).split(',')[0])}</h3>`:'';
    day=next; return heading+row(j);
  }).join('')||'<div class="empty">Your calendar is clear. Schedule a draft to see it here.</div>';
}
function renderAccounts() {
  el('accounts').innerHTML=['instagram','linkedin','tiktok'].map(p=>{
    const a=data.accounts.find(a=>a.platform===p);
    const expired=a&&Date.parse(a.expires_at)<=Date.now();
    return `<article class="card"><div class="card-body"><p class="eyebrow">${p==='tiktok'?'MANUAL HANDOFF':a&&!expired?'CONNECTED':'CONNECTION'}</p><h2>${label(p)}</h2><p>${p==='tiktok'?'Prepare the caption and media here, then finish posting in TikTok.':a?`${esc(a.label)}<br/>Authorization ${expired?'expired':'expires'} ${esc(date(a.expires_at))} EAT.`:'Connect your '+(p==='instagram'?'Creator or Business account.':'personal profile.')}</p>${p==='tiktok'?'<a href="https://www.tiktok.com/tiktokstudio/upload" target="_blank" rel="noopener noreferrer">Open TikTok Studio ↗</a>':`<button data-connect="${p}" ${!data.connections[p]?'disabled':''}>${a?'Reconnect':'Connect'} ${label(p)}</button>${!data.connections[p]?'<p>Developer-app setup required before connecting.</p>':''}${a?`<button data-disconnect="${p}" style="margin-top:12px">Disconnect</button>`:''}`}</div></article>`;
  }).join('');
}
function selectedMedia() { return Array.from(document.querySelectorAll<HTMLInputElement>('#media-options input:checked')).map(i=>i.value); }
function mediaChoices(selected:string[]) {
  el('media-options').innerHTML=[article.poster,...article.media].map((m,i)=>`<label><input type="checkbox" value="${esc(m.url)}" ${selected.includes(m.url)?'checked':''}/><img src="${esc(m.preview || m.url)}" alt="${esc(m.alt)}" loading="lazy"/><span>${i===0?'Share image':`Slide ${i}`}</span></label>`).join('');
}
function updatePreview() {
  const p=platform.value;
  const media=selectedMedia();
  el('media-controls').hidden=p!=='instagram';
  el('preview-channel').textContent=label(p);
  el('preview-name').textContent=data.accounts.find(a=>a.platform===p)?.label || 'depriver.tech';
  el('preview-caption').textContent=caption.value;
  const image=el<HTMLImageElement>('preview-image');
  const chosen=[article.poster,...article.media].find(m=>m.url===media[0]);
  image.hidden=p!=='instagram'||!chosen;
  if(chosen) { image.src=chosen.preview || chosen.url;image.alt=chosen.alt; }
  const max=p==='instagram'?2200:3000;
  el('caption-count').textContent=`${[...caption.value].length.toLocaleString()} / ${max.toLocaleString()} characters${p==='instagram'?` · ${media.length} images selected`:''}`;
  caption.maxLength=max;
}
async function openEditor(source:Article,current?:Job) {
  article=source;job=current;
  el('editor-title').textContent=article.title;
  platform.value=job?.platform||'instagram';platform.disabled=!!job;
  caption.value=job?.caption||article.caption;
  const defaultTime=new Date(Math.max(Date.now()+3600000,Date.parse(article.date)+15*60000)).toISOString();
  schedule.value=localTime(job?.scheduled_at||defaultTime);
  schedule.min=localTime(article.date);
  el('article-date').textContent=`Article publication: ${date(article.date)} EAT. The publisher waits until the article and images are reachable.`;
  const link=el<HTMLAnchorElement>('preview-source');link.href=article.url;
  mediaChoices(job?job.media.map(m=>m.url):article.media.length>0&&article.media.length<=10?article.media.map(m=>m.url):[article.poster.url]);
  el('editor-note').textContent=job?.error||(!job&&article.media.length>10?'This article has more than 10 slides. The share image is selected; choose up to 10 slides if you prefer.':'');
  const editable=!job||['draft','failed','cancelled','handoff'].includes(job.status);
  caption.disabled=!editable;schedule.disabled=!editable;
  el<HTMLButtonElement>('choose-poster').disabled=!editable;
  el<HTMLButtonElement>('save-draft').disabled=!editable;
  document.querySelectorAll<HTMLInputElement>('#media-options input').forEach(i=>i.disabled=!editable);
  el('editor-state').textContent=job?`Status: ${job.status}. ${!editable?'Unschedule before editing.':''}`:'Save a draft, then schedule it when ready.';
  const actions=[];
  if(job?.status==='draft'&&job.platform!=='tiktok')actions.push('<button type="button" data-action="schedule" class="primary">Schedule this post</button>');
  if(job?.status==='scheduled')actions.push('<button type="button" data-action="cancel">Unschedule & edit</button>');
  if(job?.status==='review'||job?.status==='handoff'){
    actions.push('<button type="button" data-action="published">Record published post</button>');
    if(job.status==='review')actions.push('<button type="button" data-action="not-published">I checked: it was not posted</button>');
  }
  if(platform.value==='tiktok')actions.push('<button type="button" data-action="download">Download caption & media links</button>');
  el('job-actions').innerHTML=actions.join('');
  el('history').hidden=!job;el('events').replaceChildren();
  updatePreview();
  if(!dialog.open)dialog.showModal();
  if(job){
    const currentId=job.id;
    try { const result=await call(`/jobs/${job.id}/events`);if(job?.id===currentId)el('events').innerHTML=result.events.map((e:any)=>`<li>${esc(date(e.created_at))} · ${esc(e.action)}${e.detail?`<br/>${esc(e.detail)}`:''}</li>`).join(''); }
    catch(error){el('editor-note').textContent=(error as Error).message;}
  }
}
async function action(task:()=>Promise<void>) {
  if(busy)return;
  busy=true;
  try{await task();}catch(error){if(dialog.open)el('editor-note').textContent=(error as Error).message;else notice((error as Error).message);}
  finally{busy=false;}
}
el<HTMLFormElement>('unlock').addEventListener('submit',event=>{
  event.preventDefault();
  action(async()=>{
    key=el<HTMLInputElement>('admin-key').value;await load();el<HTMLInputElement>('admin-key').value='';
    el('login').hidden=true;el('workspace').hidden=false;el('lock').hidden=false;notice('');
  });
});
el('lock').addEventListener('click',()=>{lock();notice('Studio locked.');});
el('refresh').addEventListener('click',()=>action(load));
el('search').addEventListener('input',renderLibrary);
el('status-filter').addEventListener('change',renderQueue);
document.querySelectorAll<HTMLButtonElement>('[data-view]').forEach(b=>b.addEventListener('click',()=>showView(b.dataset.view!)));
el('close-editor').addEventListener('click',()=>dialog.close());
caption.addEventListener('input',updatePreview);
platform.addEventListener('change',()=>{updatePreview();el('job-actions').innerHTML=platform.value==='tiktok'?'<button type="button" data-action="download">Download caption & media links</button>':'';});
el('media-options').addEventListener('change',updatePreview);
el('choose-poster').addEventListener('click',()=>{mediaChoices([article.poster.url]);updatePreview();});
el('toggle-engine').addEventListener('click',()=>action(async()=>{
  if(!data.enabled&&!confirm('Resume automatic publishing? Due scheduled posts will publish to their connected accounts.'))return;
  await call('/settings',{enabled:!data.enabled});await load();
}));
el('workspace').addEventListener('click',event=>{
  const button=(event.target as HTMLElement).closest<HTMLButtonElement>('button');if(!button)return;
  const d=button.dataset;
  action(async()=>{
    if(d.prepare)await openEditor(data.catalog.find(p=>p.slug===d.prepare)!);
    if(d.job){const j=data.jobs.find(j=>j.id===d.job)!;const source=data.catalog.find(p=>p.slug===j.source_slug)||{slug:j.source_slug,title:j.title,description:'Article removed from library. You can unschedule or reconcile its existing post.',date:j.scheduled_at,url:j.source_url,caption:j.caption,media:j.media,poster:j.media[0]||{url:'',alt:j.title}};await openEditor(source,j);}
    if(d.connect){const result=await call(`/connect/${d.connect}`,{});window.location.assign(result.url);}
    if(d.disconnect&&confirm(`Disconnect ${label(d.disconnect)}? Scheduled posts will return to drafts. A submission already in flight may still complete.`)){await call(`/accounts/${d.disconnect}`,undefined,'DELETE');await load();}
  });
});
el<HTMLFormElement>('editor-form').addEventListener('submit',event=>{
  event.preventDefault();
  action(async()=>{
    const body={slug:article.slug,platform:platform.value,caption:caption.value,scheduled_at:new Date(schedule.value+':00+03:00').toISOString(),media:selectedMedia()};
    const result=await call(job?`/jobs/${job.id}/save`:'/jobs',body);
    const id=job?.id||result.id;await load();await openEditor(article,data.jobs.find(j=>j.id===id));el('editor-note').textContent='Saved. Review the preview before scheduling.';
  });
});
el('job-actions').addEventListener('click',event=>{
  const button=(event.target as HTMLElement).closest<HTMLButtonElement>('[data-action]');if(!button)return;
  const a=button.dataset.action;
  action(async()=>{
    if(a==='download'){
      const text=`${article.title}\n\n${caption.value}\n\nArticle: ${article.url}\n\nMedia (website previews; save the images you need):\n${article.media.map((m,i)=>`${i+1}. https://depriver.tech${m.preview}`).join('\n')}`;
      const url=URL.createObjectURL(new Blob([text],{type:'text/plain'}));const link=document.createElement('a');link.href=url;link.download=`${article.slug}-tiktok.txt`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);return;
    }
    if(!job)return;
    const id=job.id;
    if(a==='schedule'){
      if(!confirm(`Schedule this exact caption for ${label(job.platform)} on ${date(job.scheduled_at)} EAT? It will publish automatically when publishing is enabled.`))return;
      await call(`/jobs/${id}/schedule`,{});
    }else if(a==='cancel')await call(`/jobs/${id}/cancel`,{});
    else if(a==='published'){
      const url=prompt('Paste the published post URL from your social account:');if(!url)return;
      await call(`/jobs/${id}/resolve`,{outcome:'published',url});
    }else if(a==='not-published'){
      if(!confirm('Have you checked the social account and confirmed this post does not exist? Returning to draft allows another publishing attempt.'))return;
      await call(`/jobs/${id}/resolve`,{outcome:'not_published',confirmed:true});
    }
    await load();await openEditor(article,data.jobs.find(j=>j.id===id));
  });
});
const connection=new URLSearchParams(location.search).get('connection');
if(connection){notice(connection==='failed'?'The account could not be connected. Check developer-app settings and try again.':`${label(connection)} connected. Unlock the studio to continue.`);history.replaceState(null,'',location.pathname);}
