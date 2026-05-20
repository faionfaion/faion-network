---
slug: template-task
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A fill-in-the-blanks template for TASK_NNN.
content_id: "87db75e2aa155d71"
tags: [sdd, task, template, execution]
---
# Template: Task File

## Summary

**One-sentence:** A fill-in-the-blanks template for TASK_NNN.

**One-paragraph:** A fill-in-the-blanks template for TASK_NNN.md files — the atomic execution units that a subagent reads and implements. Each task file includes SDD References, Task Dependency Tree, Requirements Coverage (FR-X / AD-X inline), Objective, Dependencies, Acceptance Criteria (Given-When-Then), Technical Approach (numbered steps), Files (CREATE/MODIFY), Estimated Tokens, and sections for execution output.

## Applies If (ALL must hold)

- Generating TASK_*.md files from an approved implementation plan.
- Converting implementation plan row stubs into standalone, self-contained task files.
- Ensuring the executing agent has all required context within a single file.
- Verifying completed tasks before marking them done — template defines the done state.

## Skip If (ANY kills it)

- Before the implementation plan is approved — task scope will change and the file is wasted effort.
- For research spikes where the deliverable is a decision, not code — use a lighter note format.
- When a task takes fewer than 5k tokens to execute — overhead of full template is not worth it.
- For manual human execution — human tasks need narrative description, not Given-When-Then AC.

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
