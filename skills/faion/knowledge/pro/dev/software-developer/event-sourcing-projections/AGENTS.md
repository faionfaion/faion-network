---
slug: event-sourcing-projections
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Projections listen to event streams and maintain specialized read models by applying events as idempotent UPSERTs keyed by (stream_id, position).
content_id: "ed71360f86a81f65"
tags: [event-sourcing, projections, read-models, cqrs, idempotency]
---
# Event Sourcing — Projections and Read Models

## Summary

**One-sentence:** Projections listen to event streams and maintain specialized read models by applying events as idempotent UPSERTs keyed by (stream_id, position).

**One-paragraph:** Projections listen to event streams and maintain specialized read models by applying events as idempotent UPSERTs keyed by (stream_id, position). Projections are passive — they never execute business logic, never emit domain events, and are always fully rebuildable from event offset 0.

## Applies If (ALL must hold)

- Any query that cannot be answered by loading a single aggregate — list views, cross-entity joins, analytics.
- Read-heavy surfaces where replay latency would be too slow for direct event-store queries.
- CQRS systems with multiple consumer shapes (mobile API, admin panel, reporting) each needing a different read model.
- Downstream consumers (search index, ML feature store, notification service) that need to react to business events.

## Skip If (ANY kills it)

- Business logic execution — projections are passive UPSERTs; put logic in command handlers or sagas.
- Real-time read-your-writes without a separate strategy — projection lag means a user who just placed an order may not see it in their order list immediately.

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
