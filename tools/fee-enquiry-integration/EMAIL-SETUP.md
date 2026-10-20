# Temporary email delivery for EduPlanet enquiries

The current fee and scholarship-interest forms support FormSubmit email delivery. No Google account, Google Sheet or server credential is required for this route. The spreadsheet integration remains available in the original handler files if it is wanted later.

## Current state

The owner selected **info@eduplanet.co.za** and confirmed clicking **Activate Form** on 20 October 2026. `feeEnquiryMode` is now `email` and `emailForms.activated` is true. All View fees entry links lead to included benefits. The button beneath the benefits reveals a required name, phone and email popup form. Only a positive submission acknowledgement opens the separate fee popup. There is no direct-fee bypass when the connection is unavailable. Live browser and setup checks did not confirm delivery: requests timed out or returned HTTP 403. Actual inbox delivery remains unverified.

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

- The contact-details popup requests name, contact number and email; fees appear after the service positively acknowledges the enquiry. An unavailable or inactive connection leaves the form visible with an error; fees stay closed.
- Once enabled, the scholarship form requests parent/guardian name, contact number, email and grade of interest. Until activation it presents a contact email link rather than accepting a submission. Details entered for fees are prefilled while the fee popup remains open; they can be edited.
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

The current suite has 19 tests. They check behaviour with simulated provider responses, not actual inbox delivery.
