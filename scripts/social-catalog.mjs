// The catalog stays in the Worker bundle; future articles never enter the public panel HTML.
import { readFile, readdir, mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import yaml from 'js-yaml';
import sharp from 'sharp';

const root = resolve(import.meta.dirname, '..');
const catalog = [];
const exportMedia = process.argv.includes('--media');
for (const file of (await readdir(`${root}/src/content/blog`)).filter(f => f.endsWith('.md')).sort()) {
  const source = await readFile(`${root}/src/content/blog/${file}`, 'utf8');
  const match = source.match(/^---\s*\n([\s\S]*?)\n---(?:\n|$)/);
  if (!match) throw new Error(`Missing front matter: ${file}`);
  const data = yaml.load(match[1]);
  if (data.status === 'draft') continue;
  const slug = file.slice(0, -3);
  const date = new Date(data.date).toISOString();
  const url = `https://depriver.tech/blog/${slug}/`;
  const media = [];
  if (data.carousel) {
    if (!/^[a-z0-9-]+$/.test(data.carousel)) throw new Error(`Invalid carousel: ${file}`);
    const folder = `${root}/public/carousels/${data.carousel}`;
    const slides = (await readdir(folder)).filter(f => /^\d+\.(webp|jpe?g|png)$/.test(f))
      .sort((a,b) => parseInt(a)-parseInt(b));
    for (const [index, slide] of slides.entries()) {
      const path = `/social-media/${slug}/${index + 1}.jpg`;
      media.push({ url: `https://depriver.tech${path}`, preview: `/carousels/${data.carousel}/${slide}`, alt: data.slides?.[index] || data.title });
      if (exportMedia && Date.parse(date) <= Date.now()) {
        await mkdir(`${root}/dist/social-media/${slug}`, { recursive: true });
        await sharp(`${folder}/${slide}`).resize(1080, 1350, { fit: 'contain', background: '#0b1e3f' })
          .jpeg({ quality: 90 }).toFile(`${root}/dist${path}`);
      }
    }
  }
  // A single branded share image is an explicit alternative to a long carousel.
  const posterPath = data.carousel ? `/carousels/${data.carousel}/cover.jpg` : `/og/blog/${slug}.jpg`;
  const poster = { url: `https://depriver.tech${posterPath}`, preview: posterPath, alt: data.title };
  const tags = ['depriver', 'TechTanzania', ...(data.tags || []).map(t => t.replace(/[^a-zA-Z0-9]/g, ''))].filter(Boolean);
  const caption = `${data.title}\n\n${data.description}\n\nRead more: ${url}\n\n${[...new Set(tags)].slice(0,5).map(t=>'#'+t).join(' ')}`;
  catalog.push({ slug, title: data.title, description: data.description, date, url, media, poster, caption });
}
await mkdir(`${root}/worker/src/social`, { recursive: true });
await writeFile(`${root}/worker/src/social/catalog.json`, JSON.stringify(catalog, null, 2)+'\n');
console.log(`Publisher: ${catalog.length} eligible articles. ${exportMedia ? 'Live JPEG exports generated.' : 'Private catalog generated.'}`);
