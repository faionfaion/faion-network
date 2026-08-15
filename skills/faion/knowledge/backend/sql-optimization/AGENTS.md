# SQL Optimization

## Summary

**One-sentence:** Produces a SQL optimization report (EXPLAIN ANALYZE evidence, index recommendations, query rewrites, before/after timings) for the top resource-consuming queries.

**One-paragraph:** SQL optimization improves database queries by measuring with EXPLAIN ANALYZE first, optimizing high-impact queries (frequent or resource-heavy), respecting index trade-offs (reads vs writes), and reducing data movement (filter early, fetch only needed columns). Connection pooling, caching, and materialized views complete the picture.

**Ефективно для:**

- Slow query alerts — EXPLAIN ANALYZE замість здогадок.
- Високочастотні запити (10K/день) важливіші за нічний batch.
- Composite + covering + partial індекси під реальні фільтри.
- Connection pooling + streaming для memory-bounded read paths.

## Applies If (ALL must hold)

- Slow query complaints from users or monitoring alerts.
- Database CPU or I/O consistently high (resource bottleneck).
- Application response times degrade under load.
- Before deploying features with unknown perf characteristics.

## Skip If (ANY kills it)

- Premature optimization before profiling shows the actual bottleneck.
- Over-indexing without a measured read-vs-write trade-off.
- Replacing simple working queries with complex rewrites without a benchmark.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Query + production-sized dataset | SQL + schema | service / staging DB |
| EXPLAIN ANALYZE output | text/JSON | psql / MySQL CLI |
| Slow query log threshold | ms value | ops decision |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[database-design]] | Schema shape (PK, FK, normalization) is the precondition for index choices |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 13 testable rules + skip gate: EXPLAIN first, rank by total_time, estimate skew, refresh stats, index cost, composite ordering, covering index, reduce data movement, no subquery in SELECT, cursor pagination, materialized views, pooling + streaming, regression gate | ~1900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: no measurement, wrong target, SELECT * leak, stale stats, estimate skew ignored, composite order reversed, subquery in SELECT | ~1300 |
| `content/04-procedure.xml` | essential | 7 steps: rank → baseline plan → investigate skew → propose → apply and re-measure → regression gate → ship with CONCURRENTLY | ~1100 |
| `content/05-examples.xml` | medium | One fully-worked example matching the output schema, a narrated orders-list pass, and an index-by-vibes counter-example | ~1100 |
| `content/06-decision-tree.xml` | essential | Routing tree: preconditions → plan captured → estimate skew → pagination / subquery / scan type / write mix → rule id | ~750 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `collect-explain-analyze` | haiku | Mechanical capture of EXPLAIN (ANALYZE, BUFFERS) output. |
| `propose-indexes-and-rewrites` | sonnet | Per-query judgment on composite/covering/partial indexes. |
| `synthesize-report` | sonnet | Compose the before/after report. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sql-optimization-report.md` | Markdown skeleton for the optimization report (per-query before/after). |
| `templates/sql-optimization-report.json` | JSON skeleton matching the output contract. |
| `templates/create_index_concurrently.sql` | Non-blocking index creation + the INVALID-index check + the EXPLAIN that proves the planner uses it. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sql-optimization.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[database-design]]
- [[caching-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. Tree picks between adding an index, rewriting the query, or escalating to caching / materialized view based on plan + workload characteristics.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/sql-optimization-report.json`

```json
{
  "report_id": "sql-opt-2026-05-23",
  "queries": [],
  "index_changes": {
    "added": [],
    "dropped": []
  },
  "explain_analyze_present": true,
  "net_p95_improvement_pct": 0
}
```

### `templates/create_index_concurrently.sql`

```sql
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_orders_tenant_created_id
  ON orders (tenant_id, created_at DESC, id);
-- Equality column (tenant_id) first, range/sort column last: reversing this
-- makes the index unusable for the tenant_id predicate.

-- A CONCURRENTLY build that fails leaves an INVALID index behind. Check and rebuild:
--   SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;
--   REINDEX INDEX CONCURRENTLY ix_orders_tenant_created_id;

-- Confirm the planner actually picks it up — this output is the report's after_plan:
EXPLAIN (ANALYZE, BUFFERS)
  SELECT id, created_at FROM orders
   WHERE tenant_id = 'X'
   ORDER BY created_at DESC, id DESC
   LIMIT 50;
```
