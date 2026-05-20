---
slug: writing-implementation-plans
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Bridges design.
content_id: "2994d2ea09432fba"
tags: [implementation-plan, task-breakdown, waves, dependencies, 100k-rule]
---
# Writing Implementation Plans

## Summary

**One-sentence:** Bridges design.

**One-paragraph:** Bridges design.md (AD-X decisions) and executor-ready TASK files by producing an ordered, wave-structured implementation plan. The 11-phase writing process: load SDD context → prerequisites → WBS → dependency graph → wave analysis → phase definition → task format → critical path → risk assessment → testing strategy → rollout strategy. Output is implementation-plan.md; TASK_*.md files are created separately, wave by wave.

## Applies If (ALL must hold)

- Design doc is finalized (Accepted status) and the feature is promoted to todo/ or in-progress/
- Feature has 3+ components that interact and sequencing matters
- Multiple waves of parallel tasks are possible (API before frontend, schema before service layer)
- Handoff is needed between agents or sessions — the impl-plan is the coordination artifact

## Skip If (ANY kills it)

- Feature has fewer than 3 tasks — skip the plan, write TASK files directly
- Spec or design doc is still in draft — writing the plan too early wastes tokens when requirements shift
- Bug fixes — use a single TASK file
- Exploratory spikes — impl-plans assume known solutions; spikes discover the solution

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

- parent skill: `solo/sdd/sdd-planning/`
