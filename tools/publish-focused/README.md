# EduPlanet website sources and release preparation

The ten-page Grade R–12 website is at the repository root. Its durable editing sources are in `reviewed-source/`. The 20–21 October UX and SEO improvements are prepared locally; no deployment is implied by editing or rebuilding these files.

## Editing

Edit the page sources, `shared-footer.html`, styles and scripts in `reviewed-source/`. Admissions content is also kept in `enrolment-source/body.html`; update the matching Admissions page when changing that fragment. `enrolment-source/fee-dialogs.html` is the single shared fee/scholarship dialog fragment injected into every page. Core navigation/video behaviour lives in the root `assets/js/main.js`.

Build with Python 3 and Pillow installed:

```text
python3 tools/publish-focused/prepare_review_branch.py
python3 tools/publish-focused/check_site.py
node --test tools/fee-enquiry-integration/popup.test.cjs
```

The default build prepares production metadata, distinct descriptions, canonical URLs, School/WebSite/WebPage and breadcrumb structured data, a sitemap, robots.txt and a helpful 404 page. School details live in `reviewed-source/site-identity.json`; only verified details and profiles should be added. It does not publish anything. For a separate private review deployment, use `--preview` on both Python commands; that mode excludes the review from indexing. Rebuild without `--preview` before public deployment. The check is also run by the existing GitHub Pages workflow.

Do not run the historical `tools/build_pages.py`; it generates an older website. The latest owner edit, “Select your child’s phase”, is retained on Academics.

## Parent actions

- Every Apply now link opens the existing school Google application form directly.
- View fees opens the current page’s grade-fee popup. There is no contact gate. Only the selected grade is remembered in session storage; no contact details are stored there.
- Full benefits remain visible on Admissions, with a shorter expandable summary in the popup. Stationery and optional aftercare are identified separately.
- Appointment requests lead to Contact, then the existing school WhatsApp number or accounts email. They do not book or confirm a time automatically. An approved HTTPS `VISIT_CALENDAR_URL` in `enrolment-config.json` can replace these request links later.
- Step 1 links Download the PDF form directly to the owner-supplied Google Drive PDF. The viewer opens in a new tab and offers download and print, including without signing in. `APPLICATION_PDF_URL` stores the same link.
- The scholarship form registers interest through the existing email route. Activation is owner-confirmed; inbox delivery remains unverified.

The application deadline and late-application notice are manually editable in `enrolment-config.json`. The current deadline is 30 October 2026.

## Hosting preparation

`vercel.json` includes 27 permanent redirects: 23 old school routes, two former sitemap addresses, `/index.html` to the canonical homepage, and the specific old 2024 application PDF to the supplied current Drive PDF. The old Grade 8–9 GET page now leads to Senior Phase. Facilities and uniform guidance use existing approved information; Important Documents leads to the application/downloads section. Old routes are normalised without trailing slashes. The redirect destinations and fragments have been checked locally; Vercel routing itself needs a deployed preview/production check. The Python preview server and GitHub Pages do not apply `vercel.json` redirects. No blanket catch-all redirect is used.

Reports, tools, original source media and local `output/` and `tmp/` drafts are excluded from both publishing paths. The custom 404 page should retain an actual 404 status when the host serves a missing address.

## Still needed from the school or account owner

1. Edit the Google Form: remove Grade RR; review its title, duplicate contact questions, academic-support wording, optional marketing questions, second page and confirmation. Website access alone does not grant editor access to that form.
2. A current application PDF link has been supplied and connected. Provide a booking calendar if wanted in place of the working appointment-request routes.
3. Confirm aftercare hours/charges, phase entry requirements, document checklist, subject combinations and examination-board details before publishing additional specifics.
4. Supply approved current results, staff credentials, parent testimonials and relevant reels before adding new evidence or claims.
5. Confirm a real scholarship enquiry reaches info@eduplanet.co.za. No real enquiry was sent during implementation/testing.
6. Select/connect an analytics account before measuring completed applications and appointments. No tracking service has been added.
7. Supply approved parent quotations before restoring or redirecting `/parent-testimonials/`. That one legacy page intentionally remains unresolved; no quotes or ratings have been invented.
8. Review this local version, publish through the authorised Git/hosting workflow, then test the actual domain. The live site's older application action and indexing settings remain unchanged until deployment.

## Before pushing this release

Commit the generated root pages, search files, Vercel configuration and all changed/new source/check files together. The local changes have not been committed or pushed by this implementation. The existing GitHub Pages workflow checks the generated public files before uploading. Vercel serves the production domain; verify its connected repository/branch in the hosting dashboard, then confirm the real domain receives this release. After publication, test the permanent redirects, page indexing settings and sitemap, then submit the sitemap in Search Console. Search Console exports and Google Business Profile work remain account-side tasks.
