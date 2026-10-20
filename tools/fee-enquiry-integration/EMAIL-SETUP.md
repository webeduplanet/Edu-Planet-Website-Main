# Temporary email delivery for EduPlanet enquiries

The current fee and scholarship-interest forms support FormSubmit email delivery. No Google account, Google Sheet or server credential is required for this route. The spreadsheet integration remains available in the original handler files if it is wanted later.

## Current state

The fee contact gate has been removed at the owner’s request. View fees now opens a public grade-based popup on the current page, with an expandable inclusions summary. It collects no contact details and sends no fee-enquiry emails. Apply actions link directly to the existing Google application form.

The separate scholarship-interest form still sends to **info@eduplanet.co.za**. The owner confirmed activation on 20 October 2026, but live inbox delivery remains unverified after connection timeouts/rejections.

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

5. Test the scholarship-interest form with agreed sample contact details and confirm its email arrives. Then publish the approved website update.

## Parent experience

- Fees open immediately, with no name, phone or email required and no provider request.
- The native expandable toggle contains the school’s supplied three benefit groups.
- Scholarship interest is a separate form requesting parent/guardian name, contact number, email and grade.
- Scholarship success requires a positive provider acknowledgement. Failure retains entered details, and closing an in-progress request prevents a late success confirmation.
- The website writes no contact details to browser storage. FormSubmit processes scholarship submissions; receiving-mailbox retention is controlled by the school.

## Documentation

- [FormSubmit AJAX](https://formsubmit.co/ajax-documentation)
- [Activation, inbox delivery and retention](https://formsubmit.co/help)
- [Reply-To, subjects and spam controls](https://formsubmit.co/documentation)

Run the automated checks with:

```text
node --test tools/fee-enquiry-integration/handler.test.cjs tools/fee-enquiry-integration/popup.test.cjs
```

The current suite checks public fee access and separate scholarship submission behaviour with simulated provider responses, not actual inbox delivery.
