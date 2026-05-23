# Cassandra Wide-Column Modeling Patterns

## Summary

**One-sentence:** Query-driven schema for Cassandra / DynamoDB: high-cardinality partition keys, one table per access pattern, time-bucketed partitions, LWT/counters tuned to traffic.

**One-paragraph:** Cassandra and DynamoDB schemas are driven entirely by query patterns. Each access pattern gets a dedicated table; partition keys are high-cardinality and combined with time buckets to cap partition size; secondary indexes and ALLOW FILTERING are forbidden; lightweight transactions (LWT) and counters are reserved for true compare-and-swap or atomic-increment paths. Output is a table schema bundle naming partition key + clustering keys + per-table query.

**Ефективно для:**

- Modelling time-series data (telemetry, IoT, logs) without growing one partition per device forever.
- DynamoDB designs where every access pattern needs its own table or GSI.
- Counter-heavy workloads (likes, views) avoiding read-modify-write races.
- Migrating from a relational schema where JOINs are the dominant pattern.

## Applies If (ALL must hold)

- Workload uses Apache Cassandra, ScyllaDB, or AWS DynamoDB.
- Access patterns are predictable and can be enumerated up front.
- Schema can be designed table-per-query without hitting prohibitive storage costs.
- Team is willing to denormalise to optimise reads.

## Skip If (ANY kills it)

- Workload is OLAP / analytical scans — use a columnar store (BigQuery, Snowflake) instead.
- Access patterns are exploratory / ad-hoc — use Postgres + indexes.
- Data fits comfortably in a single relational DB with no JOIN performance issues.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Access-pattern list | yaml / md | team — every query shape + QPS |
| Data-volume estimate | doc | team — rows per partition, total bytes |
| Consistency budget | yaml | team — ONE / LOCAL_QUORUM / LWT per query |

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
| `enumerate-access-patterns` | sonnet | Discovering query shapes needs judgement. |
| `design-schema` | sonnet | Partition key + clustering design requires nuance. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.cql` | Cassandra CQL schema skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nosql-cassandra-patterns.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[nosql-mongodb-patterns]]
- [[nosql-redis-patterns]]
- [[nosql-neo4j-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
