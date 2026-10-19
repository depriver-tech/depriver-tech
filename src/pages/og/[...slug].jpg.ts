// Branded 1200x630 share images (Open Graph / Twitter cards), generated at build time.
import type { APIRoute, GetStaticPaths } from "astro";
import satori from "satori";
import { Resvg } from "@resvg/resvg-js";
import sharp from "sharp";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { livePosts, slidesFor } from "../../lib/posts";

const root = process.cwd();
const font = (f: string) => readFileSync(join(root, "public/fonts", f));
const fonts = [
  { name: "Poppins", data: font("Poppins-Regular.ttf"), weight: 400 as const, style: "normal" as const },
  { name: "Poppins", data: font("Poppins-SemiBold.ttf"), weight: 600 as const, style: "normal" as const },
  { name: "Poppins", data: font("Poppins-Bold.ttf"), weight: 700 as const, style: "normal" as const },
  { name: "Hand", data: font("PatrickHand-Regular.ttf"), weight: 400 as const, style: "normal" as const },
];
const dataUri = (path: string, mime: string) => `data:${mime};base64,${readFileSync(path).toString("base64")}`;
const ME = dataUri(join(root, "public/img/privatus-editorial.png"), "image/png");

type Card = { label: string; title: string; description: string; image?: string; badge?: string };

export const getStaticPaths: GetStaticPaths = async () => {
  const posts = await livePosts();
  const pages: { params: { slug: string }; props: Card }[] = posts.map((p) => {
    const cover = p.data.carousel ? join(root, "public/carousels", p.data.carousel, "cover.jpg") : undefined;
    const n = slidesFor(p.data.carousel).length;
    return {
      params: { slug: `blog/${p.id}` },
      props: {
        label: "Privatus Cosmas · Blog",
        title: p.data.title,
        description: p.data.description,
        image: cover && existsSync(cover) ? dataUri(cover, "image/jpeg") : undefined,
        badge: n ? `Carousel · ${n} slides` : p.data.tags[0],
      },
    };
  });
  pages.push(
    { params: { slug: "home" }, props: { label: "Software engineer · Tanzania", title: "Privatus Cosmas / Priver", description: "Web and mobile apps, business systems and practical lessons. Building and learning from Mbeya, Tanzania." } },
    { params: { slug: "story" }, props: { label: "My story", title: "From Kitwe Village to Writing Code", description: "The setbacks, the second chances and everything that made me a Software Engineer & Digital Innovator." } },
  );
  return pages;
};

const el = (type: string, style: Record<string, unknown>, children?: unknown, extra: Record<string, unknown> = {}) =>
  ({ type, props: { style, children, ...extra } });

export const GET: APIRoute = async ({ props }) => {
  const c = props as Card;
  const size = c.title.length > 75 ? 48 : c.title.length > 50 ? 57 : 68;
  const lines = Array.from({length:16},(_,i)=>el("div",{position:"absolute",left:0,top:75+i*33,width:1200,height:1,background:"#d7e2e9"}));
  const svg = await satori(
    el("div", { display:"flex",width:1200,height:630,background:"#fbf7ed",fontFamily:"Poppins",position:"relative",overflow:"hidden" }, [
      ...lines,
      el("div",{position:"absolute",left:41,top:0,width:1,height:630,background:"#d79a96"}),
      el("div",{position:"absolute",left:45,top:0,width:1,height:630,background:"#d79a96"}),
      el("div",{display:"flex",position:"absolute",left:75,top:32,fontSize:18,letterSpacing:2,color:"#45607b"},"DEPRIVER.TECH / FIELD NOTES"),
      el("div",{display:"flex",position:"absolute",left:75,top:96,width:670,flexDirection:"column"},[
        el("div",{display:"flex",fontSize:17,color:"#31568b",fontWeight:600},c.badge || c.label),
        el("div",{display:"flex",fontFamily:"Hand",fontSize:size,lineHeight:1.04,color:"#17345b",marginTop:20},c.title),
        el("div",{display:"flex",width:150,height:7,background:"#f4d96e",marginTop:18,transform:"rotate(-2deg)"}),
        el("div",{display:"flex",fontSize:23,lineHeight:1.45,color:"#425873",marginTop:22,width:620},c.description.length>130?c.description.slice(0,127).trimEnd()+"…":c.description),
      ]),
      el("div",{display:"flex",position:"absolute",right:22,top:47,width:350,height:535,borderRadius:12,background:"#f3df99",transform:"rotate(3deg)"}),
      ...(c.image?[el("img",{position:"absolute",right:280,top:53,width:90,height:112,objectFit:"cover",border:"4px solid #ffffff",borderRadius:5,transform:"rotate(-8deg)"},undefined,{src:c.image,width:90,height:112})]:[]),
      el("img",{position:"absolute",right:0,bottom:0,width:385,height:513,objectFit:"contain"},undefined,{src:ME,width:385,height:513}),
      el("div",{display:"flex",position:"absolute",left:75,bottom:39,flexDirection:"column"},[
        el("div",{display:"flex",fontFamily:"Hand",fontSize:32,color:"#17345b"},"Privatus Cosmas / Priver"),
        el("div",{display:"flex",fontSize:15,color:"#45607b",marginTop:5},"Software engineer · Mbeya, Tanzania"),
      ]),
    ]) as never,{width:1200,height:630,fonts},
  );
  const png = new Resvg(svg,{fitTo:{mode:"width",value:1200}}).render().asPng();
  const jpg=await sharp(png).jpeg({quality:86,mozjpeg:true}).toBuffer();
  return new Response(new Uint8Array(jpg),{headers:{"Content-Type":"image/jpeg"}});
};
