---
slug: cqrs-pattern
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a CQRS skeleton: Command + CommandHandler returning None/ID; Query + QueryHandler returning a read model; a Mediator that dispatches by type with no handler doing both shapes.
content_id: "d00dd225398d26ea"
complexity: medium
produces: code
est_tokens: 4300
tags: [cqrs, architecture, command, query, event-driven]
---
# CQRS Pattern

## Summary

**One-sentence:** Produces a CQRS skeleton: Command + CommandHandler returning None/ID; Query + QueryHandler returning a read model; a Mediator that dispatches by type with no handler doing both shapes.

**One-paragraph:** CQRS separates write and read sides into distinct models: commands change state and return None or an ID; queries return data and never modify state. A handler is either CommandHandler or QueryHandler — never both. This lets the write side enforce invariants on a domain model while the read side uses flat projections optimised per query (Redis, Elasticsearch, denormalised SQL views).

**Ефективно для:**

- High read/write ratio з різними optimization patterns.
- Складний domain + кілька read models per use case.
- Audit trail через events що драйвлять projections.
- Eventual consistency через design, не випадково.

## Applies If (ALL must hold)

- High read/write ratio where each side has different optimization needs.
- Complex domain with separate read models per use case.
- System needs event-driven projections rebuilding read models.
- Application paired with event sourcing.

## Skip If (ANY kills it)

- Simple CRUD where reads and writes are symmetric.
- Team unfamiliar with eventual consistency.
- System needs immediate read-after-write consistency.
- Small domain where a single repository covers all queries.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain model with identified commands + queries | list | domain expert |
| Read-side persistence target (Redis / SQL view / Elasticsearch) | infra | team |
| Mediator or DI container | tool | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[clean-architecture]] | CQRS handlers sit in the application layer; clean-architecture defines that layer |

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
| `scaffold-handlers` | sonnet | Generate CommandHandler + QueryHandler stubs. |
| `author-mediator` | sonnet | Write the dispatcher with type-based routing. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/command-handler.py` | Command + CommandHandler skeleton; returns None or ID only. |
| `templates/query-handler.py` | Query + QueryHandler skeleton; returns a read model only. |
| `templates/mediator.py` | Type-based Mediator dispatching to the right handler. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cqrs-pattern.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[clean-architecture]]
- [[event-sourcing-basics]]
- [[event-sourcing-implementation]]

## Decision tree

See `content/06-decision-tree.xml`. Tree gates CQRS on read/write asymmetry + team readiness for eventual consistency; otherwise plain repository pattern is enough.
