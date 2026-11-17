# RentRecord — complete local course demo

## Product scope
RentRecord brings household bills, apartment records and local benefits into one product vision. This source implements apartment records, deposit tracking and manual bill tracking. A local-benefits screen shows fictional, not-redeemable examples. No real partner agreements are included. See the root PRD for scope.

## Launch on your Mac
From the repository root, run:

```bash
python3 src/app.py
```

Stop any previous server with Control+C. Run this in Terminal, not the Python >>> prompt.

The browser opens http://127.0.0.1:8000. Keep Terminal running. If your extracted folder is somewhere else, type `python3 ` and drag app.py into Terminal before pressing Enter.

To retain your old data: stop both apps, copy rentrecord.sqlite3 from your previous version into this folder, and retain the old copy as backup. Database extensions install automatically.

## Bill organisation groups entries into overdue, coming-up and marked-paid sections. A future-plan panel explains Gmail and authorised provider integrations; those integrations are not connected. Local benefits use an illustrative area map and fictional businesses/offers only; no exact addresses or redeemable deals are represented.

## Walkthrough
Create a fictional tenancy. Add a bill in Bills to see monthly totals, edit it, and mark it paid (self-reported). Browse the fictional offers in Local benefits. Open the tenancy and fill the six-room move-in draft with photos, conditions and notes. Save and finalise it; finalisation is irreversible in the app. Add dated notes if needed. Use Move-out for the six-item checklist, meter/forwarding/inspection details and before-and-after photos. Save before switching sections. Use Deposit to record keys returned, deposit requested and the outcome. Reminder days are your own setting, not a legal deadline; reminders appear only while using the app. Generate an editable English or Finnish request draft, then send it yourself outside the app if appropriate. Export record opens your browser's print dialog; choose Save as PDF.

## Scope and limits
This is a local prototype with simulated single-tenant identity. Real sign-in, multi-user deployment and production privacy controls are not implemented. Use fictional data only. Optional landlord links, rent logs and references are not included. No email or request is sent automatically. Request drafts are not saved; copy them before closing. Photos and tenancy data persist in SQLite on this computer. JPEG/PNG/WebP only; 3 MB each, 10 per room, 20 MB per report. HEIC requires conversion.

Finalised report entries are locked by the server and database guards. Addenda and deposit events use server-generated UTC timestamps. Checklist entries are self-reported; checking “keys returned” does not automatically start the separate deposit tracker. Use its explicit action to start that timeline. The prototype does not decide fault or provide legal advice. The record is a documentation aid.

## Verification
Run `python3 test_journey.py` from this folder for the accumulated model tests. Python and JavaScript syntax checks passed. Automated tests cover draft persistence, locks, addenda, ownership, checklist storage, deposit transitions, event dates and history protection. End-to-end browser interactions and print layout have not been independently tested in this environment.

## Files
app.py is the local HTTP server and data logic; index.html contains all screens and printable record. schema.sql and locking.sql define storage and locking rules. model.py and test_*.py contain checks. No external Python packages are required.
