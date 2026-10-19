# Personal search visibility: Privatus Cosmas / Priver

## Current status

The Docs Archive release f974b20 completed its GitHub Pages build and deployment on 19 October 2026. The Worker workflow skipped its deployment steps because deployment secrets were absent. Browser-based archive uploads are therefore not active. Live HTTP and visual checks could not be performed from this session because the domain was inaccessible to its network tools.

## Changes in this update

- Homepage title: Privatus Cosmas (Priver) | Software Engineer in Tanzania.
- Visible homepage heading names Privatus Cosmas; introduction connects Priver, software engineering and Mbeya, Tanzania.
- Person schema includes Priver as an alternate name and uses the existing portrait rather than a site icon. Profile links come from the same contact data as visible links.
- WebSite schema includes alternate site names. Blog authors and publishers refer to the same Person identifier.
- About-page title and introduction identify the person and nickname.
- A substantive software-development page describes existing services and how to discuss a project. Footer links connect it and the Docs Archive to the rest of the site.
- Sitemap metadata excludes future publication dates from the homepage last-modified value. Private tools remain excluded from the sitemap and marked noindex.
- Existing canonical URLs, social metadata, crawler access, static HTML and article publication filtering are retained.

## Focus queries

Prioritise “Privatus Cosmas”, “Privatus Cosmas software engineer”, “Priver Tanzania”, “Priver software engineer”, “software engineer in Mbeya” and specific services such as “web and mobile app developer Tanzania”. “Priver” alone is ambiguous, while “software engineer” alone has broad global competition and unclear hiring intent. No first-place ranking or fixed indexing date is promised.

Search results sampled on 19 October 2026 showed a LinkedIn profile and a PyPI profile for Privatus Cosmas; this is not a personalised Google ranking audit. The Priver query also returned unrelated companies and another engineer. Search Console is required to inspect this website's actual indexing, impressions and clicks.

## Owner steps after deployment

1. Open https://search.google.com/search-console and verify the domain property depriver.tech using the DNS record Google supplies. Alternatively verify the URL-prefix property https://depriver.tech/ with Google's supported HTML-file or meta-tag method. Keep the verification record/file in place. No verification value has been invented or installed by this update.
2. Submit https://depriver.tech/sitemap-index.xml in Sitemaps.
3. Inspect the homepage, /story/, /software-engineer-tanzania/ and /docs/. Use Test live URL to check crawl access and Google's selected canonical, then request indexing where appropriate.
4. Confirm which personal LinkedIn profile is current before changing the site's existing LinkedIn link. The source currently links to /in/incpritech/; public search also returns /in/privatus-cosmas-32aa003a2/.
5. Use a consistent public name, for example “Privatus Cosmas (Priver)”, and a direct link to https://depriver.tech/ on your own GitHub, LinkedIn and other professional profiles. These external profiles have not been edited.
6. Add genuine project case studies with the problem, your role, implementation decisions and supported results. Obtain permission before publishing client details. Avoid invented awards, client counts or copied location pages.
7. Review Search Console weekly: indexed pages, crawl errors, branded-query impressions/clicks and relevant service queries. Compare periods over several weeks rather than treating one search as a reliable ranking measurement.

## Verification

Run `npm run build`, then `node scripts/check-seo.mjs`. The check validates generated HTML metadata, canonical URLs, one H1 per key page, connected JSON-LD identities, blog author references, sitemap dates and private-page exclusions. This is not a Lighthouse score, Google Rich Results validation or proof of indexing. No browser rendering or live Core Web Vitals measurements were available during this session.

## Official guidance

- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/appearance/structured-data/profile-page
- https://developers.google.com/search/docs/appearance/site-names
- https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- https://support.google.com/webmasters/answer/9008080
