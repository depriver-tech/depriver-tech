const root=document.querySelector<HTMLElement>('[data-archive-manager]');
if(root){
 const api=root.dataset.api||'';
 const login=document.querySelector<HTMLFormElement>('#archive-login')!;
 const keyInput=document.querySelector<HTMLInputElement>('#owner-key')!;
 const workspace=document.querySelector<HTMLElement>('#archive-workspace')!;
 const form=document.querySelector<HTMLFormElement>('#archive-upload')!;
 const status=document.querySelector<HTMLElement>('#manager-status')!;
 const list=document.querySelector<HTMLElement>('#manager-list')!;
 const more=document.querySelector<HTMLButtonElement>('#manager-more')!;
 const button=document.querySelector<HTMLButtonElement>('#upload-button')!;
 const progress=document.querySelector<HTMLProgressElement>('#upload-progress')!;
 let key='',nextPage:number|null=0,generation=0;
 let active:XMLHttpRequest|null=null;
 const lock=()=>{generation++;active?.abort();active=null;key='';keyInput.value='';login.hidden=false;workspace.hidden=true;list.replaceChildren();form.reset();progress.hidden=true;button.disabled=false;status.textContent='Archive locked.';};
 async function request(path:string,method='GET'){
  const res=await fetch(api+path,{method,headers:{Authorization:`Bearer ${key}`}});
  const data=await res.json();if(!res.ok){if(res.status===401)lock();throw new Error(data.error||'Request failed.');}return data;
 }
 function render(file:any){
  const row=document.createElement('article');row.className='upload-row';
  const title=document.createElement('h3');title.textContent=file.title;
  const info=document.createElement('p');info.textContent=`${file.filename} · ${(file.size/1024/1024).toFixed(1)} MB · ${file.status}`;
  const desc=document.createElement('p');desc.textContent=file.description;
  const toggle=document.createElement('button');toggle.type='button';toggle.textContent=file.status==='published'?'Hide file':'Publish file';
  toggle.addEventListener('click',async()=>{toggle.disabled=true;const g=generation;try{const action=file.status==='published'?'hide':'publish';await request(`/admin/archive/${file.id}/${action}`,'POST');if(g!==generation)return;await load(true);status.textContent=action==='publish'?'File published. It is now publicly downloadable.':'File hidden. It is now a draft.';}catch(e){status.textContent=(e as Error).message;toggle.disabled=false;}});
  row.append(title,info,desc,toggle);
  if(file.status==='published'){const link=document.createElement('a');link.href=`${api}/archive/${file.id}/download`;link.textContent='Download';row.append(link);}
  list.append(row);
 }
 async function load(reset=false){const page=reset?0:nextPage;if(page===null)return;const g=generation;const data=await request(`/admin/archive?page=${page}`);if(g!==generation)return;if(reset)list.replaceChildren();data.files.forEach(render);nextPage=data.nextPage;more.hidden=nextPage===null;if(!list.children.length){list.textContent='No uploads yet. Add your first file above.';}}
 login.addEventListener('submit',async(e)=>{e.preventDefault();key=keyInput.value.trim();status.textContent='Checking access…';try{await load(true);if(!key)return;keyInput.value='';login.hidden=true;workspace.hidden=false;status.textContent='Archive unlocked.';}catch(e){key='';status.textContent=(e as Error).message;}});
 document.querySelector('#archive-lock')!.addEventListener('click',lock);
 window.addEventListener('pagehide',lock);
 more.addEventListener('click',async()=>{more.disabled=true;try{await load();}catch(e){status.textContent=(e as Error).message;}finally{more.disabled=false;}});
 form.addEventListener('submit',(e)=>{
  e.preventDefault();const data=new FormData(form);const file=data.get('file') as File;
  if(!file||!file.size||file.size>95*1024*1024){status.textContent='Choose a file between 1 byte and 95 MiB.';return;}
  const params=new URLSearchParams({filename:file.name,title:String(data.get('title')||''),description:String(data.get('description')||'')});
  const xhr=new XMLHttpRequest();active=xhr;const g=generation;
  xhr.open('POST',`${api}/admin/archive?${params}`);xhr.setRequestHeader('Authorization',`Bearer ${key}`);xhr.setRequestHeader('Content-Type','application/octet-stream');xhr.timeout=600000;
  button.disabled=true;progress.hidden=false;progress.value=0;status.textContent='Uploading draft…';
  xhr.upload.onprogress=(event)=>{if(event.lengthComputable)progress.value=Math.round(event.loaded/event.total*100);};
  const done=()=>{if(g!==generation)return;active=null;button.disabled=false;progress.hidden=true;};
  xhr.onload=async()=>{if(g!==generation)return;done();let result;try{result=JSON.parse(xhr.responseText);}catch{status.textContent='Upload response was not readable. Refresh the file list before retrying.';return;}
   if(xhr.status>=200&&xhr.status<300){form.reset();status.textContent='Draft uploaded. Review it below, then publish when ready.';try{await load(true);}catch{status.textContent='Draft uploaded, but the list could not refresh. Unlock the archive again to reload it.';}}
   else{if(xhr.status===401)lock();status.textContent=result.error||'Upload failed. Please try again.';}
  };
  xhr.onerror=()=>{done();if(g===generation)status.textContent='Connection lost. Check the archive list before retrying; the upload may have completed.';};
  xhr.ontimeout=()=>{done();if(g===generation)status.textContent='Upload timed out. Check the archive list before retrying.';};xhr.onabort=done;xhr.send(file);
 });
}

export {};
