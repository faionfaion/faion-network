---
slug: arch-pattern-clean
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Dependencies point inward through concentric circles: Domain (Entities) at the center, then Application (Use Cases), then Interface Adapters, then Frameworks and Drivers at the outside.
content_id: "37932c40b6da0f2d"
tags: [clean-architecture, domain-driven, dependency-inversion, layered-architecture, testability]
---
# Clean Architecture (Uncle Bob)

## Summary

**One-sentence:** Dependencies point inward through concentric circles: Domain (Entities) at the center, then Application (Use Cases), then Interface Adapters, then Frameworks and Drivers at the outside.

**One-paragraph:** Dependencies point inward through concentric circles: Domain (Entities) at the center, then Application (Use Cases), then Interface Adapters, then Frameworks and Drivers at the outside. Inner circles know nothing about outer circles.

## Applies If (ALL must hold)

- Domains with non-trivial business rules where leaking persistence or UI concerns into core logic will create technical debt within a year.
- Projects that must support multiple UI surfaces (REST API + CLI + background workers) sharing the same business logic.
- Long-lived applications where the framework or database is expected to change at least once during the product lifetime.
- Teams that need comprehensive unit-test coverage of business logic without spinning up infrastructure.
- Systems with heavy regulatory or audit requirements where invariants and policies must be clearly locatable.

## Skip If (ANY kills it)

- CRUD-only admin tools or internal scripts — the domain layer will be empty and layering adds overhead without benefit.
- Prototypes or MVPs where V1 is intentionally throwaway — premature layering slows delivery.
- Microservices where the entire domain fits in 200 lines — apply the pattern at the system boundary instead.
- Languages or runtimes where dependency-injection cost is prohibitive (Python or JS without DI containers can simulate it, but the boilerplate is real).

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
