---
slug: cqrs-pattern
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Command Query Responsibility Segregation (CQRS) separates read and write operations into different models.
content_id: "ba7dfdc2a5642e86"
tags: [cqrs, event-sourcing, architecture-pattern, read-model, event-driven]
---
# CQRS Pattern

## Summary

**One-sentence:** Command Query Responsibility Segregation (CQRS) separates read and write operations into different models.

**One-paragraph:** Command Query Responsibility Segregation (CQRS) separates read and write operations into different models. Commands change state and return void or an ID. Queries return data but never modify state. This pattern enables optimization of each side independently and integrates naturally with event sourcing.

## Applies If (ALL must hold)

- High read/write ratio with different optimization needs (e.g., 100 reads per write).
- Complex domain logic with simple queries (separation of concerns).
- Systems requiring audit trails or full history (event sourcing natural fit).
- Applications with eventual consistency requirements where lag is acceptable.
- Microservices with event-driven architecture and multiple subscribers.
- Real-time analytics where read models are constantly updated from domain events.
- Read-heavy domains where the read query shape diverges from the aggregate (dashboards, search, analytics) and JOINs in the write model are out of control.
- Front-end of an event-sourced system: queries hit projections, commands append events. CQRS plus ES is the canonical pairing.
- Hard audit and regulatory domains (finance, healthcare, supply chain) where every state transition must be a named, immutable command.
- Multi-tenant SaaS where read replicas and per-tenant denormalized caches must scale independently of the write path.
- Business behaviors (`PlaceOrder`, `ApproveLoan`, `CancelSubscription`) getting buried in REST handlers. Step up from CRUD as the domain matures.
- Microservices publishing domain events with polyglot read stores (Postgres write, Elasticsearch/Redis/OpenSearch read).

## Skip If (ANY kills it)

- Simple CRUD applications with uniform read/write patterns and no complex logic.
- Systems requiring strong immediate consistency where read-after-write must be consistent.
- Teams unfamiliar with eventual consistency or event-driven architecture (adds complexity).
- Applications where the cost of maintaining multiple models exceeds the performance benefit.
- Real-time systems where the lag between write and read model update is unacceptable.
- Simple CRUD apps with less than 10 entities and roughly symmetric read/write loads. CQRS doubles surface area for zero benefit.
- Strong-consistency UX where the user must see their own write immediately and projections can't be synchronous (most line-of-business forms with redirect-to-detail).
- Early-stage MVP or pre-product-market-fit. The cost of write and read schemas, projections, and a bus is paid up-front but the domain isn't stable enough to justify it.
- Teams without DDD or event-driven experience. CQRS without aggregate boundaries degrades into "two layers of DTOs" with no payoff.
- Real-time collaborative editing where last-writer-wins on a single mutable document is the right model (CRDT, OT—not CQRS).
- Tiny solo projects. The mediator/bus/projection plumbing is more code than the feature.

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
