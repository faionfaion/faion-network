# MongoDB Document Design Patterns

## Summary

**One-sentence:** Access-pattern-driven MongoDB schema: embedding vs referencing decision, index plan from query filters, schemaVersion field + migration scripts, TTL indexes for ephemeral data.

**One-paragraph:** Design MongoDB schemas around access patterns, not entity diagrams. Embed when the child is fetched with the parent and the count is bounded; reference when the child is queried independently or the list is unbounded. Every query filter / sort / range field needs an index; every collection carries a schemaVersion integer and migration scripts move documents forward+backward. Output is a collection schema bundle + index plan + migration scripts.

**Ефективно для:**

- New service designs where MongoDB is the chosen primary store.
- Migrating a relational schema to MongoDB without dragging the foreign-key graph along.
- Adding TTL cleanup to session / cache collections so they self-prune.
- Designing rolling migrations that do not lock the collection.

## Applies If (ALL must hold)

- Workload uses MongoDB (Atlas, self-hosted, or DocumentDB).
- Access patterns can be enumerated at design time.
- Team can index by access pattern (storage + write cost budget present).
- Migrations can be rolled forward incrementally.

## Skip If (ANY kills it)

- Workload is heavy relational with multi-collection JOINs at scale — use Postgres.
- Strong cross-document transactions required (MongoDB supports multi-doc transactions but at cost).
- Embedded full-text search is the dominant access pattern — use Elasticsearch.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Access-pattern list | yaml / md | team |
| Document size estimate | doc | team |
| Index storage budget | yaml | DBA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-embed-vs-ref` | sonnet | Decision needs judgement on cardinality + access. |
| `draft-schema` | sonnet | Schema authoring benefits from sonnet. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.json` | Mongo collection schema + index plan skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nosql-mongodb-patterns.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[nosql-cassandra-patterns]]
- [[nosql-redis-patterns]]
- [[nosql-neo4j-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
