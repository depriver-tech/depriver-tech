# Publishing studio verification — 14 October 2026

Built on branch `feat/social-publisher`. No production deployment or social publication was performed.

| Boundary | Result | Evidence |
|---|---|---|
| Static studio build | Passed | Astro built `/publisher/`; complete site build succeeded |
| Client TypeScript | Passed | Strict no-emit check of `src/scripts/publisher.ts` |
| Worker compilation | Passed | Wrangler dry-run produced a 282 KiB bundle |
| D1 schema | Passed | All 7 migration commands ran against isolated local D1 |
| HTTP authentication | Passed | Anonymous `/admin/social` returned 401 |
| HTTP catalog | Passed | Authenticated request returned 82 eligible articles |
| HTTP draft persistence | Passed | Creation returned 201; subsequent read contained the saved draft |
| HTTP scheduling guard | Passed | Scheduling without a connected account returned 400 |
| HTTP deployment gate | Passed | Enabling publishing while deployment flag was false returned 400 |
| Backend behavior | Passed | 18 tests using real SQLite and mocked provider requests |
| Publishing media | Passed | All 164 image references for 16 currently live articles exist in the build |
| Future media | Passed | Future articles have no generated `dist/social-media/<slug>` folder |
| Public page privacy | Passed | Private catalog absent from studio HTML; studio excluded from sitemap and marked noindex |
| CI definitions | Passed | Both deployment workflows parse as YAML |
| Browser interaction/layout | Not verified | Computer-use tool reported no available Chrome browser |
| Real OAuth and social posting | Not verified | Developer-app configuration and account authorization are still required |

Backend tests cover encrypted token integrity/platform binding, anonymous and cross-origin denial, credential exclusion, media/date/caption validation, duplicate jobs, expiring accounts, scheduled-post immutability, pause switches, concurrent claims, unavailable website/media, account changes, uncertain publish outcomes, stale processing recovery, persisted Instagram containers, disconnect, OAuth replay and expired state.

The provider mocks prove local control flow, not that a provider will accept a real app/account. Before enabling unattended publishing, finish the [setup guide](social-publisher.md), inspect the UI in a connected browser, and verify one actual post per enabled platform.
