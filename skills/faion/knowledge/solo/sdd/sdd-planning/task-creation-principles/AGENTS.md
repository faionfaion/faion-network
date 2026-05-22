---
slug: task-creation-principles
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Principles for decomposing an approved design into bounded, executor-ready TASK_*.
content_id: "fc74a8ef934f8a60"
tags: [sdd, task-creation, implementation, invest, decomposition]
---
# Task Creation Principles

## Summary

**One-sentence:** Principles for decomposing an approved design into bounded, executor-ready TASK_*.

**One-paragraph:** Principles for decomposing an approved design into bounded, executor-ready TASK_*.md files. Applies the INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable), SMART task goals, WBS 8-80 rule adapted to token budgets (hard cap: 100k tokens per task), Given-When-Then acceptance criteria, and full FR-X/AD-X traceability links inside each task file.

## Applies If (ALL must hold)

- Converting an approved design document into executable TASK_*.md files
- Splitting large undefined work into bounded units before assigning to a subagent
- Auditing an existing implementation plan where tasks are vague or oversized
- When faion-sdd-executor-agent will run unattended and needs unambiguous inputs

## Skip If (ANY kills it)

- Prototyping or exploratory spikes — INVEST/SMART overhead is not worth it
- Single-file hot-fixes with obvious scope — task structure adds ceremony with no return
- Early brainstorming phases before a spec exists (no FR-X to trace to yet)

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
