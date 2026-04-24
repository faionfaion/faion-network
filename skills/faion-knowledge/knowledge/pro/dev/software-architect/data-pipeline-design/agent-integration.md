# Agent Integration — Data Pipeline Design

## When to use
- Greenfield ETL/ELT design where the agent must pick batch vs streaming, ingestion tools, and warehouse.
- Generating Airflow/Dagster/Prefect DAGs and dbt models from a spec (volume, latency, sources, sinks).
- Code review of pipeline PRs: idempotency, DLQ wiring, schema-evolution risk, cost regression.
- Authoring Great Expectations / Soda / dbt test suites for an existing dataset.
- Migrating ETL → ELT (lift-and-shift to Snowflake/BigQuery/Databricks) with medallion layout.
- Producing pipeline runbooks (lag thresholds, replay procedures) from existing infra.

## When NOT to use
- Picking the warehouse vendor itself — needs procurement/legal context the agent does not have.
- Real-time SLA tuning in production without metrics access (Kafka lag, p99 latency).
- Pipelines touching regulated data (HIPAA/PCI) without a human compliance reviewer in the loop.
- One-off CSV imports that fit in a single SQL script — orchestration is overhead.

## Where it fails / limitations
- LLMs hallucinate operator names (`KubernetesPodOperator` vs `KubernetesJobOperator`); always pin Airflow / provider versions in the prompt.
- dbt model graphs over ~50 nodes overflow context — chunk by domain/folder before generating.
- Schema-evolution reasoning is weak; the model will silently break downstream consumers when a column type changes.
- Cost estimates ($/TB scanned, slot-hours) are guesses — require a human FinOps check.
- Streaming exactly-once semantics: model frequently confuses Kafka transactions with consumer-side dedup; demand explicit idempotency keys.

## Agentic workflow
Drive the design with three sequential subagent passes: (1) a planner that emits a pipeline blueprint (sources, layers, orchestrator, quality gates) from the brief, (2) a coder that materializes Airflow/Dagster DAGs + dbt models against the planner's contract, (3) a reviewer that runs `dbt parse`, `dbt test`, `airflow dags test`, and grep-checks for DLQ + retry config. Keep planner on Opus, coder on Sonnet, reviewer on Sonnet. Use one Bronze/Silver/Gold pass per layer to keep contexts small.

### Recommended subagents
- `pipeline-architect` (Opus) — pipeline-type selection, orchestrator pick, medallion layout, trade-off memo.
- `etl-coder` (Sonnet) — generates DAGs, dbt models, Spark jobs from architect's contract.
- `data-quality-reviewer` (Sonnet) — drafts Great Expectations / dbt tests, audits DLQ + idempotency.
- `dbt-modeler` (Sonnet) — focused subagent for stg/int/mart layering and naming conventions.

### Prompt pattern
```
You are pipeline-architect. Inputs: sources={...}, daily_volume=200GB,
latency=15min, stack={Snowflake, dbt, Airflow}, compliance=GDPR.
Output strictly: 1) pipeline-type decision with rationale, 2) bronze/silver/gold
table list, 3) orchestrator DAG names + cadence, 4) DLQ + retry policy,
5) failure modes table. No code yet.
```

```
You are data-quality-reviewer. Diff: <patch>. For each new model emit dbt
tests (unique, not_null, accepted_values, relationships) and at least one
freshness/volume check. Reject the diff if no DLQ wiring on streaming sources.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `airflow` | DAG run/test/backfill | `pip install apache-airflow`; airflow.apache.org |
| `dagster` / `dagit` | Asset materialization, dev UI | `pip install dagster dagster-webserver`; docs.dagster.io |
| `prefect` | Flow runs, deployments | `pip install prefect`; docs.prefect.io |
| `dbt` (core/cloud) | SQL transformation, lineage, tests | `pip install dbt-core dbt-<adapter>`; docs.getdbt.com |
| `great_expectations` | Data quality suites | `pip install great_expectations`; greatexpectations.io |
| `soda-core` | YAML-first checks (SodaCL) | `pip install soda-core-<engine>`; docs.soda.io |
| `kafka-console-consumer` / `kcat` | Inspect topics, offsets, lag | apt/brew install `kcat` |
| `airbyte` CLI / API | Manage connectors, syncs | `octavia` CLI or REST; docs.airbyte.com |
| `meltano` | Singer-tap orchestration | `pip install meltano`; meltano.com |
| `spark-submit` / `pyspark` | Run Spark jobs | spark.apache.org |
| `databricks` CLI | Workspace, jobs, repos | `pip install databricks-cli`; databricks.com |
| `snowsql` / `bq` / `psql` | Warehouse SQL execution | per-vendor docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Airflow / MWAA / Composer | OSS + managed | Yes | DAGs as code; agent edits `.py` files in repo. |
| Dagster Cloud | SaaS + OSS | Yes | Asset-first model maps cleanly to LLM diffs. |
| Prefect Cloud | SaaS + OSS | Yes | Decorator API; minimal boilerplate to generate. |
| dbt Cloud | SaaS | Yes | Has REST + Discovery API for lineage queries. |
| Snowflake / BigQuery / Databricks | SaaS | Yes | Standard SQL + warehouse-native CLIs. |
| Airbyte / Fivetran / Stitch | SaaS + OSS | Partial | Connector picks need human review for billing. |
| Confluent Cloud / MSK | SaaS | Yes | REST + `confluent` CLI for topic ops. |
| Debezium | OSS | Yes | CDC connector configs are JSON — easy to template. |
| Monte Carlo / Metaplane / Bigeye | SaaS | Partial | Anomaly detection; agent consumes alerts, not config. |
| Atlan / Alation / DataHub | SaaS + OSS | Partial | Lineage read APIs are useful as agent inputs. |
| Apache Iceberg / Delta Lake | OSS | Yes | Lakehouse format; agent writes table specs in IaC. |

## Templates & scripts
See `templates.md` for full DAG/dbt/Spark snippets. Inline preflight check before letting an agent merge a pipeline PR:

```bash
#!/usr/bin/env bash
# pipeline-preflight.sh — run inside the project root
set -euo pipefail
dbt deps
dbt parse --no-version-check
dbt compile --no-version-check
dbt test --select state:modified+ --defer --state ./prod-manifest
airflow dags list-import-errors | tee /tmp/dag-errors.txt
test ! -s /tmp/dag-errors.txt
grep -RIn --include='*.py' -E 'retries\s*=\s*0' dags/ && {
  echo "ERROR: tasks with retries=0 detected"; exit 1; } || true
grep -RIn --include='*.py' -E 'on_failure_callback' dags/ >/dev/null || {
  echo "ERROR: no on_failure_callback wiring found"; exit 1; }
echo "preflight OK"
```

## Best practices
- Force the agent to emit the trade-off matrix (batch vs stream, ETL vs ELT) BEFORE writing code; keeps it from defaulting to Airflow+Snowflake reflexively.
- Bronze layer is append-only and schema-on-read; never let the agent transform on ingest.
- Pin every connector/operator version in the prompt — pipeline ecosystems break across minor versions.
- Generate idempotency keys at the source step, not in the sink; otherwise replay corrupts state.
- Demand a DLQ + replay runbook in the same PR as the new pipeline; no orphan pipelines.
- For dbt: enforce `stg_<source>__<entity>s.sql` naming and `materialized='incremental'` only when there is a strict watermark column.
- Wire `dbt source freshness` into the orchestrator, not just CI — staleness should page on-call.
- For streaming: agent must specify exactly-once semantics layer (Kafka tx vs consumer dedup table) — never both implicit.

## AI-agent gotchas
- LLMs default to overly-eager `dbt run --full-refresh` in generated CI; always constrain with `--select state:modified+`.
- Airflow `schedule_interval` vs `schedule` keyword changed in 2.4 → 3.0; pin version or the agent emits broken DAGs.
- Spark `spark.sql.shuffle.partitions` defaults are wrong for cloud — agent must read cluster size from the prompt.
- Human checkpoint REQUIRED before: enabling backfills against prod warehouse, dropping/renaming a Silver/Gold table, changing CDC publication, raising auto-scale ceilings on Databricks/EMR.
- Agent will silently downgrade exactly-once to at-least-once when it cannot resolve a transaction config — assert in review.
- `MERGE` statements generated for incremental models often miss `WHEN NOT MATCHED BY SOURCE` clauses — soft-deletes are lost.
- Agent often forgets to set `task_concurrency` / `max_active_tis_per_dag`, leading to thundering-herd retries.

## References
- Microservices.io and ByteByteGo data-pipeline guides.
- Airflow 3.0 release notes — DAG versioning, event-driven scheduling.
- dbt Best Practices: https://docs.getdbt.com/best-practices.
- "Designing Data-Intensive Applications", Martin Kleppmann.
- "Fundamentals of Data Engineering", Joe Reis & Matt Housley.
- Confluent Patterns for Streaming ETL: https://developer.confluent.io/courses/data-pipelines/.
