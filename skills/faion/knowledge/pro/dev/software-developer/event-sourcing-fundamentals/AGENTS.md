---
slug: event-sourcing-fundamentals
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Event Sourcing persists the state of an entity as a sequence of state-changing events.
content_id: "e623d220b6ed6a5a"
tags: [event-sourcing, domain-events, immutability, audit-trail, cqrs]
---
# Event Sourcing — Fundamentals

## Summary

**One-sentence:** Event Sourcing persists the state of an entity as a sequence of state-changing events.

**One-paragraph:** Event Sourcing persists the state of an entity as a sequence of state-changing events. Instead of storing current state, you store all events that led to it. The current state is derived by replaying events.

## Applies If (ALL must hold)

- Complete audit trail required — banking, ledger, healthcare records, compliance-heavy SaaS.
- Aggregates where temporal queries are needed: "what was the state on date X", "who changed Y when".
- Systems where business rules evolve and you need to replay history through new logic (recompute royalties, retry failed reconciliations).
- Front-end of a CQRS system with multiple read models that must stay in sync from one truth — events are that truth.
- Domain-event-driven microservices where downstream consumers (search, analytics, ML feature store) subscribe to a published event log.
- Workflows requiring undo / what-if analysis (engineering simulators, financial projections).
- Complex domain with temporal queries and event-driven architectures.

## Skip If (ANY kills it)

- CRUD-shaped data with no audit need — events double the storage and triple the complexity for no payoff.
- Reporting-first products where the dominant access pattern is aggregate analytics — keep a relational warehouse, not an event store.
- Strong real-time consistency UX (banking transfer that must instantly show the new balance to the same user) without a careful read-your-writes strategy.
- Tiny solo apps and pre-PMF MVPs — the event/projection plumbing dwarfs the feature.
- Teams without DDD experience — without aggregate boundaries, the event log degenerates into a CDC log of CRUD updates.
- Domains where regulatory rules require destruction (GDPR right to erasure) and crypto-shredding is not acceptable.

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
