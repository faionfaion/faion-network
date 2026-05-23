# Event Sourcing — Implementation

## Summary

**One-sentence:** Produces a production event-sourced backend: PostgreSQL event store with optimistic concurrency on stream version, snapshots to bound replay cost, and an EventBus routing stored events to projection handlers.

**One-paragraph:** Production implementation of event sourcing: append events with an expected_version check (reject if the stream moved — never overwrite), snapshot aggregate state when replay > N events, and dispatch stored events through an EventBus to projection handlers that maintain read models. Schema uses an append-only events table plus a snapshots table keyed by (aggregate_id, version).

**Ефективно для:**

- Production ES backend (Postgres event store, snapshots, projections).
- Optimistic concurrency на stream version — append safety.
- Snapshots коли replay > 50 events.
- Projections як read models для CQRS read side.

## Applies If (ALL must hold)

- Implementing event sourcing for a production system (complements event-sourcing-basics).
- Choosing and configuring persistence backend for the event store.
- Adding snapshot support when replay is measurably slow (> 50 events).
- Wiring projections to keep read models in sync after event append.
- Writing integration tests for event replay and aggregate reconstruction.

## Skip If (ANY kills it)

- Proof-of-concept — use an in-memory event store.
- Read models can be rebuilt in seconds — snapshots add overhead for no gain.
- Teams without PostgreSQL expertise — schema + concurrency logic requires it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Event store schema target (PostgreSQL) | DDL | DBA |
| Aggregate implementations from event-sourcing-basics | module | team |
| Projection handler scaffolds | stubs | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[event-sourcing-basics]] | Aggregate + event shapes from basics drive the persistence layer here |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `author-event-store-schema` | sonnet | DDL with append-only + version unique constraint. |
| `implement-postgres-store` | sonnet | Append + load + snapshot logic. |
| `wire-projections` | sonnet | EventBus that fans out stored events to handlers. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/event-store-schema.sql` | PostgreSQL DDL with append-only constraints + snapshots table. |
| `templates/postgres-event-store.py` | Python event store with append (optimistic concurrency) + load + snapshot. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-implementation.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[event-sourcing-basics]]
- [[cqrs-pattern]]
- [[microservices-design]]

## Decision tree

See `content/06-decision-tree.xml`. Tree picks event store backend by transaction guarantees and team familiarity, and snapshot strategy by replay cost.
