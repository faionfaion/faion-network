---
slug: task-creation-template-guide
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The canonical template for TASK_NNN.
content_id: "3f0940926c125b23"
tags: [task, template, executor, token-budget, dependency-tree]
---
# Task Creation Template Guide

## Summary

**One-sentence:** The canonical template for TASK_NNN.

**One-paragraph:** The canonical template for TASK_NNN.md files — the atomic units executor agents consume. Each task file must be self-contained within a 100k token budget: SDD references (15%), dependency tree with completed-task summaries and code snippets (10%), research (25%), implementation (40%), testing (10%). The dependency tree is the most critical section — it prevents agents from re-discovering patterns already established in completed tasks.

## Applies If (ALL must hold)

- Generating TASK_NNN.md files from an approved implementation plan
- Ensuring each task contains enough context for single-agent execution without re-reading the whole codebase
- Before handing off feature execution to faion-sdd-executor-agent

## Skip If (ANY kills it)

- Before spec.md and design.md are both approved — templates will be incomplete
- Spike/research tasks with unknown scope (token budget cannot be estimated)
- New greenfield project with no prior tasks (no dependency tree to build)

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
