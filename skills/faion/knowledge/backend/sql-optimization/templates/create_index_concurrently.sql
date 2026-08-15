-- purpose: Non-blocking composite index creation with the EXPLAIN check that proves the planner uses it.
-- consumes: the table + predicate shape identified in the baseline plan.
-- produces: a migration statement plus the verification query for the report's after_plan.
-- depends-on: content/01-core-rules.xml rules composite-index-ordering and explain-before-change.
-- token-budget-impact: ~200 tokens when loaded as context.

-- Idempotent, non-blocking, safe on a live table.
-- CONCURRENTLY cannot run inside a transaction block — in Django, mark the
-- migration atomic = False; in raw psql, run it outside BEGIN.
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
