# Build spec: CBHL lead-to-loan workflows

**Why this is a UI build:** every workflow endpoint (`search`, `get definition`, `create`, `update`,
`validate`, `publish`, `step types`, `logs`) returns
`403 WORKFLOW_API_NOT_ENABLED_FOR_LOCATION`. HighLevel enables this API per sub-account, and this one isn't
enabled. Only the plain workflow list works. If HighLevel support enables it (ask for "Workflow API / workflow
builder API for sub-account giyhFtPh7MreGKeeSdCx"), these specs can be built through the connector instead.

Put all of these in one folder: **Automation → Workflows → + New folder `CBHL Lead to Loan`**.

## Shared rules (apply to every CBHL workflow)

| Rule | How |
|---|---|
| Only new-system contacts get automated outreach | Every messaging step sits after an If/Else: contact **has tag** `cbhl lead-to-loan` AND **does not have tag** `cbhl stop follow-up`. Legacy contacts never get `cbhl lead-to-loan`, so the existing database isn't enrolled. |
| DND is always respected | Leave GHL's DND handling on. CBHL-07 also removes the contact from every CBHL messaging workflow when DND turns on. |
| Pipeline | Every opportunity trigger/filter uses pipeline **CBHL Lead to Loan** (`hB1QaPi0Qh7swNDAAKzq`). |
| Re-entry | "Allow re-entry" **off**, except CBHL-05, CBHL-07 and CBHL-09, which must run on every stage/appointment change. |
| Multiple opportunities | Turn on "Allow multiple opportunities" in workflow settings **only after** the location setting "Allow duplicate opportunities" is on (see decisions). Until then GHL keeps one opportunity per contact in the pipeline. |

Status key: **READY**: fully defined, sends nothing to leads, can be published after the test.
**DRAFT**: build it, leave it in draft. **BLOCKED**: needs the input named.

---

## CBHL-01 Website Inquiry Intake (READY once the form exists)

- **Trigger:** Form Submitted → form = `CBHL General Inquiry`.
- **Actions:**
  1. Add tags `website inquiry`, `cbhl lead-to-loan`.
  2. **If/Else**: does the contact already have an **open** opportunity in CBHL Lead to Loan?
     - **Yes:** Add note "Repeat website inquiry: {{contact.inquiry_message}}". Create task for the
       opportunity owner "Repeat website inquiry from {{contact.name}}". Go to step 6.
     - **No:** continue.
  3. **Assign to user** (round robin, **only apply to unassigned contacts**): Mark Rotundo, Teresa Turner
     (default; same team as the consultation calendar. David to confirm, see decisions).
  4. **Create/Update Opportunity:** pipeline CBHL Lead to Loan, stage **New**, name `{{contact.name}} - {{contact.what_can_we_help_with}}`,
     status open, source `Website Inquiry`, owner = contact owner, fields: CBHL Loan Purpose =
     `{{contact.what_can_we_help_with}}`, CBHL Lead Received Date = today.
  5. **Create task** (assigned to contact owner): "Call new website inquiry: {{contact.name}}". Due: **decision needed**
     (suggested default: same business day).
  6. **Internal notification** to the assigned user (in-app + email to user): "New website inquiry:
     {{contact.name}}, {{contact.what_can_we_help_with}}, {{contact.phone}}".
  7. **Add to workflow:** CBHL-03 (only when CBHL-03 is published).

## CBHL-02 Facebook Lead Ad Intake (READY to build; publish only at cutover)

Same as CBHL-01 with trigger **Facebook Lead Form Submitted** (all forms on the connected page),
tags `facebook`, `mortgage ad`, `cbhl lead-to-loan`, and opportunity source `Facebook Lead Ad`.
**Don't publish** while the legacy published workflow "Mortgage Ad AI Text Drip Campaign + Notifications"
is still live; both would process the same lead. Cutover = unpublish legacy, publish CBHL-02, same minute.

## CBHL-03 New / Connected follow-up (DRAFT)

From David's table, New + Connected (merged): **8 SMS over 30 Days**, **18 Email over 90 Days**,
**Dialer campaign 'Market'**.
- **Trigger:** added by CBHL-01/02 (no own trigger), or Opportunity stage = New.
- **Goal / exit:** opportunity stage changes to anything other than New or Connected → end workflow.
- **Steps:** 8 SMS and 18 emails spread over the stated windows, with an If/Else guard (shared rules)
  before each message, plus a "Dialer campaign 'Market'" handoff step.
- **Blocked on:** message wording; which day each message goes out (the table gives only totals and
  windows); a verified email sending service; which dialer runs 'Market' and how GHL hands contacts to it;
  approved SMS consent wording for website leads; whether a reply stops the drip.

## CBHL-04 90-day expiry (READY)

Table: New + Connected → "Expires 90 days after received".
- **Trigger:** Opportunity Created OR Stage Changed → pipeline CBHL Lead to Loan, stage **New** or **Connected**.
- **Action:** Wait until **CBHL Lead Received Date + 90 days** (event/date-based wait; if the field is
  empty, wait 90 days from enrollment).
- **If/Else:** stage is still New or Connected → move to **Expired**, status **lost**, add note
  "Expired 90 days after received". Otherwise end.
- Sends nothing. **Interpretation used:** the table's "Expires" row and its separate "Expired" column are
  read as the same status. Confirm with David.

## CBHL-05 Started (New) → Started (NC) after 1 day + application date (READY except the SMS step)

Table: Started (New): "1 SMS", "Changes to Started (NC) after 1 day".
- **Trigger:** Pipeline Stage Changed → CBHL Lead to Loan → **Started (New)**. Re-entry on.
- **Actions:**
  1. Update opportunity field CBHL Application Received Date = today (if empty).
  2. *(DRAFT step)* Send SMS #1 of 1, behind the shared guard. Wording needed.
  3. Wait **1 day**.
  4. If stage is still Started (New) → move to **Started (NC)**.
- Publish with step 2 removed (or disabled) until the wording exists.

## CBHL-06 Application follow-up (DRAFT)

Table: Started (New) + Started (NC) + Started + Preapproval (merged): **8 Emails over 11 Days**.
Started (NC): **5 SMS over 5 Days**, **Dailer campaign 'App Received'**. Started: **Dailer campaign
'Started (Personal)'**. Preapproval: **Dailer campaign 'Preapproval (Personal)'**.
- **Trigger:** stage changed to Started (New) (email series); stage changed to Started (NC) (SMS series).
- **Exit:** stage moves to Locked, Closed, any dead status or DNC (CBHL-07 also removes).
- **Blocked on:** wording, per-message timing, email service, dialer identity and handoff.

## CBHL-07 Status bookkeeping and stop rules (READY)

- **Trigger:** Pipeline Stage Changed → CBHL Lead to Loan → any stage. Re-entry on.
- **Branches by new stage:**

| New stage | Actions |
|---|---|
| Preapproval | set CBHL Preapproval Issued Date = today (if empty) |
| Locked | set CBHL Lock Date; remove from CBHL-03, CBHL-05, CBHL-06 (table: No SMS / No Email) |
| Closed | set CBHL Closed Date; status **won**; remove from CBHL-03/05/06 |
| CTUD, WTD, Incomplete, Declined, Withdrawn, Wrong Language, Expired | status **lost**; remove from CBHL-03/05/06; task to owner "Add outcome note" |
| Disc/Wrong Number | as above + add tag `bad number` + DND **SMS and Call** (number is wrong; email untouched) |
| DNC | status **lost**; remove from all CBHL workflows; tag `cbhl stop follow-up`; **DND all channels** |

- A second trigger in the same workflow, **Contact DND changed → enabled**, removes the contact from all
  CBHL messaging workflows, adds `cbhl stop follow-up`, and tasks the owner "Contact opted out: review".
  It **doesn't** change the loan stage, because an SMS opt-out isn't the same as DNC.

## CBHL-08 Reply handling (READY: internal steps only)

- **Trigger:** Customer Replied (SMS, Email). Filter: has tag `cbhl lead-to-loan`.
- **Actions:** add tag `cbhl replied`; internal notification to owner "{{contact.name}} replied";
  create task "Reply from {{contact.name}}: respond". Whether a reply also stops CBHL-03's SMS series is a
  **decision** (suggested: yes, stop SMS on reply, keep email).
- GHL handles STOP/UNSUBSCRIBE keywords natively by setting DND, and CBHL-07's DND trigger handles the rest.

## CBHL-09 Consultation lifecycle (READY: internal; lead-facing messages DRAFT)

Calendar **Home Loan Consultation** (`BSwRRQDlZgYCbEJAPwdE`).
- **Trigger A:** Customer Booked Appointment (this calendar) → tags `cbhl lead-to-loan`, `appointment booked`;
  Create/Update Opportunity in **New** if none is open (source `Consultation Booking`, Lead Received Date = today);
  opportunity owner = appointment's assigned user; task "Prepare for consultation with {{contact.name}}";
  internal notification.
- **Trigger B:** Appointment Status = **rescheduled** → notify owner; update task due date.
- **Trigger C:** Appointment Status = **cancelled** → remove tag `appointment booked`; task "Follow up on
  cancelled consultation".
- **Trigger D:** Appointment Status = **no-show** (staff marks it) → task "Follow up on missed consultation".
- **Trigger E:** Appointment Status = **showed** → task "Send application / log outcome". Moving the stage
  stays a staff action.
- **DRAFT steps:** confirmation and reminder messages to the lead (wording, timing, email service).
  Until then GHL's native in-app notifications to the assigned user (already on the calendar) cover staff.

## CBHL-10 Application handoff (BLOCKED)

Send the application link and record the handoff. **Blocked on:** the application destination. The old
site used both Scout and Floify. Once confirmed, create custom value `CBHL Application URL` and add
"Send application link" to CBHL-09 Trigger E. Nothing is invented meanwhile.

## CBHL-11 External system status sync (BLOCKED)

Map the external system's statuses (identical labels to the pipeline stages) into GHL automatically,
e.g. Inbound Webhook trigger → find opportunity by **CBHL External Loan ID** → move stage.
**Blocked on:** which system this is, and whether it can send webhooks/API calls or only export.
Until then, staff move stages by hand and CBHL-04/05/07 do the automatic parts.

---

## Test plan per workflow (once built in the UI)

Use a test contact you control (your own email and phone) tagged `qa test contact` and
`cbhl lead-to-loan`. For checks that must not send anything, use the existing QA contact
`QA Test CBHL 001` (id `TvsVfgogDFS4Ynz4D6eD`, DND on, undeliverable email).

| Workflow | Test | Pass when the execution log shows |
|---|---|---|
| CBHL-01 | submit form via direct link | tags, opportunity in New with Loan Purpose + Received Date, owner set, task, notification |
| CBHL-04 | set Lead Received Date to 91 days ago on a QA opportunity in New, enroll | moved to Expired / lost |
| CBHL-05 | move QA opportunity to Started (New); temporarily set wait to 2 min | date set, moved to Started (NC) |
| CBHL-07 | move through Preapproval, Locked, Closed, Disc/Wrong Number, DNC | dates set, status won/lost, removed from other CBHL workflows, DND applied |
| CBHL-08 | reply from your test phone | tag `cbhl replied`, task, notification |
| CBHL-09 | book, reschedule, cancel; mark a booking no-show / showed | each branch's task + tags |

Only publish a workflow after its row passes. Validation (it saves without errors) isn't the same as
passing the end-to-end test.
