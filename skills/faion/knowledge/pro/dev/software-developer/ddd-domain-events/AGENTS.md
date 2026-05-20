---
slug: ddd-domain-events
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A Domain Event records that something significant happened in the domain: OrderPlaced, SubscriptionRenewed, InvoiceIssued.
content_id: "8145839ea28bb1f2"
tags: [ddd, domain-events, outbox-pattern, eventual-consistency, aggregate]
---
# DDD Domain Events: Raising, Collecting, and Dispatching

## Summary

**One-sentence:** A Domain Event records that something significant happened in the domain: OrderPlaced, SubscriptionRenewed, InvoiceIssued.

**One-paragraph:** A Domain Event records that something significant happened in the domain: OrderPlaced, SubscriptionRenewed, InvoiceIssued. Events are raised inside Aggregate command methods and appended to an internal _events list. The application layer collects events after the DB transaction commits and dispatches them to handlers. Pair with the Outbox pattern to ensure events are never lost when the process crashes between DB commit and event publish.

## Applies If (ALL must hold)

- Any state transition that triggers downstream reactions in other Bounded Contexts (order placed → billing, shipping, notifications).
- Any cross-Aggregate side effect that must be decoupled from the primary transaction.
- Audit trails: Domain Events are the natural record of what happened and when.
- Event Sourcing: the event log IS the state; Aggregates are reconstituted by replaying events.

## Skip If (ANY kills it)

- Simple intra-Aggregate reactions that can be handled in the same method — no need to raise an event if only the Aggregate itself reacts.
- Synchronous request/response flows where the caller needs the result of the downstream reaction immediately — use a direct call or query, not an event.
- Low-stakes CRUD operations with no downstream effects — event overhead is not justified.

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
