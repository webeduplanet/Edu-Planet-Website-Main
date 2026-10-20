# Temporary email delivery for EduPlanet enquiries

The current fee and scholarship-interest forms support FormSubmit email delivery. No Google account, Google Sheet or server credential is required for this route. The spreadsheet integration remains available in the original handler files if it is wanted later.

## Current state

Both forms have been implemented and tested with simulated responses. The owner selected **info@eduplanet.co.za**. On 20 October 2026, FormSubmit reported sending its activation email for the EduPlanet admissions page. The inbox owner must click **Activate Form** and confirm completion before delivery is enabled. `feeEnquiryMode` remains `local-preview`, with a clear sample-data notice; `emailForms.activated` is false. Actual inbox delivery has not been verified.

## Activation

1. Confirm the receiving school inbox.
2. Run `node tools/fee-enquiry-integration/activate-email.mjs CHOSEN-EMAIL-ADDRESS` once. This sends only a clearly labelled school setup test and requests activation; it contains no parent or learner data.
3. The inbox owner clicks the FormSubmit activation link. Check spam as well. No one needs to share mailbox credentials with Codex.
4. After the owner confirms activation, set the following in the approved site's `enrolment-config.json` and its durable source copy:

```json
"feeEnquiryMode": "email",
"emailForms": {
  "recipient": "THE-CONFIRMED-RECEIVING-ADDRESS",
  "activated": true
}
```

`feeEnquiryEndpoint` is unused in email mode. No private key is needed. Setting `activated` to true does not activate FormSubmit; the inbox owner must actually approve the service first. The guard prevents sending while that setup is incomplete.

5. Test both forms with agreed sample contact details and confirm both emails arrive. Then publish the approved website update.

## Parent experience

- Fee form: name, contact number and email; fees appear after the service positively acknowledges the enquiry.
- Scholarship form: parent/guardian name, contact number, email and grade of interest. Details entered for fees are prefilled while the fee popup remains open; they can be edited.
- Distinct email subjects identify fee enquiries and scholarship interest. The parent's email is set as Reply-To.
- A rejected, timed-out or uncertain submission retains the form details and does not show a success message. Network timeouts can still leave delivery uncertain; the code makes no automatic retries.
- Scholarship interest does not guarantee an award, availability or eligibility.
- The website keeps no contact database and writes no parent details to browser storage. FormSubmit processes the submission and documents retaining submissions for 30 days; the receiving school mailbox keeps its delivered emails according to the school's own retention settings.
- The AJAX route uses the provider's server-side spam filtering and the website's hidden honeypot. It does not present an interactive reCAPTCHA. For stronger public-traffic protection, use a hosted form with a challenge or a server-side service.

## Documentation

- [FormSubmit AJAX](https://formsubmit.co/ajax-documentation)
- [Activation, inbox delivery and retention](https://formsubmit.co/help)
- [Reply-To, subjects and spam controls](https://formsubmit.co/documentation)

Run the automated checks with:

```text
node --test tools/fee-enquiry-integration/handler.test.cjs tools/fee-enquiry-integration/popup.test.cjs
```

The current suite has 17 tests. They check behaviour with simulated provider responses, not actual inbox delivery.
