---
slug: writing-specifications
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A specification answers WHAT to build and WHY.
content_id: "4a0eca19120a99d7"
tags: [specification, requirements, acceptance-criteria, llm-execution]
---
# Writing Specifications

## Summary

**One-sentence:** A specification answers WHAT to build and WHY.

**One-paragraph:** A specification answers WHAT to build and WHY. It functions as the anti-hallucination anchor for LLM execution agents: every FR-X must be a SHALL statement meeting SMART criteria, and every acceptance criterion must use concrete values in Given-When-Then format. The spec is not considered complete until a second, fresh-context agent outputs "SPEC APPROVED" after running the AC coverage checklist (happy path, error handling, boundary conditions, security, performance, accessibility).

## Applies If (ALL must hold)

- Before any LLM-assisted implementation: the spec is the primary context document
- When requirements come as vague requests — transform them into structured FR-X + AC-X artifacts
- Writing CLAUDE.md or project rules using the three-tier boundary system (Always / Ask First / Never)
- Any feature affecting multiple files, teams, or external APIs

## Skip If (ANY kills it)

- Bug fix with a known root cause and clear fix — write the fix, not a spec
- Configuration-only change — no functional requirements to specify
- One-off script or throwaway prototype — overhead exceeds value
- When requirements are so volatile they will change before implementation starts

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
