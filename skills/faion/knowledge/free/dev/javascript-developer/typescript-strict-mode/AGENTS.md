---
slug: typescript-strict-mode
tier: free
group: dev
domain: javascript-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Full strict-mode configuration with additional safety checks, null safety patterns, type narrowing, branded types, and const assertions for catching whole classes of bugs at compile time.
content_id: "12394fa50d7d784d"
tags: [typescript, strict-mode, configuration]
---
# TypeScript Strict Mode

## Summary

**One-sentence:** Full strict-mode configuration with additional safety checks, null safety patterns, type narrowing, branded types, and const assertions for catching whole classes of bugs at compile time.

**One-paragraph:** Full strict-mode configuration with additional safety checks, null safety patterns, type narrowing, branded types, and const assertions for catching whole classes of bugs at compile time.

## Applies If (ALL must hold)

- All new TypeScript projects from day one
- JavaScript-to-TypeScript migration (enable flags incrementally)
- Library development where consumers depend on correct types
- Production applications requiring high reliability

## Skip If (ANY kills it)

- Auto-generated code (e.g., protobuf output) — add // @ts-nocheck per file instead
- Legacy codebases where enabling strict causes thousands of errors before a remediation plan exists — enable flags one at a time

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
