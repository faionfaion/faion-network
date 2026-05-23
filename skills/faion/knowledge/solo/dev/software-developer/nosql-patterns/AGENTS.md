---
slug: nosql-patterns
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Data-modelling spec for document (MongoDB), key-value (Redis), wide-column (Cassandra), and graph (Neo4j) stores; access-pattern first, TTL on every cache key, partition keys frozen at design.
content_id: "0a60349c71b62b0c"
complexity: medium
produces: spec
est_tokens: 5200
tags: [nosql, mongodb, redis, cassandra, neo4j]
---
# NoSQL Patterns

## Summary

**One-sentence:** Data-modelling spec for document (MongoDB), key-value (Redis), wide-column (Cassandra), and graph (Neo4j) stores; access-pattern first, TTL on every cache key, partition keys frozen at design.

**One-paragraph:** Most NoSQL pain comes from modelling for entities instead of for access patterns, unbounded embedded arrays, missing TTLs, and partition keys that lock the team out of future queries. This methodology produces a typed data-model spec naming the store class, embed-vs-reference verdicts with cardinality evidence, partition-key choice with the primary access query, TTL policy per Redis prefix, and an index list per MongoDB collection. The spec ships before any collection is created and is validated against a JSON Schema.

**Ефективно для:**

- Перший NoSQL store у проекті - потрібно зафіксувати модель доступу.
- Міграція heavy JSONB-таблиці в MongoDB або key-value кеш.
- Redis-кеш накопичує ключі без TTL - пора зафіксувати політику.
- Cassandra/DynamoDB вибрано і треба заморозити partition key до запуску.
- Neo4j прототип переходить в production - індекси й traversal patterns треба зафіксувати.

## Applies If (ALL must hold)

- Access patterns are documented (read/write QPS, latency budget, primary queries).
- Data shape is genuinely flexible per record OR access is single-aggregate / time-series / graph.
- One named owner for the data model (a single human signs off the spec).
- Backing store class is shortlisted to one of: document / key-value / wide-column / graph.

## Skip If (ANY kills it)

- Strong relational invariants required (financial ledger, inventory with multi-row transactions).
- Ad-hoc OLAP / BI is a hard requirement - start with Postgres + warehouse.
- Project is a throwaway prototype with no production users.
- Team is unfamiliar with the chosen store and Postgres JSONB covers the use case.
- Compliance forbids the store class (e.g. data residency rules block managed Mongo).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Access-pattern register | markdown / table of queries with QPS + latency | product + engineering |
| Cardinality estimates | rows-per-entity / array growth bounds | analytics / domain expert |
| Compliance constraints | list of restrictions (PII, residency, retention) | legal / security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[database-design]] | upstream relational baseline; spec inherits its access-pattern register format. |
| [[caching-strategy]] | consumer of the Redis-prefix + TTL section of this spec. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example for MongoDB + Redis | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-store-class` | sonnet | Score document / key-value / wide-column / graph on access patterns. |
| `draft-embed-vs-reference` | sonnet | Cardinality + read-frequency judgement. |
| `partition-key-design` | opus | Stakes high - choice is immutable at scale. |
| `ttl-policy` | haiku | Mechanical mapping prefix → ttl_seconds. |
| `index-list` | sonnet | Match indexes to query predicates. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nosql-data-model.json` | JSON skeleton for the data-model spec artefact. |
| `templates/redis-ttl-policy.yaml` | Prefix → TTL policy template. |
| `templates/nosql_picker.py` | Heuristic access-pattern → store class picker (CLI helper for the spec author). |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nosql-patterns.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[database-design]]
- [[caching-strategy]]
- [[sql-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs — relational invariants needed?, access-pattern shape, expected partition skew, AI-tagging requirements — onto one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks the store class, and surfaces the partition-key decision early.
