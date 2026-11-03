# Covered Bridge Home Loans: GHL backend

Account **Covered Bridge Home Loans**, locationId `giyhFtPh7MreGKeeSdCx` (company `CCaMpBMKYkOGGcV6G3bb`).
This folder documents the backend only. The website files elsewhere in this repo were not changed.

| File | What it is |
|---|---|
| `requirements/david-status-table.md` | Verbatim transcription of David's status table (Oct 29 email) |
| `snapshots/2026-11-03_pre-change_inventory.json` | Configuration before any change |
| `snapshots/2026-11-03_changes-and-tests.json` | Every asset created (IDs, trace IDs) and every test with its result |
| `build-specs/01-inquiry-form.md` | Exact UI build for the inquiry form |
| `build-specs/02-workflows.md` | CBHL-01…11 workflow specs, status, test plan |
| `build-specs/03-legacy-cleanup-and-migration.md` | Dispositions for the 23 legacy workflows, old pipelines, 110-opportunity migration |
| `website-embeds.md` | Calendar/form embed codes and placement guide for the website |

## Built and verified via API (2026-11-03)

| Asset | ID | Verified by |
|---|---|---|
| Pipeline **CBHL Lead to Loan**, 17 stages = David's statuses, exact labels | `hB1QaPi0Qh7swNDAAKzq` | read-back + full status-path test |
| 8 opportunity fields (External Loan ID, Loan Purpose, Lead Received / Application Received / Preapproval Issued / Lock / Closed dates, Status Notes) | see snapshot | values written and read back on a QA opportunity |
| 4 contact fields for the inquiry form (What can we help with?, Property State, Inquiry Message, CBHL Inquiry Source) | see snapshot | values written and read back on the QA contact |
| Tags `cbhl lead-to-loan`, `website inquiry`, `cbhl stop follow-up`, `cbhl replied`, `qa test contact` | see snapshot | read-back |
| Calendar **Home Loan Consultation** (round robin Mark Rotundo + Teresa Turner, Mon–Fri 8–17 ET, 30 min, outbound call) | `BSwRRQDlZgYCbEJAPwdE` | read-back + free-slot query |
| Custom value **CBHL Consultation Booking Link** | `7oVLXRZSbblZ5SnMN80f` | read-back |
| QA contact **QA Test CBHL 001** (undeliverable email, DND on) | `TvsVfgogDFS4Ynz4D6eD` | dedupe, DND, opportunity tests |

Direct GHL links:
- Pipeline: https://app.gohighlevel.com/v2/location/giyhFtPh7MreGKeeSdCx/opportunities/list (choose "CBHL Lead to Loan")
- Calendars: https://app.gohighlevel.com/v2/location/giyhFtPh7MreGKeeSdCx/settings/calendars
- Booking page: https://api.leadconnectorhq.com/widget/booking/BSwRRQDlZgYCbEJAPwdE

## Channel and integration check

| Channel | Finding |
|---|---|
| SMS | Twilio (default provider), number +1 814-699-9642 "David's number", SMS/MMS/voice. A2P brand values say "Valor Home Loans". A2P approval status isn't readable through the API. |
| Email | **No email provider configured** (conversation channel list empty, `defaultEmailService` empty). "From Email" custom value = [redacted]@valorhldirect.com, sending domain unverified. Email workflows stay draft. |
| Calling | Voice-capable number; all users on web-app calling. |
| Dialer ('Market', 'App Received', 'Started (Personal)', 'Preapproval (Personal)') | Not identified. Nothing in this account names the dialer. |
| Smartlead | Not detected (no fields, tags, workflows or values reference it). The connector can't list installed marketplace apps, so absence isn't confirmed. No cold campaigns set up. |
| iBluSend / Project Blue | Same as Smartlead: not detected, absence not confirmed. |

## Blocked by platform access

1. **Workflow API disabled for this sub-account** (`403 WORKFLOW_API_NOT_ENABLED_FOR_LOCATION` on
   definition/search/create/validate/publish/logs). Existing workflows can't be read, changed or
   unpublished from here, and new ones can't be created. Fix: HighLevel support enables it, or the specs
   are built in the UI.
2. **No form create/edit API.** The inquiry form is a UI build (spec ready).
3. **Location setting "Allow duplicate opportunities" is off.** Tested: a second application for the
   same contact is rejected (`OPPORTUNITY_NO_DUPLICATE`) even after the first is won. Turn on in
   Settings → Business Profile → General (or Opportunities settings) to keep separate applications.
4. **This build session's network blocks GHL web hosts**, so there's no browser route and no live widget render test.

## Resume checkpoint

State at 2026-11-03 ~13:50 UTC:
- Phases done: discovery refresh, snapshots, pipeline/fields/tags/values, calendar, API QA tests, specs.
- Nothing published. No legacy item changed. No messages sent. No existing contacts touched.
- Next actions, in order, when unblocked:
  1. Build form (01) → record its ID in `website-embeds.md` and CBHL-01.
  2. Build READY workflows CBHL-01, 04, 05 (minus SMS), 07, 08, 09 (internal) → test per table in 02 → publish.
  3. Decide migration mappings → run migration (03) → archive Inbound Leads.
  4. Cutover: unpublish legacy Facebook drips, publish CBHL-02 in the same minute.
  5. When copy/timing/email/dialer arrive: fill CBHL-03/05/06/09 draft steps, test, publish.
  6. When the application destination is confirmed: custom value + CBHL-10.
