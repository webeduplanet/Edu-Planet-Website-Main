# EduPlanet Independent School website

The ten-page Grade R–12 website is at the repository root, with Foundation, Intermediate, Senior and FET phase pages. UX, consistency and SEO improvements from the 20–21 October 2026 reviews are prepared locally for review.

## Local preview

Serve the repository with a static server, for example:

```text
python3 -m http.server 8001 --bind 127.0.0.1
```

Open `http://127.0.0.1:8001/`.

## Current experience

- Direct Google application links and shared View fees access.
- Ungated 2027 grade-fee popup with a fixed title/close control and Apply action.
- Full Admissions benefits plus expandable popup summary; optional aftercare is separated from tuition inclusions.
- Working appointment requests via the existing school WhatsApp and accounts email.
- Concise phase-specific copy, consistent names/actions/footer and mobile refinements.
- Poster-first mobile hero and a quiet desktop background video; no visible video control.
- Distinct metadata, canonical URLs, school structured data, sitemap and public search-indexing settings.
- Facilities and uniform guidance, 23 recovered old school routes, old application-PDF recovery and a helpful 404 page.
- Local PDF drafts and intermediate files excluded from published uploads.

No live deployment has been performed as part of this implementation.

## Editing and checks

See [source and release instructions](tools/publish-focused/README.md). Edit the durable sources in `tools/publish-focused/reviewed-source/`, then rebuild. The historical `tools/build_pages.py` generates an older website and must not be used for this version.

```text
python3 tools/publish-focused/prepare_review_branch.py
python3 tools/publish-focused/check_site.py
node --test tools/fee-enquiry-integration/popup.test.cjs
```

The generator requires Python 3 and Pillow. `--preview` produces explicitly non-indexable private-review files; the default prepares public-release files. Neither command publishes the website.

## External connections

Fees collect no contact details. The separate scholarship-interest form retains its enabled email route to info@eduplanet.co.za; activation is confirmed but actual inbox delivery remains unverified. No secret credentials or analytics service have been added. The owner-supplied application PDF is linked from Admissions. Google Form editing, a booking calendar, verified evidence and a live deployment check remain separate owner/account tasks.
