# RentRecord

## Everyday rental life, organised

RentRecord is a tenant-focused product for keeping household bills, apartment records and rental responsibilities in one structured place. Planned local partner offers add everyday benefits for restaurants, groceries and services.

Course: AI in Expert Work — Vibe Code assignment. Author: Tolga Tufar.

## Problem and value

A tenant may need to check several places to find household bills, apartment photos, moving tasks and deposit information. RentRecord proposes one home-centred workspace to make this information easier to organise, find and act on.

The intended audience is students, young adults and international tenants in Finland. This audience and its needs are hypotheses to validate; no interview findings or proven savings are claimed.

| Area | Intended value | Submission status |
| --- | --- | --- |
| Household bills | Add/edit/delete bills, see overdue, upcoming and paid groups, and record payments made elsewhere | Implemented; browser test pending. Gmail/provider integrations are future work |
| Apartment records | Find room-by-room move-in and move-out photos and notes | Implemented in local prototype |
| Moving and deposit | Follow tasks and record deposit progress | Implemented; final browser tests pending |
| Local benefits | Browse an illustrative area map and sample restaurant, grocery and service offers | Map and offers implemented; fictional locations and offers only |

## Run the prototype

Clone this repository or use Code → Download ZIP and extract it. Python 3 is required; no external Python packages are needed. From the repository folder run:

```bash
python3 src/app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) if needed. Keep Terminal open; stop with Control+C. The application uses Python, SQLite and HTML/JavaScript. It has a simulated Demo Tenant, not real sign-in. A fresh install has no complete demo tenancy.

Use fictional details: Example Street 1, Demo Landlord, landlord@example.test, rent €800 and deposit €1,600. Save records before switching sections.

## Verification

From the repository folder:

```bash
cd src
python3 test_journey.py
```

Automated checks passed on 10 November 2026 for report persistence, input rejection, ownership functions, finalisation, addenda, checklist storage and deposit history. The user confirmed database checks, setup/save/reload/high-deposit warning and move-in draft persistence. Bills and sample-benefits screens were added on 17 November 2026; their browser flows have not yet been independently verified. Final browser tests and print layout remain pending.

## Project documents

PRD defines the product vision and acceptance criteria. BRAINSTORM explains the four-quadrant analysis. TASKS separates implemented work, verification and planned work. AGENTS gives development constraints. Notes contain an interview plan, not completed research. The flow and presentation guide explain the concept and demonstration. src contains runnable application code.

## Limits and submission

The current code includes manual bill tracking, monthly totals, self-reported paid status, and a sample local-benefits screen alongside apartment records and deposit tracking. Sample offers are fictional and cannot be redeemed. No real partners, payment processing, bank connections, measured savings or confirmed rewards funding are included. The record is a documentation aid, not legal advice or guaranteed legal evidence. Use fictional data only.

GitHub repository: https://github.com/tutimuti128/RentRecord. Moodle format, deadline and final submission must be checked by the author.
