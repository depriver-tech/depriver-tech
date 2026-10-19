const root=document.querySelector<HTMLElement>('[data-archive]');
if(root){
 const api=root.dataset.api||'';
 const list=document.querySelector<HTMLElement>('#archive-list')!;
 const search=document.querySelector<HTMLInputElement>('#archive-search')!;
 const category=document.querySelector<HTMLSelectElement>('#archive-category')!;
 const count=document.querySelector<HTMLElement>('#archive-count')!;
 const status=document.querySelector<HTMLElement>('#archive-status')!;
 const empty=document.querySelector<HTMLElement>('#archive-empty')!;
 const more=document.querySelector<HTMLButtonElement>('#archive-more')!;
 let nextPage:number|null=0;
 const seen=new Set<string>();
 function filter(){let visible=0;for(const card of list.querySelectorAll<HTMLElement>('.file-card')){card.hidden=!(category.value==='all'||card.dataset.category===category.value)||!card.dataset.search?.includes(search.value.trim().toLowerCase());if(!card.hidden)visible++;}count.textContent=`${visible} ${visible===1?'resource':'resources'}${nextPage!==null?' loaded':''}`;empty.hidden=visible>0;}
 search.addEventListener('input',filter);category.addEventListener('change',filter);
 function text(tag:string,value:string,className=''){const el=document.createElement(tag);el.textContent=value;el.className=className;return el;}
 async function load(){
  if(nextPage===null||!api)return;
  more.disabled=true;status.textContent='Loading files…';
  try{
   const res=await fetch(`${api}/archive?page=${nextPage}`);if(!res.ok)throw new Error('unavailable');
   const data=await res.json();if(!Array.isArray(data.files))throw new Error('invalid');
   for(const file of data.files){
    if(typeof file.id!=='string'||!/^[a-f0-9-]{36}$/.test(file.id)||seen.has(file.id))continue;seen.add(file.id);
    const card=text('article','','file-card');card.dataset.category=file.category;card.dataset.search=`${file.title} ${file.filename} ${file.description}`.toLowerCase();
    card.append(text('span',`${String(file.extension).toUpperCase()} / ${file.category}`,'file-label'),text('h3',file.title),text('p',file.description||file.filename),text('span',`${(file.size/1024/1024).toFixed(1)} MB · ${String(file.created_at).slice(0,10)}`,'file-meta'));
    const a=document.createElement('a');a.textContent='Download file ↓';a.href=`${api}/archive/${file.id}/download`;card.append(a);list.append(card);
   }
   nextPage=Number.isInteger(data.nextPage)&&data.nextPage>nextPage! ? data.nextPage:null;
   more.hidden=nextPage===null;more.textContent='Load more files';status.textContent=nextPage===null?'':'More files are available. Load more to search the rest of the archive.';filter();
  }catch{status.textContent='New uploads could not be loaded. The featured notebooks and practice files are still available.';more.hidden=false;more.textContent='Retry loading files';}
  finally{more.disabled=false;}
 }
 more.addEventListener('click',load);void load();
}

export {};
