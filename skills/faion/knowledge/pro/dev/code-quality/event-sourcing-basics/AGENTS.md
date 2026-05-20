---
slug: event-sourcing-basics
tier: pro
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Event Sourcing persists the state of an aggregate as an ordered, immutable sequence of domain events rather than current state.
content_id: "6ca70e33be98ac41"
tags: [event-sourcing, event-store, events, immutability, audit-trail]
---
# Event Sourcing — Basics

## Summary

**One-sentence:** Event Sourcing persists the state of an aggregate as an ordered, immutable sequence of domain events rather than current state.

**One-paragraph:** Event Sourcing persists the state of an aggregate as an ordered, immutable sequence of domain events rather than current state. The current state is derived by replaying events from the beginning (or from a snapshot). The core rule: once an event is written, it is never modified — it is the source of truth; the in-memory state is a cache. Traditional state-based storage loses the history of what happened and why. Event sourcing provides a complete audit trail for free, enables time-travel debugging (rebuild state at any point in the past), supports projections that rebuild read models from history, and integrates naturally with event-driven architectures because the event log is the message bus.

## Applies If (ALL must hold)

- Complete audit trail is required (financial, healthcare, compliance, legal)
- Complex domain with temporal queries ("what was the state of this order at 3pm yesterday?")
- Event-driven architecture where downstream services need to consume history
- Systems requiring state reconstruction after data corruption or logic bug
- Paired with CQRS to build independent read projections from the event stream

## Skip If (ANY kills it)

- Simple CRUD applications — event sourcing adds infrastructure complexity with no benefit when history is irrelevant
- Strong consistency requirements across aggregates — event replay is inherently eventual
- Team unfamiliar with the pattern — misunderstanding immutability or apply-order causes subtle correctness bugs
- High-frequency writes with tiny payloads (telemetry, metrics) — use a time-series DB instead
- Schema evolution is unplanned — changing an event's fields breaks replay of historical streams

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
