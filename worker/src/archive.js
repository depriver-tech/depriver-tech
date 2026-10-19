// Owner-managed files. R2 remains private; every download checks publication in D1.
export const MAX_UPLOAD_BYTES = 95 * 1024 * 1024;
const TYPES = {
  pdf:'documents', doc:'documents', docx:'documents', odt:'documents', txt:'documents', md:'documents',
  csv:'documents', xls:'documents', xlsx:'documents', ppt:'documents', pptx:'documents', epub:'documents',
  jpg:'images', jpeg:'images', png:'images', webp:'images', gif:'images', avif:'images',
  apk:'applications', aab:'applications', exe:'applications', msi:'applications', dmg:'applications',
  deb:'applications', rpm:'applications', appimage:'applications',
  zip:'archives', '7z':'archives', tar:'archives', gz:'archives', tgz:'archives',
};
const ID = /^[a-f0-9-]{36}$/;
const columns = 'id, title, description, filename, category, extension, size, status, created_at';
export function fileDetails(filename) {
  if (typeof filename !== 'string' || filename.length > 180 || !filename.trim() || /[\x00-\x1f\x7f/\\]/.test(filename)) return null;
  const extension = filename.split('.').pop().toLowerCase();
  return TYPES[extension] ? { filename, extension, category:TYPES[extension] } : null;
}
function pagination(url) {
  const raw = url.searchParams.get('page') || '0';
  return /^\d{1,6}$/.test(raw) ? Number(raw) : null;
}
export async function archivePublic(request, env, json, cors) {
  if (!env.ARCHIVE_FILES) return json({error:'Archive uploads are not configured yet.'},503);
  const url=new URL(request.url), parts=url.pathname.split('/').filter(Boolean);
  if (request.method !== 'GET' && request.method !== 'HEAD') return json({error:'Method not allowed.'},405);
  if(parts.length===1){
    const page=pagination(url);if(page===null)return json({error:'Invalid page.'},400);
    const {results}=await env.DB.prepare(`SELECT ${columns} FROM archive_files WHERE status = 'published' ORDER BY created_at DESC, id DESC LIMIT 51 OFFSET ?1`).bind(page*50).all();
    return json({files:results.slice(0,50),nextPage:results.length>50?page+1:null});
  }
  if(parts.length!==3 || parts[2]!=='download' || !ID.test(parts[1]))return json({error:'File not found.'},404);
  const row=await env.DB.prepare("SELECT * FROM archive_files WHERE id = ?1 AND status = 'published'").bind(parts[1]).first();
  if(!row)return json({error:'File not found.'},404);
  const obj= request.method==='HEAD' ? await env.ARCHIVE_FILES.head(row.object_key) : await env.ARCHIVE_FILES.get(row.object_key);
  if(!obj)return json({error:'File not found.'},404);
  const safeName=row.filename.replace(/[^a-zA-Z0-9._ -]/g,'_');
  const encoded=encodeURIComponent(row.filename).replace(/['()*]/g,ch=>'%'+ch.charCodeAt(0).toString(16).toUpperCase());
  return new Response(request.method==='HEAD'?null:obj.body,{headers:{
    ...cors,'Content-Type':'application/octet-stream','Content-Length':String(obj.size),
    'Content-Disposition':`attachment; filename="${safeName}"; filename*=UTF-8''${encoded}`,
    'X-Content-Type-Options':'nosniff','Content-Security-Policy':"sandbox; default-src 'none'",
    'Cache-Control':'no-store',
  }});
}
// Called only after the shared ADMIN_KEY check. PUBLISHER_KEY does not grant access.
export async function archiveAdmin(request, env, json) {
  if(!env.ARCHIVE_FILES)return json({error:'Archive storage is not configured. Follow docs/docs-archive.md.'},503);
  const url=new URL(request.url),parts=url.pathname.split('/').filter(Boolean);
  if(parts.length===2 && request.method==='GET'){
    const page=pagination(url);if(page===null)return json({error:'Invalid page.'},400);
    const {results}=await env.DB.prepare(`SELECT ${columns} FROM archive_files ORDER BY created_at DESC, id DESC LIMIT 51 OFFSET ?1`).bind(page*50).all();
    return json({files:results.slice(0,50),nextPage:results.length>50?page+1:null,maxUploadBytes:MAX_UPLOAD_BYTES});
  }
  if(parts.length===2 && request.method==='POST'){
    const detail=fileDetails(url.searchParams.get('filename'));
    const title=(url.searchParams.get('title')||'').trim();
    const description=(url.searchParams.get('description')||'').trim();
    if(!detail || title.length<2 || title.length>120 || description.length>1000 || /[\x00-\x1f]/.test(title+description))return json({error:'Use a supported file, a title of 2-120 characters, and a description up to 1000 characters.'},400);
    const length=request.headers.get('Content-Length');
    if(!length || !/^\d+$/.test(length))return json({error:'A file size is required.'},411);
    const size=Number(length);
    if(!Number.isSafeInteger(size)||size<1||size>MAX_UPLOAD_BYTES)return json({error:'File must be between 1 byte and 95 MiB.'},413);
    if(!request.body)return json({error:'File is empty.'},400);
    const id=crypto.randomUUID(),key=`files/${id}/${detail.filename}`;
    // Raw file streams retain their platform-provided length and do not buffer large installers in memory.
    const uploaded=await env.ARCHIVE_FILES.put(key,request.body,{httpMetadata:{contentType:'application/octet-stream'}});
    if(!uploaded || uploaded.size!==size){await env.ARCHIVE_FILES.delete(key);return json({error:'Upload length mismatch. Please try again.'},400);}
    try {
      await env.DB.prepare('INSERT INTO archive_files (id, object_key, title, description, filename, category, extension, size, status) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, \'draft\')')
        .bind(id,key,title,description,detail.filename,detail.category,detail.extension,size).run();
    }catch(error){await env.ARCHIVE_FILES.delete(key);throw error;}
    return json({file:{id,title,description,...detail,size,status:'draft'}},201);
  }
  if(parts.length===4 && ID.test(parts[2]) && ['publish','hide'].includes(parts[3]) && request.method==='POST'){
    const row=await env.DB.prepare('SELECT * FROM archive_files WHERE id = ?1').bind(parts[2]).first();
    if(!row)return json({error:'File not found.'},404);
    if(parts[3]==='publish' && !(await env.ARCHIVE_FILES.head(row.object_key)))return json({error:'Stored file is missing; upload it again before publishing.'},409);
    const status=parts[3]==='publish'?'published':'draft';
    await env.DB.prepare('UPDATE archive_files SET status = ?1 WHERE id = ?2').bind(status,parts[2]).run();
    return json({ok:true,status});
  }
  return json({error:'Route not found.'},404);
}
