---
slug: creational-patterns
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Object creation mechanisms that increase flexibility and reuse.
content_id: "36b47157b368ac6a"
tags: [design-patterns, creational, factory, builder, dependency-injection, object-pool, prototype, singleton]
---
# Creational Design Patterns

## Summary

**One-sentence:** Object creation mechanisms that increase flexibility and reuse.

**One-paragraph:** Object creation mechanisms that increase flexibility and reuse. Factory Method for runtime type selection, Builder for complex multi-step construction, Dependency Injection for loose coupling, Object Pool for expensive resource reuse, Prototype for cloning, Abstract Factory for product families, Singleton for process-global resources (use sparingly).

## Applies If (ALL must hold)

- Writing object-creation code where the concrete type is decided at runtime (e.g. payment provider by country, storage backend by config).
- Constructor has 4+ parameters or many optional params — Builder beats telescoping constructors.
- Refactoring code with duplicated `new X(...)` chains spread across modules — centralize via Factory.
- Reviewing legacy code for Singleton overuse and proposing DI migrations.
- Writing test fixtures and mocks — DI and Factory Method dramatically reduce test scaffolding.
- Working with expensive-to-create resources (DB connections, HTTP clients, threads) — Object Pool.

## Skip If (ANY kills it)

- Trivial constructors with 1-3 params — `dataclass` / record / struct is enough.
- Cross-cutting infra concerns where DI containers already exist (FastAPI Depends, NestJS providers, Spring beans).
- One-off scripts where pattern overhead exceeds the value.
- High-performance hot paths where DI lookup cost matters (resolve once, hold reference).
- Singleton for anything that holds mutable state, has dependencies, or differs between tests.

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
