---
slug: design-doc-structure
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A design document answers "HOW are we building this?" — it bridges spec (what) and code (impl).
content_id: "78076e216ebb4b87"
tags: [design-document, architecture, traceability, specification, sdd]
---
# Design Document Structure

## Summary

**One-sentence:** A design document answers "HOW are we building this?" — it bridges spec (what) and code (impl).

**One-paragraph:** A design document answers "HOW are we building this?" — it bridges spec (what) and code (impl). The canonical structure is: reference docs, overview, FR/AD traceability matrix, architectural decisions (AD-X) with alternatives and consequences, file change table (CREATE/MODIFY), data models, API contracts, security, performance, testing strategy, and migration plan. Every file change must trace to an FR and an AD.

## Applies If (ALL must hold)

- After `spec.md` is approved and before writing the implementation plan
- Feature has non-trivial architectural decisions: schema, API contracts, auth, caching
- Code will be written by an agent executor — design.md is the authoritative file-creation instruction
- Feature spans multiple files or services requiring explicit data flow definition
- Security or performance concern exists — these sections create explicit review targets

## Skip If (ANY kills it)

- Single-file, single-concern changes with no architectural decisions (waste)
- `spec.md` is still Draft — design decisions cannot be made until requirements are stable
- Internal refactors with no API/schema changes — write an ADR instead
- Spike/research tasks: output is an ADR or updated spec, not a design doc

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
