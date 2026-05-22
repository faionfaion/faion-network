---
slug: arch-pattern-ddd
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Eric Evans (2003) defined DDD as a way to tackle complexity in the heart of software by building a shared model between developers and domain experts.
content_id: "d1bb1cd70cdc6255"
tags: [ddd, bounded-context, aggregate, domain-events, ubiquitous-language]
---
# Domain-Driven Design (DDD)

## Summary

**One-sentence:** Eric Evans (2003) defined DDD as a way to tackle complexity in the heart of software by building a shared model between developers and domain experts.

**One-paragraph:** Eric Evans (2003) defined DDD as a way to tackle complexity in the heart of software by building a shared model between developers and domain experts. Strategic DDD identifies bounded contexts, subdomains, and context maps. Tactical DDD provides building blocks: Entities, Value Objects, Aggregates, Domain Events, Repositories, Domain Services, and Factories.

## Applies If (ALL must hold)

- Complex domains with intricate, non-obvious business rules that require close collaboration with domain experts.
- Systems with multiple clearly identifiable bounded contexts where the same concept (e.g., "Customer") means different things in different parts of the domain.
- Large-scale applications where consistency boundaries (aggregate invariants) are critical and transaction scope must be explicit.
- Microservices systems where bounded context boundaries map naturally to service boundaries.
- Teams with access to domain experts willing to develop and maintain a ubiquitous language.

## Skip If (ANY kills it)

- Simple CRUD domains with no real business rules — Entities, Aggregates, and Repositories are overhead with nothing to protect.
- Teams without access to domain experts — DDD requires collaborative domain modeling; without it, you get well-named but shallow domains.
- Prototypes where the domain is still being discovered — stabilise the model first, then apply DDD structure.
- Time-pressured MVPs — the investment in ubiquitous language and context mapping pays off over months, not days.

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
