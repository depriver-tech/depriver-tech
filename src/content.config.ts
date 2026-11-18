import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

// Every post is a Markdown file in src/content/blog, tracked in git.
// status: live  -> published on the next push
// status: draft -> hidden (page and listing are removed on the next push)
// date in the future -> scheduled: hidden until that time, then published by the daily 19:05 EAT deploy
//   (write it with a time, e.g. date: 2026-10-10T19:00:00+03:00)
const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    status: z.enum(["live", "draft"]).default("live"),
    tags: z.array(z.string()).default([]),
    cover: z.string().optional(),
    // carousel posts: folder name in public/carousels (import with scripts/add-carousel.py)
    carousel: z.string().optional(),
    // optional caption per slide, shown under the viewer and used as image alt text
    slides: z.array(z.string()).default([]),
  }),
});

const study = defineCollection({
  loader: glob({pattern: "**/*.md", base: "./src/content/study"}),
  schema: z.object({title:z.string(),module:z.string(),code:z.string(),number:z.number().int().min(1).max(8),objective:z.string()}),
});
export const collections = { blog, study };
