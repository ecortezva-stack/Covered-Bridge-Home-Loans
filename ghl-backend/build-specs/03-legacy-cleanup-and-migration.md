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

## Contact-deletion workflow ("Email & Phone Validation + Contact Deletion", published)

Behavior is **unknown**: the name alone doesn't establish it, and its definition can't be read through
the API (403). Required before it may process any new Home Loans lead:
1. Open it (Workflow API or browser), then **save its full configuration** to
   `snapshots/legacy-workflows/5c7d9ad3-…json` (API) or as a clone `zz Saved - Email & Phone Validation +
   Contact Deletion (2026-11)` plus screenshots of every step (browser).
2. Record its **triggers** (contact created? tag? form?), **filters**, **validation provider** (GHL
   built-in verification is billed per check), **deletion conditions**, and **dependencies** (tags it sets
   that other workflows read, e.g. `dnd email`/`dnd sms`).
3. **Disable the deletion behavior** (unpublish, or remove the Delete Contact step and republish) before
   CBHL-01 is published. If validation itself is wanted, replace "delete" with: set `CBHL Email Status` /
   `CBHL Phone Status`, add DND on the invalid channel, add tag `bad number` where relevant, and a task.
4. Never delete the workflow itself before step 1 is saved.

## Migration mapping for the 110 open opportunities (prepared, NOT run)

Counts (2026-11-03): Attempted Contact 86, Not Interested 12, Bad Number 5, Connected 2, Unreachable on
CRM 2, Missed Appointment 1, DNC 1, Active Client 1.

**On every migrated record**, whatever its target stage (fields exist, ids in the snapshot):
- `CBHL Legacy Pipeline` = "Inbound Leads"; `CBHL Legacy Stage` = exact old label incl. emoji;
  `CBHL Legacy Status` = old status (all currently `open`); `CBHL Legacy Owner` = owner name + user id.
  The owner itself (`assignedTo`) is kept unchanged.
- `CBHL Lead Received Date` = original opportunity created date (not the migration date).
- `CBHL Legacy Outreach Occurred` = Yes (legacy SMS/email drips and dialing ran on these leads).
- Contact tag `cbhl legacy migrated`. **Never** `cbhl lead-to-loan`, so no initial outreach restarts.

| Old stage | n | Target stage | `CBHL Lead Disposition` | Notes |
|---|---|---|---|---|
| Attempted Contact ☎️ | 86 | New (reconsidered: kept, but marked) | Attempted Contact | Attempts already happened: Legacy Outreach Occurred = Yes, excluded from CBHL-03. "Connected" would overstate it. |
| Connected | 2 | Connected | (blank) | direct match |
| Bad Number 📵 | 5 | Disc/Wrong Number | (blank) | + `CBHL Phone Status` = Wrong Number **only if** staff confirm. Otherwise "Unknown"; the stage records the legacy call result. |
| DNC | 1 | DNC | (blank) | + DND all channels (check current DND first; don't remove any existing DND) |
| Not Interested 😑 | 12 | **New** (status unchanged: open) | **Not Interested** | Preserved as a disposition, **not** turned into Withdrawn/Declined/DNC. Stage New only because David's table has no lead-level "not interested" status; the disposition plus the legacy fields carry the truth. Excluded from outreach (legacy tag). *Alternative for David: keep these 12 in the old pipeline until he defines a status.* |
| Unreachable on CRM | 1 | **New** | Unreachable on CRM | Meaning unconfirmed. `CBHL Phone Status` stays "Unknown" (not "Wrong Number"). |
| Unreachable on CRM ("Melody Test Only", opp `XNb3sQWjb9r1E2xpiqk3`) | 1 | **New** | Test Record | + contact tag `cbhl test record`; excluded from all outreach and from reporting filters. Not deleted. |
| Missed Appointment ⏰ | 1 | **New** | Missed Appointment | Appointment history stays on the contact. No application progress inferred. |
| Active Client 🤝 | 1 | **New** | Active Client | Current classification kept until the real milestone (Started/Preapproval/Locked/Closed) is confirmed. Then staff move the stage. |

Why "New" for the unmapped dispositions: GHL needs a stage. New is the only status in David's table
that claims nothing about application progress, and the disposition field stops it being read as a
fresh lead. If David prefers, those 16 records can stay in the old pipeline instead (no data lost either way).

**Execution plan (run only after: legacy workflows inspected/saved, stage-driven legacy workflows
unpublished, CBHL-07 published, David approves this mapping):**
1. Dry run: export id, stage, owner, status and created date of all 110 to `snapshots/` (no PII in the repo copy).
2. Contact-level: add `cbhl legacy migrated` (and `cbhl test record` for Melody) **before** moving any
   opportunity, so any CBHL trigger sees the exclusion.
3. Per opportunity: write the legacy fields, then move to the target stage in CBHL Lead to Loan with
   owner and status unchanged.
4. Read back counts per stage and disposition, and diff against the dry run.
5. Watch for 48 h; then rename the old pipeline `zz Archived - Inbound Leads`. Never delete it while populated.
