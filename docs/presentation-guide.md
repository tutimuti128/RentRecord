## Five-minute presentation

| Time | Topic | What to say or show |
| --- | --- | --- |
| 0:00–0:45 | Problem and audience | Tenants need to manage bills, apartment information and moving responsibilities. Fragmentation is our problem hypothesis. |
| 0:45–1:30 | Product value | One organised home workspace: expenses, records and tasks; local benefits are an additional product area with fictional examples in the prototype. |
| 1:30–3:30 | Working demonstration | Create fictional tenancy; save room photos/notes; show finalisation, checklist, comparison and deposit timeline; open print export if rehearsed. |
| 3:30–4:15 | Product vision | Show the bills screen grouped into overdue, coming up and marked paid; explain entries are manual and payment status is self-reported. Open the future integrations roadmap. Show the illustrative map and sample local offers; state that all names, areas and offers are fictional and not redeemable. |
| 4:15–5:00 | AI use and limits | AI helped draft requirements, code and checks. The author ran the prototype and confirmed setup and report persistence. Explain pending verification and next validation step. |

## Opening

“RentRecord helps tenants organise everyday rental life in one place. It combines a vision for household bill tracking and relevant local benefits with apartment records, moving tasks and deposit tracking. The intended value is clearer expenses and easier access to important rental information.”

## Demonstration boundaries

The live code covers apartment records, deposit tracking and manual bill tracking organised by due status. The local-benefits screen contains an illustrative neighbourhood map and fictional, non-redeemable offers. Gmail, electricity-provider and payment integrations are roadmap concepts only. No actual partners, measured savings, proven demand or guaranteed deposit recovery are claimed. Use fictional tenancy data. Bills and offers were added recently and still need browser acceptance testing. Rehearse finalisation and export before relying on them live.

## Questions and answers

| Question | Suggested answer |
| --- | --- |
| Why this problem? | I chose a familiar responsibility: organising information throughout a tenancy. I still need to validate how serious the problem is for the target audience. |
| What is the value? | Make expenses and responsibilities easier to understand and rental records easier to retrieve. |
| Why use it instead of existing tools? | The proposed benefit is one home-centred structure. I have not established superiority or uniqueness; that requires user comparisons. |
| What did AI do? | AI assisted requirements, code generation, checks and documentation. I launched the app and tested saving and reloading. |
| What did you change? | I defined the target user and scope, reviewed the flow and tested the prototype. Specific implementation changes should be described only if I can explain them. |
| How would it earn revenue? | Partner listing fees or referral commissions are hypotheses to test, not established income. |
| What is unfinished? | Real authentication, actual partner agreements, complete demo seeding and browser verification of the new bills/offers screens and print output. |
| What comes next? | Verify the reorganised bills screen and illustrative offers map in the browser; define and validate an authorised bill-import approach; observe five tenants' current methods; ask prospective businesses what offers they could support. |

## Repository and final submission

The current project files are published at [github.com/tutimuti128/RentRecord](https://github.com/tutimuti128/RentRecord). Use the latest `main` branch. To start the app from the repository folder, run `python3 src/app.py`.

Do not upload personal databases, real apartment photos, credentials or caches. Use this .gitignore:

```txt
__pycache__/
*.py[cod]
*.sqlite3
*.sqlite3-*
*.db
.env
.env.*
!.env.example
.DS_Store
```

If the repository is private, give the assessor access. Download the current repository ZIP when you need a copy of the code and documentation; preserve the folder structure.

## Final submission check

- Documentation and code both available to the assessor.
- README starts the app successfully.
- Presentation distinguishes working features from planned features.
- Required Moodle format and deadline checked by the author.
- Submission actually sent through the required channel.

Notion updates and GitHub account creation do not automatically submit to Moodle.
