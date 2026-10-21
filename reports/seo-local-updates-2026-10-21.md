# Local SEO and legacy-link improvements

Prepared 21 October 2026. Local changes only: no commit, push, deployment, account changes or backlink outreach performed in this task.

## Applied

- All ten generated public pages are indexable, with distinct titles/descriptions and self-referencing canonical URLs.
- Navigation uses `/` as the homepage. `/index.html` has a permanent redirect to `/` on Vercel.
- Added consistent School, WebSite and WebPage structured data, with breadcrumbs on the nine inner pages. Name, address, telephone, admissions/general email, logo, founding year and EMIS use existing school information. No invented reviews, ratings or social profiles.
- Sitemap contains exactly the ten canonical public URLs. robots.txt identifies it and keeps internal folders excluded.
- Permanent redirects cover 23 of the 24 recovered old school page paths. The old Grade 8–9 GET page leads directly to Senior Phase.
- Added a concise photo-led Facilities section using approved campus information. Added practical uniform guidance pointing to current school contacts. The Important Documents address leads to the existing application/PDF area.
- Redirects also recover the two old sitemap addresses and the specific 2024 application-PDF address. The supplied Google Drive file remains the application PDF destination.
- The 404 page retains noindex and excludes structured data copied from Contact. Unknown URLs are not redirected to Home.
- `output/` and `tmp/` form drafts and intermediate files are excluded from both publishing paths, alongside the existing tools/reports/source-media exclusions.
- Build checks validate indexing, metadata, canonical URLs, structured data, all 35 fee amounts, PDF/Google Form actions, sitemap contents, legacy-route coverage, redirect destinations and draft exclusions.

## Deliberately pending

- `/parent-testimonials/`: approved parent quotations have not been supplied. It remains unresolved rather than inventing testimonials or redirecting to unrelated content.
- Search Console verification, sitemap submission, indexing requests and backlink exports require the school's account or exported data.
- Google Business Profile updates and actual backlink outreach remain external tasks.
- The active Vercel project/repository/branch and post-deployment HTTP redirects must be confirmed on publication. The simple local preview server and GitHub Pages do not apply Vercel redirect configuration.

## Checked

- Public-site structural/SEO check passes.
- All ten form-behaviour tests pass, without sending enquiries.
- Facilities and uniform guidance checked in the browser.
- Git whitespace check passes.
- Other local work and the supplied PDF link are retained. No staged files or commits were created by this task.

## Before pushing

Commit all intended changed/new root pages, `robots.txt`, `sitemap.xml`, `404.html`, Vercel/publishing configuration, source files and checks together. In particular include the new `site-identity.json`, `legacy-pages.json` and `check_site.py` files. Push to the branch connected to the active production project; then check the real domain's noindex status, sitemap and redirects. The existing GitHub Pages workflow validates public files, while the Vercel-specific redirects apply only on Vercel.
