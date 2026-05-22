---
slug: sql-optimization
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: SQL optimization is the practice of analyzing and improving database queries to reduce execution time, minimize resource consumption, and improve application responsiveness.
content_id: "6379d7bf056266f9"
tags: [sql, database, performance, query-optimization, indexing]
---
# SQL Optimization

## Summary

**One-sentence:** SQL optimization is the practice of analyzing and improving database queries to reduce execution time, minimize resource consumption, and improve application responsiveness.

**One-paragraph:** SQL optimization is the practice of analyzing and improving database queries to reduce execution time, minimize resource consumption, and improve application responsiveness. Measure with EXPLAIN ANALYZE before optimizing. Optimize the right queries: frequent ones and those consuming most database resources. Remember that indexes are not free: they speed reads but slow writes. Always filter data early, join smartly, and fetch only needed columns. Consider the full picture: query optimization, connection pooling, caching, and materialized views.

## Applies If (ALL must hold)

- Slow query complaints from users or monitoring alerts.
- Database CPU or I/O consistently high, indicating resource bottleneck.
- Application response times degrading under load, especially under high concurrency.
- Before deploying new features with complex or unknown performance characteristics.
- Regular performance audits and maintenance as data grows.

## Skip If (ANY kills it)

- Premature optimization before establishing actual bottleneck with profiling.
- Over-optimizing rarely-run queries; effort should focus on high-traffic paths.
- Over-indexing (more indexes = slower writes without proportional read speedup).
- Replacing simple working queries with complex optimizations without benchmarking trade-offs.
- Caching strategy that defeats database optimizations (e.g., caching and stale reads).

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
