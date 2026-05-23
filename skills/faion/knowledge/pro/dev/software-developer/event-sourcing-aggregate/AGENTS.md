---
slug: event-sourcing-aggregate
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Event-sourced aggregate root pattern — replay events to rebuild state, mutate only in apply handlers, command methods emit, repository.save with expected_version.
content_id: "7fa8d12d9d29ae0a"
complexity: medium
produces: code
est_tokens: 4200
tags: [event-sourcing, aggregate, domain-driven-design, command-handler, optimistic-concurrency]
---
# Event Sourcing — Aggregate Root Pattern

## Summary

**One-sentence:** Event-sourced aggregate root pattern — replay events to rebuild state, mutate only in apply handlers, command methods emit, repository.save with expected_version.

**One-paragraph:** An event-sourced aggregate reconstructs state by replaying events through `apply()` handlers; it emits new events from command methods but NEVER mutates state directly there. The repository loads `(events, version)`, the command runs, and `save(stream_id, new_events, expected_version)` enforces optimistic concurrency. This methodology pins five rules: apply-only mutation, command methods emit + return, expected_version on save, `from_events` reconstruction, `collect_pending_events` boundary. Output: aggregate + event classes + repository scaffold conforming to `02-output-contract.xml`.

**Ефективно для:**

- New event-sourced aggregates (Order, Subscription, Wallet).
- Migrating CRUD entity to ES while preserving domain logic.
- Codifying invariants as event-emission patterns.
- Concurrency-safe writes via expected_version.
- Pair-trained AI agent runs per `[[event-sourcing-agentic]]`.

## Applies If (ALL must hold)

- Event sourcing is the persistence pattern (not just notifications).
- An event-store library (or hand-rolled equivalent) is in place.
- Aggregates per `[[ddd-aggregates]]` are the unit of consistency.
- The team understands optimistic concurrency + version semantics.

## Skip If (ANY kills it)

- CRUD app pretending to use ES — overhead exceeds benefit.
- Aggregate has no invariants — events without invariants are just an audit log; use `[[ddd-domain-events]]` instead.
- Sub-millisecond write latency requirement — replay overhead dominates.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Event catalog | YAML/Markdown | repo |
| Aggregate boundary | spec | spec |
| Event-store API docs | URL | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[event-sourcing-fundamentals]] | Core invariants the aggregate must protect. |
| [[ddd-aggregates]] | Aggregate-root rules (no public setters etc.). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: apply-only-mutation, command-emits-returns, expected-version-on-save, from-events-reconstruction, collect-pending-boundary | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for aggregate spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: mutate-in-command, save-without-version, lazy-apply, leaked-events | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on aggregate workload → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-event-list` | sonnet | Domain judgment. |
| `write-apply-handlers` | sonnet | Mechanical mapping per event. |
| `write-concurrency-test` | haiku | Generate expected_version clash test. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Aggregate.py` | Event-sourced aggregate skeleton |
| `templates/Repository.py` | Repository with expected_version semantics |
| `templates/ConcurrencyTest.py` | Optimistic-concurrency clash test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-aggregate.py` | Validate aggregate spec | Pre-commit on spec artefact |

## Related

- [[event-sourcing-fundamentals]]
- [[event-sourcing-projections]]
- [[event-sourcing-snapshots]]
- [[event-sourcing-versioning]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (write rate, concurrency, replay cost) to a rule from `01-core-rules.xml` and either approves ES-aggregate scaffolding or redirects to a CRUD aggregate / read-model-only design.
