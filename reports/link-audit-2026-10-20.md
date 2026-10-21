# EduPlanet legacy-link audit and recommendations

Checked 20 October 2026 (Africa/Johannesburg). This is a review report; no website pages or redirects were changed.

## Findings

- All 10 current HTML pages returned HTTP 200. One initial connection error for Foundation Phase cleared on recheck; it is not a confirmed broken page.
- Current HTML navigation and fragment destinations resolve in the repository. The live HTML crawl found no confirmed broken current page/resource references after the Foundation recheck. This does not mean every button performs its intended action: several controls use configuration placeholders.
- **24 old school page addresses return HTTP 404**, after the non-www address redirects to www. These were recovered from the school’s archived 2024 navigation, not invented from common page names.
- The older application PDF returned **HTTP 403**, with access/challenge content rather than the PDF. This is an access failure in the automated check, not evidence that the document has been deleted.
- The existing Google application form returned HTTP 200 and its title is “EduPlanet School - Fees & Application Form”. No application or personal data was submitted. Its contents and response handling still need an owner review before reuse.
- **All 10 live pages contain `noindex, nofollow`.** This is a separate release issue that tells search engines not to index these pages. Remove those review-era directives for the public release.
- `/sitemap.xml`, `/sitemap_index.xml`, `/wp-sitemap.xml` and `/robots.txt` return 404. Missing robots.txt is not itself a crawl block. Publish a current sitemap and a simple robots.txt pointing to it; replace the old WordPress sitemap address with a redirect to the new sitemap.
- No canonical page tags were found in the current source. Add self-referencing canonical URLs and choose one home address (`/` rather than both `/` and `/index.html`).

## Reconnect the parent actions first

| Control/resource | Observed condition | Recommendation |
| --- | --- | --- |
| Apply online / Continue my application | Live `APPLICATION_FORM_URL` is a placeholder, so the buttons open an email-help dialog | Reuse the working Google Form after checking 2027 dates, the Grade R intake, current fees and the requested documents. Use one consistent form destination throughout. |
| PDF application | Placeholder in the new site; previous WordPress PDF returns 403 | Supply an approved current PDF and host it within this repository at a stable address such as `/downloads/application-form.pdf` (proposed). Redirect the specific old PDF address to that replacement once it exists. Do not simply relabel the 2024 document as current. |
| Make an appointment | `VISIT_CALENDAR_URL` is a placeholder | Connect the actual booking calendar. Until then, make the button’s email/contact behaviour clear; do not imply that an appointment has been booked. |
| Read the full FAQ | `FAQ_URL` is a placeholder | Restore a short parent FAQ within Admissions and point the button to it. Reuse relevant questions from the previous version, updating the grade range and current process. A separate FAQ page is optional, not necessary. |
| Scholarship interest | Currently presents a contact email link | Keep that working fallback until the info@eduplanet.co.za FormSubmit activation and delivery tests are complete. A mailto link opens the parent’s email app; it does not send automatically. |
| View fees | Current grade selector works; fee collection route remains inactive | Keep the functioning fee view. Restore the contact form only once its email route is activated and tested. |

Working application form: [EduPlanet fees and application Google Form](https://docs.google.com/forms/d/e/1FAIpQLScvcPgIQBKiv7iKn_6qZiruPIOeQ464HQEsWTzH6ri8QJT2MA/viewform).

Old PDF checked: [2024 application PDF](https://eduplanet.co.za/wp-content/uploads/2023/08/Eduplanet-Application-Form-2024.pdf).

## Old page → recommended destination

All 24 source paths below returned 404. Destinations without a qualification already exist. **PROPOSED SECTION** means content must be restored and the section created before that fragment is used in a redirect. The mappings are recommendations, not installed redirects.

| Old address | Destination relative to www.eduplanet.co.za | Reuse/fix recommendation |
| --- | --- | --- |
| `/about/` | `about.html` | Redirect to the current About page. |
| `/accreditation-umalusi/` | `academics.html#standards` | Reuse current, verified accreditation information here; check documents before carrying over older claims. |
| `/admissions/` | `admissions.html` | Redirect; connect the application controls as a separate urgent fix. |
| `/blog/` | `school-life.html` | Old menu calls this NEWSLETTER. Recover relevant school news or newsletter downloads; use School Life unless a regularly maintained news page is wanted. |
| `/contact/` | `contact.html` | Redirect to current contact details and directions. |
| `/culture/` | `school-life.html#creative-learning` | Redirect to creative learning; retain useful current cultural activities. |
| `/extra-curricular/` | `school-life.html` | Consolidate into School Life instead of recreating a separate overview. |
| `/facilities/` | `school-life.html#facilities [PROPOSED SECTION]` | Add a short photo-led facilities section before redirecting to this fragment, using the approved current facilities information. |
| `/fee-structure/` | `admissions.html?view=fees#fees` | Redirect to the working grade-based 2027 fee popup. |
| `/fet/` | `matric.html` | Redirect to the Grades 10–12 page. |
| `/foundation-phase/` | `early-years.html` | Redirect to the Foundation Phase page, now Grades R–3. Keep the working destination filename for continuity. |
| `/get/` | `academics.html#learning-phases` | Use the current phase overview; retain access to the individual phase pages. |
| `/high/` | `academics.html#learning-phases` | Use the phase overview; confirm the old page’s grade coverage before selecting a more specific landing page. |
| `/important-documents/` | `admissions.html#downloads [PROPOSED SECTION]` | Restore a compact downloads area with current approved documents before adding this fragment redirect. |
| `/intermediate-phase/` | `intermediate.html` | Redirect to Grades 4–6. |
| `/literacy-program/` | `academics.html#teaching-support` | Reuse relevant current support information. Confirm the old programme still operates before making programme-specific promises. |
| `/mathematics-program/` | `academics.html#teaching-support` | Combine useful current maths support information with teaching support; verify any distinct programme details. |
| `/outings-camps/` | `school-life.html` | Retain current camp and outing information within School Life; avoid old dates and booking details. |
| `/parent-testimonials/` | `about.html#parent-experiences [PROPOSED SECTION]` | Select a few current, approved parent quotes for existing pages rather than recreating a long separate testimonials page. |
| `/primary/` | `academics.html#learning-phases` | Redirect to the phase overview so families can choose Foundation or Intermediate. |
| `/school-life/` | `school-life.html` | Redirect to the current School Life page. |
| `/senior-phase/` | `senior.html` | Redirect to Grades 7–9. |
| `/sport/` | `school-life.html#sport` | Redirect to the existing sport section. |
| `/uniform/` | `school-life.html#uniform [PROPOSED SECTION]` | Restore current uniform guidance and supplier/contact details or an approved downloadable guide before linking to this fragment. |

## Keep recovery simple

1. Restore the application route and a current printable form; connect the appointment and FAQ actions.
2. Add permanent redirects for old pages that already have direct equivalents, especially fees, admissions, contact and the four phase pages. Test both slash variants and verify the destination and any fragment. Vercel supports these redirects in its configuration.
3. Recover the small set of useful parent resources: uniform guidance, current downloads, verified accreditation material and selected parent experiences. Place them within existing pages where practical. A full old WordPress rebuild is unnecessary.
4. Remove public-page noindex directives, add canonical URLs and publish a current sitemap. Keep any actual private/review areas excluded separately.
5. Add a helpful 404 page with phase, fees, admissions and contact links. Preserve an actual 404 status for unknown pages.

Use permanent redirects to the closest relevant content. Avoid redirecting every missing address to the homepage, and avoid a blanket `/wp-content/*` redirect to an HTML page. Specific old PDFs and reused media should point to the corresponding replacement file. Obsolete plugin scripts and genuinely retired content can remain 404, or return 410 when intentionally removed.

The previous static version also used `/#discover` and Admissions `#faq1`–`#faq6`, which are absent now. These are potential old bookmark targets, rather than broken links currently emitted by the new navigation. Restore section aliases if needed. URL fragments are not sent to the server, so fix them in page markup or browser navigation rather than relying on a server redirect.

## Evidence and limits

- [Archived school newsletter/menu, 31 July 2024](https://web.archive.org/web/20240731035010id_/https://eduplanet.co.za/blog/)
- [Archived school Contact/menu, 31 July 2024](https://web.archive.org/web/20240731042616id_/https://eduplanet.co.za/contact/)
- [Live form-link configuration](https://www.eduplanet.co.za/enrolment-config.json)
- [Google’s site-move and URL-mapping guidance](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)
- [Vercel redirect documentation](https://vercel.com/docs/routing/redirects)

The archive confirms the former navigation; it does not establish that every old page’s full content or downloadable documents can be recovered. The domain also has much older retail-era archive entries predating this school; those should not be treated as school content to restore.

This audit covers the repository’s 10 pages, public live HTML links and directly referenced resources, the previous static version’s application destinations, and the recovered legacy menu. It does not exhaust every URL ever used, test submissions, crawl every resource referenced inside CSS or JavaScript, or validate email delivery. A Google Search Console “Not found”/Links export or hosting request logs would identify additional incoming addresses and show which old links still receive traffic, without requiring full account access.
