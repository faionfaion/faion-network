<!--

purpose: Markdown skeleton for the optimization report (per-query before/after).
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (sql-optimization)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
-->


# SQL Optimization Report — <date>

## Summary

- DB: <db_engine>
- Workload: <workload_type>
- Queries reviewed: <queries_reviewed>
- Net p95 change: <p95_change>

## Per-query findings

### Q1: <primary_query_name>

**Before**

```sql
-- before
SELECT * FROM orders WHERE user_id = $1 AND created_at > $2;
```

EXPLAIN ANALYZE (before): <buffers_rows_time>

**Change**

- Add composite index: `CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);`
- Replace `SELECT *` with explicit column list.

**After**

```sql
-- after
SELECT id, status, total FROM orders WHERE user_id = $1 AND created_at > $2;
```

EXPLAIN ANALYZE (after): <buffers_rows_time>

## Index hygiene

- Dropped: <list>
- Added: <list>
- Rebuilt: <list>

## Cache & pool changes

- pgbouncer pool size: <before> -> <after>
- App-level cache: <key_pattern> TTL <seconds>
