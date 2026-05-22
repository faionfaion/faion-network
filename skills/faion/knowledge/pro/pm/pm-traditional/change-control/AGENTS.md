---
slug: change-control
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Change control is the formal process that evaluates every proposed change to scope, schedule, cost, or quality against the approved baseline before any work begins.
content_id: "5a43867c425632e1"
tags: [change-control, scope, ccb, governance]
---
# Change Control

## Summary

**One-sentence:** Change control is the formal process that evaluates every proposed change to scope, schedule, cost, or quality against the approved baseline before any work begins.

**One-paragraph:** Change control is the formal process that evaluates every proposed change to scope, schedule, cost, or quality against the approved baseline before any work begins. It requires a written change request with impact analysis, a tiered decision-authority matrix, and a register that tracks both approved and rejected requests — because rejected requests that resurface three times are real requirements signals.

## Applies If (ALL must hold)

- Fixed-bid or fixed-scope contracts where every change has billing implications.
- Multi-stakeholder programs with a Change Control Board (CCB) and tiered authority.
- Regulated work (medical, finance, government) where audit trail of approved changes is mandatory.
- Any project where scope creep cost more than 15% of original budget on prior runs.

## Skip If (ANY kills it)

- Pure agile sprints with an empowered Product Owner — backlog reordering replaces CR ceremony.
- Internal tools or R&D where changes are the work.
- Solo projects — apply a lightweight CHANGES.md instead.
- Phases before the scope baseline is signed off — there is nothing to "change" yet.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/pm/pm-traditional/`
