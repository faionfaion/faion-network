---
slug: event-sourcing-snapshots
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Snapshots periodically save the derived aggregate state so that reconstruction skips replaying the entire event history.
content_id: "317c31a1167e0d2b"
tags: [event-sourcing, snapshots, performance, aggregate]
---
# Event Sourcing — Snapshot Strategy

## Summary

**One-sentence:** Snapshots periodically save the derived aggregate state so that reconstruction skips replaying the entire event history.

**One-paragraph:** Snapshots periodically save the derived aggregate state so that reconstruction skips replaying the entire event history. Snapshots are a performance cache ONLY — the system MUST be able to reconstruct correct state from event offset 0 at any time. Snapshots must be invalidated and rebuilt whenever the event schema changes.

## Applies If (ALL must hold)

- Aggregate streams with more than 50–100 events per instance where command latency is measurably impacted by replay.
- Long-running aggregates (multi-year accounts, high-frequency order streams) where the event count grows unbounded.
- After profiling confirms that aggregate reconstruction is the bottleneck — do not add snapshots speculatively.

## Skip If (ANY kills it)

- Short-lived aggregates with small event counts — replay is cheap, snapshot overhead (storage, invalidation) costs more than it saves.
- Systems without a tested "rebuild snapshot from events" path — stale snapshots + schema-changed events produce silently wrong state.
- Treating snapshots as the truth to skip event replay entirely — this breaks event-versioning and schema migration.

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
