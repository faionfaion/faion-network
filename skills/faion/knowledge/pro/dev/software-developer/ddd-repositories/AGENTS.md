---
slug: ddd-repositories
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: DDD Repository pattern — domain owns the interface (no ORM types); infra implements; returns reconstituted aggregates; queries by identity only.
content_id: "207b6709f6301590"
complexity: medium
produces: code
est_tokens: 4200
tags: [ddd, repository, persistence, aggregate, infrastructure]
---
# DDD Repository Pattern: Domain-Owned Persistence Interfaces

## Summary

**One-sentence:** DDD Repository pattern — domain owns the interface (no ORM types); infra implements; returns reconstituted aggregates; queries by identity only.

**One-paragraph:** A Repository provides a collection-like interface for accessing Aggregates. The Domain layer defines the interface (`find_by_id`, `save`, `delete`); the Infrastructure layer implements it against the ORM. The domain MUST never import SQLAlchemy / EF / JPA types; the repository returns fully reconstituted aggregate objects, never raw ORM models. Collection queries by arbitrary criteria belong in Read Models / Query Services, not in the repository. This methodology pins five rules: domain owns the interface, return aggregates not ORM models, identity-only queries, infra translates persistence ↔ domain, ports + adapters. Output: a repository interface + implementation + mapper conforming to `02-output-contract.xml`.

**Ефективно для:**

- Persisting aggregate roots cleanly without ORM coupling in domain code.
- Replacing the ORM in the future (SQLAlchemy → Django ORM → EF) without domain rewrites.
- Testing domain logic without spinning up a DB (mock the repository).
- Multi-store systems where one aggregate lives in DB + Redis + S3.
- Cross-language DDD reference architecture.

## Applies If (ALL must hold)

- Domain logic exists separately from persistence code.
- The team commits to keeping ORM imports out of the domain.
- Aggregates per `[[ddd-aggregates]]` are the persistence unit.
- The application needs `find_by_id` + `save` more often than arbitrary queries.

## Skip If (ANY kills it)

- CRUD-only project — Active Record on the model is enough.
- Reporting service with mostly arbitrary queries — use Query Services / projections.
- Single-file script — overhead exceeds benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Aggregate root + value objects | source | repo |
| ORM model (existing) | source | repo |
| DB connection / session | config | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ddd-aggregates]] | Repository persists aggregates as a unit. |
| [[ddd-value-objects]] | Value objects need (de)serialization across the persistence boundary. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: domain-owns-interface, return-aggregates, identity-only-queries, infra-translates, ports-and-adapters | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for repository spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: orm-types-in-domain, arbitrary-query-method, lazy-load-leak, fat-repository | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on aggregate write-pattern → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-interface` | sonnet | Vocabulary + boundary judgment. |
| `write-implementation` | sonnet | ORM mapping scaffolding. |
| `write-domain-mock` | haiku | Mechanical in-memory stub for tests. |

## Templates

| File | Purpose |
|------|---------|
| `templates/RepositoryInterface.py` | Domain-layer interface skeleton |
| `templates/SqlAlchemyRepository.py` | Infra implementation + mapper |
| `templates/InMemoryRepository.py` | Test double for domain tests |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ddd-repositories.py` | Validate repository spec against schema | Pre-commit on spec artefact |

## Related

- [[ddd-aggregates]]
- [[ddd-value-objects]]
- [[ddd-anti-corruption-layer]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (query shape, aggregate count, ORM dependency cost) to a rule from `01-core-rules.xml`. Use it whenever adding a new repository or refactoring a method that currently returns `IQueryable`/`QuerySet`.
