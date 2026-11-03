# Legacy workflows, old pipelines and the 110 existing opportunities

The workflow definitions couldn't be read through the API (403, see 02-workflows.md). The dispositions
below are based on names, status and what the account contains. Each one must be **opened in the
builder and confirmed** before it's changed. Before deleting anything, use **⋯ → Clone** or export it
first so it can be recovered.

## Existing workflows (23)

| Workflow | Status | Proposed | Why / what to check |
|---|---|---|---|
| Email & Phone Validation + Contact Deletion | **published** | **Review first, likely unpublish** | Deletes contacts. Check its trigger and delete conditions. Contacts, conversations and appointments must be preserved, so automatic deletion should stop unless David confirms it. (An API-created QA contact was not deleted within 3 minutes.) |
| Email & Phone Validation + DND Tag | published | Keep for now | Probably sets `dnd email`/`dnd sms` tags (seen on existing contacts). Confirm it doesn't message anyone. |
| Mortgage Ad AI Text Drip Campaign + Notifications \| Facebook Lead Forms (v19) | published | Keep until cutover, then unpublish | Live Facebook lead intake and SMS. CBHL-02/03 replace it. Never run both. |
| Mortgage Ad Email Drip Campaign \| Facebook Lead Form (v11) | published | Keep until cutover, then unpublish | Replaced by CBHL-03 email series. |
| Remove From Email & Text Drip When Pipeline Stage Changes | published | Keep until cutover, then unpublish | Stop logic for the two drips above. CBHL-07 replaces it. |
| Bad Number Automation | published | Unpublish at cutover | Tied to old "Bad Number" stage. CBHL-07 (Disc/Wrong Number) replaces it. |
| Unresponsive - SMS x2 | published | Unpublish at cutover | Tied to old "Unresponsive" stage (0 opportunities). Not in David's table. |
| Nurture Stage - 3-Month Real Estate Newsletter | published | Unpublish | Real-estate newsletter content tied to old "Nurture" stage (0 opportunities). Not in David's table. |
| Form 1 Opt-in SMS | published | Review | Which site uses "Form 1"? If nothing does, unpublish. |
| Appointment Confirmation + Reminder | draft | Replace (CBHL-09) | Never published. |
| Attempted Contact | draft | Review | Created by staff on Sep 3, so ask its author before removing. |
| 0.0 SMS Text Drip Campaign + Notifications \| Facebook Lead Form | draft | Retire | Superseded template. |
| 0.0 Updated SMS Text Drip Campaign + Notifications \| Facebook Lead Form | draft | Retire | Superseded template. |
| 0.1 Lead Responded But Have Not Booked - Conversation AI | draft | Retire | Template. |
| 0.2 Email Drip Campaign \| Facebook Lead Form | draft | Retire | Template. |
| 01. AI Text Drip Campaign + Notifications \| Facebook Lead Forms + VOICE AI | draft | Retire | Template. |
| AI Automation | draft | Review | Unknown content. |
| Add Imported Leads To Pipeline | draft | Retire | Imported Leads pipeline is empty. |
| FB Lead Form \| SMS Drip Campaign \| Notifications | draft | Retire | Template. |
| 21 Day Cash Offer AI Text and Email Drip Campaign + Notifications \| Z buyer | draft | Delete | Real-estate investor template, not mortgage. |
| Motivated Seller Cash Offer AI Text and Email Drip Campaign + Notifications \| Facebook Lead Forms | draft | Delete | Same. |
| Buyer - Homes List YT Ad Automation | draft | Delete | Real-estate agent template. |
| YT Seller Ad Automation | draft | Delete | Real-estate agent template. |

"Retire" = move to a folder `zz Retired (2026-11)` and leave in draft. "Delete" only after cloning/export.

## Other legacy configuration

| Item | Proposed |
|---|---|
| Pipeline **Imported Leads** (`qkO9qAqk3oIWHZWHfsx2`, 0 opportunities) | Delete after confirming no published workflow references it. |
| Pipeline **Inbound Leads** (`IEOoQLn1URNe0y1DHj4o`, 110 open) | Keep. Retire only after the migration below, then rename `zz Archived - Inbound Leads`. Never delete while populated. |
| Calendars **Intro Call** and **Intro Call with David** | Both currently unbookable (no hours / no team) and have no appointments. Deactivate after confirming no workflow sends their links. |
| Real-estate-agent custom fields (Monthly Budget, Brokerage, Specialties, Service Areas, Provide 4 Cities…, About Me) and duplicate forms (A2P EIN ×2, A2P Sole Prop ×2, Lead Magnet, Opt-in Form \| Buyer Guide / Homes list / Individual Listing / Seller Guide, Onboarding Form \| REMA) | Template leftovers. Delete forms in the UI after checking submissions; delete fields only if empty. |

## Migrating the 110 open opportunities

Counts by current stage (2026-11-03): Attempted Contact 86, Not Interested 12, Bad Number 5,
Connected 2, Unreachable on CRM 2 (one is "Melody Test Only"), Missed Appointment 1, DNC 1,
Active Client 1. All other stages: 0.

| Old stage | Count | New stage | Status |
|---|---|---|---|
| Attempted Contact ☎️ | 86 | New | clear (not yet contacted = New Lead) |
| Connected | 2 | Connected | clear |
| DNC | 1 | DNC | clear |
| Bad Number 📵 | 5 | Disc/Wrong Number | clear |
| Not Interested 😑 | 12 | **decision** | no matching status in David's table (Withdrawn? Expired? leave in old pipeline?) |
| Unreachable on CRM | 2 | **decision** | one is a test record ("Melody Test Only"); delete that one? |
| Missed Appointment ⏰ | 1 | **decision** | Connected? |
| Active Client 🤝 | 1 | **decision** | Started / Preapproval / Locked? |

**How it will run (by API, once decided):**
1. Unpublish the legacy stage-driven workflows first (Bad Number, Unresponsive, Nurture, Remove From Drip),
   so moving records doesn't fire old automations.
2. For each opportunity: move to the CBHL Lead to Loan stage, keep owner, set CBHL Lead Received Date =
   original created date. **Don't** add `cbhl lead-to-loan`, so no new outreach starts. CBHL-04
   (expiry) and CBHL-07 (bookkeeping/stop rules) may act on them, and neither sends anything.
3. Read back counts per stage, then archive the old pipeline.

Moving an opportunity between pipelines keeps its contact, conversations, notes, tasks and appointments.
