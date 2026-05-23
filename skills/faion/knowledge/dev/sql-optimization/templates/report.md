<!-- purpose: Markdown skeleton for an SQL-optimisation report. -->
<!-- consumes: see content/02-output-contract.xml inputs for sql-optimization -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

# SQL Optimisation Report

- query_id: REPLACE
- date: REPLACE
- sample_size: 50

## Baseline plan

```
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
  SELECT ...
```

```
<plan output>
```

Actual rows: REPLACE
Wall clock p95: REPLACE ms

## Applied change

- type: index_added
- statement: `CREATE INDEX CONCURRENTLY ix_... ON table (col1, col2 DESC, id);`

## After plan

```
<plan output>
```

Actual rows: REPLACE
Wall clock p95: REPLACE ms

## Delta

- wall_clock_delta_ms: REPLACE
- buffers reduced: REPLACE

## Decision

- merge: yes/no
- monitor: REPLACE
