---
slug: task-creation-parallelization
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Decompose an approved `design.
content_id: "1d0f913fdc2448e5"
tags: [task-decomposition, parallelization, wave-execution, invest-criteria, context-budget]
---
# Task Creation & Parallelization

## Summary

**One-sentence:** Decompose an approved `design.

**One-paragraph:** Decompose an approved `design.md` into LLM-executable `TASK-XXX-*.md` files, each bounded by the 100k token rule, then organize them into dependency waves for parallel execution. Each task must satisfy INVEST criteria: Independent within its wave, Negotiable on impl details, Valuable (traces to FR-X), Estimable (token budget), Small (single context window), Testable (Given-When-Then AC).

## Applies If (ALL must hold)

- Decomposing an approved `design.md` before execution begins
- Planning wave-based parallel execution across multiple agents or worktrees
- Checking that each task fits the 100k token context budget
- Propagating patterns from early waves into later-wave task context
- Managing strict finish-to-start dependencies (a task needing output from two others waits for both)

## Skip If (ANY kills it)

- Feature is a single-task implementation (less than 30k tokens) — one task, no waves needed
- `design.md` is not yet approved — do not decompose while spec is still changing
- Tasks are unknown until runtime (data-driven pipelines) — decomposition cannot be done upfront
- Experimental/spike work where implementation approach is undefined — discover first, decompose after

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
