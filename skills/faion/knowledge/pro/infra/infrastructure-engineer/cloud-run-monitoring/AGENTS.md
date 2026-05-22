---
slug: cloud-run-monitoring
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cloud Run exports metrics to Cloud Monitoring automatically (request count, latency, instance count, CPU/memory utilization).
content_id: "d68ea08e5673de5d"
tags: [gcp, cloud-run, monitoring, logging, observability]
---
# Cloud Run Monitoring and Observability

## Summary

**One-sentence:** Cloud Run exports metrics to Cloud Monitoring automatically (request count, latency, instance count, CPU/memory utilization).

**One-paragraph:** Cloud Run exports metrics to Cloud Monitoring automatically (request count, latency, instance count, CPU/memory utilization). Applications MUST emit structured JSON logs to stdout/stderr to enable Cloud Logging parsing. Cloud Trace integrates via OpenTelemetry or the Cloud Trace client library. Configure alerting policies on error rate and p99 latency for production SLOs.

## Applies If (ALL must hold)

- Setting up structured logging for a Cloud Run service or job.
- Creating Cloud Monitoring dashboards and alerting policies for Cloud Run.
- Configuring Cloud Trace for distributed tracing across Cloud Run services.
- Debugging service errors, latency spikes, or scaling issues via logs and metrics.
- Defining SLOs and error budgets for production Cloud Run services.
- Monitoring Cloud Run job executions and failed tasks.

## Skip If (ANY kills it)

- VPC and network configuration — see cloud-run-vpc-access.
- Autoscaling tuning based on metrics — see cloud-run-autoscaling.
- GKE workload monitoring — use Workload Identity + Prometheus instead.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/infrastructure-engineer/`
