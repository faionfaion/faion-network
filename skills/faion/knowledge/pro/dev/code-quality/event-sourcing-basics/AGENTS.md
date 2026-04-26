# Event Sourcing — Basics

## Summary

Event Sourcing persists the state of an aggregate as an ordered, immutable sequence of domain events rather than current state. The current state is derived by replaying events from the beginning (or from a snapshot). The core rule: once an event is written, it is never modified — it is the source of truth; the in-memory state is a cache.

## Why

Traditional state-based storage loses the history of what happened and why. Event sourcing provides a complete audit trail for free, enables time-travel debugging (rebuild state at any point in the past), supports projections that rebuild read models from history, and integrates naturally with event-driven architectures because the event log is the message bus.

## When To Use

- Complete audit trail is required (financial, healthcare, compliance, legal)
- Complex domain with temporal queries ("what was the state of this order at 3pm yesterday?")
- Event-driven architecture where downstream services need to consume history
- Systems requiring state reconstruction after data corruption or logic bug
- Paired with CQRS to build independent read projections from the event stream

## When NOT To Use

- Simple CRUD applications — event sourcing adds infrastructure complexity with no benefit when history is irrelevant
- Strong consistency requirements across aggregates — event replay is inherently eventual
- Team unfamiliar with the pattern — misunderstanding immutability or apply-order causes subtle correctness bugs
- High-frequency writes with tiny payloads (telemetry, metrics) — use a time-series DB instead
- Schema evolution is unplanned — changing an event's fields breaks replay of historical streams

## Content

| File | What's inside |
|------|---------------|
| `content/01-event-definitions.xml` | Base Event dataclass, order event hierarchy (OrderCreated through OrderCancelled) |
| `content/02-event-sourced-aggregate.xml` | Order aggregate with `_apply` dispatch, `create` factory, `from_events` reconstruct, pending events |
| `content/03-antipatterns.xml` | Mutable events, large catch-all events — bad/good examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/base-event.py` | Frozen Event dataclass + example domain event skeleton |
| `templates/aggregate-base.py` | Event-sourced aggregate base with `_apply`, version tracking, pending events |
