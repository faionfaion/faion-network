---
slug: dev-methodologies-architecture
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for backend architecture covering database schema design, ORM query optimization, caching, background jobs, API response shapes, authentication, and structured logging.
content_id: "a243f4eef28f1591"
tags: [architecture, database, api, performance, observability]
---
# Dev Methodologies — Architecture

## Summary

**One-sentence:** Patterns for backend architecture covering database schema design, ORM query optimization, caching, background jobs, API response shapes, authentication, and structured logging.

**One-paragraph:** Patterns for backend architecture covering database schema design, ORM query optimization, caching, background jobs, API response shapes, authentication, and structured logging. Apply patterns incrementally — commit and test after each one.

## Applies If (ALL must hold)

- Drafting backend architecture for a new service: choosing DB schema layout, ORM access patterns, cache strategy, queue/worker split, auth model.
- Reviewing an existing service for N+1 queries, missing indexes, blocking I/O, ad-hoc auth, or unstructured logging.
- Generating migration scripts (Alembic / Django / knex) and verifying they are backward compatible (expand-then-contract for CD).
- Standardizing API response envelopes across a polyglot codebase.

## Skip If (ANY kills it)

- Frontend / UI architecture — this set is backend-only (DB, API, cache, queue, observability).
- Greenfield prototyping where the cost of patterns exceeds the value (one-off scripts, throwaway demos).
- Replacement for a real DBA on high-stakes schema design (sharding, multi-region, ACID-vs-BASE trade-offs).
- When the hosting platform already prescribes patterns (e.g. Supabase, Firebase) — defer to platform conventions.

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

- parent skill: `solo/dev/automation-tooling/`
