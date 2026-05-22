---
slug: wbs-creation
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Without a WBS, estimates are guesses and dependencies are invisible until they block progress.
content_id: "a8221dfd16c637b7"
tags: [planning, wbs, scope-management, pmi, decomposition]
---
# Work Breakdown Structure Creation

## Summary

**One-sentence:** Without a WBS, estimates are guesses and dependencies are invisible until they block progress.

**One-paragraph:** Without a WBS, estimates are guesses and dependencies are invisible until they block progress. Deliverable-oriented decomposition forces the team to answer "what will be produced?" before "how will we produce it?", which surfaces scope gaps and prevents activity-focused planning that omits unassigned outputs. The WBS dictionary transforms numbered IDs into testable acceptance criteria.

## Applies If (ALL must hold)

- New projects where scope is fixed enough to decompose into deliverables (more than four weeks of work).
- Fixed-bid proposals where each work package needs an hours/cost line for the estimate.
- Programs requiring a contractual scope baseline with WBS IDs for traceability.
- Migration or cutover projects where a missing deliverable is expensive.

## Skip If (ANY kills it)

- Pure-Scrum backlog work where the product backlog serves the same role.
- Exploratory R&D — the deliverables are unknown before the work begins.
- Single-week tasks — a checklist is faster.
- Continuous operations or service catalog work — use the service catalog instead.

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
