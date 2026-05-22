---
slug: vector-db-monitoring
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "44f1919c3c15e88d"
summary: Instruments a production vector DB with Prometheus metrics, Grafana dashboard, warning/critical alerts for latency / error / memory / disk, and capacity planning baselines.
complexity: medium
produces: config
est_tokens: 3400
tags: [vector-database, monitoring, prometheus, alerting, observability]
---

# Vector Database Monitoring and Alerting

## Summary

**One-sentence:** Wires Prometheus + Grafana on the vector DB with warning + critical thresholds for the four pillars (latency, error rate, memory, disk) plus capacity planning baselines.

**One-paragraph:** Vector DBs fail differently from generic databases: HNSW degrades on memory pressure rather than dropping rows, recall drifts silently on data growth, p99 latency spikes on quantization-induced cache misses. This methodology pins what to monitor (query p50/p95/p99, error rate %, RAM headroom, disk usage, segment count, queue depth), at what thresholds, and with what runbook link. Output: a `monitoring.yaml` declaring metric collectors + dashboards + alert rules + capacity targets, importable into Prometheus / Grafana.

**Ефективно для:**

- Production self-host Qdrant / Weaviate / Milvus — managed (Pinecone) має своє моніторинг; для self-host треба будувати.
- SLA-driven продуктів — explicit p95 + recall alert ловить деградацію до того як user noticed.
- Capacity planning — disk + memory growth тренди вказують коли скейлити до того як OOM.
- Multi-tenant — per-tenant latency + error rate ловить tenant-specific deg.

## Applies If (ALL must hold)

- Vector DB in production (self-hosted)
- Prometheus / Grafana / equivalent already running OR planned within feature
- On-call rotation defined (alerts without on-call are noise)

## Skip If (ANY kills it)

- Managed DB (Pinecone) — use provider dashboard
- Dev / staging only — over-engineered
- No on-call — alerts go nowhere

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `prometheus-stack.yaml` | YAML | infra |
| `sla.yaml` | YAML | (latency_p95, error_rate_pct, memory_pct, disk_pct) |
| `oncall-routing.yaml` | YAML | PagerDuty / Opsgenie config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `vector-databases` | DB chosen |
| `vector-db-setup-prod` | Prod deploy baseline |
| `retrieval-drift-alerting-recipe` | Application-layer drift complement |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: four-pillar coverage, paged-vs-ticket routing, capacity baseline, dashboard SLO panel, runbook link required | 1100 |
| `content/02-output-contract.xml` | essential | monitoring.yaml schema | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: missing memory metric, alert-without-runbook, single global threshold, no capacity trend, dashboard-only-no-alert | 900 |
| `content/04-procedure.xml` | essential | 5 steps: scrape config → dashboard → alert rules → runbook + on-call → capacity reviews | 700 |
| `content/05-examples.xml` | essential | Worked example: Qdrant Prometheus + Grafana with paged alerts | 500 |
| `content/06-decision-tree.xml` | essential | Routes alert by metric + severity | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `prometheus_rules_drafting` | sonnet | Schema synthesis |
| `runbook_drafting` | sonnet | Trade-offs |
| `monitoring_yaml_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/monitoring.schema.yaml` | Schema for monitoring.yaml |
| `templates/prometheus-rules.yaml` | Reference rule set |
| `templates/_smoke-test.yaml` | Minimum-viable spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-db-monitoring.py` | Lint monitoring.yaml | Pre-commit |

## Related

- [[vector-databases]] · [[vector-db-setup-prod]] · [[retrieval-drift-alerting-recipe]]
- external: [Qdrant metrics](https://qdrant.tech/documentation/guides/monitoring/) · [Prometheus best practices](https://prometheus.io/docs/practices/alerting/)

## Decision tree

See `content/06-decision-tree.xml`. Routes alert by metric class + severity → page / ticket / suppress.
