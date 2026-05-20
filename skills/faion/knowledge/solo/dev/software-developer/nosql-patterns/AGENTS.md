---
slug: nosql-patterns
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Data modeling methodology for document (MongoDB), key-value (Redis), wide-column (Cassandra), and graph (Neo4j) stores.
content_id: "76e8079eb73de0ee"
tags: [nosql, mongodb, redis, cassandra, neo4j]
---
# NoSQL Patterns

## Summary

**One-sentence:** Data modeling methodology for document (MongoDB), key-value (Redis), wide-column (Cassandra), and graph (Neo4j) stores.

**One-paragraph:** Data modeling methodology for document (MongoDB), key-value (Redis), wide-column (Cassandra), and graph (Neo4j) stores. Model for access patterns first, not entities; choose embedding vs referencing by read frequency; set TTL on all cache keys; enable schema validation on MongoDB collections. Start with Postgres unless access patterns explicitly justify a NoSQL store.

## Applies If (ALL must hold)

- Schema genuinely flexible per record (event payloads, IoT readings, CMS blocks).
- One-document reads of nested aggregates (user with embedded preferences and addresses).
- Time-series workloads where bucket pattern + TTL fit naturally.
- Graph-shaped data (recommendations, social graphs) where traversal beats recursive CTEs.
- High write throughput per partition exceeding RDBMS comfort (>5k writes/sec sustained).
- Polyglot persistence: hot sessions in Redis, cold archival elsewhere, search in OpenSearch.

## Skip If (ANY kills it)

- Strong relational integrity required (financial ledgers, inventory with multi-row invariants).
- Complex ad-hoc queries or OLAP — use Postgres + DuckDB or a data warehouse.
- Team is unfamiliar with the chosen store and project is small — Postgres JSONB covers 80% of use cases.
- Default choice "because microservices" — start with Postgres until pain is measured.
- Reporting/BI is a hard requirement — most BI tools assume SQL.

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

- parent skill: `solo/dev/software-developer/`
