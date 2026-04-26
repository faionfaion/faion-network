# Agent Integration — SQL Optimization

## When to use
- Production slow-query alerts (Datadog DBM, pg_stat_statements top-N, slow log) where a measurable minority of queries cause the majority of pain.
- Pre-launch load test reveals p99 latency dominated by DB time and `EXPLAIN ANALYZE` shows seq scans on large tables, sort spilling to disk, or hash joins on huge sets.
- Schema migration adding indexes; verifying the new index is actually used by the planner and doesn't regress existing plans.
- Periodic audits (quarterly) on hot tables: index bloat, missing partial indexes, dead tuples, autovacuum lag.
- Writing new features against a non-trivial data model where you want to validate the planned query shape before code is merged.

## When NOT to use
- Prematurely optimising before profiling — index spam slows writes and confuses the planner.
- ORM problems that aren't SQL problems (N+1 from lazy loading, fetch joins missing). Fix at the ORM first; the SQL is a symptom.
- OLAP-style aggregates over hundreds of millions of rows on an OLTP DB. Move to a warehouse / columnar store; SQL tuning won't save you.
- Tiny tables (<10k rows) where seq scans are objectively fine; optimising is busywork.
- Where the bottleneck is connection-pool exhaustion or row-level lock contention, not query plan. Tune pgbouncer / isolation level first.

## Where it fails / limitations
- **Stats drift.** A perfect plan today becomes a sequential scan tomorrow because `ANALYZE` ran on a 5%-sample of a now-100M-row table. Without scheduled `ANALYZE` and statistics-target tuning, plans degrade silently.
- **Index hint over-reach.** Postgres has no `USE INDEX`; agents try to force plans with `SET enable_seqscan = off` in app code. Brittle; revisit the data shape instead.
- **Composite index column order.** Equality columns first, then range. The README example is right; agents flip the order and the index is unused.
- **`SELECT *`.** README implies it; production needs explicit columns to enable index-only scans (`INCLUDE`-covering).
- **`OFFSET` pagination on large sets.** `OFFSET 100000` reads + discards 100k rows. Switch to keyset/seek pagination.
- **Implicit type casts.** `WHERE id = '123'` on `bigint id` casts every row; index unused. Postgres EXPLAIN says `Filter`, not `Index Cond`.
- **`OR` across columns.** Disables single-index plan; rewrite as `UNION ALL` of two indexed queries or use a partial/expression index.
- **Function on indexed column.** `WHERE LOWER(email) = ?` with a btree on `email` doesn't use the index; need `LOWER(email)` expression index or store normalized form.
- **Bloat ≠ indexed.** `pg_stat_user_indexes.idx_scan` near zero means the index is unused; carrying it costs writes.
- **Transactional read of a stale plan.** Long transactions hold MVCC snapshots; queries plan against old stats and produce surprises.
- **Cross-DB advice doesn't transfer.** MySQL InnoDB, Postgres, SQL Server, Oracle each have different planners; README is implicitly Postgres-flavored. Agents apply Postgres tactics to MySQL and break.

## Agentic workflow
Drive query optimization as a five-stage pipeline: (1) a discovery agent pulls top-N slow queries from `pg_stat_statements` (or DBM) and groups by normalized SQL fingerprint; (2) a plan agent runs `EXPLAIN (ANALYZE, BUFFERS)` against representative bind values and extracts plan shape (seq vs index scan, join type, sort/spill, rows estimate vs actual); (3) a hypothesis agent proposes ≤2 fixes per query (rewrite, index add, partition/CTE inlining, denormalize) with cost/benefit; (4) a change agent emits the migration (CREATE INDEX CONCURRENTLY, ANALYZE, query rewrite) plus rollback; (5) a verification agent re-runs EXPLAIN and confirms latency in staging under realistic load (k6/pgbench), then ships to prod. Persist the slow-query catalogue + applied fixes in `.aidocs/product_docs/sql-perf.md` so the next quarter's audit doesn't restart from scratch. Pair with `pro/dev/backend-systems/database-design/` for schema-level fixes.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task = one query optimization (plan capture + fix + verification). Opus when fixes touch schema; sonnet for query rewrites.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — `EXPLAIN` output and fixture data routinely include emails, names, addresses; scrub before pasting into commit messages or issues.
- A **sql-review-agent** (worth adding under `agents/`): linter for `SELECT *` in production code paths, `OFFSET >1000`, missing `LIMIT` on list endpoints, implicit casts, functions on indexed columns, indexes added without `CONCURRENTLY`, indexes added without `pg_stat_user_indexes` review of redundant indexes.

### Prompt pattern
Plan analysis:
```
You are a SQL optimizer. Given the query <q> and the EXPLAIN
(ANALYZE, BUFFERS) output <plan>, report:
  - rows estimated vs actual at each node,
  - the dominant cost node,
  - whether the bottleneck is IO, CPU, sort, hash spill, or network,
  - up to 2 hypotheses for improvement (index | rewrite | denormalize
    | partition | materialize),
  - for each hypothesis: write/read trade-off, side effects,
    rollback plan.
Reject hypotheses that disable enable_* GUCs in app code.
```

Anti-pattern review:
```
Review a SQL/migration PR. Flag:
(1) SELECT * in user-facing query path,
(2) OFFSET > 1000 in pagination logic,
(3) WHERE function(indexed_col) without an expression index,
(4) implicit casts (e.g., bigint = text literal),
(5) CREATE INDEX without CONCURRENTLY on a populated table > 1M rows,
(6) new index that overlaps an existing index prefix,
(7) ORM call in a hot path without .includes/.eager_load equivalent,
(8) missing LIMIT on a list endpoint backing-query.
Cite file:line. No fixes — only flags.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `psql \timing` + `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` | Plan + actual runtime | bundled |
| `pg_stat_statements` | Top-N slow / frequent queries | `CREATE EXTENSION pg_stat_statements` |
| `pgbadger` | Postgres log analysis (top queries, error trends) | https://pgbadger.darold.net |
| `pgbouncer` / `pgcat` | Connection pooling — orthogonal to query plans but often the real bottleneck | https://www.pgbouncer.org / https://github.com/postgresml/pgcat |
| `pgmustard` | Pretty EXPLAIN visualiser + recommendations | https://www.pgmustard.com |
| `explain.depesz.com` | Free EXPLAIN visualiser | https://explain.depesz.com |
| `pev2` | Plan visualiser (interactive tree) | https://github.com/dalibo/pev2 |
| `pgbench` | Built-in load generator | bundled |
| `hyperfine` | Wall-clock comparison harness for query iterations | https://github.com/sharkdp/hyperfine |
| `pgcli` / `usql` | Better REPL than `psql` for exploration | https://www.pgcli.com |
| `sqlfluff` | SQL linter with style + correctness rules | https://www.sqlfluff.com |
| `pganalyze` CLI | Query insights, index advisor | https://pganalyze.com |
| `pg_repack` | Online table/index rebuild without exclusive lock | https://github.com/reorg/pg_repack |
| `pgvector` advisors / `dexter` | Index suggester from `pg_stat_statements` | https://github.com/ankane/dexter |
| `mysqltuner` (MySQL equivalent) | Tuning suggestions | https://github.com/major/MySQLTuner-perl |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Datadog DBM / New Relic / SolarWinds DPA | SaaS | yes | Continuous query profiling; APIs for top-N. |
| pganalyze | SaaS | yes | First-class index/plan advisor; CLI + API. |
| Aiven / Supabase / Neon / Crunchy Bridge | SaaS | yes | Managed Postgres with built-in pg_stat_statements + advisor. |
| AWS Performance Insights | SaaS | yes | Top SQL by load; works on RDS/Aurora. |
| pgwatch2 / pgexporter + Grafana | OSS | yes | Self-hosted dashboards + alerts. |
| Percona Toolkit (`pt-query-digest`) | OSS | yes | MySQL slow log analysis. |
| Vitess | OSS | yes | If sharding is the answer; agents need careful prompts. |
| TimescaleDB / Citus | OSS | yes | If partitioning by time/tenant fixes the plan. |
| ParadeDB / pg_search | OSS | yes | If full-text patterns are the bottleneck and Postgres FTS isn't enough. |
| dbt + adapters | OSS / SaaS | yes | If the slow query is OLAP and belongs in a warehouse model. |

## Templates & scripts
README ships EXPLAIN guidance, index strategies, query rewrites. Add a perf-review SQL pack:

```sql
-- top 20 slowest queries (mean) past 24h
SELECT query, calls, mean_exec_time, total_exec_time, rows
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- unused indexes (candidates for drop)
SELECT s.schemaname, s.relname, s.indexrelname, s.idx_scan,
       pg_size_pretty(pg_relation_size(s.indexrelid)) AS size
FROM pg_stat_user_indexes s
JOIN pg_index i ON i.indexrelid = s.indexrelid
WHERE s.idx_scan = 0 AND NOT i.indisunique
ORDER BY pg_relation_size(s.indexrelid) DESC;

-- duplicate / overlapping indexes
SELECT a.schemaname, a.relname, a.indexrelname AS idx_a,
       b.indexrelname AS idx_b
FROM pg_stat_user_indexes a
JOIN pg_stat_user_indexes b USING (relid)
JOIN pg_index ia ON ia.indexrelid = a.indexrelid
JOIN pg_index ib ON ib.indexrelid = b.indexrelid
WHERE a.indexrelid < b.indexrelid
  AND ia.indkey::text LIKE ib.indkey::text || '%';

-- bloat hint
SELECT relname, n_live_tup, n_dead_tup,
       round(n_dead_tup::numeric / NULLIF(n_live_tup, 0) * 100, 2) AS dead_pct
FROM pg_stat_user_tables
ORDER BY dead_pct DESC NULLS LAST
LIMIT 20;
```

Inline EXPLAIN review prompt for an agent — keep alongside the migration:

```bash
#!/usr/bin/env bash
# explain-review.sh — capture before/after EXPLAIN for a migration
set -euo pipefail
db="${1:?usage: explain-review.sh DB QUERY_FILE}"
qfile="${2:?}"
echo "## BEFORE"
psql "$db" -X -c "EXPLAIN (ANALYZE, BUFFERS) $(cat "$qfile")"
echo
echo "Apply migration, then run:"
echo "  psql $db -f migration.sql"
echo
echo "## AFTER"
psql "$db" -X -c "EXPLAIN (ANALYZE, BUFFERS) $(cat "$qfile")"
```

## Best practices
- **Measure with production-like data.** Plan changes in staging with full-volume snapshot, not synthetic tiny dataset.
- **Plan reads + write trade-offs.** Each new index slows INSERT/UPDATE/DELETE on that table. Track `pg_stat_user_indexes.idx_scan` for 30 days before committing to keep an index.
- **`CREATE INDEX CONCURRENTLY`** on populated tables; never blocking lock in production.
- **Composite index column order = equality, range, sort.** Equality columns first; range columns next (only the leftmost range is index-usable); sort columns last to enable backward scans.
- **Covering indexes (`INCLUDE`)** for index-only scans on hot read paths.
- **Partial indexes** for hot subsets (`WHERE status = 'pending'`).
- **Keyset pagination** instead of `OFFSET` once you exceed page-30-ish.
- **`CTE` is an optimization fence** in older Postgres (<12); inlining via subqueries can change the plan substantially.
- **Avoid functions on indexed columns** — store normalized values or use expression indexes.
- **Track `n_distinct` and `correlation`** in `pg_stats`; raise statistics target on skewed columns to give the planner better selectivity estimates.
- **Autovacuum tuning per hot table.** Default scale-factors are wrong for very large tables; reduce `autovacuum_vacuum_scale_factor` for hot ones.
- **Prefer `array_agg` / `jsonb_agg` over N+1.** Single query with aggregation beats N round-trips most of the time.
- **`ORDER BY ... LIMIT` should match an index's order.** Otherwise expect a Sort node — fine on small N, painful on large.
- **Watch `Rows Removed by Filter`.** A high count means the access path returned too many rows; an index can help.
- **Don't trust the first plan.** Run EXPLAIN ANALYZE multiple times — buffer cache state matters.

## AI-agent gotchas
- **`SELECT *` reflex.** Agents copy `SELECT *` from notebooks. Force explicit column lists everywhere except admin tools.
- **Index per query.** Agents add a fresh index for every new query, accumulating overlapping indexes. Force a check against existing indexes before adding.
- **`USE INDEX`-style hints.** Agents try to force a plan with `enable_seqscan=off`. Block in app code; only allowed in DBA-only tooling.
- **`OFFSET` pagination.** Agents implement OFFSET-based list endpoints. Force keyset-based for any list expected to grow past a few pages.
- **Forgotten `ANALYZE` after backfill.** Agent backfills 50M rows; planner has stale stats. Force `ANALYZE table_name` in the migration footer.
- **Implicit cast in WHERE.** `WHERE id = $1` with `$1` bound as text against `bigint id`. Force typed parameter binding.
- **Function-call on indexed column.** `LOWER(email)` filter without an expression index. Lint or force the expression index.
- **Cross-DB advice.** Agent applies Postgres `INCLUDE` to MySQL, which doesn't have it. Pin DB engine + version in the prompt.
- **Index naming sprawl.** Agents emit `idx1`, `idx2`, `users_email_idx_v2`. Force a naming convention (`idx_<table>_<cols>__<purpose>`).
- **Skipping `EXPLAIN (BUFFERS)`.** Agent runs only `EXPLAIN ANALYZE`; misses cache-hit ratio. Always include `BUFFERS`.
- **Hallucinated EXPLAIN nodes.** Agents invent operators (`Range Scan`, `Skip Scan` in vanilla Postgres). Pin to the engine docs.
- **Human-in-loop on schema/index drops.** Removing an index ON a 1B-row table is a one-way door under load. Stop and ask.
- **Premature denormalization.** Agents add a redundant column "for speed" without query proof. Force a slow-query exhibit before approving.

## References
- "Use The Index, Luke!" — Markus Winand. https://use-the-index-luke.com
- Postgres docs — Performance Tips. https://www.postgresql.org/docs/current/performance-tips.html
- Postgres docs — Indexes. https://www.postgresql.org/docs/current/indexes.html
- pg_stat_statements docs. https://www.postgresql.org/docs/current/pgstatstatements.html
- pgmustard — EXPLAIN guide. https://www.pgmustard.com/docs/explain
- depesz — EXPLAIN articles. https://www.depesz.com/tag/explain/
- "High Performance MySQL," 4th ed. — Schwartz et al.
- pganalyze blog — Postgres tuning case studies. https://pganalyze.com/blog
- Crunchy Data blog. https://www.crunchydata.com/blog
- Sibling methodologies in this repo: `pro/dev/backend-systems/database-design/`, `pro/dev/backend-systems/nosql-patterns/`, `pro/dev/backend-systems/caching-strategy/`.
