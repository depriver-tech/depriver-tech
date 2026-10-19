import {test} from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import worker from '../src/index.js';
import {fileDetails,MAX_UPLOAD_BYTES} from '../src/archive.js';
function env(){
 const sqlite=new DatabaseSync(':memory:');sqlite.exec(readFileSync(new URL('../migrations/0002_archive.sql',import.meta.url),'utf8'));
 const DB={prepare(sql){const st=sqlite.prepare(sql);let args=[];const q={bind(...v){args=v;return q;},async first(){return st.get(...args)||null;},async all(){return {results:st.all(...args)};},async run(){return st.run(...args);}};return q;}};
 const objects=new Map();const ARCHIVE_FILES={async put(key,body){const data=await new Response(body).arrayBuffer();objects.set(key,data);return {size:data.byteLength};},async get(key){const b=objects.get(key);return b?{size:b.byteLength,body:b}:null;},async head(key){return this.get(key);},async delete(key){objects.delete(key);}};
 return {DB,ARCHIVE_FILES,ADMIN_KEY:'admin-test',PUBLISHER_KEY:'publisher-test',ALLOWED_ORIGINS:'https://depriver.tech',objects};
}
const send=(e,path,method='GET',body,headers={})=>worker.fetch(new Request('https://api.example.test'+path,{method,headers,...(body===undefined?{}:{body})}),e,{});
const auth={Authorization:'Bearer admin-test',Origin:'https://depriver.tech'};
async function upload(e,name='lesson.pdf',body='pdf-content'){return send(e,`/admin/archive?filename=${encodeURIComponent(name)}&title=Test%20file&description=Example`,'POST',body,{...auth,'Content-Length':String(body.length)});}
test('only owner can manage; publisher and foreign origins denied',async()=>{
 const e=env();assert.equal((await send(e,'/admin/archive')).status,401);
 assert.equal((await send(e,'/admin/archive','GET',undefined,{Authorization:'Bearer publisher-test'})).status,401);
 assert.equal((await send(e,'/admin/archive','GET',undefined,{...auth,Origin:'https://evil.test'})).status,403);
});
test('upload -> draft hidden -> publish -> exact download -> hide',async()=>{
 const e=env();const response=await upload(e);assert.equal(response.status,201);const {file}=await response.json();
 assert.equal(file.status,'draft');assert.equal((await (await send(e,'/archive')).json()).files.length,0);
 assert.equal((await send(e,`/archive/${file.id}/download`)).status,404);
 assert.equal((await send(e,`/admin/archive/${file.id}/publish`,'POST',undefined,auth)).status,200);
 const listed=await (await send(e,'/archive')).json();assert.equal(listed.files.length,1);assert.ok(!JSON.stringify(listed).includes('object_key'));
 const result=await send(e,`/archive/${file.id}/download`);assert.equal(await result.text(),'pdf-content');assert.equal(result.headers.get('X-Content-Type-Options'),'nosniff');assert.match(result.headers.get('Content-Disposition'),/^attachment/);assert.equal(result.headers.get('Cache-Control'),'no-store');
 const head=await send(e,`/archive/${file.id}/download`,'HEAD');assert.equal(head.status,200);assert.equal(await head.text(),'');
 await send(e,`/admin/archive/${file.id}/hide`,'POST',undefined,auth);assert.equal((await send(e,`/archive/${file.id}/download`)).status,404);assert.equal(e.objects.size,1);
});
test('all requested file groups can be uploaded',async()=>{
 for(const name of ['guide.pdf','notes.docx','photo.png','android.apk','installer.exe','app.AppImage','bundle.zip']){const response=await upload(env(),name);assert.equal(response.status,201,name);}
});
test('reject paths, active web formats, empty files, oversized and unknown lengths',async()=>{
 for(const file of ['../secret.pdf','folder\\file.pdf','index.html','image.svg','script.js','bad\nname.pdf'])assert.equal(fileDetails(file),null);
 assert.equal((await upload(env(),'bad.html')).status,400);
 assert.equal((await upload(env(),'empty.pdf','')).status,413);
 assert.equal((await send(env(),'/admin/archive?filename=a.pdf&title=Title','POST','x',auth)).status,411);
 assert.equal((await send(env(),'/admin/archive?filename=a.pdf&title=Title','POST','x',{...auth,'Content-Length':String(MAX_UPLOAD_BYTES+1)})).status,413);
});
test('stored length mismatch rolls back object',async()=>{const e=env();const r=await send(e,'/admin/archive?filename=a.pdf&title=Title','POST','x',{...auth,'Content-Length':'2'});assert.equal(r.status,400);assert.equal(e.objects.size,0);});
test('database failure removes the newly uploaded object',async()=>{const e=env();const original=e.DB.prepare;e.DB.prepare=(sql)=>{if(sql.startsWith('INSERT'))throw new Error('simulated DB failure');return original(sql);};const old=console.error;console.error=()=>{};try{assert.equal((await upload(e)).status,500);assert.equal(e.objects.size,0);}finally{console.error=old;}});
test('unconfigured storage gives an actionable response',async()=>{const e=env();delete e.ARCHIVE_FILES;assert.equal((await send(e,'/archive')).status,503);assert.equal((await send(e,'/admin/archive','GET',undefined,auth)).status,503);});
test('publication requires the stored object and invalid pages are rejected',async()=>{const e=env();const {file}=await (await upload(e)).json();e.objects.clear();assert.equal((await send(e,`/admin/archive/${file.id}/publish`,'POST',undefined,auth)).status,409);assert.equal((await send(e,'/archive?page=-1')).status,400);});
test('pagination includes all files without exposing drafts',async()=>{const e=env();for(let i=0;i<52;i++){const {file}=await (await upload(e,`${i}.pdf`)).json();await send(e,`/admin/archive/${file.id}/publish`,'POST',undefined,auth);}await upload(e,'draft.pdf');const first=await (await send(e,'/archive')).json();const second=await (await send(e,'/archive?page=1')).json();assert.equal(first.files.length,50);assert.equal(first.nextPage,1);assert.equal(second.files.length,2);assert.equal(second.nextPage,null);assert.equal(new Set([...first.files,...second.files].map(f=>f.id)).size,52);});
