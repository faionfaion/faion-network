---
slug: cloud-run-autoscaling
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cloud Run scales from 0 to 1000+ instances based on concurrent requests.
content_id: "34c45408af478473"
tags: [gcp, cloud-run, autoscaling, cold-start, performance]
---
# Cloud Run Autoscaling and Performance

## Summary

**One-sentence:** Cloud Run scales from 0 to 1000+ instances based on concurrent requests.

**One-paragraph:** Cloud Run scales from 0 to 1000+ instances based on concurrent requests. Concurrency per instance (default 80), min instances (default 0), and startup CPU boost are the three primary levers for balancing cost, latency, and throughput. Billing mode switches between request-based and instance-based depending on whether background work is needed.

## Applies If (ALL must hold)

- Configuring min/max instances for a production Cloud Run service.
- Tuning concurrency for CPU-bound vs I/O-bound workloads.
- Eliminating cold start latency for critical services.
- Choosing between request-based and instance-based billing.
- Optimizing container startup time to reduce cold start duration.
- Troubleshooting latency spikes under variable load.

## Skip If (ANY kills it)

- Cloud Run Jobs (run-to-completion) — Jobs use task parallelism, not request-based autoscaling.
- GKE workloads — GKE uses HorizontalPodAutoscaler with different levers (CPU/memory metrics).
- Service deployment commands — see cloud-run-deployment.

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
