---
slug: design-doc-writing-process
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A 7-phase process for writing design.
content_id: "1ea7ea2d51df604c"
tags: [design-process, architecture-decisions, specification-driven-development, workflow, sdd]
---
# Design Document Writing Process

## Summary

**One-sentence:** A 7-phase process for writing design.

**One-paragraph:** A 7-phase process for writing design.md: (1) load SDD context and constitution, (2) codebase research to discover existing patterns, (3) build a FR traceability matrix, (4) write ADR-style Architecture Decisions (AD-X), (5) plan file structure with CREATE/MODIFY table, (6) define data models and database schema, (7) write API contracts. The process is sequential by design — skipping Phase 2 or 3 produces designs that conflict with existing code or leave FRs without implementing ADs.

## Applies If (ALL must hold)

- After spec.md is approved and before implementation-plan.md is created.
- When the feature touches multiple subsystems and API contracts must be pinned.
- When codebase patterns need to be discovered before architecture decisions are made.
- Generating ADR-style decisions (AD-X) that executor agents will reference during coding.

## Skip If (ANY kills it)

- Features with no new architecture (CRUD on an existing model) — copy existing AD patterns directly without a full design process.
- Hot-fixes where the solution is already known.
- Before spec.md is approved — design without locked requirements causes rework.

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
