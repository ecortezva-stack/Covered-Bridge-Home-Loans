# Covered Bridge Home Loans: GHL backend

Account **Covered Bridge Home Loans**, locationId `giyhFtPh7MreGKeeSdCx` (company `CCaMpBMKYkOGGcV6G3bb`).
Backend only. The website files in this repo weren't changed. The repo is public, so staff emails are
redacted here.

| File | Contents |
|---|---|
| `requirements/david-status-table.md` | David's status table, verbatim |
| `snapshots/2026-11-03_pre-change_inventory.json` | Configuration before any change |
| `snapshots/2026-11-03_changes-and-tests.json` | Every asset created (IDs, trace IDs) and every test with an honest result |
| `build-specs/01-inquiry-form.md` | Inquiry form build |
| `build-specs/02-workflows.md` | CBHL-01…11, duplicate prevention, reply rules, SLA proposal, test plan |
| `build-specs/03-legacy-cleanup-and-migration.md` | Legacy workflows, contact-deletion workflow plan, migration mapping (not run) |
| `build-specs/04-access-unblock.md` | HighLevel support request + exact browser-access steps |
| `build-specs/05-proposed-sequences.md` | PROPOSED SMS/email sequences and SMS consent wording (inactive) |
| `website-embeds.md` | Embed codes and placement for the website |

## Built and verified through the API

| Asset | ID | Verified |
|---|---|---|
| Pipeline **CBHL Lead to Loan**, 17 stages = David's exact labels | `hB1QaPi0Qh7swNDAAKzq` | read-back; status path test |
| 14 opportunity fields: application tracking (External Loan ID, Loan Purpose, 5 milestone dates, Status Notes) + disposition/legacy (Lead Disposition, Legacy Pipeline/Stage/Status/Owner, Legacy Outreach Occurred) | snapshot | full read-back |
| 8 contact fields: inquiry (4), Phone Status, Email Status, SMS Consent, SMS Consent Date | snapshot | read-back |
| 8 tags: `cbhl lead-to-loan`, `website inquiry`, `cbhl stop follow-up`, `cbhl replied`, `cbhl active lead`, `cbhl legacy migrated`, `cbhl test record`, `qa test contact` | snapshot | read-back |
| Calendar **Home Loan Consultation** (active; Mark Rotundo + Teresa Turner; Mon–Fri 8–17 ET) | `BSwRRQDlZgYCbEJAPwdE` | read-back + slots |
| Custom value: booking link | `7oVLXRZSbblZ5SnMN80f` | read-back |
| QA contact (DND, undeliverable) + QA opportunity kept for the duplicate re-test | `TvsVfgogDFS4Ynz4D6eD`, `y4rOSIYMy2YooyXML50C` | n/a |

Test results that count as **verified**: write access, contact dedupe by email, field persistence,
status path including won/lost, calendar availability, application lookup by External Loan ID (via the
contact's opportunity list; full-text search can't do it).
**Not verified (still outstanding):** that follow-up actually stops on DND/stop tag/reply (only storage
was shown), that legacy workflows can't interfere (3 quiet minutes proves nothing about delayed triggers),
the second application per contact (setting off), every workflow, the form, and the widget rendering.

Nothing is published except the consultation calendar. No legacy item, contact or opportunity was changed.

## Remaining decisions for David (one list)

1. **CTUD, WTD, NC.** Definitions of these exact labels (kept unexpanded until then).
2. **90-day expiry.** Confirm it moves the record to **Expired**, that "received" = lead received date
   (original created date for migrated records), and the exclusions (proposed: upcoming appointment,
   recent reply, open staff task). CBHL-04 stays off until confirmed.
3. **Dialer.** Which product runs campaigns 'Market', 'App Received', 'Started (Personal)',
   'Preapproval (Personal)', how contacts are added/removed, and who has admin access. Nothing is assumed.
4. **External status source.** Which system holds these statuses, whether it can send status-change
   webhooks or API access, its application ID, and the contact match keys (requirements: 02 → CBHL-11).
5. **Message copy and spacing.** Approve or edit the PROPOSED sequences in 05 (counts and windows come
   from the table; days and wording are proposals).
6. **Reply rule.** Confirm the default: a genuine reply stops the New/Connected sales sequence and
   creates a task; application-stage messages (8 emails / 5 SMS) and appointment notices continue.
7. **Email sender.** Sending domain/provider and From address for GHL operational email (not assumed to be
   the old Valor sender or the Emailpal outreach inboxes).
8. **SMS identity and consent.** The brand name SMS is sent as (must match the A2P registration, currently
   "Valor Home Loans"), and approval of the PROPOSED consent wording (05 §F).
9. **Email footer / legal identity.** Legal entity and NMLS disclosure wording for emails (old site:
   "Boxcar Mortgage, LLC DBA Valor Home Loans, NMLS #1969375", not confirmed for this brand).
10. **Application link.** Scout, Floify or other (not chosen here).
11. **Assignment + SLA.** Approve the PROPOSED round robin to Mark and Teresa and the first-call task due
    within one business hour (Mon–Fri 8–17 ET).
12. **Migration mapping.** Approve 03's mapping, especially placing Not Interested (12), Unreachable on
    CRM (1), Missed Appointment (1) and Active Client (1) in stage **New** with their disposition
    preserved, or keeping those 15 in the old pipeline until statuses exist for them. Also: the actual
    milestone of the Active Client record.
13. **Contact-deletion workflow.** Once its behavior is documented: confirm whether any validation should
    remain (deletion itself will be disabled either way).

## Minimum access steps to unblock the build

1. **Browser route (required for the form and the duplicate setting, and covers workflows too):** on a
   Mac/Linux computer, Claude desktop app → Settings → Claude Code → Remote Control → add an empty folder
   (e.g. `~/cbhl-ghl-automation`), then tell this session. Approve the folder request, then sign in to GHL
   yourself in the browser window that opens, as an admin of this sub-account (a dedicated "CBHL
   Automation" staff user is recommended). Full steps: 04-access-unblock.md §2.
2. **Workflow API (optional but preferred for workflows):** send the support request in
   04-access-unblock.md §1 from an agency admin login.

## Resume checkpoint (2026-11-03 ~14:10 UTC)

Done: data model (pipeline, 22 fields, 8 tags, booking link value), calendar, API tests, lookup method for
retry-safe dedupe, migration mapping, proposed sequences and consent wording, access/support documents.

Next, as soon as browser access exists:
1. Save + inspect all 9 published legacy workflows (Contact Deletion first) → disable deletion.
2. Turn on Allow duplicate opportunities → re-test second application + same-ID retry (QA opportunity
   `y4rOSIYMy2YooyXML50C`, External Loan ID `QAEXT1001`) → delete the QA opportunity.
3. Build form → embed → record its form ID in `website-embeds.md`.
4. Build CBHL-01 (proposed assignment/SLA marked), 05 (no SMS), 07, 08, 09 internal; build 02, 03, 04,
   06 as OFF.
5. Run the 02-workflows.md test plan, including the reply-vs-service and stop-rule end-to-end tests.
   Publish only what passes.
6. After David's decisions: migration, sequences, dialer/sync, application link.
