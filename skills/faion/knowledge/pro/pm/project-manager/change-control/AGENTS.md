# Change Control

## Summary

Route every change request through a formal log → impact analysis → tiered decision → baseline update cycle. Tier authority by size: PM approves minor (< 1 day, < $500), Sponsor approves medium (1-5 days, < $5k), CCB approves major. The rule: never auto-approve — the agent prepares the impact packet; a human approver signs off before implementation begins.

## Why

Uncontrolled changes are the primary mechanism by which scope creep destroys budgets. A formal register makes every change visible and comparable, catches repeat requests (same CR under a new title), and ensures baselines (scope, schedule, budget) stay synchronized after approval. Tiering by size prevents the CCB from becoming a bottleneck that pushes stakeholders toward informal workarounds.

## When To Use

- Fixed-scope, fixed-budget engagements (agency contracts, SoWs) where every change has billing impact
- Regulated environments (finance, healthcare, government) requiring an audit trail of decisions
- Projects with multiple stakeholders submitting asks via different channels — register forces one queue
- Late-stage projects (> 50% complete) where every change has compounded ripple effects
- Programs where one project's change affects sibling projects

## When NOT To Use

- Pure agile teams with continuous backlog refinement — change is the default state, not the exception
- Discovery/research phases — you want changes; controlling them defeats the purpose
- Solo projects where you are both requester and approver — capture as a TODO, not a CR

## Content

| File | What's inside |
|------|---------------|
| `content/01-change-process.xml` | Six-step process, status values, impact assessment areas, decision tier rules |
| `content/02-change-antipatterns.xml` | Common failures: informal approval, hidden ripple effects, repeat CRs, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/change-request.md` | CR form: description, justification, impact table, options, decision block |
| `templates/change-register.md` | Change register table: CR ID, date, description, requester, impact, status |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/cr-router.py` | Assign approval tier (PM/Sponsor/CCB) from impact YAML (days, cost, risk level) |
