# EduPlanet Independent School website — reviewed version

This branch contains the reviewed ten-page website for Grade R–12. The four phase pages, selected photographs, 2027 fee selector, admissions updates and aligned logo are included at the repository root.

**Review status:** the on-page review notice and noindex metadata remain. The fee enquiry popup is an explicitly labelled demonstration and does not save or send contact details. This branch is not ready to replace production until those connections and production cleanup are completed. See [release notes](tools/publish-focused/README.md).

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

The fee collection and scholarship registration forms are not connected. The prepared server-side integration and setup instructions remain in `tools/fee-enquiry-integration/`. No secret credentials have been added. The application, PDF, appointment and FAQ destinations still use labelled review placeholders.

## Publishing

Keep the review branch separate from `main` until production preparation is complete. GitHub Pages is configured to deploy pushes to `main`; the live domain was observed on Vercel. Confirm the production Git integration in the hosting account before merging or promoting this branch.
