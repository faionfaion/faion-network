---
slug: cqrs-pattern
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Command Query Responsibility Segregation (CQRS) separates read and write operations into distinct models: commands change state and return void or an ID; queries return data and never modify state.
content_id: "ba7dfdc2a5642e86"
tags: [cqrs, architecture, command, query, event-driven]
---
# CQRS Pattern

## Summary

**One-sentence:** Command Query Responsibility Segregation (CQRS) separates read and write operations into distinct models: commands change state and return void or an ID; queries return data and never modify state.

**One-paragraph:** Command Query Responsibility Segregation (CQRS) separates read and write operations into distinct models: commands change state and return void or an ID; queries return data and never modify state. The concrete rule: a handler class is either a CommandHandler (returns None or ID) or a QueryHandler (returns a read model) — never both. This split allows each side to evolve independently: write side uses the domain model with full invariant enforcement; read side uses flat projections optimized for query patterns (Redis, Elasticsearch, denormalized SQL views).

## Applies If (ALL must hold)

- High read/write ratio where each side has different optimization requirements
- Complex domain with separate read models needed per use case
- Systems requiring audit trails where events drive read model projections
- Applications with eventual consistency requirements (microservices, event-driven)
- Paired with event sourcing where projections rebuild from the event log

## Skip If (ANY kills it)

- Simple CRUD apps — the two-model overhead exceeds benefit when reads and writes are symmetric
- Teams unfamiliar with eventual consistency — stale reads cause correctness bugs if the team does not design for them
- Systems that need immediate read-after-write consistency and cannot tolerate any lag
- Small domains where a single repository and DTO cover all query needs without duplication

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

- parent skill: `pro/dev/code-quality/`
