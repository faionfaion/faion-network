<!-- purpose: Index creation snippet using CONCURRENTLY + REINDEX guidance. -->
<!-- consumes: see content/02-output-contract.xml inputs for sql-optimization -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

-- Idempotent index creation; non-blocking; safe for production
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_orders_tenant_created_id
  ON orders (tenant_id, created_at DESC, id);

-- Confirm planner uses it:
EXPLAIN (ANALYZE, BUFFERS)
  SELECT id, created_at FROM orders
   WHERE tenant_id = 'X'
   ORDER BY created_at DESC, id DESC
   LIMIT 50;
