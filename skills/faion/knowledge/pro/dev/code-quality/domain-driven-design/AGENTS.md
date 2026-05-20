---
slug: domain-driven-design
tier: pro
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Domain-Driven Design (DDD) is a software development approach that models complex business domains through a shared ubiquitous language, explicit bounded contexts, and rich domain objects (entities, value objects, aggregates) that enforce business invariants.
content_id: "bee2d7d111e00161"
tags: [ddd, domain, architecture, modeling, ubiquitous-language]
---
# Domain-Driven Design

## Summary

**One-sentence:** Domain-Driven Design (DDD) is a software development approach that models complex business domains through a shared ubiquitous language, explicit bounded contexts, and rich domain objects (entities, value objects, aggregates) that enforce business invariants.

**One-paragraph:** Domain-Driven Design (DDD) is a software development approach that models complex business domains through a shared ubiquitous language, explicit bounded contexts, and rich domain objects (entities, value objects, aggregates) that enforce business invariants. The core rule: domain logic lives inside the model, not in services — an Order that cannot be placed when empty is safer than a service that checks emptiness before calling order.place(). Without DDD, business rules scatter across controllers, services, and database queries, creating the anemic domain model antipattern where the same invariant is enforced in multiple places and breaks silently when one copy is missed.

## Applies If (ALL must hold)

- Complex business domain where rules will keep changing (orders, billing, inventory, claims, pricing)
- Splitting a monolith — DDD bounded contexts define service boundaries before you draw service lines
- Refactoring an anemic codebase where logic has leaked into controllers/services
- A team includes a domain expert who can sit in modeling sessions
- Multiple teams share a codebase and need explicit context maps to negotiate ownership

## Skip If (ANY kills it)

- CRUD admin tools, reporting dashboards, or scrapers — the "domain" is just data; DDD adds ceremony with no payoff
- Solo prototype or MVP under ~2k LOC where requirements still flip weekly
- Hot data-pipeline / ETL code — the model is rows and transformations, not aggregates with invariants
- Real-time / latency-critical paths where repository hydration and event dispatch cost is not justified
- Team has no access to a domain expert — you will produce a developer-invented model the business does not recognize

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

- parent skill: `pro/dev/code-quality/`
