---
slug: ddd-repositories
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A Repository provides a collection-like interface for accessing Aggregates.
content_id: "4cb7540e6f02e51e"
tags: [ddd, repository, persistence, aggregate, infrastructure]
---
# DDD Repository Pattern: Domain-Owned Persistence Interfaces

## Summary

**One-sentence:** A Repository provides a collection-like interface for accessing Aggregates.

**One-paragraph:** A Repository provides a collection-like interface for accessing Aggregates. The domain layer defines the interface (abstract class with find_by_id, save, delete); the infrastructure layer provides the ORM implementation. The domain never imports ORM types. The Repository returns fully reconstituted Aggregates — never raw ORM models — and is responsible for translating between domain objects and persistence models.

## Applies If (ALL must hold)

- Any Aggregate that must be persisted and reloaded across requests or transactions.
- When you want to unit-test domain logic without a running database.
- When the domain layer must remain ORM-agnostic (to support multiple backends or future migrations).
- Systems where the query side and write side diverge: Repository handles write-side Aggregate loading; a separate Read Model handles query-side projections.

## Skip If (ANY kills it)

- Simple CRUD apps where the ORM model IS the domain model — a thin Active Record is faster and produces no value in return for the indirection.
- Read-side projections and reporting queries — those go in a Query Service or Read Model, not a Repository.
- Throwaway scripts or ETL pipelines where ORM is used directly and domain concepts do not apply.

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

- parent skill: `pro/dev/software-developer/`
