---
slug: ddd-aggregates
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An Aggregate is a cluster of domain objects (Entities + Value Objects) treated as a single unit for data changes.
content_id: "6f7f0aa308665927"
tags: [ddd, aggregate, domain-model, invariants, rich-domain]
---
# DDD Aggregates: Invariant-Enforcing Cluster Roots

## Summary

**One-sentence:** An Aggregate is a cluster of domain objects (Entities + Value Objects) treated as a single unit for data changes.

**One-paragraph:** An Aggregate is a cluster of domain objects (Entities + Value Objects) treated as a single unit for data changes. One Entity is designated the Aggregate Root: all external access goes through the root, and all business invariants are enforced inside the root's methods. No public setters; use intention-revealing command methods (order.place(), order.cancel()) that validate state before mutating it.

## Applies If (ALL must hold)

- Any domain object with lifecycle state and business invariants (Order, Subscription, Account, Booking).
- When multiple entities must change together atomically (Order + its OrderLines).
- When you need to record that something happened (Domain Events) as part of a state transition.
- Complex domains with multiple teams: the Aggregate root is the API contract for the cluster.

## Skip If (ANY kills it)

- Pure CRUD entities with no invariants — a plain ORM model with getters/setters is simpler and faster.
- Read-only projections or query models — Aggregates are for the write side; read models use flat DTOs.
- ETL / batch transforms where there is no transactional domain logic.

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
