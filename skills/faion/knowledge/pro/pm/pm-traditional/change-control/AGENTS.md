# Change Control

## Summary

Change control is the formal process that evaluates every proposed change to scope, schedule, cost, or quality against the approved baseline before any work begins. It requires a written change request with impact analysis, a tiered decision-authority matrix, and a register that tracks both approved and rejected requests — because rejected requests that resurface three times are real requirements signals.

## Why

Uncontrolled changes are the mechanism by which scope creep destroys budgets. "Small" changes bypass analysis and accumulate silently. A formal process makes every change visible, analyzes its cost before commitment, and creates an audit trail. Bundling minor changes weekly prevents bureaucratic overhead while maintaining control.

## When To Use

- Fixed-bid or fixed-scope contracts where every change has billing implications.
- Multi-stakeholder programs with a Change Control Board (CCB) and tiered authority.
- Regulated work (medical, finance, government) where audit trail of approved changes is mandatory.
- Any project where scope creep cost more than 15% of original budget on prior runs.

## When NOT To Use

- Pure agile sprints with an empowered Product Owner — backlog reordering replaces CR ceremony.
- Internal tools or R&D where changes are the work.
- Solo projects — apply a lightweight CHANGES.md instead.
- Phases before the scope baseline is signed off — there is nothing to "change" yet.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | CR lifecycle: receive, log, analyze impact, decide, implement, close |
| `content/02-rules.xml` | Rules for authority thresholds, rejected CR tracking, agentic CR workflow, and hidden-change detection |

## Templates

| File | Purpose |
|------|---------|
| `templates/change-request-form.md` | Structured CR form with impact analysis and options table |
| `templates/change-register.md` | Register table template with status tracking |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/cr_drift.sh` | Sums schedule/cost impact of approved CRs in a Markdown register |
