# Publishing studio

Private owner UI: `/publisher/`. The static page is a sign-in shell, excluded from the sitemap and marked noindex. Every catalog, job and connection request requires the dedicated Worker `PUBLISHER_KEY` (the existing `ADMIN_KEY` also works); the UI keeps the key in memory only. Future article text is bundled into the Worker, never embedded in the public page. Existing public carousel files remain governed by the site's existing asset layout.

## What this release supports

- Existing non-draft articles, including their scheduled dates and image previews.
- Editable captions and EAT calendar; one persistent job per article/platform.
- Instagram professional accounts through Instagram Login: single JPEG or 2–10 selected JPEGs. Longer articles default to the share image; an explicit subset can be chosen. No silent truncation, Reels or Stories in this release.
- LinkedIn **personal profiles**, using OpenID Connect and Share on LinkedIn. Text and article links, not document/PDF or company-page publishing in this release.
- TikTok caption/media-link export and manual completion recorded with a post URL. No TikTok token or unsupported private Direct Post application.
- Single-use OAuth state, AES-GCM token encryption bound to each platform, expiry checks, account pinning when scheduling, disconnect and global pause.
- A five-minute scheduler. The article and selected JPEGs must be reachable before publishing. Schedule at least 15 minutes after the article's date; GitHub scheduled builds can be delayed.
- Bounded retry for pre-publish transient errors; ambiguous results and crashed executions require human reconciliation. Published jobs cannot be rescheduled. This deliberately favors avoiding duplicate public posts over automatic recovery from ambiguous delivery.

There is no claim of exactly-once delivery across external APIs. A failed response can conceal a successful post. Use **Check account**, record the post URL, or explicitly confirm it was not posted before returning it to draft. Pause/disconnect cannot recall an HTTP submission already in flight.

## Local verification

```sh
npm ci
npm run social:test
npm run build
cd worker
npx wrangler d1 execute depriver-engage --local --file migrations/0001_social.sql
npx wrangler dev
```

The build generates publishing JPEGs into `dist/social-media/` only for articles whose publication dates have arrived. The private catalog is generated into ignored `worker/src/social/catalog.json`; Wrangler regenerates it before bundling. The `publisher-worker.yml` workflow redeploys on changes to articles and Worker code once its Cloudflare repository secrets are configured. Without those secrets it emits a warning and does not deploy; manually redeploy the Worker after source changes. Static website deployment alone does not refresh the private catalog.

## Provision once, without publishing

1. Back up the existing D1 database using the Cloudflare dashboard/export before migration.
2. From `worker/`, apply the additive schema:

   ```sh
   npx wrangler d1 execute depriver-engage --remote --file migrations/0001_social.sql
   ```

3. Generate a 32-byte encryption key (`openssl rand -base64 32`) and enter it using `npx wrangler secret put SOCIAL_TOKEN_KEY`. Do not commit it or paste it in chat. Losing/rotating it requires reconnecting accounts. Keep the existing `ADMIN_KEY`. Provision a separate `PUBLISHER_KEY` for studio access; it cannot access moderation endpoints.
4. Create developer applications in Meta and LinkedIn. Enter their secrets with Wrangler:

   ```sh
   npx wrangler secret put INSTAGRAM_CLIENT_ID
   npx wrangler secret put INSTAGRAM_CLIENT_SECRET
   npx wrangler secret put LINKEDIN_CLIENT_ID
   npx wrangler secret put LINKEDIN_CLIENT_SECRET
   ```

5. Configure exact OAuth redirect URLs:

   - `https://depriver-engage.depriver-tech.workers.dev/social/oauth/instagram/callback`
   - `https://depriver-engage.depriver-tech.workers.dev/social/oauth/linkedin/callback`

6. Instagram: Business Login for Instagram, professional account, permissions `instagram_business_basic` and `instagram_business_content_publish`. Follow Meta's access/review requirements for the accounts being connected. LinkedIn: enable **Share on LinkedIn** and **Sign In with LinkedIn using OpenID Connect**; request `openid profile w_member_social`.
7. Verify the API versions in `worker/wrangler.toml` are still supported before launch. Keep `SOCIAL_PUBLISHING_ENABLED = "false"` during setup. Deploy the Worker, then deploy the site including its post-build JPEG export.
8. Open `/publisher/`, unlock with the studio access key, and use **Connections** to authorize accounts. Confirm the account labels and expiry dates. Tokens are never returned to the browser. Reconnect before expiry; automatic token refresh is not implemented.

For subsequent automatic Worker deployments, configure repository secrets `CLOUDFLARE_API_TOKEN` (scoped to this account's Worker and D1 deployment needs) and `CLOUDFLARE_ACCOUNT_ID`. OAuth client secrets and the encryption key belong in Worker secrets, not GitHub or the browser. The CI workflow runs tests, applies the idempotent additive migration, and deploys the Worker. The website workflow remains separate; runtime availability checks bridge deployment ordering.

## Enable automatic posting

After connecting the correct accounts, prepare and review a real post. Set `SOCIAL_PUBLISHING_ENABLED = "true"`, redeploy the Worker, then use **Resume publishing** in the studio. Individual posts still require **Schedule this post**. There is no bulk auto-enrollment of the backlog. The scheduler only processes explicitly scheduled jobs, one per five-minute invocation to bound provider subrequests. Posts on multiple platforms may therefore publish several minutes apart.

Validate one post per platform end to end before scheduling a batch: verify the actual account, image order, caption, saved provider ID, post URL and queue history. Remote provider behavior cannot be proven by local mocks. Inspect Worker logs without logging tokens or OAuth codes.

## Operations

- **Pause publishing** stops future submissions; reconnecting does not silently change the account assigned to a scheduled post.
- Unschedule before editing. Saving clears stale container IDs.
- Expired/disconnected accounts fail safely and require reconnection/review.
- The browser does not automatically refresh while you edit; use **Refresh** for current status.
- Account disconnect deletes the stored encrypted token and returns scheduled jobs to drafts. Revoke app access in the provider account too if needed.
- No upload storage or AI generation is included. This first release reuses the site's existing content and media pipeline.
- The admin UI uses the existing owner-key trust model. HTTPS is required; do not share the key. A future multi-user product should use individual sessions, roles and scoped accounts.

## Primary references

- [LinkedIn Share on LinkedIn](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin)
- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [LinkedIn OpenID Connect](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2)
- [Instagram publishing](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/content-publishing)
- [Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/business-login)
- [TikTok intended use and publishing UX](https://developers.tiktok.com/docs/en/content-sharing-guidelines)
- [Cloudflare scheduled handler](https://developers.cloudflare.com/workers/runtime-apis/handlers/scheduled/)
