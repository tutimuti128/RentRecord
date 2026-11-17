# RentRecord — delivery checklist and test log

## Status convention

Implemented means code exists. Verified means the stated test was completed. Planned means the submitted code does not include the feature. An unchecked acceptance task is not a claim that no implementation exists.

## Planning

- [x] Product summary and four-quadrant brainstorm.
- [x] PRD with one coherent product concept, value, scope and acceptance criteria.
- [x] Development instructions and run instructions.
- [ ] Interview five target tenants and record actual findings.
- [ ] Compare participants' current tools with the proposed workflow.
- [ ] Verify any legal claims before using them in presentation or product.
- [ ] Confirm Moodle submission format and deadline.

## Current code and verification

| Task | Delivery status | Verification |
| --- | --- | --- |
| B1 Data model | Implemented | User confirmed database checks |
| B2 Tenancy setup | Implemented | User confirmed saving, reload and deposit warning |
| B3 Move-in rooms/photos/notes | Implemented | User confirmed save and reload |
| B4 Finalisation/addenda | Implemented | Automated checks passed; UI test pending |
| B5 Move-out checklist | Implemented | Storage checks passed; UI test pending |
| B6 Photo comparison | Implemented | Browser walkthrough pending |
| B7 Deposit tracking | Implemented | Transition/history checks passed; reminder UI pending |
| B8 Finnish/English drafts | Implemented | Browser verification pending |
| B9 Printable record | Implemented | Print layout and contents pending |
| B10 Authentication and privacy | Partial | Ownership functions tested; fixed demo identity, no genuine second-user test |
| B11 Complete demo tenancy | Planned | No complete seeded tenancy included |

## Implemented; verification pending

- [x] B12 Manual household bills: add/edit/delete, due dates and self-reported status (M9, AT-10); browser verification pending.
- [x] B13 Monthly expense summary by due month, with paid/outstanding totals and overdue labels (M10, AT-11); browser verification pending.
- [x] B14 Local-benefits screen with fictional, not-redeemable sample offers (M11, AT-12); browser verification pending.

## Planned product work

- [ ] Validate local partner interest; do not describe prospects as agreed partners.
- [ ] Optional landlord confirmation, shared access, recurring bills and interface translation.
- [ ] Real authentication, deletion/retention controls and production privacy review before deployment.

## Submission

- [x] Runnable source ZIP attached in src.
- [x] README contains startup, demonstration data and limitations.
- [x] Presentation outline and concept flow prepared in the project documentation.
- [ ] Add the actual GitHub repository URL and upload documentation/code there.
- [ ] Run outstanding browser acceptance tests; record failures honestly.
- [ ] Rehearse the demonstration.
- [ ] Submit through Moodle in its required format.

## Test results log

| Test | Result | Date | Notes |
| --- | --- | --- | --- |
| AT-01 | User confirmed | 10 November 2026 | B2 saving, refresh persistence and high-deposit warning confirmed in chat. |
| AT-02 | Partial | 10 November 2026 | B3 photos and notes persisted in user test. Automated finalisation/locking checks passed; finalisation UI not user-tested. |
| AT-03 | Automated checks passed; UI pending | 10 November 2026 | Dated addenda preserve original report in tests. |
| AT-04 | Partial; UI pending | 10 November 2026 | Checklist persistence tested; full photo comparison walkthrough pending. |
| AT-05 | Partial; UI pending | 10 November 2026 | Stage transitions, server dates and event preservation tested; elapsed-day/reminder UI not verified. |
| AT-06 | Pending | 10 November 2026 | Bilingual editable drafts implemented; final browser test pending. |
| AT-07 | Pending | 10 November 2026 | Browser print export implemented; output layout/content not independently verified. |
| AT-08 | Partial; not production privacy | 10 November 2026 | Ownership denial tested in data functions. Fixed demo identity means real two-user browser isolation is not implemented or verified. |
| AT-09 | Not implemented | 10 November 2026 | Optional landlord link excluded. |

## Additional planned tests

| Test | Status | Reason |
| --- | --- | --- |
| AT-10 Bills | Implemented; browser test pending | Added per-tenancy bill records with add/edit/delete and external-payment labels |
| AT-11 Monthly summary | Implemented; browser test pending | Due-month totals for total, marked paid, outstanding and overdue |
| AT-12 Local offers | Sample screen implemented; browser test pending | Fictional examples labelled not redeemable; no partner agreements claimed |

Previously recorded automated results refer to the 10 November 2026 run. New bills and sample-benefits screens were added on 17 November 2026 and have not yet been browser-tested. No completed interviews, verified payments, measured savings or partner contracts are claimed.
