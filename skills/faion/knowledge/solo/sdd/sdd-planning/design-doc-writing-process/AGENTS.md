# Design Document Writing Process

## Summary

A 7-phase process for writing design.md: (1) load SDD context and constitution, (2) codebase research to discover existing patterns, (3) build a FR traceability matrix, (4) write ADR-style Architecture Decisions (AD-X), (5) plan file structure with CREATE/MODIFY table, (6) define data models and database schema, (7) write API contracts. The process is sequential by design — skipping Phase 2 or 3 produces designs that conflict with existing code or leave FRs without implementing ADs.

## Why

Codebase research before architecture decisions (Phase 2) is the highest-ROI step: designs written without it introduce naming inconsistencies, duplicate patterns, and API contracts that conflict with existing routes. The traceability matrix (Phase 3) catches gaps before any AD is written, not after. Two-turn structure (Phases 1-3 → human review → Phases 4-7) prevents committing to contracts before the coverage is confirmed.

## When To Use

- After spec.md is approved and before implementation-plan.md is created.
- When the feature touches multiple subsystems and API contracts must be pinned.
- When codebase patterns need to be discovered before architecture decisions are made.
- Generating ADR-style decisions (AD-X) that executor agents will reference during coding.

## When NOT To Use

- Features with no new architecture (CRUD on an existing model) — copy existing AD patterns directly without a full design process.
- Hot-fixes where the solution is already known.
- Before spec.md is approved — design without locked requirements causes rework.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process-phases.xml` | All 7 phases with rules: context loading, codebase research pattern table, traceability matrix format, ADR decision format (Context/Decision/Rationale/Alternatives/Consequences/Traces to), file structure table, data model examples, API contract format. |
| `content/02-checklist.xml` | Phase-by-phase quality checklist for each of the 7 phases, plus final quality review gate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/find-patterns.sh` | Shell script for Phase 2: discovers service, handler, model, and migration patterns across a codebase using ripgrep. |
