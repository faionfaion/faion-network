# Event Sourcing — Implementation

## Summary

Implementation-level guide for event sourcing: event store (PostgreSQL), optimistic concurrency via stream versioning, snapshots to bound replay cost, projections that maintain read models, and an EventBus that routes stored events to projection handlers. The core rule: append events with an `expected_version` check; reject if the stream moved — never overwrite.

## Why

Without optimistic concurrency, two concurrent command handlers can each read version N, apply their events, and write, with one silently overwriting the other. The `expected_version` check makes concurrent writes fail fast and forces a retry, preserving aggregate invariants under load. Snapshots prevent unbounded replay time as streams grow (snapshot every 50 events is a common heuristic).

## When To Use

- Implementing event sourcing for a production system (complements event-sourcing-basics)
- Choosing and configuring a persistence backend for the event store
- Adding snapshot support when aggregate replay is measurably slow (&gt; 50 events)
- Wiring projections to keep read models in sync after event append
- Writing integration tests for event replay and aggregate reconstruction

## When NOT To Use

- Proof-of-concept or prototype — use an in-memory event store; skip PostgreSQL and snapshots until performance demands them
- Simple read models that can be rebuilt in seconds — snapshots add write overhead for no gain
- Teams without PostgreSQL expertise — the schema and concurrency logic require understanding of advisory locks and UPSERT semantics

## Content

| File | What's inside |
|------|---------------|
| `content/01-event-store.xml` | Abstract EventStore interface, PostgresEventStore with optimistic concurrency, serialization |
| `content/02-schema.xml` | SQL schema for events table and snapshots table |
| `content/03-snapshots.xml` | SnapshotStore, EventSourcedOrderRepository with snapshot load + save + frequency |
| `content/04-projections.xml` | OrderDetailsProjection handlers, EventBus routing, projection SQL schema |

## Templates

| File | Purpose |
|------|---------|
| `templates/event-store-schema.sql` | Events + snapshots + projections DDL ready to run |
| `templates/postgres-event-store.py` | PostgresEventStore skeleton with append, read_stream, serialize/deserialize |
