# EduPlanet SEO and legacy-link priorities

Checked 21 October 2026, Africa/Johannesburg. Public checks only; no website or account settings changed. Request evidence: `seo-live-check-2026-10-21.json`.

## Current public findings

- All ten public HTML pages return 200 but contain `noindex, nofollow`. The additional `/index.html` version does too. This is the most urgent SEO issue. [Google: noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing).
- All ten have the same generic meta description and no canonical link. Home is available at both `/` and `/index.html`.
- `/robots.txt` and `/sitemap.xml` return 404, as do the two former WordPress sitemap addresses. Missing robots.txt alone does not block crawling.
- The 24 previously recovered school page addresses still return 404, with and without trailing slashes.
- The older application PDF returns 403 after redirecting to www. This is an access failure in this check; it does not establish deletion.
- No JSON-LD structured data was found on the ten public pages.
- HTTP and non-www homepage requests already redirect to the HTTPS www homepage. Keep this working consolidation.
- An intentionally unknown URL returns a genuine 404. Preserve that status for truly missing content.
- The public server identifies itself as Vercel. Publication should be verified on the actual domain; a GitHub commit/push alone does not establish that the intended Vercel production project deployed it.

## Work order

1. Confirm the repository and branch connected to the active Vercel production project, publish the approved release, and check the public HTML again. The local release already removes public noindex tags and supplies distinct metadata, canonical links, sitemap and robots.txt; these are not yet live.
2. Activate and test the prepared permanent redirects for twenty old school page paths and the two former sitemap addresses. Verify the HTTP redirect, final destination, slash handling and target section. Map to relevant replacement content; do not send every old address to Home. [Google: site moves and URL mapping](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes).
3. Improve the old `/get/` mapping after confirming its original coverage: search-visible old content describes Grades 8–9, so the current Senior Phase is more specific than the generic phase overview. Do not change it solely on the menu label. Confirm old `/high/` coverage separately.
4. Recover current, approved content for the four unresolved routes: `/facilities/`, `/important-documents/`, `/parent-testimonials/` and `/uniform/`. Facilities and parent experiences can be sections of existing pages. The supplied application PDF now gives Important Documents a useful destination at Admissions; add any further current documents before creating a broader download library. Confirm uniform instructions rather than reusing an old supplier blindly.
5. Give the specific old application-PDF URL a permanent redirect to a stable current application resource. A school-owned download URL would make future document changes easier; the supplied Drive viewer can remain the current download destination. Do not redirect every old WordPress media file to one document.
6. Use Search Console to submit the working sitemap, inspect representative pages and redirects, and request indexing of key pages after fixes. Review indexing and search performance over time; no ranking or indexing-date guarantee is implied.
7. Add accurate school/organization structured data with the visible name, address, phone, logo, URL and verified official profile links. Validate the markup. [Google: organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization).

## Recover and grow useful backlinks

- Start with Search Console's External Links and Page Indexing/Not Found exports. Match old linked URLs to the redirect list and prioritise pages that still receive links or visits. Search Console provides a sample, not an exhaustive backlink inventory. An exported file is sufficient to continue this analysis without granting full account access. [Google: Links report](https://support.google.com/webmasters/answer/9049606?hl=en).
- Update important existing listings and partner links to their final current URLs where the school controls the listing or can request a correction. Keep redirects for links and bookmarks that cannot be updated.
- Keep the verified Google Business Profile accurate: school name, address, telephone, website, hours, category and recent approved photos. Invite genuine parent reviews consistently and respond to feedback. [Google: local ranking guidance](https://support.google.com/business/answer/7091?hl=en).
- Identify genuine education, community, church, sporting and sponsor relationships where a relevant school listing or factual story would help their readers. Obtain links to the most useful phase, admissions or event page. No outreach was sent.
- Publish useful current resources that others can reference: phase transition guidance, school-visit information and approved community/sports achievements. Keep location wording natural, using Gqeberha/Port Elizabeth where relevant. Keep useful existing URLs stable.

## Limits

This check refreshes current-page metadata and the known legacy page inventory. It is not a full backlink inventory or a ranking/performance measurement. No Search Console, Business Profile, Vercel dashboard, traffic-log or email-account access was used. CSS/JavaScript asset references, form submissions and inbox delivery were not tested in this pass.
