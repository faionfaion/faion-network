---
slug: modular-monolith
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A modular monolith is a single deployable unit with strict module boundaries: each module maps to one bounded context, exposes only a public API, owns its database schema, and never directly imports internals of another module.
content_id: "e42590d3f75c8831"
tags: [modular-monolith, bounded-context, module-boundaries, ddd, strangler-fig]
---
# Modular Monolith

## Summary

**One-sentence:** A modular monolith is a single deployable unit with strict module boundaries: each module maps to one bounded context, exposes only a public API, owns its database schema, and never directly imports internals of another module.

**One-paragraph:** A modular monolith is a single deployable unit with strict module boundaries: each module maps to one bounded context, exposes only a public API, owns its database schema, and never directly imports internals of another module. Boundary enforcement is mandatory via static analysis (import-linter, ArchUnit, depguard) wired into CI — without it, boundaries decay within weeks.

## Applies If (ALL must hold)

- New project: team size <= 10, business model not fully validated
- Refactoring a "big ball of mud" monolith — module boundaries first, extraction later
- Needing DDD bounded contexts without distributed-systems complexity
- Planning future microservices extraction (modular monolith is the required prior step)
- Establishing schema-per-module isolation on a shared PostgreSQL instance
- Adding import-boundary linting as a CI gate to an existing codebase

## Skip If (ANY kills it)

- Independent scaling per module is already needed (traffic profiles differ by 10x+) — use microservices
- Multiple teams (10+) with independent release cadences requiring autonomous deploys
- Polyglot tech stacks required per domain (different languages/runtimes)
- Regulatory or fault-isolation requirements demand hard process separation
- Throwaway prototype where module ceremony adds no value
- Existing monolith already has clean package structure and passing tests — don't add ceremony

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

- parent skill: `solo/dev/software-architect/`
