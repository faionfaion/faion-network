-- purpose: SQL query: list tables with RLS off + their owner.
-- consumes: see content/02-output-contract.xml inputs for supabase-mvp-stack
-- produces: artefact conforming to content/02-output-contract.xml
-- depends-on: content/01-core-rules.xml + content/04-procedure.xml
-- token-budget-impact: ~200-700 tokens when loaded as context

SELECT n.nspname AS schema,
       c.relname AS table,
       c.relowner::regrole AS owner,
       c.relrowsecurity AS rls_enabled
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r'
  AND n.nspname NOT IN ('pg_catalog', 'information_schema')
  AND c.relrowsecurity = false
ORDER BY schema, table;
