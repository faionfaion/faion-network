---
slug: event-sourcing-aggregate
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The event-sourced aggregate root reconstructs its state by replaying a list of past events and emits new events (never mutating state directly) when commands succeed.
content_id: "013b5c3c1e3ae0db"
tags: [event-sourcing, aggregate, domain-driven-design, command-handler, optimistic-concurrency]
---
# Event Sourcing — Aggregate Root Pattern

## Summary

**One-sentence:** The event-sourced aggregate root reconstructs its state by replaying a list of past events and emits new events (never mutating state directly) when commands succeed.

**One-paragraph:** The event-sourced aggregate root reconstructs its state by replaying a list of past events and emits new events (never mutating state directly) when commands succeed. State MUST be mutated only inside apply() handlers, never inside command methods.

## Applies If (ALL must hold)

- Implementing an event-sourced domain model that has business invariants to enforce.
- Any aggregate root in a CQRS system where commands are handled and events are persisted.
- When you need to reconstruct aggregate state from a repository (load events, replay, then execute command).

## Skip If (ANY kills it)

- Simple CRUD entities with no invariants — the apply/replay overhead adds zero value.
- Cross-aggregate operations — never load two aggregates and mutate both in one command handler; use sagas/process managers instead.

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
