<!--
purpose: Markdown skeleton for the optimization report (per-query before/after).
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (sql-optimization)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
variables:
  - name: date
    type: string
    required: true
    description: The date these measurements were taken, ISO. A plan is a function of row counts and statistics, so an undated report is a claim about a database that no longer exists.
  - name: db_engine
    type: string
    required: true
    description: Engine and major version the plans came from - "PostgreSQL 16". Plan shapes and optimiser behaviour change between majors, so the version is part of the evidence, not decoration.
  - name: workload_type
    type: enum
    required: true
    options: [OLTP, OLAP, mixed]
    description: Which workload these queries serve. It decides what "better" means - OLTP buys p95 on one row, OLAP buys throughput over many, and a fix for one routinely hurts the other.
  - name: queries_reviewed
    type: integer
    required: true
    description: How many queries were actually examined, not how many exist. The reader needs to know whether this is the worst three or the whole workload before trusting the headline number.
  - name: p95_change
    type: string
    required: true
    description: Net p95 change across the reviewed set, with its sign. If something got slower, it goes here too - a report containing only wins is a selection, not a measurement.
  - name: primary_query_name
    type: string
    required: true
    description: A name for Q1 that a developer will recognise in the codebase - the endpoint or function that issues it. "The slow one" is not findable by grep six months later.
-->
# SQL Optimization Report — {{date}}

## Summary

- DB: {{db_engine}}
- Workload: {{workload_type}}
- Queries reviewed: {{queries_reviewed}}
- Net p95 change: {{p95_change}}

## Per-query findings

### Q1: {{primary_query_name}}

**Before**

```sql
-- before
SELECT * FROM orders WHERE user_id = $1 AND created_at > $2;
```

EXPLAIN ANALYZE (before): [buffers / rows / time]

**Change**

- Add composite index: `CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);`
- Replace `SELECT *` with explicit column list.

**After**

```sql
-- after
SELECT id, status, total FROM orders WHERE user_id = $1 AND created_at > $2;
```

EXPLAIN ANALYZE (after): [buffers / rows / time]

## Index hygiene

- Dropped: [list]
- Added: [list]
- Rebuilt: [list]

## Cache & pool changes

- pgbouncer pool size: [before] -> [after]
- App-level cache: [key pattern] TTL [seconds]
