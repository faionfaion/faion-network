---
slug: impl-plan-task-format
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The executor agent parses TASK files mechanically — it must find every required field in a known location.
content_id: "a3b20bd00d4e7739"
tags: [task-format, sdd, executor, invest, planning]
---
# Implementation Plan Task Format

## Summary

**One-sentence:** The executor agent parses TASK files mechanically — it must find every required field in a known location.

**One-paragraph:** The executor agent parses TASK files mechanically — it must find every required field in a known location. Vague AC items ("works correctly") leave no observable outcome; the executor cannot determine success. The INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable) ensure tasks can be executed in isolation without blocking sibling waves, and that each task fits within the 100k token budget.

## Applies If (ALL must hold)

- Converting design.md architecture decisions into executor-ready TASK_*.md files.
- Defining structure for an implementation plan that supports parallel waves.
- Auditing existing task files for INVEST compliance before executor assignment.

## Skip If (ANY kills it)

- One-off scripts or changes outside the SDD lifecycle — overhead exceeds benefit.
- Research spikes where the output is a document, not code.
- Tasks under ~15k tokens — the format overhead is not justified.

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
