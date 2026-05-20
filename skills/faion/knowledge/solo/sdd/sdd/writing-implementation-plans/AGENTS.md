---
slug: writing-implementation-plans
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An implementation plan bridges design docs and executable tasks by transforming architectural decisions (AD-X) into ordered, token-budgeted work units optimized for LLM agent execution.
content_id: "2994d2ea09432fba"
tags: [implementation, planning, sdd, tasks, waves]
---
# Writing Implementation Plans

## Summary

**One-sentence:** An implementation plan bridges design docs and executable tasks by transforming architectural decisions (AD-X) into ordered, token-budgeted work units optimized for LLM agent execution.

**One-paragraph:** An implementation plan bridges design docs and executable tasks by transforming architectural decisions (AD-X) into ordered, token-budgeted work units optimized for LLM agent execution. The 100k token rule ensures each task fits within a focused context window. Wave analysis identifies parallel execution opportunities. Every task must trace to an AD-X or FR-X — orphan tasks are a quality gate failure.

## Applies If (ALL must hold)

- After spec and design are both in Approved status.
- When feature has 3+ tasks requiring ordered execution.
- When design doc contains parallel-eligible work (Wave 1 / Wave 2 pattern).
- When task token estimates exceed 30k (simple tasks may skip formal plan).

## Skip If (ANY kills it)

- Before spec or design are approved — planning against unapproved docs creates rework.
- For trivial single-file changes that need no coordination.
- For bug fixes that touch one file and have no dependencies.
- When design doc has no AD-X decisions (no design = no plan needed).

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

- parent skill: `solo/sdd/sdd/`
