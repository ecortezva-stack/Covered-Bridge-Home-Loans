# Build spec: CBHL General Inquiry form

**Why this is a UI build:** the GHL connector has no create/edit operation for native forms. The browser route
isn't available from the cloud session either: GHL hosts are blocked by its network policy, and it has no GHL login.
Everything the form maps to already exists, so the build is drag-and-drop with no new fields.

Where: GHL → Covered Bridge Home Loans → Sites → Forms → Builder → **+ Add Form** → Start from scratch.

## Form

| Setting | Value |
|---|---|
| Form name | `CBHL General Inquiry` |
| Layout | Single column |
| Font | Inter (matches the site) |
| Button color | `#D2A34C` (site gold), button text `#0D0D0D` |
| Field label color | `#0D0D0D`; background transparent (the Contact page box supplies the panel) |

## Fields, in this order

| # | Field (drag from) | Label shown | Required | Maps to |
|---|---|---|---|---|
| 1 | Personal info → **Full Name** | Full name | Yes | standard `full_name` (GHL splits first/last) |
| 2 | Personal info → **Email** | Email | Yes | standard `email` (duplicate matching key) |
| 3 | Personal info → **Phone** | Phone (optional) | No | standard `phone` (2nd matching key) |
| 4 | Custom fields → **What can we help with?** | What can we help with? | Yes | `contact.what_can_we_help_with` (id `hdB9COoga33lwhQ2D60k`), options: Buying a Home / Refinancing / Exploring Loan Options / General Question |
| 5 | Custom fields → **Property State (if known)** | Property state, if known | No | `contact.property_state_if_known` (id `B5QmIhxxt2tMzRfUfp1x`) |
| 6 | Custom fields → **Inquiry Message** | Brief message (optional) | No | `contact.inquiry_message` (id `fPPzPGYeAmh0NqL3GIit`) |
| 7 | Custom fields → **CBHL Inquiry Source**, set to **Hidden** | — | No | `contact.cbhl_inquiry_source` (id `n1hBhMlVT6CDFR3LLxWu`). Hidden value: query key `cbhl_source`, default value `website`. |
| 8 | Text element (not a field) | "Please don't include Social Security numbers, account numbers or other financial details. This form is for general questions and is not a mortgage application." | n/a | n/a |
| 9 | **Consent checkbox** | **Wording needed. See below.** | n/a | n/a |

Do **not** add SSN, date of birth, credit score, income, account numbers, file uploads, or any
application questions.

### Consent (decision needed before SMS follow-up)

The contact-page notes say any communication consent belongs in the form itself. They also rule out
credit-check authorization, bundled marketing consent and automatic SMS enrollment. SMS follow-up to form
leads under the registered A2P campaign needs approved opt-in wording. That wording is a legal/compliance
decision, so it isn't written here. Until it's supplied:
- build the form without the checkbox,
- form leads still get the internal routing (opportunity, owner, task, notification). The 8-SMS drip in
  CBHL-03 stays draft either way.

## Form settings (gear icon)

| Setting | Value |
|---|---|
| On submit | **Message**: "Thank you. A Covered Bridge Home Loans team member will be in touch soon. If you'd like to pick a time now, you can book a consultation here: {{ custom_values.cbhl_consultation_booking_link }}" |
| Sticky contact | Off (public website) |
| Add tags to contact | `website inquiry` (the workflow also adds it, so this is belt and braces) |
| Facebook pixel / conversion | Leave off unless David asks |

Save, then **Integrate → Embed**. Copy the iframe code and send the form ID back so the workflow and the
docs can reference it (the form ID is the string after `/widget/form/`).

## What happens on submit (CBHL-01 workflow, see 02-workflows.md)

1. GHL matches or creates the contact by email/phone (location setting: no duplicate contacts; verified
   by API test: same email in a different case updated the existing contact).
2. CBHL-01 tags the contact `website inquiry` + `cbhl lead-to-loan`, creates or updates the opportunity
   in **CBHL Lead to Loan → New**, and sets Loan Purpose and Lead Received Date.
3. Owner assignment, a call task and an internal notification follow.

## Test plan once built (use the direct link, not the website)

Use the form's direct URL `https://api.leadconnectorhq.com/widget/form/<FORM_ID>` and a test email
address you control. Use the QA phone only if one is supplied; otherwise leave phone blank.
1. Submit with all required fields → contact created with the 4 custom values, tags present, opportunity in New.
2. Submit again with the same email, uppercase → same contact, no second opportunity, note/task added.
3. Submit with `?cbhl_source=qa-direct-link` on the URL → hidden field stores `qa-direct-link`.
4. Check CBHL-01's execution log (Automation → workflow → Execution Logs) shows each step as executed.
