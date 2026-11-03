# Build spec: CBHL lead-to-loan workflows (rev. 2, 2026-11-03)

**Builder:** Claude (the backend owner), not the website owner. Route: Workflow API once HighLevel
enables it, otherwise an authorized browser session (see 04-access-unblock.md). Every workflow endpoint
currently returns `403 WORKFLOW_API_NOT_ENABLED_FOR_LOCATION`.

Folder: **Automation → Workflows → `CBHL Lead to Loan`**.

Status key: **BUILD+PUBLISH after test**: fully defined, sends nothing to leads. **BUILD, KEEP OFF**:
waiting on a named decision or dependency. **BLOCKED**: can't be built until a dependency exists.

## Shared rules

| Rule | Implementation |
|---|---|
| Outreach eligibility | Before **every** lead-facing message: contact has `cbhl lead-to-loan` AND lacks `cbhl stop follow-up`, `cbhl legacy migrated`, `cbhl test record`. SMS steps also require `CBHL SMS Consent` = Yes. DND is respected natively. |
| Legacy database | Migrated/legacy contacts never get `cbhl lead-to-loan`, and get `cbhl legacy migrated`, so no initial outreach restarts. |
| Pipeline | All opportunity triggers/filters: **CBHL Lead to Loan** `hB1QaPi0Qh7swNDAAKzq`. |
| No contact deletion | No CBHL workflow deletes contacts. Invalid details are recorded in `CBHL Phone Status` / `CBHL Email Status`, the `bad number` tag, DND, and the Disc/Wrong Number stage. |
| Sales vs. service messages | **Sales sequences** (CBHL-03 SMS/email) stop on a genuine reply. **Service messages** (appointment confirmations/reminders in CBHL-09, application communications in CBHL-06/CBHL-10) **don't** stop on a reply. They stop only on DND/opt-out, `cbhl stop follow-up`, or the stage rules. |

## Duplicate prevention

Requires the location setting **Allow duplicate opportunities = ON** (approved, not yet applied: no API
route, see 04-access-unblock.md).

| Case | Rule | How it's enforced |
|---|---|---|
| Repeat website inquiry / double-submit | Never a second **lead** opportunity while one is open | Tag `cbhl active lead` = the contact has an open New/Connected opportunity. CBHL-01 checks it first: present → note + task only; absent → add the tag **as the first action**, then create the opportunity. CBHL-07 removes the tag when that opportunity leaves New/Connected. |
| Lead that later applies | Same opportunity moves forward (New → Started (New)) | Staff or the sync move the stage. Nothing new is created. |
| New, separate application (e.g. second property) | New opportunity with its own External Loan ID | Created by staff or the sync (CBHL-11). |
| Integration retry / repeated status event | Same External Loan ID → update, never create | Integration lookup **verified by API on 2026-11-03**: list the contact's opportunities in the pipeline (`GET /opportunities/search?contactId=…&pipelineId=…&status=all`), match `CBHL External Loan ID` in the returned `customFields`, then update by id; create only if no match. (Full-text search does **not** index custom fields, also verified, so it must not be used for matching.) |
| Same person, new email/phone | Contact dedupe by email then phone (location setting, verified) | Native. |

Known limit: two submissions within the same second can both pass the tag check before either adds it.
Test this (double-click submit). If GHL lets both through, add a 1-minute "wait + re-check" before
creation.

**Re-test after the setting is on:** (1) a second application with a different External Loan ID is
created alongside the first; (2) repeating the same External Loan ID updates rather than creates;
(3) a repeat website inquiry adds a note/task, not an opportunity.

---

## CBHL-01 Website Inquiry Intake (BUILD+PUBLISH after test; assignment rule PROPOSED)

- **Trigger:** Form Submitted → `CBHL General Inquiry`.
- **Actions:**
  1. Add tags `website inquiry`, `cbhl lead-to-loan`.
  2. If `CBHL SMS Consent` = Yes → set `CBHL SMS Consent Date` = today.
  3. **If** tag `cbhl active lead` present → note "Repeat inquiry: {{contact.inquiry_message}}" + task to
     owner "Repeat inquiry from {{contact.name}}" (due per SLA below) → **end**.
  4. Add tag `cbhl active lead`.
  5. **Assign to user. PROPOSED, pending David:** round robin Mark Rotundo / Teresa Turner, only
     unassigned contacts. (They're the verified consultation-calendar team. Their assignment to all
     inquiries isn't confirmed.)
  6. **Create opportunity** (duplicates allowed): stage **New**, source `Website Inquiry`, owner = contact
     owner, Loan Purpose = `{{contact.what_can_we_help_with}}`, Lead Received Date = today.
  7. **First-call task. PROPOSED SLA, pending David:** "Call new inquiry: {{contact.name}}" due
     **within one business hour**, business hours = Mon–Fri 08:00–17:00 America/New_York (verified on
     every team calendar):
     - submitted Mon–Fri 08:00–15:59 → due submission + 1 hour;
     - submitted 16:00–16:59 → due next business day 08:00 + the remaining minutes;
     - outside hours/weekends → due next business day 09:00.
     Builder approach: If/Else on day/time → three "Create task" variants; the last uses "Wait until
     time window Mon–Fri 08:00" then due in 1 hour.
  8. Internal notification to owner (in-app + email to the user).
  9. Add to CBHL-03 (only once CBHL-03 is approved and published).

## CBHL-02 Facebook Lead Ad Intake (BUILD, KEEP OFF until cutover)

CBHL-01 with trigger Facebook Lead Form Submitted, source `Facebook Lead Ad`, tags `facebook`,
`mortgage ad`. Cutover: unpublish the legacy "Mortgage Ad AI Text Drip…" and "Mortgage Ad Email Drip…"
and publish CBHL-02 in the same minute, after both legacy workflows have been inspected and saved.

## CBHL-03 New/Connected sales follow-up (BUILD, KEEP OFF)

8 SMS / 30 days, 18 emails / 90 days, "Dialer campaign 'Market'". Proposed copy and spacing:
05-proposed-sequences.md (A, B).
- **Exit:** stage leaves New/Connected; **genuine reply** (see CBHL-08); DND; stop tag.
- **Off until:** copy and spacing approved; email provider + sender confirmed; SMS consent wording
  approved and A2P sender identity confirmed; dialer provider and handoff method known (the 'Market'
  step stays out until then).

## CBHL-04 90-day expiry → Expired (BUILD, KEEP OFF: David must confirm)

**Proposed mapping:** table row "Expires 90 days after received" → stage **Expired**, status lost.
Built but **inactive** until David confirms (a) that it means the Expired status, (b) the start date
("received" = CBHL Lead Received Date, proposed; for migrated records the original created date), and
(c) exclusions (proposed: has an upcoming appointment, tag `cbhl replied` in the last 14 days, or owner
has an open task).
- **Trigger:** opportunity enters New or Connected → wait until Lead Received Date + 90 days → If still
  New/Connected and no exclusion → Expired / lost + note. Sends nothing.

## CBHL-05 Started (New) → Started (NC) after 1 day (BUILD+PUBLISH after test; SMS step OFF)

- **Trigger:** stage changed to Started (New). Re-entry on.
- Set Application Received Date (if empty) → *(SMS C1, OFF)* → wait 1 day → if still Started (New)
  → move to **Started (NC)**. Uses David's label as-is ("NC" not expanded).

## CBHL-06 Application communications (BUILD, KEEP OFF)

8 emails / 11 days (Started (New) → Preapproval), 5 SMS / 5 days (Started (NC)), dialer campaigns
'App Received', 'Started (Personal)', 'Preapproval (Personal)'. Proposed copy: 05 (C–E).
These are **service** messages: a reply doesn't stop them (decision confirmed as default; reconfirm
with David). Exit: Locked, Closed, dead statuses, DNC, DND, stop tag.

## CBHL-07 Status bookkeeping and stop rules (BUILD+PUBLISH after test)

**Trigger 1:** stage changed (any) in CBHL Lead to Loan. Re-entry on.

| New stage | Actions |
|---|---|
| leaves New/Connected | remove tag `cbhl active lead`; remove from CBHL-03 |
| Preapproval | Preapproval Issued Date (if empty) |
| Locked | Lock Date; remove from CBHL-03/05/06 |
| Closed | Closed Date; status won; remove from CBHL-03/05/06 |
| CTUD, WTD, Incomplete, Declined, Withdrawn, Wrong Language, Expired | status lost; remove from CBHL-03/05/06; task "Add outcome note" |
| Disc/Wrong Number | as above + `CBHL Phone Status` = Wrong Number or Disconnected (staff picks) + tag `bad number` + DND SMS/Call (email untouched) |
| DNC | status lost; remove from all CBHL workflows; tag `cbhl stop follow-up`; DND all channels |

**Trigger 2:** Contact DND changed (enabled) → remove from CBHL-03/06 sales/service sequences as the
channel requires; tag `cbhl stop follow-up` if all channels; task "Opt-out received: review". Loan stage
unchanged.

## CBHL-08 Reply handling (BUILD+PUBLISH after test, together with CBHL-03)

- **Trigger:** Customer Replied (SMS, Email), contact has `cbhl lead-to-loan`.
- **Genuine human reply** = not an auto-reply/out-of-office, and not a STOP/opt-out keyword (opt-outs are
  handled by DND → CBHL-07 Trigger 2). Filter: message body doesn't contain common auto-reply markers
  ("automatic reply", "out of office", "auto-reply"). Email replies flagged as auto-submitted are skipped.
- **Actions:** add `cbhl replied`; **remove from CBHL-03 only** (sales sequence); task to owner
  "Reply from {{contact.name}}: respond" (due per the CBHL-01 SLA); internal notification.
- **Not affected:** CBHL-09 appointment notifications and CBHL-06/10 application communications.

**Distinction test (required before publishing):** QA contact enrolled in CBHL-03 **and** with an
upcoming consultation (CBHL-09 reminders scheduled). Reply "Thanks, talk soon" → CBHL-03 shows "removed",
the CBHL-09 reminder still sends. Then reply "STOP" → DND on, CBHL-07 Trigger 2 fires, and no further
sales or service SMS sends.

## CBHL-09 Consultation lifecycle (internal steps BUILD+PUBLISH after test; lead messages OFF)

Calendar Home Loan Consultation `BSwRRQDlZgYCbEJAPwdE`.
- Booked → tags `cbhl lead-to-loan`, `appointment booked`; if no `cbhl active lead`, add it and create a
  New opportunity (source `Consultation Booking`); owner = appointment user; task "Prepare for
  consultation"; notification.
- Rescheduled → notify owner; move task due date.
- Cancelled → remove `appointment booked`; task "Follow up on cancelled consultation".
- No-show (staff sets) → task "Follow up on missed consultation"; opportunity disposition **unchanged**.
- Showed → task "Log outcome / next step". The stage stays a staff decision.
- **Lead-facing confirmation/reminder messages:** service messages, OFF until copy, email sender and SMS
  consent are approved.

## CBHL-10 Application handoff (tracking built; link messages OFF)

The surrounding tracking already exists: Application Received Date, stage Started (New), External Loan ID.
"Send application link" stays off until the destination is confirmed. Scout vs Floify is **not** chosen
here. When confirmed: create custom value `CBHL Application URL`, then enable.

## CBHL-11 External status sync (BLOCKED: requirements)

Not working, and not claimed to work. Requirements:

| Requirement | Needed from |
|---|---|
| Source system name and admin access (which product holds these statuses) | David |
| Integration method: outbound webhooks on status change, API polling, or file export | system admin/vendor |
| Stable application ID per loan → stored in `CBHL External Loan ID` | system |
| Contact match keys sent with each event (email and/or phone) | system |
| Event mapping: external status label → GHL stage (1:1 with the 17 labels; the labels already match) | confirm labels are identical in the source |
| Milestone dates (application received, preapproval, lock, closing) in the payload | system |
| Retry behavior / event IDs, so retries are idempotent (lookup method above) | system |
| GHL side: Inbound Webhook trigger (premium action) or a small API relay | after Workflow API/UI access |

---

## Test plan (each must pass in the execution log before publishing)

Test contacts: a contact you control, tagged `qa test contact` + `cbhl lead-to-loan`, with consent;
plus `QA Test CBHL 001` (`TvsVfgogDFS4Ynz4D6eD`, DND on, undeliverable) for no-send checks.

| Workflow | Test | Pass condition |
|---|---|---|
| CBHL-01 | direct-link submission, in and out of business hours | tags, `cbhl active lead`, opportunity in New with fields, owner, task due per SLA, notification |
| CBHL-01 | same email again; double-click submit | note/task only; exactly one opportunity |
| Duplicate setting | second application with a new External Loan ID; retry with the same ID | two opportunities; retry updates |
| CBHL-04 (when approved) | Received Date set 91 days back | moved to Expired/lost; exclusions respected |
| CBHL-05 | wait shortened to 2 min for the test | Started (New) → Started (NC) |
| CBHL-07 | every stage branch | dates, status, tag removal, DND, removals |
| CBHL-08 | genuine reply vs auto-reply vs STOP | only the genuine reply stops CBHL-03; STOP sets DND; service messages continue after a genuine reply |
| CBHL-09 | book, reschedule, cancel, no-show, showed | each branch acts; no stage inference |
| **Stop rules end-to-end** | DND/stop-tag contact enrolled in every CBHL sequence | **no message sends** (still outstanding: stored values ≠ proven stopping) |
| **Legacy interference** | after legacy inspection, run intake with legacy workflows in their final state over ≥ 48 h | no legacy action on CBHL contacts (still outstanding) |
