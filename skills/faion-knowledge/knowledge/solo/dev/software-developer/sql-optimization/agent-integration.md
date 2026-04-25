# Agent Integration — SQL Optimization

## When to use
- A specific query is on the slow-query log or APM "top N by total time" — clear target, clear baseline.
- Database CPU / IO is consistently above headroom (~70%) and you need to find the offending workload.
- Pre-launch load test surfaces P95 latency regressions tied to one or two queries.
- Pagination, search, or aggregation feature is slated to scale 10x in the next quarter and needs proactive tuning.
- Migrating storage (Postgres major upgrade, RDS class change, Aurora-to-Postgres) — re-baseline before/after.
- LLM-driven query authoring: agents need a strict pipeline (EXPLAIN → index check → rewrite → benchmark) to avoid invented optimizations.

## When NOT to use
- The bottleneck is application-level (N+1 ORM calls, serialization, missing cache) — fix that first; query tuning won't help.
- Tiny tables (< 10k rows) where seq scan is already faster than any index — the planner is right; leave it alone.
- One-off analytical queries running once a quarter — engineer time is more expensive than the query.
- Multi-tenant SaaS with extreme schema variance per tenant — invest in partitioning / sharding strategy first.
- Without a representative dataset and workload (`pg_stat_statements`, production-like volume) — you'll optimize the wrong thing.

## Where it fails / limitations
- EXPLAIN without ANALYZE lies — it shows estimates, not actual rows / time. Agents that read plans without execution stats produce false positives.
- Index advice in isolation is dangerous: every new index slows writes, bloats WAL, and competes for buffer cache.
- Plan instability across data growth: a query plan that's optimal at 1M rows flips at 10M and degrades silently.
- Statistics drift: planner needs `ANALYZE`; stale stats produce bad plans regardless of indexes.
- Cross-DB advice doesn't transfer: Postgres EXPLAIN ≠ MySQL EXPLAIN ≠ SQL Server execution plan; agents trained on Postgres patterns will misadvise on MySQL.
- Optimizer hints (`/*+ INDEX(...) */`) are vendor-specific and a maintenance trap; readers don't see why.
- Connection pooling, prepared-statement caching, and wire-protocol overhead can dominate query cost — pure SQL tuning misses these.
- Agents readily suggest materialized views without operational plan (refresh cadence, lock window, replication lag).

## Agentic workflow
A four-step loop, each step gated. (1) **Identify** — an agent pulls top queries from `pg_stat_statements` (or `slow_log`), ranked by `total_exec_time`. (2) **Diagnose** — for each top query, run `EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT JSON)` against a prod-shaped staging DB; feed the JSON plan to a planner-reading agent. (3) **Propose** — generate index / rewrite / partition candidates with cost estimates and write impact; emit each candidate as an SDD task. (4) **Validate** — apply candidate to staging, re-run EXPLAIN, compare plan + latency + buffer hits; require improvement of ≥30% on the metric of interest before merge. Schedule re-baseline weekly via cron. Human-approve any DDL change in prod (CREATE INDEX CONCURRENTLY, REFRESH MATERIALIZED VIEW).

### Recommended subagents
- `faion-sdd-executor-agent` — gate: every DDL change ships with a migration, a rollback, and benchmark numbers.
- A **plan-reader** subagent (worth creating): system prompt = "given EXPLAIN JSON, list bottlenecks (seq scan on >100k rows, hash join with disk spill, nested loop with high outer rows, sort with disk)". Cheap (haiku) and runs on every diff.
- A **migration-author** subagent: emits `CREATE INDEX CONCURRENTLY`, `ALTER TABLE ... SET STATISTICS`, partition DDL with safety checks (IF NOT EXISTS, lock_timeout, statement_timeout).
- `faion-feature-executor` (skill) — sequences identify → diagnose → propose → validate as ordered tasks.

### Prompt pattern
Plan reading:
```
Input: EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) output. Output: a
markdown table with one row per node having any of: actual_rows >
estimate*10, Seq Scan with rows > 50000, Sort with "Disk:" present,
Nested Loop with outer rows > 1000, BitmapHeapScan with high "Recheck
Cond" rejects. For each, suggest a remediation (index, rewrite, raise
work_mem, partition). No invention; cite node IDs.
```

Index-impact pre-flight:
```
Proposed index: CREATE INDEX <name> ON <table> (<cols>) [INCLUDE
<...>] [WHERE <...>]. Estimate write amplification by listing every
INSERT/UPDATE/DELETE statement against <table> in the codebase
(grep). Reject the proposal if write QPS * extra_index_cost_ms > read
QPS * query_savings_ms. Output JSON {decision, rationale, evidence}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `psql` + `\timing on` | Native Postgres CLI; baseline tool | `apt install postgresql-client` |
| `pgbadger` | Slow-log analyzer with HTML reports | https://pgbadger.darold.net |
| `pgmustard` (CLI / web) | EXPLAIN ANALYZE visualization + advice | https://www.pgmustard.com |
| `explain.dalibo.com` | Web visualizer for plans (also self-hostable) | https://explain.dalibo.com |
| `hyperfine` | Repeated benchmark with statistical comparison | `cargo install hyperfine` |
| `pgbench` / `sysbench` | Synthetic workload + scale-out testing | https://www.postgresql.org/docs/current/pgbench.html |
| `pt-query-digest` (Percona) | MySQL slow-log analyzer | https://docs.percona.com/percona-toolkit/ |
| `pg_stat_statements` | Built-in query stats extension | enable in `shared_preload_libraries` |
| `auto_explain` | Auto-log slow plans | enable in `postgresql.conf` |
| `hypopg` | Hypothetical indexes — test impact without creating | `CREATE EXTENSION hypopg;` |
| `dexter` | Index advisor based on `pg_stat_statements` | https://github.com/ankane/dexter |
| `sqlfluff` | SQL linter (style, dialect, anti-patterns) | `pip install sqlfluff` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| pganalyze | SaaS | Yes — REST API | Best-in-class query / index advisor; agent-callable. |
| Datadog DBM | SaaS | Yes — API | Query insights with execution plans and historical stats. |
| New Relic Query Performance | SaaS | Yes — API | Spans + plans correlated with traces. |
| EverSQL | SaaS | Yes — REST | SQL rewrite + index advisor; CI integration. |
| Aurora Performance Insights | SaaS (AWS) | Yes — CloudWatch API | Wait-event analysis. |
| pgHero | OSS | Partial — UI | Self-hosted dashboard; no rich API. |
| Percona Monitoring and Management | OSS | Yes — API | Postgres + MySQL monitoring + slow-log analytics. |
| Metabase / Redash | OSS | Yes — API | Run + diff queries; useful for benchmarking. |
| OtterTune | SaaS | Yes — API | ML-based parameter tuning (also tunes queries). |

## Templates & scripts
See `templates.md` and `examples.md`. Inline candidate-finder (≤50 lines):

```bash
#!/usr/bin/env bash
# top-queries.sh — rank queries by total time and emit a tuning ticket per top-N.
set -euo pipefail
DB="${1:?usage: top-queries.sh <conn-string> [N]}"
N="${2:-10}"

psql "$DB" -X -A -F $'\t' -c "
  SELECT
    queryid, calls, mean_exec_time::int AS mean_ms,
    total_exec_time::int AS total_ms,
    rows / NULLIF(calls,0) AS rows_per_call,
    LEFT(query, 200) AS sql_preview
  FROM pg_stat_statements
  WHERE query !~* '^(SET |COMMIT|BEGIN|ROLLBACK|EXPLAIN)'
  ORDER BY total_exec_time DESC
  LIMIT $N;
" | awk -F '\t' 'NR>1 {
  printf("---\nQUERY %s\n calls=%s mean=%sms total=%sms rows/call=%s\n  %s\n", $1,$2,$3,$4,$5,$6)
}' > top.txt

# For each, ask the plan-reader agent for advice.
while read -r line; do
  qid=$(awk '/^QUERY/ {print $2}' <<<"$line")
  [[ -z "$qid" ]] && continue
  sql=$(psql "$DB" -X -A -t -c "SELECT query FROM pg_stat_statements WHERE queryid=$qid")
  plan=$(psql "$DB" -X -A -t -c "EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) $sql")
  printf '{"queryid":%s,"sql":%s,"plan":%s}\n' \
    "$qid" "$(jq -Rn --arg s "$sql" '$s')" "$plan" \
    >> plans.ndjson
done < top.txt
```

Pipe `plans.ndjson` to the plan-reader agent, then open SDD tasks per recommendation.

## Best practices
- Always profile against production-shaped data and concurrency. Tuning on a 10k-row dev DB is theater.
- Use `EXPLAIN (ANALYZE, BUFFERS, VERBOSE)` — buffer counts catch IO problems plan times miss.
- Add covering / partial indexes only when read frequency × savings > write frequency × cost. Use `hypopg` to estimate before `CREATE INDEX`.
- Use `CREATE INDEX CONCURRENTLY` in prod, with `lock_timeout` and `statement_timeout`. Never naked `CREATE INDEX` on a hot table.
- Switch deep pagination from `OFFSET` to keyset / cursor when collection size > ~10k rows.
- Replace `LIKE '%foo%'` with proper full-text (`tsvector` + GIN) or trigram (`pg_trgm`) — ad-hoc LIKE doesn't scale.
- Refresh `ANALYZE` after big data changes; use `ALTER TABLE ... SET STATISTICS` on skewed columns.
- Connection pooling (PgBouncer in transaction mode) is mandatory above ~100 connections; without it tuning gains are dwarfed by connection overhead.
- For aggregations on growing tables, materialized views with `REFRESH ... CONCURRENTLY` and a refresh schedule beat live `GROUP BY`.
- Treat schema changes as code: migrations + rollback + benchmark numbers in the PR.

## AI-agent gotchas
- Agents propose indexes on every `WHERE` column without considering write amplification. Always run the impact pre-flight.
- LLMs read estimated row counts as ground truth; force them to use `actual_rows` from EXPLAIN ANALYZE.
- Plan-reading agents miss disk-spill (`Sort Method: external merge Disk: ...`) because the line is buried; provide a checklist of red-flag substrings in the prompt.
- Agents propose composite indexes with wrong column order — they ignore selectivity. Require the agent to cite `n_distinct` from `pg_stats` for each column.
- Suggesting `ORDER BY ... LIMIT` "fixes" without verifying actual cardinality leads to plans that flip under data growth. Validate with twice the data volume.
- LLMs confidently mix dialects (Postgres syntax in MySQL solution). Pin the dialect in the system prompt and reject foreign syntax.
- Agents propose materialized views without a refresh strategy; require the proposal to include refresh cadence, lock impact, and replication-lag implications.
- Hint-injection: agents add `/*+ INDEX(t, idx) */` and other vendor hints which break on engine upgrades. Disallow hints unless explicitly approved.
- Human-in-loop checkpoint: every prod DDL change (index, partition, materialized view, column type change) must be human-approved with the EXPLAIN diff and benchmark attached.
- Agents skip the rollback section. Mandate that every migration includes the inverse DDL.

## References
- "Use The Index, Luke" — Markus Winand. https://use-the-index-luke.com/
- "PostgreSQL Performance Tips" (official). https://www.postgresql.org/docs/current/performance-tips.html
- Bruce Momjian — "Explaining the Postgres Query Optimizer". https://momjian.us/main/writings/pgsql/optimizer.pdf
- "High Performance MySQL", 4e — Schwartz et al. (O'Reilly, 2021).
- pganalyze blog — https://pganalyze.com/blog
- Citus / Microsoft PG team blog — https://www.citusdata.com/blog/
- Percona Database Performance blog — https://www.percona.com/blog/category/postgresql/
- Sibling methodologies: `database-design/`, `nosql-patterns/`, `caching-strategy/`, `performance-testing/`.
