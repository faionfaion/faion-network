---
slug: nosql-cassandra-patterns
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cassandra and DynamoDB schemas are driven entirely by query patterns.
content_id: "0d6606e8b73637cd"
tags: [cassandra, dynamodb, wide-column, partition-key, time-series]
---
# Cassandra Wide-Column Modeling Patterns

## Summary

**One-sentence:** Cassandra and DynamoDB schemas are driven entirely by query patterns.

**One-paragraph:** Cassandra and DynamoDB schemas are driven entirely by query patterns. Partition keys determine data distribution and must have high cardinality to avoid hot nodes. Clustering columns determine sort order within a partition. Time-bucketed partition keys prevent unbounded partitions in time-series workloads. Materialized views and duplicate tables serve different access patterns without application-side joins.

## Applies If (ALL must hold)

- Write-heavy time-series workloads (IoT sensor data, metrics, logs, events) at high throughput.
- Horizontally scalable storage where Postgres or MongoDB cannot sustain the write rate.
- Multi-region active-active deployments where last-write-wins or LWT (lightweight transactions) are acceptable.
- Known, stable access patterns — Cassandra schema design assumes you will not add arbitrary ad-hoc queries later.

## Skip If (ANY kills it)

- Ad-hoc or analytical queries — ALLOW FILTERING is an antipattern and a performance hazard; use a warehouse instead.
- Strong-consistency multi-row transactions — Cassandra LWT (BATCH with IF conditions) is expensive and not equivalent to ACID transactions.
- Small datasets or low write rates where Postgres handles the workload without distributed overhead.
- Workloads where access patterns are unknown or evolve frequently — schema changes in Cassandra require duplicate tables and migration runs.

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

- parent skill: `pro/dev/backend-systems/`
