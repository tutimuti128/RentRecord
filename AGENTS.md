# `AGENTS.md` — RentRecord development instructions

## Project

RentRecord organises household bills, apartment condition records, moving tasks and deposit information, with planned local partner benefits. Read PRD and TASKS before editing.

## Scope

The submitted Python/SQLite prototype implements tenancy records and deposit tracking. Manual bills, monthly summaries and local offer listings are planned M9–M11. Do not describe them as implemented until code and verification support that claim.

## Working approach

- Follow task dependencies and preserve functioning code.
- Complete authorised work without requiring approval between routine stages.
- Keep implementations small and readable.
- Use the current product concept consistently, without comparisons to other products owned by the author.
- Distinguish implementation, automated tests and user acceptance tests.
- Check uncertain APIs in official documentation.
- Do not invent research, partnerships, results or completed work.

## Required rules

- Enforce ownership server-side; do not treat a fixed demo identity as production authentication.
- Finalised reports are immutable; subsequent notes are dated addenda.
- Event timestamps come from the server and do not prove when a photo was captured.
- Payment statuses are self-reported unless a real verification integration exists.
- Manual bill tracking never claims to execute a payment.
- Offers show terms and expiry; fictional offers are labelled.
- Never claim legal fault, binding evidence or guaranteed deposit recovery.
- Use fictional records only and keep databases, personal photos and secrets out of GitHub.
- Validate bill amounts, dates and monthly totals when those features are built.
- Add no payment processing, banking integration or points economy without an explicit scope change.

## Debugging and delivery

Find the cause, fix it and run relevant checks. Preserve user data during changes. Document run instructions, known limitations and exact verification evidence.
