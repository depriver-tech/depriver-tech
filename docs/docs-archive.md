# Docs Archive

Public page: `/docs/`. Owner upload desk: `/docs/manage/`. The Git notebook PDF is bundled at `/archive/git-the-practical-notebook.pdf`, so it works independently of the upload service.

## Publishing the service

The existing GitHub Actions Worker workflow runs the archive tests, ensures a private R2 bucket, applies the additive D1 migration, then deploys. Configure repository secrets `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` for this account's Workers deployment, D1 changes and R2 bucket creation/access. R2 must be activated on the account. Do not make the bucket public. Without these secrets the existing workflow skips backend deployment and emits a warning; a successful website deployment alone does not enable uploads.

Manual setup from an authenticated machine:

```sh
npm ci
npm run archive:test
npm run social:test
npm run build
# With the deployment environment variables available:
node scripts/ensure-archive-bucket.mjs
cd worker
npx wrangler d1 execute depriver-engage --remote --file migrations/0002_archive.sql
npx wrangler deploy
```

The binding is `ARCHIVE_FILES`; bucket name is `depriver-docs-archive`. The existing `ADMIN_KEY` remains the owner credential. No new secrets are embedded in the page. The social `PUBLISHER_KEY` does not grant archive access. Applying the SQL creates a new table/index and does not modify existing engagement data.

## Everyday use

1. Open `/docs/manage/` and unlock with the existing owner admin key.
2. Give the file a clear title and description. For applications include version, operating system and installation notes.
3. Select a supported file and choose **Upload as draft**. Progress appears during transfer.
4. Review the displayed details and choose **Publish file**. The file becomes public immediately through the API, without rebuilding the site.
5. Choose **Hide file** to remove it from public listing and disable new downloads. Previously downloaded copies cannot be recalled. Hiding preserves the object and metadata as a draft.
6. Lock the archive when finished. The key is held in memory only; refreshing requires unlocking again.

## Supported files and limits

Documents: PDF, DOC/DOCX, ODT, TXT, Markdown, CSV, XLS/XLSX, PPT/PPTX, EPUB. Images: JPEG, PNG, WebP, GIF, AVIF. Applications: APK/AAB, EXE/MSI, DMG, DEB/RPM, AppImage. Archives: ZIP, 7z, TAR, GZ/TGZ.

Maximum upload: 95 MiB (99,614,720 bytes). Larger applications require a future multipart upload implementation or external release hosting. Downloads stream from R2. The upload request uses the raw file body and its browser-provided Content-Length, avoiding multipart form buffering. Empty files, unsupported extensions, path separators, and control characters are rejected. Uploads have a ten-minute client timeout.

All uploaded files download as attachments with `application/octet-stream`, `nosniff`, a restrictive CSP and no-store caching. HTML, JavaScript and SVG uploads are not allowed. Every public download checks published status in D1; the R2 bucket stays private. Extension checks are not malware detection. There is no virus scanner, signature verification, resumable upload, or image preview in this release. The owner should only publish files they have reviewed. No permanent deletion endpoint is exposed.

Listing is paginated at 50 files. Search and category filters operate on loaded results; **Load more** fetches the rest. Errors keep the static Git lesson available. Titles/descriptions are rendered as text, never HTML. The manager is noindex and excluded from the sitemap, while API authorization provides actual access control.

## Verification

- `npm run archive:test`: 9 tests using real SQLite with an R2-compatible test double, covering auth, draft isolation, publish/download/hide, upload groups, validation, size mismatch rollback, database failure cleanup, missing storage, missing objects and pagination.
- `npm run social:test`: regression coverage for the existing social Worker features.
- `npm run build`: full static site build.
- After production deployment: verify an anonymous upload is denied; upload a small test document as owner; verify its draft download returns 404; publish, download and compare bytes; hide and verify 404 again. Do not claim this live flow passed based on the local test double alone.

A process termination between writing R2 and saving D1 can leave an unlisted orphan object. Periodic storage reconciliation can remove objects with no matching metadata. No automated cleanup is included.

## Rebuilding the lesson

Install `reportlab` in a Python environment and run `python studio/git-notebook/build.py`. The generator embeds the local Patrick Hand, Poppins and Liberation Mono fonts, produces the PDF plus an editable Markdown text companion, and fails if text exceeds the page layout. Patrick Hand's SIL OFL is included beside the font. The approved concept is implemented as vector notebook lines, handwritten headings and callouts, and selectable precise command blocks.

Primary technical reference: https://developers.cloudflare.com/r2/api/workers/workers-api-reference/
