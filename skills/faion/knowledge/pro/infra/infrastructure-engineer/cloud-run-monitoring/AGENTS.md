---
slug: cloud-run-monitoring
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Cloud Run observability: structured JSON logging, Cloud Monitoring dashboards, SLO alerting, Cloud Trace propagation, gcloud log queries for services and jobs, and cost optimization monitoring.
content_id: "5ff0b284d88f7722"
complexity: medium
produces: config
est_tokens: 4100
tags: [gcp, cloud-run, monitoring, logging, observability]
---
# Cloud Run Monitoring

## Summary

**One-sentence:** Cloud Run observability: structured JSON logging, Cloud Monitoring dashboards, SLO alerting, Cloud Trace propagation, gcloud log queries for services and jobs, and cost optimization monitoring.

**One-paragraph:** Cloud Run exports metrics to Cloud Monitoring automatically (request count, latency, instance count, CPU/memory utilization). Applications MUST emit structured JSON logs to stdout/stderr to enable Cloud Logging parsing. Cloud Trace integrates via OpenTelemetry or the Cloud Trace client library. Configure alerting policies on error rate and p99 latency for production SLOs.

**Ефективно для:**

- Production Cloud Run сервіси з обов'язковим SLO + alerting на 5xx/p99.
- Структуроване JSON логування на stdout з trace-кореляцією.
- Distributed tracing через X-Cloud-Trace-Context між мікросервісами.
- Debug latency-spikes або помилок через log-based metrics + Cloud Trace.

## Applies If (ALL must hold)

- Setting up structured logging for a Cloud Run service or job.
- Creating Cloud Monitoring dashboards and alerting policies for Cloud Run.
- Configuring Cloud Trace for distributed tracing across Cloud Run services.
- Debugging service errors, latency spikes, or scaling issues via logs and metrics.
- Defining SLOs and error budgets for production Cloud Run services.
- Monitoring Cloud Run job executions and failed tasks.

## Skip If (ANY kills it)

- VPC and network configuration — see `cloud-run-vpc-access`.
- Autoscaling tuning — see `cloud-run-autoscaling`.
- GKE workload monitoring — use Workload Identity + managed Prometheus instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service name + revision | string | Cloud Run deploy |
| Notification channels | PagerDuty / email / Pub/Sub | ops |
| SLO target | p99 latency / error budget | product owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cloud-run-deployment]] | Sibling methodology that supplies context required here. |
| [[cloud-run-autoscaling]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-config` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-cloud-run-monitoring.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cloud-run-monitoring.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cloud-run-monitoring.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[cloud-run-deployment]]
- [[cloud-run-autoscaling]]
- [[cloud-run-vpc-access]]
- [[gcp-cloud-run-serverless]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. cloud-run-monitoring vs an adjacent sibling).
