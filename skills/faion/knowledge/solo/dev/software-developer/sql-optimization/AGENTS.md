# SQL Optimization

## Summary

Profile queries with `EXPLAIN (ANALYZE, BUFFERS)` before touching any index or query, add composite indexes with equality columns first and range columns last, replace OFFSET pagination with keyset cursors, and batch inserts/updates. Measure actual vs estimated rows — large discrepancies indicate stale statistics.

## Why

Unoptimized queries on tables above ~100k rows cause latency spikes that compound under load. Sequential scans that were fast at 10k rows become multi-second at 10M rows. OFFSET pagination degrades O(N) with page depth. Covering indexes eliminate table heap lookups. Without EXPLAIN ANALYZE, optimization is guesswork — the planner's chosen plan often differs from the developer's assumption.

## When To Use

- A query takes more than 100ms under normal load
- Database CPU or IO is consistently above 70%
- Application response times degrade as data grows
- Adding a new feature that queries large or frequently joined tables
- Regular performance audits before capacity events

## When NOT To Use

- Tables under ~10k rows — full scans are typically sub-millisecond
- Write-heavy tables where index overhead outweighs read gain
- Premature optimization of queries not yet on the hot path
- Before running EXPLAIN ANALYZE — never add indexes without profiling first

## Content

| File | What's inside |
|------|---------------|
| `content/01-analysis.xml` | EXPLAIN ANALYZE usage rules; reading plan nodes (Seq Scan, Index Scan, Hash Join) |
| `content/02-indexes.xml` | Composite index column order rule; covering indexes; partial indexes; expression indexes |
| `content/03-query-patterns.xml` | Keyset pagination vs OFFSET; N+1 via subquery vs JOIN; batch insert/update; materialized views |
| `content/04-antipatterns.xml` | SELECT *, LIKE '%x%', ORDER BY RAND(), implicit type cast, missing WHERE on UPDATE/DELETE |

## Templates

none
