# SQL Optimization

## Summary

**One-sentence:** SQL optimisation report: EXPLAIN ANALYZE before/after, index changes, composite index ordering, cursor pagination, materialized views, with measured wall-clock delta per query.

**One-paragraph:** SQL optimisation fails when changes ship without EXPLAIN ANALYZE evidence, when stale statistics produce wrong plans that indexes can't fix, when composite indexes order range columns first, when subqueries in SELECT create N+1, and when OFFSET pagination drags at depth. This methodology produces an optimisation report: per-query EXPLAIN ANALYZE before/after, applied changes (index added / query rewrite / VACUUM ANALYZE), wall-clock delta, and a recommendation gate (regression check).

**Ефективно для:**

- Slow query report - підготувати оптимізаційний план з вимірами.
- Composite index `(range_col, eq_col)` - переставити порядок.
- OFFSET 10000 - перейти на cursor pagination.
- Dashboard query 8s+ - матеріалізована view + REFRESH CONCURRENTLY.
- Subquery в SELECT - переписати на JOIN з aggregation.

## Applies If (ALL must hold)

- Database is PostgreSQL (or compatible with EXPLAIN ANALYZE).
- Slow query log or APM identifies queries above SLO budget.
- Owner can apply migrations (index creation, statistics refresh).
- Staging or read-replica has production-equivalent data volume.

## Skip If (ANY kills it)

- Database is a key-value or document store - use nosql-patterns instead.
- Query is in a hot loop without persistent data - profile application code first.
- Staging is empty - optimisation evidence is meaningless without prod volume.
- Bottleneck is clearly application-side (deserialisation, network).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Slow query list | queries + p95 latency + frequency | APM / pg_stat_statements |
| Schema dump | CREATE TABLE + indexes per table | DB owner |
| Staging snapshot | production-volume restore | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[performance-testing]] | perf SLOs frame which queries need optimisation. |
| [[database-design]] | schema choices upstream of query optimisation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: EXPLAIN before change, ANALYZE on skew, composite ordering, cursor pagination, no subquery in SELECT, materialized views for aggregates, regression gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: capture plan, fix skew, design index, apply, verify | ~900 |
| `content/05-examples.xml` | essential | Worked example for an orders list query | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `capture-plan` | haiku | Mechanical EXPLAIN invocation. |
| `diagnose-plan` | sonnet | Interpret join order + index use. |
| `design-change` | sonnet | Choose index / rewrite / MV. |
| `regression-gate` | opus | Stakes high; wrong index ships to prod. |

## Templates

| File | Purpose |
|------|---------|
| `templates/report.md` | Markdown skeleton for an SQL-optimisation report. |
| `templates/create_index_concurrently.sql` | Index creation snippet using CONCURRENTLY + REINDEX guidance. |
| `templates/_smoke-test.json` | Minimum viable sql-optimisation report for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sql-optimization.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[database-design]]
- [[performance-testing]]
- [[nosql-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - EXPLAIN captured, stats skew, index shape - onto a rule from `content/01-core-rules.xml`. Use it before any optimisation: it catches explain-skipped and stats-skew-ignored upstream.
