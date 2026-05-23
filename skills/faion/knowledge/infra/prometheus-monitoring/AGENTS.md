# Prometheus Monitoring

## Summary

**One-sentence:** Prometheus monitoring spec: metric naming + label cardinality limits + recording rules + alert hygiene + scrape-interval discipline for Kubernetes workloads.

**One-paragraph:** Prometheus is the default Kubernetes monitoring stack: pull-based metrics, PromQL queries, Alertmanager routing. The trap teams fall into: unbounded labels (user_id, request_id) blow up cardinality; counter values used directly in dashboards produce sawtooth graphs; alerts fire on causes (pod crashed) instead of symptoms (error rate up) creating alert fatigue. This methodology codifies the rules: histograms over summaries for distributed latency, snake_case namespace_name_unit naming, label-cardinality ≤10, scrape interval ≥15s default, recording rules for expensive dashboard queries, symptom-based alerts with runbook URLs.

**Ефективно для:**

- Kubernetes workload observability — service discovery + scrape + alert.
- Custom-metrics для SLI/SLO measurement (RED/USE method).
- Контроль cardinality blowup до того, як Prometheus OOM-нется.
- Recording rules для expensive dashboard queries (10x швидше).

## Applies If (ALL must hold)

- Kubernetes cluster with workloads needing metric-based observability
- Application SLI/SLO measurement via custom metrics (RED / USE method)
- Alert routing with Alertmanager (Slack, PagerDuty, email)
- Pre-computing expensive dashboard queries with recording rules

## Skip If (ANY kills it)

- Log aggregation — use Loki or ELK; Prometheus is metrics only
- Distributed tracing — use Jaeger or Tempo, not Prometheus
- High-cardinality event data (per-request attributes) — use log/trace systems
- Sub-second resolution required — Prometheus scrape interval minimum ~10s

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prometheus + Alertmanager + node-exporter | Helm charts or operator install | platform team |
| ServiceMonitor CRD (Prometheus Operator) | Kubernetes manifests | ops |
| Long-term storage backend (Thanos / Mimir / Cortex) | object-storage bucket + remote_write config | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[alert-deduplication-playbook]] | Alert hygiene context — what 'good alert' means |
| [[slo-definition-template-per-service-class]] | Defines SLI targets the metrics measure |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `metric_audit` | haiku | Mechanical listing of cardinality offenders |
| `rule_rewrite` | sonnet | Bounded judgment on symptom vs cause |
| `recording_rule_design` | sonnet | PromQL synthesis from dashboard queries |

## Templates

| File | Purpose |
|------|---------|
| `templates/alertmanager-config.yaml` | Alertmanager config template |
| `templates/prometheus-rule.yaml` | Prometheus rule template |
| `templates/prompt-monitoring-strategy.txt` | Prompt monitoring strategy template |
| `templates/servicemonitor.yaml` | Servicemonitor template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prometheus-monitoring.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[alert-deduplication-playbook]]
- [[slo-definition-template-per-service-class]]
- [[alert-noise-budget]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
