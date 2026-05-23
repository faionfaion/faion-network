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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-projections.py` | Validate projection spec | Pre-commit on spec artefact |

## Related

- [[event-sourcing-fundamentals]]
- [[event-sourcing-aggregate]]
- [[event-sourcing-versioning]]
- [[event-sourcing-snapshots]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (view shape, throughput, consistency need) to a rule from `01-core-rules.xml`. Use it when adding a new read model or refactoring an existing projection.
