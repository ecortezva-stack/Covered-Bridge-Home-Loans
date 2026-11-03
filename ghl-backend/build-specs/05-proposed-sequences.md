# PROPOSED message sequences and SMS consent (inactive)

> **Status: PROPOSED. Not approved, not built, not sending.** Message counts and windows come from
> David's table. **Message wording, the day each message goes out, and the send window are proposals**
> written for this document, not requirements. Every sequence stays inactive until David approves the
> copy and spacing, the sending setup is confirmed (email provider and sender, A2P SMS identity) and
> the SMS consent wording is approved.

## Tokens used

| Token | Meaning | State |
|---|---|---|
| `{{contact.first_name}}` | lead's first name | available |
| `{{user.first_name}}` | assigned loan officer's first name | available once an owner is assigned |
| `[SENDER BRAND]` | the business name messages are sent as | **Decision.** SMS must match the registered A2P brand (custom value "Friendly Business Name (A2P)" = "Valor Home Loans"). "Friendly Business Name (For Messages)" is empty. Not replaced with "Covered Bridge Home Loans" without David's confirmation. |
| `{{ custom_values.cbhl_consultation_booking_link }}` | consultation booking link | exists |
| `[APPLICATION LINK]` | online application | **unconfirmed** (Scout vs Floify not chosen). Messages that need it are marked and stay off. |
| `[EMAIL FOOTER]` | sender identity, physical address, licensing disclosure, unsubscribe link | **Decision.** Legal entity/NMLS wording must be approved. The old site shows "Boxcar Mortgage, LLC DBA Valor Home Loans, NMLS #1969375", which isn't confirmed for this brand. |

## Proposed send rules (all sequences)

- Send window: Mon–Fri 9:00–17:00 in the contact's timezone (falls back to America/New_York). This sits
  inside the verified 8:00–17:00 business hours, so replies can be handled. Use the workflow's
  "Wait → time window" before each message.
- Every message step has the guard: has `cbhl lead-to-loan`; lacks `cbhl stop follow-up`,
  `cbhl legacy migrated`, `cbhl test record`; DND respected.
- Stop rules: see 02-workflows.md (status changes, genuine replies, opt-outs).
- No rates, APRs, payment amounts, "pre-approved"/"guaranteed" claims or other mortgage-advertising trigger terms.

---

## A. New + Connected: "8 SMS over 30 Days" (PROPOSED)

| # | Proposed day | Proposed text |
|---|---|---|
| 1 | 0 (on intake, in window) | Hi {{contact.first_name}}, this is {{user.first_name}} with [SENDER BRAND]. Thanks for reaching out about your home loan questions. When's a good time for a quick call? Reply STOP to opt out. |
| 2 | 1 | Hi {{contact.first_name}}, {{user.first_name}} again. If it's easier, you can pick a time for a short phone consultation here: {{ custom_values.cbhl_consultation_booking_link }} |
| 3 | 3 | {{contact.first_name}}, are you mainly looking to buy, refinance, or just exploring options right now? A one-word reply is fine. |
| 4 | 6 | Hi {{contact.first_name}}, a quick conversation can help you understand which loan options may fit your plans. Want me to give you a call? |
| 5 | 10 | {{contact.first_name}}, just checking in. Is now still a good time to talk about your home plans, or should I follow up later? |
| 6 | 15 | Hi {{contact.first_name}}, if questions about documents, timing or the loan process are holding you back, I'm happy to walk through them. Book a time: {{ custom_values.cbhl_consultation_booking_link }} |
| 7 | 22 | {{contact.first_name}}, I don't want to crowd your inbox. Should I keep you on my list for when you're ready? |
| 8 | 29 | Hi {{contact.first_name}}, this is my last text for now. Whenever you're ready to talk about buying or refinancing, just reply here. [SENDER BRAND]. Reply STOP to opt out. |

## B. New + Connected: "18 Email over 90 Days" (PROPOSED)

Every email ends with `[EMAIL FOOTER]`. Sender: **decision** (not the old Valor sender or Emailpal inboxes unless David confirms).

| # | Day | Subject | Body (summary of proposed copy) |
|---|---|---|---|
| 1 | 0 | We received your question | Thanks for contacting us; {{user.first_name}} will reach out; option to book a consultation (link). |
| 2 | 1 | A quick call can save you time | What a first conversation covers: goals, timeline, questions; booking link. |
| 3 | 3 | Buying, refinancing, or exploring? | Brief description of each path and how the conversation differs; reply to say which fits. |
| 4 | 5 | Common loan types, in plain language | Conventional, FHA, VA, USDA overview (no rates, no eligibility promises). |
| 5 | 8 | What documents usually come up | Typical document categories so nothing is a surprise; "don't email sensitive documents". |
| 6 | 11 | How the home loan process works | Steps from first conversation to closing (mirrors the website's How It Works page). |
| 7 | 15 | Questions worth asking any lender | Checklist the reader can use. |
| 8 | 19 | Thinking about down payment? | General points on down payment and assistance programs (no amounts promised). |
| 9 | 24 | Credit: what to know before you apply | General guidance; no score thresholds promised. |
| 10 | 29 | Still planning your move? | Check-in; reply or book. |
| 11 | 35 | Refinancing: when it's worth a conversation | General reasons people review a refinance; no rate claims. |
| 12 | 42 | Timing your home search | Planning timeline in general terms. |
| 13 | 49 | Mortgage terms, decoded | Short glossary (links to the Resources page). |
| 14 | 56 | What happens after you apply | Preview of application, documents, review and closing. |
| 15 | 64 | Your plans may have changed, and that's fine | Ask whether to keep in touch. |
| 16 | 72 | A few FAQs | Pulls 3 questions from the FAQ page. |
| 17 | 81 | Ready when you are | Soft check-in; booking link. |
| 18 | 89 | Should we close your file? | Last message; reply to stay in touch; otherwise no more emails in this series. |

Full body text for each email is to be written once the sender identity and footer are approved, so the copy
matches the brand that's actually sending.

## C. Started (New): "1 SMS" (PROPOSED)

| # | Day | Text |
|---|---|---|
| 1 | 0 (on entering Started (New)) | Hi {{contact.first_name}}, this is {{user.first_name}} with [SENDER BRAND]. We received your application. I'll be in touch about next steps. Reply here with any questions. Reply STOP to opt out. |

## D. Started (NC): "5 SMS over 5 Days" (PROPOSED. **NC meaning unconfirmed**)

The copy below stays neutral because "NC" isn't defined. Revise it once David defines it.

| # | Day of Started (NC) | Text |
|---|---|---|
| 1 | 0 | Hi {{contact.first_name}}, {{user.first_name}} here with [SENDER BRAND] about your home loan application. When's a good time for a quick call to go over next steps? |
| 2 | 1 | {{contact.first_name}}, I'd like to connect about your application. You can also pick a time here: {{ custom_values.cbhl_consultation_booking_link }} |
| 3 | 2 | Hi {{contact.first_name}}, just following up on your application. A short call will help keep things moving. |
| 4 | 3 | {{contact.first_name}}, is there a better number or time to reach you about your application? |
| 5 | 4 | Hi {{contact.first_name}}, last text for now about your application. Reply here or call when it's convenient. [SENDER BRAND]. Reply STOP to opt out. |

## E. Started (New) through Preapproval: "8 Emails over 11 Days" (PROPOSED)

One series from the first Started (New) entry; it continues through Started (NC), Started and Preapproval
and ends at Locked, Closed, any dead status or DNC.

| # | Day | Subject | Body (summary) |
|---|---|---|---|
| 1 | 0 | We received your application | Confirms receipt; who the loan officer is; what happens next. |
| 2 | 1 | What to expect next | Review, document requests, timing in general terms. |
| 3 | 2 | Gathering documents | Typical document list; use only the secure method your loan officer gives you. |
| 4 | 4 | Questions so far? | Invite questions; reply or book a call. |
| 5 | 6 | Understanding your loan estimate | General explanation of what a Loan Estimate is (no figures). |
| 6 | 8 | Staying on track | Avoid big credit changes during the process (general guidance). |
| 7 | 10 | Checking in on your application | Status check; contact loan officer. |
| 8 | 11 | Here to help | Final email in the series; how to reach the team. |

`[APPLICATION LINK]` isn't used in any of these. Any "finish your application" message stays off until
the link is confirmed (CBHL-10).

---

## F. PROPOSED SMS consent wording for the inquiry form

Optional, **unchecked** checkbox, separate from submitting the form (SMS consent isn't a condition of
contact):

> ☐ I agree to receive text messages from **[SENDER BRAND — must match the registered A2P brand]**
> about my home loan inquiry, including follow-up and appointment reminders, at the phone number I
> provided. Message frequency varies (for a new inquiry, up to 8 messages over 30 days). Message and data
> rates may apply. Reply STOP to opt out or HELP for help. Consent isn't a condition of any purchase or
> loan. See our Privacy Policy and Terms of Use.

Needs: David's/compliance approval, the sender brand that matches the A2P registration, and the final
Privacy Policy/Terms URLs (currently drafts on the site). Until approved, the form ships **without** the
checkbox and form leads receive **no SMS** (CBHL-03 SMS steps check for consent; see 02-workflows.md).
