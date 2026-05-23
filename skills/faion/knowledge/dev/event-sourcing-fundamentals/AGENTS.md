# Event Sourcing — Fundamentals

## Summary

**One-sentence:** Event Sourcing core invariants — immutable events as source of truth, replay derives state, past-tense business names, append-only log, stream + version.

**One-paragraph:** Event Sourcing persists the state of an entity as an ordered sequence of immutable events; current state is derived by replaying the sequence. Events MUST be immutable, past-tense business facts, ordered by stream version, and append-only. This methodology pins five rules: events immutable + append-only, events as source of truth, ordered replay, past-tense business names, one stream per aggregate. Output: a decision-record spec (use ES or not) + event catalog conforming to `02-output-contract.xml`.

**Ефективно для:**

- Teams adopting ES for the first time — establish invariants before writing code.
- Audit + compliance: full history of every state change.
- Time-travel debugging — reproduce past state by replaying to a version.
- CQRS systems where projections rebuild from the event log.
- Distributed systems where eventual consistency between contexts is acceptable.

## Applies If (ALL must hold)

- The domain genuinely benefits from full audit history.
- The team has read DDD aggregates + can design past-tense events.
- An event store (or plan to build one) exists.
- Read-side latency tolerates async projection updates.

## Skip If (ANY kills it)

- Simple CRUD with no audit requirement — overhead exceeds benefit.
- Sub-millisecond write + read latency requirement on the same model.
- Team unfamiliar with eventual consistency.
- Schema thrashes weekly — versioning cost dominates.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain glossary | Markdown | domain owner |
| Aggregate boundary | spec | spec |
| Audit + compliance needs | requirements | stakeholder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ddd-aggregates]] | ES aggregates inherit aggregate rules. |
| [[ddd-domain-events]] | Sibling pattern — events as notifications. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: events-immutable-append-only, events-source-of-truth, ordered-replay, past-tense-business-names, one-stream-per-aggregate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for ES-decision spec | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: mutate-event, state-stored-alongside, crud-event-names | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked example: deciding ES vs CRUD for an Order entity | ~600 |
| `content/06-decision-tree.xml` | essential | Routing tree on audit/read-pattern → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-es-or-not` | sonnet | Cost/benefit judgment. |
| `name-events` | sonnet | Past-tense naming requires domain judgment. |
| `draft-event-catalog` | haiku | Mechanical formatting once names exist. |

## Templates

| File | Purpose |
|------|---------|
| `templates/event-catalog.yml` | Event catalog seed file |
| `templates/decision-record.md` | ES vs CRUD decision record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-fundamentals.py` | Validate ES-decision spec | Pre-commit on spec artefact |

## Related

- [[event-sourcing-aggregate]]
- [[event-sourcing-projections]]
- [[event-sourcing-versioning]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (audit-need, read-pattern, schema stability) to a rule from `01-core-rules.xml` and either approves ES or redirects to a state-stored aggregate with domain events.
