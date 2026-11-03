# David's external-system status table (verbatim transcription)

Source: email from David Bassett, "Current status / workflow data for Covered Bridge Home Loans",
Thu Oct 29 (2026), 11:21 PM, provided as a screenshot on 2026-11-03.
Signature: David T. Bassett, Managing Director, https://coveredbridgebrands.com

Spelling is kept exactly as written (including "Dailer"). Merged cells are shown once with the
columns they span.

## Status row (17 columns, left to right) and colour groups

| # | Status | Colour group |
|---|---|---|
| 1 | New | blue |
| 2 | Connected | blue |
| 3 | Started (New) | green |
| 4 | Started (NC) | green |
| 5 | Started | green |
| 6 | Preapproval | light green |
| 7 | Locked | light orange |
| 8 | Closed | yellow |
| 9 | CTUD | salmon |
| 10 | WTD | salmon |
| 11 | Incomplete | salmon |
| 12 | Declined | salmon |
| 13 | Withdrawn | salmon |
| 14 | Disc/Wrong Number | salmon |
| 15 | Wrong Language | salmon |
| 16 | Expired | salmon |
| 17 | DNC | red |

## Rows

| Row | Cell text | Columns covered |
|---|---|---|
| SMS | 8 SMS over 30 Days | New + Connected (merged) |
| SMS | 1 SMS | Started (New) |
| SMS | 5 SMS over 5 Days | Started (NC) |
| SMS | No SMS | Started |
| SMS | No SMS | Preapproval |
| SMS | No SMS | Locked |
| SMS | No SMS | Closed |
| SMS | No SMS | CTUD through Expired (merged) |
| SMS | No SMS | DNC |
| Email | 18 Email over 90 Days | New + Connected (merged) |
| Email | 8 Emails over 11 Days | Started (New) + Started (NC) + Started + Preapproval (merged) |
| Email | No Email | Locked |
| Email | No Email | Closed |
| Email | No Email | CTUD through Expired (merged) |
| Email | No Email | DNC |
| Dialer | Dialer campaign 'Market' | New + Connected (merged) |
| Dialer | (blank) | Started (New) |
| Dialer | Dailer campaign 'App Received' | Started (NC) |
| Dialer | Dailer campaign 'Started (Personal)' | Started |
| Dialer | Dailer campaign 'Preapproval (Personal)' | Preapproval |
| Dialer | (blank) | Locked, Closed, each of CTUD..Expired, DNC |
| Automatic Changed | Expires 90 days after received | New + Connected (merged) |
| Automatic Changed | Changes to Started (NC) after 1 day | Started (New) |
| Automatic Changed | (blank) | all other columns |
| Description | New Lead | New |
| Description | Contacted Lead | Connected |
| Description | Application Received | Started (New) + Started (NC) + Started (merged) |
| Description | Preapproval issued | Preapproval |
| Description | Lock | Locked |
| Description | Closed Loan | Closed |
| Description | Dead Lead/Loan | CTUD through Expired (merged) |
| Description | Do Not Contact | DNC |

## What the table does NOT specify (kept unresolved, not invented)

- Meaning of **CTUD**, **WTD** and **NC** (in "Started (NC)").
- Message wording for any SMS or email.
- Send timing inside each window (e.g. which day each of the 8 SMS / 18 emails goes out).
- Which dialer system runs campaigns 'Market', 'App Received', 'Started (Personal)',
  'Preapproval (Personal)', and how GHL should hand contacts to it.
- What moves a record from Started (NC) to Started, or between other statuses, other than the two
  automatic changes listed.
- What the 90-day expiry moves the record to (the "Expired" column exists; the table does not
  explicitly connect them).
- Whether the external system pushes these statuses into GHL or staff set them in GHL.
