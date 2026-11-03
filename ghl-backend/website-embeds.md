# Website embeds and placement guide (for the page builder)

Nothing in the website files was changed. Paste these into your GHL pages yourself.

## 1. Consultation booking calendar (exists now)

Calendar: **Home Loan Consultation**, ID `BSwRRQDlZgYCbEJAPwdE`.
Mon–Fri 8:00–17:00 ET, 30-minute phone consultations, team member calls the booker.

**Direct link** (for buttons and backend testing):

```
https://api.leadconnectorhq.com/widget/booking/BSwRRQDlZgYCbEJAPwdE
```

The same link is stored as custom value `{{ custom_values.cbhl_consultation_booking_link }}`.

**Embed code** (Custom HTML/JavaScript element, full width):

```html
<iframe src="https://api.leadconnectorhq.com/widget/booking/BSwRRQDlZgYCbEJAPwdE" style="width: 100%;border:none;overflow: hidden;" scrolling="no" id="BSwRRQDlZgYCbEJAPwdE_cbhl"></iframe><br><script src="https://link.msgsndr.com/js/form_embed.js" type="text/javascript"></script>
```

What was verified: the calendar ID and settings were read back through the API, and the API returned bookable
slots 8:00–16:30 ET on weekdays. What wasn't: rendering. This build session's network blocks GHL's public
hosts, so the page couldn't be loaded here. Before pasting, open **Calendars → Home Loan Consultation → ⋯ →
Share → Embed code** and compare. If GHL shows a different script domain (white-label), use GHL's copy.

**Placement:**
- **Contact page:** under the inquiry form, add a "Prefer to pick a time? Book a consultation" button
  linking to the direct link (opens in a new tab). Or embed the widget below the form box.
- **Optional `/book` page:** header global section → one Custom HTML element with the embed code →
  footer global section. Don't add it to the menu until the reminder workflow (CBHL-09) is live.
- Don't put the widget inside the dark hero panel. It needs a light background and at least 360px width.

## 2. General inquiry form (UI build pending: see build-specs/01-inquiry-form.md)

The native form can't be created through the API. When it's built, its embed code will look like this
(replace `FORM_ID`):

```html
<iframe src="https://api.leadconnectorhq.com/widget/form/FORM_ID" style="width:100%;height:100%;border:none;border-radius:4px" id="inline-FORM_ID" data-layout="{'id':'INLINE'}" data-trigger-type="alwaysShow" data-activation-type="alwaysActivated" data-deactivation-type="neverDeactivate" data-form-name="CBHL General Inquiry" data-layout-iframe-id="inline-FORM_ID" data-form-id="FORM_ID" title="CBHL General Inquiry"></iframe>
<script src="https://link.msgsndr.com/js/form_embed.js"></script>
```

Always paste GHL's own copy from **Forms → CBHL General Inquiry → Integrate → Embed**, not this template.

**Placement:** Contact page → inside `<div class="cbhl-contact__form">`, replacing the comment block marked
`GHL FORM EMBED GOES HERE`. The box shows automatically once it isn't empty.

**Source tracking:** to tell pages apart, add `?cbhl_source=<page>` to the iframe `src`, e.g.
`.../widget/form/FORM_ID?cbhl_source=contact-page`. Without it the hidden field records `website`.

## 3. Application button

Stays hidden (`applicationUrl` is empty) until the application destination is confirmed (Scout vs Floify
on the old site). Nothing to paste yet.

## 4. Website-to-GHL tests to run once your pages are live

1. Contact page loads the form; submit with your own test email → contact, tags `website inquiry` +
   `cbhl lead-to-loan`, opportunity in **CBHL Lead to Loan → New**, owner assigned, task created
   (needs CBHL-01 published).
2. `CBHL Inquiry Source` shows the page value (or `website`).
3. Submit again with the same email → no duplicate contact, no second opportunity.
4. Booking button/widget opens the calendar on desktop and phone width; book a slot with your test
   email → appointment on Mark's or Teresa's calendar, contact assigned to that person
   (CBHL-09 adds the opportunity once published).
5. Reschedule and cancel using the links in the confirmation → appointment status updates.
6. Check browser console for blocked third-party scripts if the iframe doesn't resize.
