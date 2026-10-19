import type { APIRoute } from "astro";
import { readFileSync } from "node:fs";
import { basename, join } from "node:path";
import { zipSync, strToU8 } from "fflate";
import { livePosts, slidesFor, type Post } from "../../lib/posts";

export async function getStaticPaths() {
  return (await livePosts()).flatMap((post) => {
    const slides = slidesFor(post.data.carousel);
    return [
      { params: { file: `${post.id}.txt` }, props: { post, slides, archive: false } },
      ...(slides.length ? [{ params: { file: `${post.id}.zip` }, props: { post, slides, archive: true } }] : []),
    ];
  });
}

export const GET: APIRoute = ({ props, site }) => {
  const { post, slides, archive } = props as { post: Post; slides: string[]; archive: boolean };
  const text = [
    post.data.title,
    "By Privatus Cosmas",
    post.data.date.toISOString().slice(0, 10),
    new URL(`/blog/${post.id}/`, site).href,
    "",
    post.data.description,
    "",
    post.body ?? "",
    ...(slides.length ? ["", "Slide captions", ...slides.map((_, i) => `${i + 1}. ${post.data.slides[i] ?? `${post.data.title}, slide ${i + 1}`}`)] : []),
    "",
  ].join("\n");
  if (!archive) return new Response(text, { headers: { "Content-Type": "text/plain; charset=utf-8" } });

  const files: Record<string, Uint8Array> = { "article.txt": strToU8(text) };
  for (const slide of slides) files[`slides/${basename(slide)}`] = readFileSync(join(process.cwd(), "public", slide));
  // Images are already compressed; storing them keeps builds fast and preserves quality.
  const zip = zipSync(files, { level: 0 });
  return new Response(new Uint8Array(zip), { headers: { "Content-Type": "application/zip" } });
};
