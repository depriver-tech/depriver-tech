# depriver.tech

Personal storytelling site and blog for Privatus Cosmas. Built with Astro, GSAP and Lenis.
Colours and fonts match the Instagram carousels.

## Run it
    npm install
    npm run dev        # http://localhost:4321
    npm run build      # static site in dist/

## Pages
- `/`: the blog (home page)
- `/story/`: the life story, told as chapters
- `/blog/<post>/`: individual posts (`/blog` redirects to `/`)

## Themes
Press **T** anywhere (or click the palette icon) to open the theme menu, **Shift+T** to jump to the next theme.
It has Auto/Light/Dark, a search box, and grouped themes (Depriver plus every Omarchy theme on this machine)
with a live preview card. The choice is remembered per visitor.
After installing or changing Omarchy themes, run `npm run themes` to regenerate
`src/styles/themes.css` and `src/data/themes.json`, then commit them.

## Where things live
- `/publisher/`: private social publishing studio; see [setup and operating guide](docs/social-publisher.md).
- `src/data/story.ts`: every chapter of the life story, services, lessons and contact details. Edit text here.
- `STORY.md`: the raw life-story notes (local only, git-ignored, never published).
- `src/content/blog/*.md`: blog posts (Markdown).
- `studio/`: carousel design sources (render with `npm run carousel -- <slug>`).
- `worker/`: views + likes API (Cloudflare Worker).
- `scripts/terrain.mjs`: generates the topographic background artwork.

## Publishing (everything lives in git)
Posts are Markdown files in `src/content/blog/`. The file name is the link:
`src/content/blog/coding-basics-for-beginners.md` → `https://depriver.tech/blog/coding-basics-for-beginners/`.
Use short, lowercase, hyphenated names.

```md
---
title: "My post title"
description: "One or two sentences, shown on cards and in link previews."
date: 2026-10-01
status: live          # live = published · draft = hidden
tags: ["tech"]
cover: /img/blog/photo.jpg     # optional (text posts)
carousel: my-carousel          # optional: folder in public/carousels
slides:                        # optional: one caption per slide (also alt text)
  - "Slide 1 caption"
---
Write the caption / article here in Markdown.
```

Push to `main` and GitHub Actions publishes it in about a minute. To take a post down, set `status: draft` and push.

## Carousels
Every carousel is designed in `studio/` (shared palette, fonts and helpers in `studio/base.py`, your photo in `studio/assets/`).

    npm run carousel -- coding-basics-for-beginners

renders `studio/<slug>/make.py` to full-size Instagram JPGs in `studio/<slug>/export/` (not committed) and imports
web slides into `public/carousels/<slug>/`. Then write `src/content/blog/<slug>.md` with `carousel: <slug>`.
New carousel: copy one of the `studio/<slug>/` folders, rename it to the new slug, and edit `make.py`.

## Post downloads
Every published post includes a **Download article (TXT)** link with the complete article and source URL.
Carousel posts also offer **Download all slides (ZIP)** with every numbered image and the article in one file.
These files are generated at build time under `/downloads/`, using the same publication filter as the blog;
draft and future posts do not get downloads. Download links work without JavaScript.

## Link previews
Every post gets a branded 1200×630 share image at `/og/blog/<slug>.jpg` (built by `src/pages/og/`), plus full
Open Graph/Twitter tags, so links unfurl properly on WhatsApp, X, LinkedIn and Facebook.

## AI discoverability
- `/llms.txt` and `/llms-full.txt`: plain-text profile, story and posts for AI assistants (generated from `src/data/story.ts` and posts).
- schema.org JSON-LD `Person` + `WebSite` on every page, `ProfilePage` on /story/, `BlogPosting` on posts.
- `robots.txt` explicitly welcomes AI crawlers; `sitemap-index.xml` lists every live page with last-modified dates.

## Cloudflare (free tier) · `worker/`
One Worker powers views, likes, comments (no login), the contact form and the "Ask about me" assistant.

| Feature | Cloudflare service | Free allowance |
|---|---|---|
| API | Workers | 100,000 requests/day |
| Views, likes, comments, messages | D1 (SQLite) | 5 GB, 5M reads + 100k writes/day |
| "Ask about me" assistant | Workers AI | 10,000 neurons/day |
| Spam protection | Turnstile | unlimited |
| Visitor stats | Web Analytics | unlimited, cookie-free |

Spam protection without logins: Turnstile, a honeypot field, per-visitor rate limits, and comments with links held for review.
Moderate at `https://depriver.tech/moderate/` with the `ADMIN_KEY`. Optional Telegram alerts for new comments and messages.

Setup (once):

    cd worker
    npx wrangler login
    npx wrangler d1 create depriver-engage                            # paste the id into wrangler.toml
    npx wrangler d1 execute depriver-engage --remote --file schema.sql
    npx wrangler secret put SALT          # any long random string
    npx wrangler secret put ADMIN_KEY     # your moderation password
    npx wrangler deploy                   # prints https://depriver-engage.<account>.workers.dev

Then set `engageApi` in `src/data/site.ts` to that URL and push. Optional:
- Turnstile: create a widget for depriver.tech in the dashboard, put the site key in `site.ts` → `turnstileSiteKey`
  and run `npx wrangler secret put TURNSTILE_SECRET`.
- Web Analytics: add depriver.tech in the dashboard and put the token in `site.ts` → `cfAnalyticsToken`.
- Telegram alerts: `npx wrangler secret put TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

Local testing: `npx wrangler dev` in `worker/` with a `.dev.vars` file, and `engageApi: "http://localhost:8787"`.
