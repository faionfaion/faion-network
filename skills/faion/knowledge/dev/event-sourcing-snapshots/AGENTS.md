# Event Sourcing — Snapshot Strategy

## Summary

**One-sentence:** ES snapshot strategy — cache-only acceleration of replay (every N events), always rebuildable from offset 0, mandatory invalidation on event schema bump.

**One-paragraph:** Snapshots accelerate aggregate load by persisting derived state at version V; subsequent loads replay only events with version > V. They are a performance cache ONLY — correctness must be unaffected if every snapshot is dropped. When an event class is added, removed, or renamed (schema bump), ALL snapshots for that aggregate type MUST be invalidated and rebuilt before deploying the new event version. This methodology pins five rules: cache-only, every-N-events policy, schema-bump invalidation, fall-back to log-replay, version-aware storage. Output: snapshot policy + storage schema + rebuild script conforming to `02-output-contract.xml`.

**Ефективно для:**

- Long-lived aggregates with thousands of events (wallets, subscriptions).
- Cold-load performance budgets.
- Reducing replay CPU during projection rebuild.
- Bounded snapshot growth (one row per (stream_id, snapshot_version)).
- Migration plans tied to event-schema versioning.

## Applies If (ALL must hold)

- An ES aggregate has noticeable load latency (> 100ms cold replay).
- Event stream length per aggregate is > ~200 events.
- The team can commit to schema-bump invalidation discipline.
- Storage for snapshots exists (DB table, Redis, blob store).

## Skip If (ANY kills it)

- Aggregate has < ~200 events on average — replay is fast enough.
- Team cannot enforce schema-bump invalidation — snapshots will silently corrupt.
- Snapshots would have to be "smart" (apply business logic at restore) — that's the antipattern.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Aggregate type + replay benchmarks | spec / measurements | repo |
| Event-schema version | catalog | repo |
| Snapshot storage | DDL / config | infra |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[event-sourcing-aggregate]] | Aggregate must support `from_events` reconstruction. |
| [[event-sourcing-versioning]] | Schema-bump triggers snapshot invalidation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: cache-only, every-n-events, schema-bump-invalidation, fall-back-replay, version-aware-storage | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for snapshot policy spec | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: snapshot-as-truth, no-invalidation, smart-snapshot | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on aggregate size + cost → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-snapshot-policy` | sonnet | Cost/benefit judgment. |
| `write-snapshot-storage` | sonnet | DDL + (de)serializer mapping. |
| `wire-invalidation-on-version-bump` | sonnet | CI guard on schema-version + snapshots. |

## Templates

| File | Purpose |
|------|---------|
| `templates/snapshot.sql` | Snapshot table DDL |
| `templates/SnapshotStore.py` | Snapshot store with version + payload |
| `templates/invalidate.py` | Schema-bump invalidation script |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-snapshots.py` | Validate snapshot policy spec | Pre-commit on spec artefact |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[event-sourcing-aggregate]]
- [[event-sourcing-versioning]]
- [[event-sourcing-projections]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (aggregate-length, replay cost, schema cadence) to a rule from `01-core-rules.xml`. Use it whenever introducing snapshots or revisiting the every-N policy.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/snapshot.sql`

```sql
CREATE TABLE IF NOT EXISTS aggregate_snapshots (
    aggregate_type    TEXT NOT NULL,
    stream_id         UUID NOT NULL,
    snapshot_version  BIGINT NOT NULL,
    schema_version    INTEGER NOT NULL,
    payload           JSONB NOT NULL,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (aggregate_type, stream_id, snapshot_version)
);

CREATE INDEX IF NOT EXISTS idx_aggregate_snapshots_latest
    ON aggregate_snapshots (aggregate_type, stream_id, snapshot_version DESC);
```

### `templates/SnapshotStore.py`

```python
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Optional, Protocol
from uuid import UUID

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Snapshot:
    aggregate_type: str
    stream_id: UUID
    snapshot_version: int
    schema_version: int
    payload: dict


class DB(Protocol):
    def execute(self, sql: str, *args) -> None: ...
    def fetchone(self, sql: str, *args) -> Optional[tuple]: ...


class SnapshotStore:
    def __init__(self, db: DB, current_schema_version: int) -> None:
        self._db = db
        self._schema = current_schema_version

    def get_latest(self, aggregate_type: str, stream_id: UUID) -> Optional[Snapshot]:
        row = self._db.fetchone(
            "SELECT snapshot_version, schema_version, payload "
            "FROM aggregate_snapshots WHERE aggregate_type=%s AND stream_id=%s "
            "ORDER BY snapshot_version DESC LIMIT 1",
            aggregate_type, str(stream_id),
        )
        if row is None:
            return None
        snap_v, schema_v, payload = row
        if schema_v != self._schema:
            log.info("snapshot schema_version %s != current %s; falling back to replay", schema_v, self._schema)
            return None
        try:
            return Snapshot(aggregate_type, stream_id, snap_v, schema_v, json.loads(payload))
        except Exception as exc:
            log.warning("snapshot deserialise failed for %s/%s: %s", aggregate_type, stream_id, exc)
            return None

    def write(self, snap: Snapshot) -> None:
        self._db.execute(
            "INSERT INTO aggregate_snapshots(aggregate_type, stream_id, snapshot_version, schema_version, payload) "
            "VALUES (%s, %s, %s, %s, %s)",
            snap.aggregate_type, str(snap.stream_id), snap.snapshot_version, snap.schema_version,
            json.dumps(snap.payload),
        )

    def invalidate(self, aggregate_type: str) -> None:
        self._db.execute("DELETE FROM aggregate_snapshots WHERE aggregate_type=%s", aggregate_type)
```

### `templates/invalidate.py`

```python
from __future__ import annotations

import argparse
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="invalidate all snapshots for an aggregate type before deploying a new event schema version")
    ap.add_argument("aggregate_type", help="PascalCase aggregate type (e.g. Order)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.stdout.write(
        f"would DELETE FROM aggregate_snapshots WHERE aggregate_type='{args.aggregate_type}'\n"
        if args.dry_run
        else f"connect to DB and run invalidate('{args.aggregate_type}') on SnapshotStore\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
