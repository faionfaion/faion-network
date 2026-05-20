---
slug: sql-optimization
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Profile queries with `EXPLAIN (ANALYZE, BUFFERS)` before touching any index or query, add composite indexes with equality columns first and range columns last, replace OFFSET pagination with keyset cursors, and batch inserts/updates.
content_id: "6379d7bf056266f9"
tags: [sql, query-optimization, postgresql, indexing, performance]
---
# SQL Optimization

## Summary

**One-sentence:** Profile queries with `EXPLAIN (ANALYZE, BUFFERS)` before touching any index or query, add composite indexes with equality columns first and range columns last, replace OFFSET pagination with keyset cursors, and batch inserts/updates.

**One-paragraph:** Profile queries with `EXPLAIN (ANALYZE, BUFFERS)` before touching any index or query, add composite indexes with equality columns first and range columns last, replace OFFSET pagination with keyset cursors, and batch inserts/updates. Measure actual vs estimated rows — large discrepancies indicate stale statistics.

## Applies If (ALL must hold)

- A query takes more than 100ms under normal load
- Database CPU or IO is consistently above 70%
- Application response times degrade as data grows
- Adding a new feature that queries large or frequently joined tables
- Regular performance audits before capacity events

## Skip If (ANY kills it)

- Tables under ~10k rows — full scans are typically sub-millisecond
- Write-heavy tables where index overhead outweighs read gain
- Premature optimization of queries not yet on the hot path
- Before running EXPLAIN ANALYZE — never add indexes without profiling first

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
