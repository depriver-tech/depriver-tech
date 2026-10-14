import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import { readdirSync, readFileSync } from "node:fs";

const SITE = "https://depriver.tech";

// Last-modified dates for the sitemap, read from each post's front matter (updated > date).
const postDates = Object.fromEntries(
  readdirSync("./src/content/blog")
    .filter((f) => f.endsWith(".md"))
    .map((f) => {
      const fm = readFileSync(`./src/content/blog/${f}`, "utf8").split("---")[1] ?? "";
      const pick = (k) => fm.match(new RegExp(`^${k}:\\s*["']?([0-9-]{10})`, "m"))?.[1];
      const live = !/^status:\s*draft/m.test(fm);
      return [`${SITE}/blog/${f.replace(/\.md$/, "")}/`, live ? pick("updated") ?? pick("date") : null];
    }),
);
const newest = Object.values(postDates).filter(Boolean).sort().at(-1);

export default defineConfig({
  site: SITE,
  redirects: { "/blog": "/" },
  integrations: [
    sitemap({
      filter: (page) => !page.includes("/moderate/") && !page.includes("/publisher/") && page !== `${SITE}/blog/`,
      serialize(item) {
        if (item.url in postDates) {
          item.lastmod = postDates[item.url] ? new Date(postDates[item.url]).toISOString() : undefined;
          item.changefreq = "monthly";
          item.priority = 0.8;
        } else if (item.url === `${SITE}/`) {
          item.lastmod = newest ? new Date(newest).toISOString() : undefined;
          item.changefreq = "weekly";
          item.priority = 1.0;
        } else if (item.url === `${SITE}/story/`) {
          item.changefreq = "monthly";
          item.priority = 0.9;
        }
        return item;
      },
    }),
  ],
});
