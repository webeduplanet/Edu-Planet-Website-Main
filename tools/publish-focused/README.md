# Reviewed EduPlanet website

The `codex/reviewed-eduplanet-site` branch contains the actual reviewed website pages at the repository root, plus the supporting CSS, JavaScript and selected photographs. These include the Grade R–12 offering, Foundation Phase naming, updated logo alignment, phase actions, 2027 grade fee selector, concise admissions steps and scholarship-interest wording.

This is a review branch. Public review notices have been removed; `noindex` metadata remains. It has not changed the production `main` branch or the live website. Apply actions now open the existing Google application form directly. View fees opens the current page’s grade-fee popup, with the supplied Learning Resources, Academic Support and Sport & Extramurals content under a collapsed toggle. The fee contact popup is removed; scholarship interest remains a separate form.

## Before production deployment

- Verify the scholarship-interest email route. See [Email setup](../fee-enquiry-integration/EMAIL-SETUP.md). The owner confirmed activation for info@eduplanet.co.za on 20 October 2026.
- Verify an actual scholarship-interest email reaches the inbox.
- Supply the appointment booking destination, or agree an accounts-office contact fallback.
- Verify the printable application document destination; the existing live PDF URL returned HTTP 403 during checking.
- Remove noindex metadata as part of production preparation. Review controls and demonstration notices are already removed.
- Set production page titles, descriptions and canonical URLs.

The existing application Google Form URL was recovered from the live website and checked successfully. It appears in `release-status.json`; the reviewed preview still uses its labelled placeholder until production preparation.

## Editing and regenerating this branch

The durable copy of the reviewed version is in `reviewed-source/`. Edit those sources and run:

```text
python3 tools/publish-focused/prepare_review_branch.py
```

This copies the reviewed pages and assets to the repository root. It preserves the public page content and does not enable email delivery. Do not run the historical `tools/build_pages.py` for this version; that script generates the older website.

## Sending this branch to GitHub

In GitHub Desktop, select `codex/reviewed-eduplanet-site` and use **Publish branch** (or **Push origin** if the branch has already been published). A repository push requires a signed-in GitHub account with write access. Keep this branch separate from `main` until the unfinished connections and production cleanup have been completed.
