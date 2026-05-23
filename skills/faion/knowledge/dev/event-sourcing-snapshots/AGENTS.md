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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-snapshots.py` | Validate snapshot policy spec | Pre-commit on spec artefact |

## Related

- [[event-sourcing-aggregate]]
- [[event-sourcing-versioning]]
- [[event-sourcing-projections]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (aggregate-length, replay cost, schema cadence) to a rule from `01-core-rules.xml`. Use it whenever introducing snapshots or revisiting the every-N policy.
