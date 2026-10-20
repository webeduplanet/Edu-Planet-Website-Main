# EduPlanet Independent School website — reviewed version

This branch contains the reviewed ten-page website for Grade R–12. The four phase pages, selected photographs, 2027 fee selector, admissions updates and aligned logo are included at the repository root.

**Review status:** Public review notices and the fee contact gate are removed. Apply actions link directly to the school’s Google application form. View fees opens a shared grade-fee popup on the current page, with the supplied inclusions in a collapsed toggle. Noindex metadata and the remaining PDF/appointment placeholders still need release cleanup. See [release notes](tools/publish-focused/README.md).

## Pages

- `index.html` — Home
- `about.html` — Vision, mission and values
- `academics.html` — Curriculum and learning support
- `early-years.html` — Foundation Phase, Grades R–3
- `intermediate.html` — Grades 4–6
- `senior.html` — Grades 7–9
- `matric.html` — Grades 10–12
- `admissions.html` — Four application steps and 2027 fees
- `school-life.html` — Sport, activities and school life
- `contact.html` — School contact details

## Running locally

Serve the repository with a static server, for example `python3 -m http.server 8000`. Open `http://127.0.0.1:8000/`.

## Editing

The durable reviewed sources are in `tools/publish-focused/reviewed-source/`. Update them and run:

```text
python3 tools/publish-focused/prepare_review_branch.py
```

The historical `tools/build_pages.py` produces the older website and must not be used to regenerate this reviewed version.

## Forms

Fees are public and collect no contact details. The separate scholarship-interest form retains its enabled email route to info@eduplanet.co.za, with actual inbox delivery still unverified. No secret credentials have been added. See `tools/fee-enquiry-integration/EMAIL-SETUP.md`.

## Publishing

Keep the review branch separate from `main` until production preparation is complete. GitHub Pages is configured to deploy pushes to `main`; the live domain was observed on Vercel. Confirm the production Git integration in the hosting account before merging or promoting this branch.
