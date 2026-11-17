# RentRecord — Product Requirements Document

Submission edition \| 12 November 2026

## 1. Product summary

RentRecord helps tenants organise rental life in one place: household bills, apartment condition records, moving tasks and deposit tracking. Local businesses may provide relevant restaurant, grocery and service offers. The product is presented as one standalone concept.

## 2. Problem, audience and value

The problem hypothesis is fragmented rental information: bills in different services, photos in a phone gallery, and moving responsibilities in messages or memory. Bringing these into a consistent structure could reduce the effort of finding information and following tasks.

Primary audience: students, young adults and international tenants renting in Finland. Landlords may receive exported records; local businesses are prospective offer providers. No partnerships or completed interviews are claimed.

| User task | Product response | Value to test |
| --- | --- | --- |
| Understand household expenses | Bills list, due dates and monthly totals | Faster understanding of what is due |
| Recall apartment condition | Room-by-room photos and notes | Easier retrieval and comparison |
| Finish a tenancy | Checklist and deposit timeline | Clearer view of remaining actions |
| Find local savings | Offers with conditions and expiry | Relevant, usable discounts |

## 3. Scope and delivery status

The product vision has three areas: Home and bills; Apartment records and moving; Local benefits. The local prototype implements apartment records, deposit tracking, manual bill tracking and a sample local-benefits screen. The new bills and benefits screens still need browser acceptance testing.

Manual entry is the initial scope for bills. Users pay through their usual external services; a paid label does not verify settlement. Partner offers require actual agreements before public use. No points system or payment-based reward is included.

## 4. Requirements

Existing identifiers are retained for traceability.

| ID | Requirement | Current status |
| --- | --- | --- |
| M1 | User-specific tenancy: address, landlord, rent, deposit and start date; genuine sign-in for deployed use | Setup implemented; real authentication absent |
| M2 | Default rooms, room additions/removals, photos, condition and notes | Implemented; draft persistence user-tested |
| M3 | Finalise report with server timestamp; block edits; allow dated addenda | Implemented; automated checks passed |
| M4 | Move-out checklist: cleaning, meters, keys, forwarding address, inspection and photos | Implemented; browser test pending |
| M5 | Move-out room photos and side-by-side comparison | Implemented; browser test pending |
| M6 | Deposit stages, server-recorded events, elapsed days and user-set reminder | Implemented; some automated coverage |
| M7 | Editable Finnish and English deposit request drafts | Implemented; browser test pending |
| M8 | Printable tenancy record: details, reports, checklist and deposit history | Implemented; print verification pending |
| M9 | Manual bills: provider, category, amount, due date, month derived from due date and self-reported payment status; add/edit/delete | Implemented; browser test pending |
| M10 | Monthly bills summary: total, marked paid, outstanding and overdue labels, filtered by due month | Implemented; browser test pending |
| M11 | Local offers: sample listings show business label, category, location, benefit, terms and expiry | Fictional sample listings implemented; not redeemable; no confirmed partners |

Future options: landlord confirmation, shared-household access, recurring bills and full Finnish/English interface. Shared bill splitting is not assumed in the initial scope.

## 5. Non-goals

Payment execution, banking or e-invoice integrations, real reward points, automatic legal judgement, filing disputes, guaranteed deposit recovery, native mobile apps and automatic proof of payment. No business success or uniqueness claim is made.

## 6. User journey

1. Create a tenancy and open its home overview.
2. Document rooms at move-in; save and finalise the report.
3. During the tenancy, add or update bills, review the monthly summary, and mark payments made externally as self-reported.
4. Optionally browse clearly labelled fictional local-offer examples and read their conditions.
5. At move-out, complete tasks and compare room photos.
6. Explicitly record keys returned in the deposit tracker, then deposit requested and its outcome.
7. Edit a request draft if needed and send it outside the application.
8. Export the tenancy record.

The checklist and deposit tracker are separate in the prototype: checking the keys item does not start the deposit timeline.

## 7. Data

| Entity | Main fields | Status |
| --- | --- | --- |
| User | identity, name, email | Fixed fictional identity in prototype |
| Tenancy | owner, address, landlord, rent, deposit, dates | Implemented |
| Report and room | tenancy, type, room, condition, note, photos, finalisation | Implemented |
| Addendum | report, note, server creation time | Implemented |
| Checklist | tenancy, task states and move-out details | Implemented in journey storage |
| Deposit event | tenancy, stage, server time | Implemented in journey storage |
| Bill | owner, tenancy, provider, category, amount, due date, month, payment label | Planned |
| Partner and offer | business, location, category, benefit, terms, validity | Planned |

The implementation uses SQLite; some journey information is stored as JSON rather than separate entity tables.

## 8. Rules and design

- Enforce ownership on the server. Fixed demo identity is insufficient for deployed multi-user privacy.
- Finalised report entries remain unchanged; additions are dated.
- Server event timestamps indicate recording time, not independently verified photo capture time.
- Show a high-deposit warning above three months of entered rent. Do not present unverified legal interpretations.
- Reminder periods are user settings, not legal deadlines.
- A self-reported payment is clearly labelled; no bank verification is implied.
- Future bill totals use one currency and integer cents; exclude deleted entries and define the selected month clearly.
- Offers show limitations and expiry; demonstration offers must be labelled fictional.
- Use text labels alongside status colours and responsive navigation.
- Use fictional demo data. Deletion and retention controls require implementation and verification before real personal data use.

## 9. Acceptance criteria

| Test | Pass condition |
| --- | --- |
| AT-01 Setup | Valid tenancy persists; deposit above 3x rent shows warning |
| AT-02 Report | Three-room report finalises, shows timestamp and blocks edits |
| AT-03 Addendum | New dated note appears without changing original entries |
| AT-04 Move-out | Checklist reaches completion and before/after photos display |
| AT-05 Deposit | Valid stages, elapsed days and configured reminder display correctly |
| AT-06 Drafts | Both languages include correct tenancy facts and remain editable |
| AT-07 Export | Printable record contains details, reports, tasks and deposit history |
| AT-08 Privacy | A genuinely signed-in second user cannot retrieve another user's data |
| AT-09 Landlord link | Future optional confirmation uses scoped, expiring access |
| AT-10 Bills | Bill add/edit/delete persists; invalid amounts/dates are rejected. Implementation present; browser test pending |
| AT-11 Summary | Monthly totals agree with bill records; overdue and self-reported paid labels display correctly. Implementation present; browser test pending |
| AT-12 Offers | Fictional demo offers show category/location/terms/expiry and are labelled not redeemable. Implementation present; browser test pending |

TASKS records actual verification. Planned tests are not marked passed.

## 10. Value validation and risks

No user interviews, partner agreements or measured outcomes are available. Test whether users can find monthly obligations and apartment records more easily, whether manual bill entry is acceptable, and whether local businesses will offer meaningful benefits. Measure task completion, retrieval time, missed fields and willingness to reuse. Compare with each participant's own current method.

Major risks: manual-entry effort, infrequent moving use, privacy, feature overload and partner recruitment. Prospective partner listing fees or referral commissions are possible business hypotheses, not validated revenue. Household bill tracking remains useful only if users find its effort justified.
