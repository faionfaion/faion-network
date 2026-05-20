---
slug: impl-plan-examples
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three scaled implementation plan examples (3-task simple, 7-task medium, 12-task complex) plus a task-split example for oversized tasks exceeding the 100k token budget.
content_id: "933bb6d90e736131"
tags: [implementation-plan, examples, wave-analysis, critical-path, task-splitting]
---
# Implementation Plan Examples

## Summary

**One-sentence:** Three scaled implementation plan examples (3-task simple, 7-task medium, 12-task complex) plus a task-split example for oversized tasks exceeding the 100k token budget.

**One-paragraph:** Three scaled implementation plan examples (3-task simple, 7-task medium, 12-task complex) plus a task-split example for oversized tasks exceeding the 100k token budget. Each example shows wave analysis tables, dependency graphs (text/table format), critical path chains, and per-task breakdowns with AC and file lists. Used as structural references when generating or reviewing real implementation plans.

## Applies If (ALL must hold)

- Bootstrapping a new implementation plan for a feature of known complexity (simple/medium/complex).
- Validating a generated plan against a known-good structural reference.
- Teaching wave analysis and critical path before an agent attempts it on a real feature.
- Identifying the split point for tasks that exceed the 100k token budget (use the refactoring split example).

## Skip If (ANY kills it)

- Copying example task names, file paths, or effort estimates into a real plan — examples are structural references only.
- Referencing hour-based effort estimates from examples — project rules prohibit time estimates; use token estimates only.
- For plans with more than 20 tasks — examples top out at 12; very large features need a custom approach.
- Using ASCII wave diagrams from the examples — project rules prohibit ASCII art; use tables only.

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
