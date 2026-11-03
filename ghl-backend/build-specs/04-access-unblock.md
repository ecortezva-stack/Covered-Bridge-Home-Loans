# Access needed to finish the backend build

Three things can't be done through the current connector:

| Task | API route | Browser route |
|---|---|---|
| Build/inspect/unpublish workflows | Workflow API (403 for this sub-account today) | yes |
| Build the inquiry form | **none exists** | yes |
| Turn on "Allow duplicate opportunities" | **none exposed** | yes |

So an authorized browser session is the one route that unblocks everything. The Workflow API request
is still worth filing, because API-built workflows can be snapshotted and diffed exactly.

## 1. HighLevel support request (copy and send from the agency account)

Send from an **agency admin** login for the agency that owns company `CCaMpBMKYkOGGcV6G3bb`
(GHL → Help (?) → Contact support / support chat, or support@gohighlevel.com).

> **Subject:** Workflow API access for sub-account giyhFtPh7MreGKeeSdCx: eligibility and enablement
>
> Hello HighLevel Support,
>
> Our integration calls the public Workflow API endpoints for sub-account **giyhFtPh7MreGKeeSdCx**
> ("Covered Bridge Home Loans", company ID CCaMpBMKYkOGGcV6G3bb) and every request returns:
>
> `403 Forbidden, code WORKFLOW_API_NOT_ENABLED_FOR_LOCATION: "The workflow API is not enabled for
> location giyhFtPh7MreGKeeSdCx … the API is currently available to selected sub-accounts only, and this
> one is not among them."`
>
> Affected endpoints (all tested 2026-11-03): `GET /workflows/{id}/definition`, `POST /workflows/search`,
> `GET /workflows/step-types`, `POST /workflows/definition/validate`. Listing workflows via
> `GET /workflows/` works. First failing request: 2026-11-03, about 13:30 UTC.
>
> Please tell us:
> 1. Is this sub-account (or our agency/plan) **eligible** for the Workflow API (definition read, create,
>    update, status/publish, logs)?
> 2. If yes, can you **enable** it for giyhFtPh7MreGKeeSdCx, and is there anything we must accept or
>    configure first (beta terms, plan level, app scopes `workflows.readonly`, `workflows.write`,
>    `workflows.publish`, `workflows.logs`)?
> 3. If not, is there a waitlist or an expected date?
>
> Also: is there a public API to set the sub-account setting "Allow duplicate opportunities", or is it
> UI-only?
>
> Thank you,
> [name], [agency name]

Don't assume support will enable it. Its answer decides whether workflows are built by API or by browser.

## 2. Browser route: exact steps (needed for the form and setting regardless)

The cloud session that's building this can't reach GHL's web hosts and has no GHL login. The working
route is **Remote Control from a computer that you or David own**, where you sign in to GHL yourself and
the build then runs in that browser:

1. On a **Mac or Linux** computer (Windows isn't supported for this), install the **Claude desktop app**
   and sign in with the same Claude account as this session.
2. Create an empty folder, e.g. `~/cbhl-ghl-automation`. It can't be your home folder, a hidden folder,
   or inside `~/Library`.
3. In the desktop app: **Settings → Claude Code → Remote Control** → add that folder. (Or, in a
   terminal inside the folder, run `claude remote-control`.) Keep the app running.
4. Tell this session it's ready. It will request that folder. Approve the prompt on your computer.
5. The session installs a browser automation runtime **inside that folder** and opens a **visible**
   browser window. **You** sign in to GHL in that window, including any 2FA code. **Never paste a GHL
   password or code into chat.** The login is stored only in a browser profile in that folder, so you can
   revoke it by deleting the folder.
6. Sign in as a user with **admin rights on the Covered Bridge Home Loans sub-account** (needed for
   Settings → Business Profile, forms and workflows). Recommended: create a dedicated staff user (e.g.
   "CBHL Automation", Admin, this sub-account only) in **Settings → My Staff** so changes are attributable
   and the access can be removed afterwards.
7. Remove access after the build: disconnect Remote Control in the desktop app and delete the folder (and
   the dedicated user if one was created).

What the browser session will then do, in order: save and inspect the Contact Deletion workflow and the
other published legacy workflows → disable the deletion behavior → turn on Allow duplicate opportunities
→ build the CBHL General Inquiry form → build CBHL-01/05/07/08/09 (internal parts) → run the tests in
02-workflows.md → publish only what passes → re-test duplicate scenarios.

Not recommended: putting GHL credentials into the cloud environment's secrets and opening its network to
GHL. A fresh cloud container triggers a new-device 2FA challenge each time, which still needs a person.
