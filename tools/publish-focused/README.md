# Reviewed EduPlanet website

The `codex/reviewed-eduplanet-site` branch contains the actual reviewed website pages at the repository root, plus the supporting CSS, JavaScript and selected photographs. These include the Grade R–12 offering, Foundation Phase naming, updated logo alignment, phase actions, 2027 grade fee selector, concise admissions steps and scholarship-interest wording.

This is a review branch. It retains a clear review notice and `noindex` metadata. It has not changed the production `main` branch or the live website. Fee enquiry details are still discarded in the explicitly labelled demonstration mode.

## Before production deployment

- Confirm the receiving inbox and activate the temporary email route for both the fee enquiry and scholarship-interest forms. See [Email setup](../fee-enquiry-integration/EMAIL-SETUP.md). Both forms currently remain in demonstration mode; no email has been sent.
- Verify an actual email from each form reaches that inbox before enabling submissions publicly.
- Supply the appointment booking destination, or agree an accounts-office contact fallback.
- Verify the printable application document destination; the existing live PDF URL returned HTTP 403 during checking.
- Remove the review toolbar, review/export controls, demonstration mode and noindex metadata as part of production preparation.
- Set production page titles, descriptions and canonical URLs.

The existing application Google Form URL was recovered from the live website and checked successfully. It appears in `release-status.json`; the reviewed preview still uses its labelled placeholder until production preparation.

## Editing and regenerating this branch

The durable copy of the reviewed version is in `reviewed-source/`. Edit those sources and run:

```text
python3 tools/publish-focused/prepare_review_branch.py
```

This copies the reviewed pages and assets to the repository root. It preserves the labelled review experience. Do not run the historical `tools/build_pages.py` for this version; that script generates the older website.

## Sending this branch to GitHub

In GitHub Desktop, select `codex/reviewed-eduplanet-site` and use **Publish branch** (or **Push origin** if the branch has already been published). A repository push requires a signed-in GitHub account with write access. Keep this branch separate from `main` until the unfinished connections and production cleanup have been completed.
