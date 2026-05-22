---
slug: typescript-patterns
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Advanced type patterns including utility types, generics, type guards, discriminated unions, and Zod schema validation for expressing domain constraints in the type system and catching errors at compile time.
content_id: "a7d887fc47dc3e23"
tags: [typescript, types, validation]
---
# TypeScript Patterns

## Summary

**One-sentence:** Advanced type patterns including utility types, generics, type guards, discriminated unions, and Zod schema validation for expressing domain constraints in the type system and catching errors at compile time.

**One-paragraph:** Advanced type patterns including utility types, generics, type guards, discriminated unions, and Zod schema validation for expressing domain constraints in the type system and catching errors at compile time.

## Applies If (ALL must hold)

- Defining repository interfaces with generic CRUD contracts
- Handling API responses where success and error shapes differ
- Validating unknown external input (API bodies, env vars, form data)
- Building reusable generic components or data structures
- Needing exhaustive checks on a union type

## Skip If (ANY kills it)

- Simple scripts or one-off tools — strict generics add noise without benefit
- Prototyping where types would be reworked immediately anyway
- When a plain interface suffices — avoid generics unless the type parameter is actually reused

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

- parent skill: `free/dev/javascript-developer/`
