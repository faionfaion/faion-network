# OKR Setting

## Summary

OKRs (Objectives and Key Results) combine qualitative inspiring goals (Objectives) with quantitative outcome measures (Key Results). The core rule: KRs must be outcomes, not tasks — any KR that starts with "ship/launch/build/release" is a task in disguise and must be rewritten as a measurable metric movement.

## Why

Without a structured goal framework, teams either set unmeasurable goals ("improve the product") or rigid task lists that survive even when the strategy changes. OKRs fix this by separating the ambition (Objective) from the measurement (KR), enabling teams to pivot implementation while preserving the goal. The 70% confidence target prevents sandbagging and creates psychological safety for stretch goals.

## When To Use

- Quarterly goal-setting with 2-50 person teams that need shared focus
- Mid-sized org with 3-5 strategic priorities that must cascade across teams
- Solo creator or founder using OKRs to focus a self-directed quarter
- Aligning a cross-functional initiative (eng + design + marketing) on shared outcome metrics
- Existing goal system is broken — everyone "achieved 100%" or no one tracks

## When NOT To Use

- Pre-PMF startup where every week pivots — OKRs become stale before the quarter ends; use weekly bets
- Agencies or consultancies where every project is a deliverable — billable utilization tracking beats OKRs
- Pure delivery teams (compliance, internal IT) — OKRs need outcome variability that does not exist in service work
- Org with no metric infrastructure — KRs that require new instrumentation will fail because the data never arrives
- Psychologically unsafe culture — OKRs amplify fear-driven behavior into sandbagging or punishment

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Objective and Key Result characteristics, scoring scale (0.0-1.0), structural rules |
| `content/02-process.xml` | 6-step OKR setting process from strategy alignment to weekly tracking |
| `content/03-antipatterns.xml` | KR-as-task, sandbagging, OKR theatre, cascading dilution, compensation coupling |

## Templates

| File | Purpose |
|------|---------|
| `templates/okr-template.md` | Quarterly OKR doc with baseline/target/current/score table per KR |
| `templates/kr-lint.py` | Python linter: fails OKR YAML files containing task-shaped or unbaselined KRs |
