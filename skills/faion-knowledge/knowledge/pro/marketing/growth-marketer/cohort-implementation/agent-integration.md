# Agent Integration — Cohort Analysis Implementation

## When to use
- You have completed the framing in `cohort-basics` and need to ship cohort tables, dashboards, and refresh jobs in production.
- Migrating from ad-hoc analytics-tool reports (Mixpanel / Amplitude built-ins) to warehouse-native cohort models in BigQuery / Snowflake / Redshift / Postgres.
- Building executive dashboards that must refresh daily and survive schema changes (need dbt tests, not hand-written SQL files).
- Embedding cohort tables into a product analytics surface (Metabase / Looker / Mode / Hex / internal BI).

## When NOT to use
- Pre-instrumentation: events are not consistent or `signup_date` is unreliable. Fix the data first.
- Tiny scale (< few thousand users) — use the analytics-tool built-in or a notebook; production pipeline overhead is not justified.
- One-off investigation that will not be re-run — stop at a SQL notebook, do not productionize.

## Where it fails / limitations
- `LEFT JOIN events e ON c.user_id = e.user_id AND e.event_date >= c.signup_date` blows up on warehouses with billions of rows; partition pruning and clustering are required.
- Materialized views (BigQuery `CREATE MATERIALIZED VIEW`) have allowlisted aggregation patterns; complex `DATEDIFF` + `WHERE IN (...)` predicates may force a full-refresh model.
- Time-zones: signup at user-local time, events at UTC — naive `DATE_TRUNC('week', signup_date)` mis-buckets users near boundaries.
- Behavioral cohort queries are fragile to schema drift (new `event_type` values, renamed feature flags). Schema tests must run alongside.
- Pivoting wide cohort tables in SQL is verbose; downstream BI tools usually want long-format with explicit `cohort, day_offset, retention_pct` rows.
- Heatmap visualizations from naive matplotlib become unreadable past 30 cohorts × 12 columns; use Looker / Hex with tooltips, not static PNGs.

## Agentic workflow
Use subagents to (1) author dbt models from a cohort spec, (2) write tests (`unique`, `not_null`, `relationships`, plus custom retention-pct sanity bounds), (3) propose materialization strategy (view / table / incremental / materialized view), and (4) generate the BI dashboard JSON / LookML / Hex notebook. The agent never edits production warehouse directly — it produces a PR against the dbt repo and a Looker/Hex artifact for review.

### Recommended subagents
- `data-engineer` / `bi-engineer` (sonnet) — dbt models, incremental logic, partitioning.
- `data-analyst` (sonnet) — query correctness, retention-pct bounds, sample-size guards.
- `dashboard-author` (sonnet) — Metabase/Looker/Hex artifact generation.
- `qa-data` (sonnet) — backfill validation against a golden cohort week.

### Prompt pattern
```
Input: warehouse=BigQuery; tables analytics.users(user_id, signup_date_utc, signup_tz),
       analytics.events(user_id, event_type, event_ts_utc); retention_metric=login
Goal: dbt incremental model 'cohort_retention_weekly' with day_offsets [1,7,14,30,60,90]
      partitioned by cohort_week, clustered by user_id; tests for not_null, retention_pct between 0 and 100,
      cohort_size > 0
Output: 1) models/cohort_retention_weekly.sql, 2) schema.yml with tests,
        3) Looker view + explore stub
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt-core` + adapter | Cohort models, tests, docs | `pip install dbt-bigquery` (or snowflake/redshift) |
| `bq` (BigQuery) | Run, schedule, materialize cohort views | `gcloud components install bq` |
| `snowsql` | Snowflake runner for cohort SQL | https://docs.snowflake.com/en/user-guide/snowsql |
| `duckdb` CLI | Local prototyping on Parquet/CSV before warehouse push | `brew install duckdb` |
| `pandas` + `pyarrow` + `seaborn` | Notebook prototypes, heatmaps | `pip install pandas pyarrow seaborn` |
| `metabase-api` | Programmatic dashboard creation | `pip install metabase-api` |
| `lkml` | Generate / parse LookML for cohort views | `pip install lkml` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BigQuery | SaaS | Yes — REST + bq | Free quota, materialized views, partitioning |
| Snowflake | SaaS | Yes — REST + snowsql | Snowpark optional, native dbt support |
| Redshift | SaaS | Yes — REST + psql | Materialized views with refresh cadence |
| Databricks | SaaS | Yes — REST + Python SDK | Cohorts in Spark / SQL warehouses |
| dbt Cloud | SaaS | Yes — REST + GitOps | Scheduled runs, lineage, tests |
| Metabase | OSS | Yes — REST | Lightweight cohort dashboards |
| Looker | SaaS | Yes — content API + LookML | Strong for governance |
| Mode / Hex | SaaS | Yes — REST | Notebook + dashboard hybrid |
| Amplitude / Mixpanel / PostHog | SaaS / OSS | Yes — REST | Built-in retention reports as fallback |

## Templates & scripts
See `README.md` for canonical SQL (basic / behavioral / feature-cohort) and pandas variants. The README ships a daily refresh in `schedule + while True` — replace that with cron / Airflow / dbt Cloud / Cloud Scheduler in production. Skeleton dbt model that works on BigQuery and Snowflake:

```sql
-- models/marts/growth/cohort_retention_weekly.sql
{{ config(
    materialized='incremental',
    unique_key=['cohort_week','day_offset','user_id'],
    partition_by={'field':'cohort_week','data_type':'date'},
    cluster_by=['user_id']
) }}
WITH users AS (
  SELECT user_id,
         CAST(DATE_TRUNC(DATE(signup_ts_utc), WEEK(MONDAY)) AS DATE) AS cohort_week,
         signup_ts_utc
    FROM {{ ref('stg_users') }}
    {% if is_incremental() %}
      WHERE signup_ts_utc >= (SELECT MAX(signup_ts_utc) FROM {{ this }}) - INTERVAL 90 DAY
    {% endif %}
),
events AS (
  SELECT user_id, event_ts_utc
    FROM {{ ref('stg_events') }}
   WHERE event_type = 'login'
)
SELECT u.cohort_week,
       u.user_id,
       DATE_DIFF(DATE(e.event_ts_utc), DATE(u.signup_ts_utc), DAY) AS day_offset
  FROM users u
  JOIN events e USING (user_id)
 WHERE e.event_ts_utc >= u.signup_ts_utc
   AND DATE_DIFF(DATE(e.event_ts_utc), DATE(u.signup_ts_utc), DAY) IN (1,7,14,30,60,90)
```

```yaml
# models/marts/growth/schema.yml
version: 2
models:
  - name: cohort_retention_weekly
    columns:
      - name: cohort_week
        tests: [not_null]
      - name: user_id
        tests: [not_null]
      - name: day_offset
        tests:
          - accepted_values: { values: [1,7,14,30,60,90] }
```

## Best practices
- Use `COUNT(DISTINCT user_id)` not `COUNT(*)` — duplicate events inflate retention.
- Always store cohort tables as long-format (`cohort, day_offset, retention_pct`) and pivot in BI; pivoting in SQL kills schema flexibility.
- Materialize cohort_size as a column on every row — downstream tools should never recompute it.
- Backfill into a partitioned table; do not rebuild the whole table on every run once you cross 100M rows.
- Test retention_pct ∈ [0, 100] and cohort_size > 0 with dbt tests — these catch JOIN bugs and survivorship filters early.
- Pin the retention metric definition in the model's description; a silent change from `login` to `core_action` invalidates all historical comparisons.
- For analytics-tool exports (Mixpanel / Amplitude), validate that the warehouse model matches the tool's number to within 1pp before trusting the dashboard.

## AI-agent gotchas
- LLMs love to write `DATEDIFF(day, ...)` even on warehouses where the canonical signature is `DATE_DIFF(end, start, DAY)` (BigQuery) or `DATEDIFF(day, start, end)` (Snowflake/Redshift). Specify the warehouse in the prompt.
- Time-zone bugs: the agent will silently swap `signup_date` with `signup_ts_utc` and break downstream comparisons. Force one canonical column per concept.
- "Materialized view" suggestions from LLMs ignore engine constraints (BQ has limited DML refresh, Snowflake materialized views cost differently). Validate the materialization choice against engine docs.
- Survivorship leaks via `INNER JOIN` on activity tables — agents that omit `LEFT JOIN` will under-count cohort_size.
- Visualizations: matplotlib heatmaps from agents bake hard-coded `vmin/vmax`; insist on data-driven scales or quantiles.
- Schedulers: the `schedule + while True` recipe in the README is fine for dev but agents should not paste it into production code. Substitute Airflow DAG / Cloud Scheduler / dbt Cloud job.
- Privacy: behavioral cohort queries that join on email or unhashed PII bypass anonymization controls. Force agents to use `user_id` only.

## References
- Brian Balfour, "Retention deep dive" — https://brianbalfour.com
- dbt Labs, "How we structure our dbt projects" — https://docs.getdbt.com/best-practices
- BigQuery materialized views — https://cloud.google.com/bigquery/docs/materialized-views-intro
- Snowflake retention/cohort patterns — https://docs.snowflake.com
- Mode Analytics, "Cohort analysis with SQL" — https://mode.com/sql-tutorial/sql-cohort-analysis
- Amplitude / Mixpanel retention docs — https://amplitude.com / https://docs.mixpanel.com
- Andrew Chen, "Power user curve" — https://andrewchen.com/power-user-curve
