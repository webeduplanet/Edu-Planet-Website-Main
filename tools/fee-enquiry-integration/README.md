# Connect EduPlanet fee enquiries to your Google Sheet

The custom website popup is ready for a private Google Sheet connection. This package is prepared locally; it has not created a Google resource, deployed a public endpoint or submitted any contact details.

## How it works

Parent enters name, phone and email → the website's server checks the details → Google confirms a new row in the enquiries spreadsheet → fees appear in the existing popup.

If saving fails, the fees stay hidden and the form retains the entered details for retry. The fee table is already included in the website source; this enquiry step is not access control for confidential documents.

A dedicated Google service account is the website's identity. Share only the enquiries spreadsheet with that account. You do not need to connect your personal Google Drive to Codex, grant domain-wide delegation, or make the spreadsheet public. The service account has Editor access to the one spreadsheet; Google does not offer an append-only sharing role. Keep this account dedicated to this integration.

## 1. Create your enquiries spreadsheet

In Google Sheets, create a spreadsheet named **EduPlanet — 2027 Fee Enquiries**. Rename its worksheet tab **Fee enquiries**.

Paste this tab-separated header into cell A1:

```text
Received at (UTC)	Name	Contact number	Email	Enquiry
```

It must occupy exactly five columns, A–E. Do not add other school records to this file. Keep the sharing setting Restricted. Freeze the header row if you wish.

The website writes phone numbers as text, preserving their leading zeros. Timestamps are UTC; the column says so explicitly.

## 2. Create the website's service account

Use a school-controlled Google Cloud project:

1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a project for the website.
3. Under **APIs & Services → Library**, enable **Google Sheets API**.
4. Under **IAM & Admin → Service Accounts**, create a dedicated account named `eduplanet-fee-enquiries`.
5. No project-wide IAM role or domain-wide delegation is needed for this integration. Note its generated email address.
6. Create a JSON key for that service account. Keep it private and enter it directly into your hosting provider's secret environment settings in Step 4. Do not paste it into this chat, commit it to Git or put it in any website folder. If your organisation blocks key creation, stop here; an administrator can choose keyless hosting instead.

[Google's service-account and individual-file sharing instructions](https://developers.google.com/workspace/guides/create-credentials#service-account).

## 3. Grant access to this spreadsheet only

Open the enquiries spreadsheet → **Share** → add the service account email as **Editor**. Leave notifications off. Keep general access Restricted.

Copy the spreadsheet ID: the part between `/d/` and `/edit` in its URL. This ID is not the private JSON key. The integration does not need a public spreadsheet link.

## 4. Install the small server endpoint

Tell Codex which host you use before activating anything. The existing site can remain static, but a private server-side function is needed to hold the credential and send confirmed submissions.

### Vercel

Copy the prepared files into a deployment checkout:

- `handler.cjs` → `lib/fee-enquiry-core.cjs`
- `vercel-handler.cjs` → `api/fee-enquiry.js`

The endpoint is `/api/fee-enquiry`. Use Node 20 or newer. There are no npm dependencies.

### Netlify

Copy:

- `handler.cjs` → `lib/fee-enquiry-core.cjs`
- `netlify-handler.cjs` → `netlify/functions/fee-enquiry.cjs`

The endpoint is `/.netlify/functions/fee-enquiry`. Use Node 20 or newer and include the function in your site's deployment configuration.

### GitHub Pages / other static hosting

GitHub Pages cannot execute this endpoint. The website can stay there while the small function runs on a server host. Set the website configuration to that function's HTTPS URL and allow the website's exact origin below. For other hosting, confirm whether Node server functions are supported before choosing an adapter.

### Server environment variables

| Variable | Value |
| --- | --- |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | The entire private JSON key, entered as a secret directly in the hosting dashboard. |
| `GOOGLE_SHEET_ID` | The spreadsheet ID from Step 3. |
| `GOOGLE_SHEET_TAB` | `Fee enquiries` |
| `FEE_ENQUIRY_ALLOWED_ORIGINS` | Exact allowed website origins, comma-separated. For example `https://eduplanet.co.za,https://www.eduplanet.co.za`. Add `http://127.0.0.1:8000` only while testing the local preview. |

Use only origins actually used by the school. There is no shared secret to expose in the browser. Origin checks and a hidden spam field reduce accidental/automated traffic; they are not user authentication. The built-in request limit is per server instance, not a global distributed limit. Configure your hosting provider's endpoint rate limit before public activation.

## 5. Activate only after the endpoint is ready

The local preview configuration currently remains:

```json
"feeEnquiryMode": "local-preview",
"feeEnquiryEndpoint": ""
```

Once the endpoint is deployed and the sheet is shared with the dedicated account, update `enrolment-config.json` in the approved preview:

```json
"feeEnquiryMode": "connected",
"feeEnquiryEndpoint": "https://YOUR-ENDPOINT-HOST/api/fee-enquiry"
```

For a same-host Vercel deployment, the endpoint can be `/api/fee-enquiry`. Netlify uses its path above. A connected preview sends real enquiries to your sheet. The notice in the popup will change from the local demonstration notice to an explanation of the details being sent to the school's enquiries sheet for follow-up. No marketing subscription is created.

Rebuild the local admissions page with `update_enrolment.py` after changing the source or scripts. Configuration values themselves load on refresh. The current working preview is `/private/tmp/eduplanet-phase-preview`; it still needs to be copied into a durable approved deployment checkout before publication. No production page has been changed by preparing this package.

## 6. Confirm the complete flow

Use an agreed test name, phone and email. Check that:

1. Invalid or missing fields prevent submission.
2. One valid submission creates one row in the chosen Google Sheet, and then reveals the fees.
3. The phone's leading zero is retained.
4. Google or network failure leaves the form visible, displays an error and does not claim success.
5. Both phone and desktop views work.

The 12 local automated tests use simulated Google responses. They verify validation, allowed origins, JWT signing, exact sheet headers, RAW text values, acknowledged writes, failures and per-instance throttling. They do not verify a real Google connection. A network timeout after Google has written a row can leave its outcome uncertain; this implementation makes no automatic retries and does not promise exactly-once delivery. Review for a duplicate if someone retries after an uncertain response.

Run the prepared checks with a current Node runtime:

```text
node --test tools/fee-enquiry-integration/handler.test.cjs tools/fee-enquiry-integration/popup.test.cjs
```

## What to send back

- Your hosting provider.
- The spreadsheet link or ID (not publicly shared).
- The service account's email address once created.
- The endpoint URL when deployed.

Keep the private key and all other credentials in your own hosting account. No Google Drive plugin connection is required for this route.
