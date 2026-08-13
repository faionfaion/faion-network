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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/event-store-schema.sql`

```sql
-- append-only events table + per-aggregate version uniqueness
CREATE TABLE events (
    event_id        UUID         PRIMARY KEY,
    aggregate_id    UUID         NOT NULL,
    aggregate_type  TEXT         NOT NULL,
    event_type      TEXT         NOT NULL,
    payload         JSONB        NOT NULL,
    occurred_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
    version         INTEGER      NOT NULL,
    UNIQUE (aggregate_id, version)
);
CREATE INDEX events_aggregate_idx ON events(aggregate_id, version);
REVOKE UPDATE, DELETE ON events FROM PUBLIC;  -- append-only at grant level

CREATE TABLE snapshots (
    aggregate_id    UUID         NOT NULL,
    version         INTEGER      NOT NULL,
    state           JSONB        NOT NULL,
    captured_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (aggregate_id, version)
);
```

### `templates/postgres-event-store.py`

```python
"""
from __future__ import annotations
import json
from dataclasses import asdict
from typing import List, Optional
from uuid import UUID

import psycopg


class ConcurrencyError(Exception):
    pass


class PostgresEventStore:
    def __init__(self, conn: psycopg.Connection) -> None:
        self.conn = conn

    def append(self, aggregate_id: UUID, aggregate_type: str, events: List[object], expected_version: int) -> None:
        with self.conn.cursor() as cur:
            for i, ev in enumerate(events, start=1):
                try:
                    cur.execute(
                        "INSERT INTO events(event_id, aggregate_id, aggregate_type, event_type, payload, version)"
                        " VALUES (%s, %s, %s, %s, %s, %s)",
                        (str(getattr(ev, "event_id")), str(aggregate_id), aggregate_type, type(ev).__name__,
                         json.dumps(asdict(ev), default=str), expected_version + i),
                    )
                except psycopg.errors.UniqueViolation as e:
                    raise ConcurrencyError(f"stream moved at version {expected_version + i}") from e

    def load_events(self, aggregate_id: UUID, from_version: int = 0) -> list[dict]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT version, event_type, payload FROM events WHERE aggregate_id = %s AND version > %s ORDER BY version",
                (str(aggregate_id), from_version),
            )
            return [{"version": v, "type": t, "payload": p} for v, t, p in cur.fetchall()]

    def load_snapshot(self, aggregate_id: UUID) -> Optional[dict]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT version, state FROM snapshots WHERE aggregate_id = %s ORDER BY version DESC LIMIT 1",
                (str(aggregate_id),),
            )
            row = cur.fetchone()
            return {"version": row[0], "state": row[1]} if row else None

    def save_snapshot(self, aggregate_id: UUID, version: int, state: dict) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO snapshots(aggregate_id, version, state) VALUES (%s, %s, %s)"
                " ON CONFLICT (aggregate_id, version) DO NOTHING",
                (str(aggregate_id), version, json.dumps(state)),
            )
```
