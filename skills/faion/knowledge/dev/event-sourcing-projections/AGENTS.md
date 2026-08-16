# Event Sourcing — Projections and Read Models

## Summary

**One-sentence:** Event-sourced projections — pure read models built from event streams via idempotent UPSERTs; checkpointed position; rebuildable from offset 0; no side effects.

**One-paragraph:** Projections listen to event streams and maintain specialized read models. Handlers MUST be idempotent (UPSERT keyed by `(stream_id, position)`), MUST track their checkpoint, MUST NOT execute business logic or emit domain events, and MUST be fully rebuildable by truncating the read table + replaying from offset 0. This methodology pins five rules: idempotent UPSERT, checkpoint table, no side effects, rebuildable from zero, scheduled rebuild test. Output: a projection class + checkpoint schema + rebuild script conforming to `02-output-contract.xml`.

**Ефективно для:**

- CQRS read sides where multiple views project from the same event log.
- Rebuilding analytics / search indexes from history.
- Quarterly disaster-recovery rehearsal (rebuild from log).
- Read latency tuned per view (denormalized tables, search engines).
- Projections that survive event-schema versioning per `[[event-sourcing-versioning]]`.

## Applies If (ALL must hold)

- Event sourcing is in place per `[[event-sourcing-fundamentals]]`.
- A read model is needed for query patterns the aggregate doesn't serve.
- The team accepts eventual consistency between writes + reads.
- A checkpoint table (or equivalent) can be added in the read store.

## Skip If (ANY kills it)

- No ES — no events to project from.
- Real-time consistency required — projections lag; route to a read-through cache.
- The read model is identical to the aggregate state — just use the aggregate's `from_events`.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Event catalog | YAML / Markdown | repo |
| Read-model schema | DDL | spec |
| Event-store subscription API | URL | infra |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[event-sourcing-fundamentals]] | Event invariants the projection depends on. |
| [[event-sourcing-versioning]] | Upcasters needed when event schema changes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: idempotent-upsert, checkpointed-position, no-side-effects, rebuildable-from-zero, rebuild-test-quarterly | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for projection spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: non-idempotent-insert, business-logic-in-projection, missing-checkpoint, no-rebuild-path | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on view shape + write-frequency → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-read-model` | sonnet | Schema judgment. |
| `write-projection-handlers` | sonnet | Mapping per event. |
| `write-rebuild-script` | haiku | Mechanical truncate + replay loop. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Projection.py` | Projection class skeleton with idempotent UPSERTs |
| `templates/checkpoint.sql` | Checkpoint table DDL |
| `templates/rebuild.py` | Truncate + replay script |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-projections.py` | Validate projection spec | Pre-commit on spec artefact |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[event-sourcing-fundamentals]]
- [[event-sourcing-aggregate]]
- [[event-sourcing-versioning]]
- [[event-sourcing-snapshots]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (view shape, throughput, consistency need) to a rule from `01-core-rules.xml`. Use it when adding a new read model or refactoring an existing projection.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Projection.py`

```python
from __future__ import annotations

from typing import Protocol


class ReadStore(Protocol):
    def upsert(self, table: str, key: dict, payload: dict) -> None: ...
    def delete(self, table: str, key: dict) -> None: ...
    def get_checkpoint(self, name: str) -> int: ...
    def set_checkpoint(self, name: str, position: int) -> None: ...


class OrdersListProjection:
    NAME = "orders_list"
    TABLE = "orders_list"

    def __init__(self, store: ReadStore) -> None:
        self._store = store

    def handle(self, event, position: int) -> None:
        method = getattr(self, f"_on_{type(event).__name__}", None)
        if method is not None:
            method(event)
        self._store.set_checkpoint(self.NAME, position)

    def _on_OrderPlaced(self, ev) -> None:
        self._store.upsert(
            self.TABLE,
            key={"order_id": ev.order_id},
            payload={
                "order_id": ev.order_id,
                "customer_id": ev.customer_id,
                "status": "placed",
                "total": 0,
            },
        )

    def _on_ItemAdded(self, ev) -> None:
        self._store.upsert(
            self.TABLE,
            key={"order_id": ev.order_id},
            payload={"increment_total": ev.price * ev.quantity},
        )

    def _on_OrderCancelled(self, ev) -> None:
        self._store.delete(self.TABLE, key={"order_id": ev.order_id})
```

### `templates/checkpoint.sql`

```sql
CREATE TABLE IF NOT EXISTS projection_checkpoint (
    name             TEXT PRIMARY KEY,
    stream_position  BIGINT NOT NULL,
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### `templates/rebuild.py`

```python
from __future__ import annotations

import argparse
import sys
from typing import Iterable, Protocol


class EventSource(Protocol):
    def read_all_events(self) -> Iterable: ...


class ReadStore(Protocol):
    def truncate(self, table: str) -> None: ...
    def delete_checkpoint(self, name: str) -> None: ...


def rebuild(projection, source: EventSource, store: ReadStore) -> int:
    store.truncate(projection.TABLE)
    store.delete_checkpoint(projection.NAME)
    count = 0
    for position, event in enumerate(source.read_all_events(), start=1):
        projection.handle(event, position=position)
        count += 1
    return count


def main() -> int:
    ap = argparse.ArgumentParser(description="rebuild a projection from offset 0")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.dry_run:
        sys.stdout.write("dry-run OK\n")
        return 0
    sys.stdout.write("instantiate projection + source + store, then call rebuild()\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
