# NoSQL Patterns

## Summary

Data modeling methodology for document (MongoDB), key-value (Redis), wide-column (Cassandra), and graph (Neo4j) stores. Model for access patterns first, not entities; choose embedding vs referencing by read frequency; set TTL on all cache keys; enable schema validation on MongoDB collections. Start with Postgres unless access patterns explicitly justify a NoSQL store.

## Why

NoSQL pathologies (hot partitions, unbounded arrays, missed indexes, orphan fields) only appear at scale and are expensive to fix retroactively. Documenting access patterns before choosing a store prevents premature optimization and prevents locking into a model that doesn't match query needs.

## When To Use

- Schema genuinely flexible per record (event payloads, IoT readings, CMS blocks).
- One-document reads of nested aggregates (user with embedded preferences and addresses).
- Time-series workloads where bucket pattern + TTL fit naturally.
- Graph-shaped data (recommendations, social graphs) where traversal beats recursive CTEs.
- High write throughput per partition exceeding RDBMS comfort (>5k writes/sec sustained).
- Polyglot persistence: hot sessions in Redis, cold archival elsewhere, search in OpenSearch.

## When Not To Use

- Strong relational integrity required (financial ledgers, inventory with multi-row invariants).
- Complex ad-hoc queries or OLAP — use Postgres + DuckDB or a data warehouse.
- Team is unfamiliar with the chosen store and project is small — Postgres JSONB covers 80% of use cases.
- Default choice "because microservices" — start with Postgres until pain is measured.
- Reporting/BI is a hard requirement — most BI tools assume SQL.

## Content

| File | What's inside |
|------|---------------|
| `content/01-mongodb.xml` | Embedding vs referencing decisions, bucket pattern for time-series, indexing rules. |
| `content/02-redis.xml` | Data structure selection (string/hash/list/set/sorted-set/stream), TTL rule, pub/sub vs streams. |
| `content/03-cassandra-neo4j.xml` | Cassandra partition key design, time-bucketed tables; Neo4j Cypher patterns and index rules. |
| `content/04-antipatterns.xml` | Forcing relational patterns, unbounded arrays, missing TTL, hot partitions, schemaless rot. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nosql_picker.py` | Heuristic script mapping access-pattern keywords to recommended store. |
