# DDD Aggregates: Invariant-Enforcing Cluster Roots

## Summary

**One-sentence:** DDD Aggregate root pattern — cluster Entities + Value Objects under one root, enforce invariants via intention-revealing methods, no public setters, identity-only cross-aggregate refs.

**One-paragraph:** An Aggregate is a cluster of domain objects treated as a single unit for data changes. One Entity is the Aggregate Root: all external access goes through it; all invariants are enforced inside its command methods. No public setters; mutation happens through `order.place(...)`, `order.cancel()`. Aggregates reference other aggregates by identity (UUID), never by object reference. This methodology pins five rules: root-only mutation, raise events on state change, identity-only cross-aggregate refs, invariants-as-tests, small aggregate size. Output: an aggregate class + invariant tests conforming to `02-output-contract.xml`.

**Ефективно для:**

- Rich domain with non-trivial invariants (order placement, payment, scheduling).
- Cross-table consistency boundaries within one transaction.
- Codebases adopting CQRS — aggregates own the write side.
- Teams enforcing no-public-setter discipline in code review.
- AI-generated code where regression to anaemic domain is the default.

## Applies If (ALL must hold)

- Domain has invariants that span multiple entities/value objects.
- Strong consistency required within the aggregate's transactional boundary.
- The team has internalized DDD vocabulary.
- Writes go through a repository; queries can use read models / projections.

## Skip If (ANY kills it)

- CRUD-only entity with no real invariants — overhead exceeds benefit.
- Read-heavy reporting service — use projections / DTOs directly.
- Aggregate would span more than ~5 entities — split into smaller aggregates.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain glossary | Markdown | domain owner |
| Invariants list | Markdown bullet list | spec |
| Existing entity sketch | language source / ERD | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ddd-value-objects]] | Aggregates compose value objects for self-validating attributes. |
| [[ddd-repositories]] | Repositories return aggregates; aggregate boundary defines persistence boundary. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: root-only-mutation, raise-event-on-mutation, identity-only-refs, invariant-as-test, small-aggregate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for aggregate spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: bypass-root, god-aggregate, object-ref-across-aggregates, invariant-in-service | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: identify boundary → root + invariants → command methods → events → tests | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on consistency boundary + size → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-boundary` | sonnet | Judgment on consistency edges. |
| `write-aggregate-class` | sonnet | Domain scaffolding. |
| `derive-invariant-tests` | haiku | Mechanical mapping of invariant → failing test. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Aggregate.py` | Python aggregate root with collected events |
| `templates/Aggregate.cs` | C# aggregate root with private setters |
| `templates/invariant-tests.md` | Markdown checklist of invariant→test mappings |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ddd-aggregates.py` | Validate aggregate spec against schema | Pre-commit on spec artefact |

## Related

- [[ddd-value-objects]]
- [[ddd-repositories]]
- [[ddd-domain-events]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (consistency boundary, aggregate size, transaction scope) to a rule from `01-core-rules.xml`. Use it whenever proposing a new aggregate or refactoring a large one.
