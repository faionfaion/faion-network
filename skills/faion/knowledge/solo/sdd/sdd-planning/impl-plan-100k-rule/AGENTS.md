---
slug: impl-plan-100k-rule
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every task assigned to an agent must fit within a 100k token context budget.
content_id: "63939344596b5260"
tags: [implementation-plan, token-budget, task-decomposition, context-management, task-splitting]
---
# Implementation Plan: 100k Token Rule

## Summary

**One-sentence:** Every task assigned to an agent must fit within a 100k token context budget.

**One-paragraph:** Every task assigned to an agent must fit within a 100k token context budget. The budget has fixed overhead (agent prompt ~8k, project context ~12k, task file ~3k, buffer ~15k) plus variable codebase reading. Tasks exceeding 80k tokens must be split before any TASK file is written. Three splitting strategies: by component, by layer, by dependency wave.

## Applies If (ALL must hold)

- Before assigning any task to faion-sdd-executor-agent — validate context budget fits.
- When decomposing a large design into tasks and unsure whether to split or combine.
- Auditing an existing implementation plan where tasks seem to exceed context window.
- Estimating total project token cost before committing to an implementation approach.

## Skip If (ANY kills it)

- Micro-tasks under 5k tokens — budget calculation overhead is not worth it.
- Reading-only research passes — context budget still applies but failure mode is less severe.
- Attempting to skip the rule for Claude 200k context — focus degrades at high utilization even within window limits.

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
