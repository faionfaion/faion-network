---
slug: language-framework-guide
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A tier-0 decision router for stack selection.
content_id: "dbbfc8d00bed04e4"
tags: [stack-selection, language-choice, framework-selection, adr, tooling]
---
# Language and Framework Selection Guide

## Summary

**One-sentence:** A tier-0 decision router for stack selection.

**One-paragraph:** A tier-0 decision router for stack selection. Given a project brief, map the task type to the canonical language (Python, TypeScript, Go, Rust) and framework (Django, FastAPI, React, Next.js). Provide format/lint/test commands per language. Output recommendations with two alternatives and an ADR stub — never just a stack name.

## Applies If (ALL must hold)

- Day-zero greenfield: agent must propose a stack for a project brief.
- A spec says "use the right tool" — this is the canonical default mapping.
- Generating boilerplate format/lint/test commands for CI scaffolding.
- Sanity-check: is the chosen language/framework a mismatch for the stated requirements?

## Skip If (ANY kills it)

- Team has an existing stack mandate — don't override without an ADR.
- Domains with non-obvious constraints (regulatory, hardware, cloud lock-in) — use a richer ADR flow.
- Picking between equally valid options for a short experiment — decision overhead exceeds value.
- ML/embedded/blockchain/games — table is not authoritative outside web/API scope.

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

- parent skill: `free/dev/software-developer/`
