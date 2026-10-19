import assert from 'node:assert/strict';
import {readFileSync,readdirSync} from 'node:fs';
const read=p=>readFileSync(`dist/${p}`,'utf8');
const schema=html=>[...html.matchAll(/<script\b[^>]*type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/g)].flatMap(m=>JSON.parse(m[1]));
const pages=[['about/index.html','https://depriver.tech/about/'],['index.html','https://depriver.tech/'],['story/index.html','https://depriver.tech/story/'],['software-engineer-tanzania/index.html','https://depriver.tech/software-engineer-tanzania/'],['docs/index.html','https://depriver.tech/docs/']];
for(const [path,url] of pages){const html=read(path);assert.match(html,/<title>[^<]+<\/title>/);assert.ok(html.includes(`rel="canonical" href="${url}"`),`canonical ${path}`);assert.match(html,/<meta name="description" content="[^"]+"/);assert.ok(!/content="noindex/.test(html));assert.equal((html.match(/<h1(?:\s|>)/g)||[]).length,1,`one h1 ${path}`);schema(html);}
const home=read('index.html');assert.match(home,/<title>Privatus Cosmas \(Priver\)/);assert.ok(home.includes('I’m Privatus Cosmas, also known as Priver.'));
const person=schema(home).find(x=>x['@type']==='Person');assert.ok(person.alternateName.includes('Priver'));assert.equal(person.jobTitle,'Software Engineer');assert.equal(person.image,'https://depriver.tech/img/me-cut.webp');
const site=schema(home).find(x=>x['@type']==='WebSite');assert.ok(site.alternateName.includes('depriver.tech'));
for(const href of person.sameAs)assert.ok(home.includes(`href="${href}"`),`consistent identity link ${href}`);
assert.equal(schema(read('story/index.html')).find(x=>x['@type']==='ProfilePage').mainEntity['@id'],person['@id']);
for(const slug of readdirSync('dist/blog')){let html;try{html=read(`blog/${slug}/index.html`);}catch{continue;}const post=schema(html).find(x=>x['@type']==='BlogPosting');if(post){assert.equal(post.author['@id'],person['@id']);assert.equal(post.publisher['@id'],person['@id']);}}
const xml=readdirSync('dist').filter(p=>/^sitemap.*\.xml$/.test(p)).map(read).join('');
for(const url of ['/about/','/docs/','/software-engineer-tanzania/','/story/'])assert.ok(xml.includes(`https://depriver.tech${url}`));
for(const url of ['/docs/manage/','/publisher/','/moderate/'])assert.ok(!xml.includes(url));
for(const [,date] of xml.matchAll(/<lastmod>(.*?)<\/lastmod>/g))assert.ok(Date.parse(date)<=Date.now(),`future sitemap date ${date}`);
assert.match(read('docs/manage/index.html'),/content="noindex/);
console.log('SEO checks passed: titles, descriptions, one H1, canonical URLs, identity/schema links, article authors, sitemap dates and private-page exclusions.');

const about=read('about/index.html');
assert.equal(schema(about).find(x=>x['@type']==='ProfilePage').mainEntity['@id'],person['@id']);
assert.equal(person.url,'https://depriver.tech/about/');
assert.ok(about.includes('id="contact"'));
const header=home.match(/<header\b[\s\S]*?<\/header>/)[0];
assert.ok(header.includes('href="/about/"'));
assert.ok(!header.includes('/story/'));
assert.ok([...home.matchAll(/<footer\b[\s\S]*?<\/footer>/g)].some(m=>m[0].includes('href="/story/"')));
console.log('About page, main navigation, contact anchor and preserved story footer link verified.');
