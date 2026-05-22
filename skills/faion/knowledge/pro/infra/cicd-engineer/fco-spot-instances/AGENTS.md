---
slug: fco-spot-instances
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Spot instances (AWS), Preemptible VMs (GCP), and Spot VMs (Azure) provide access to unused cloud capacity at 70-90% discounts versus on-demand pricing, subject to 2-minute reclaim notices.
content_id: "5560046b8d9919fa"
tags: [finops, spot-instances, preemptible, cloud-cost, fault-tolerant]
---
# Spot and Preemptible Instance Strategy

## Summary

**One-sentence:** Spot instances (AWS), Preemptible VMs (GCP), and Spot VMs (Azure) provide access to unused cloud capacity at 70-90% discounts versus on-demand pricing, subject to 2-minute reclaim notices.

**One-paragraph:** Spot instances (AWS), Preemptible VMs (GCP), and Spot VMs (Azure) provide access to unused cloud capacity at 70-90% discounts versus on-demand pricing, subject to 2-minute reclaim notices. Successfully using Spot requires: fault-tolerant architecture, checkpointing for long-running jobs, graceful interruption handling, instance type diversification, and automatic fallback to on-demand when Spot is unavailable.

## Applies If (ALL must hold)

- CI/CD pipelines — highest Spot fit; jobs are inherently stateless and retryable.
- Batch processing, data pipelines, and ETL jobs — can checkpoint and resume.
- ML training workloads — checkpoint every N steps, resume on interruption.
- Rendering, transcoding, and simulation jobs — naturally parallelizable and restartable.
- Dev and test environments — interruption is tolerable outside business hours.
- Scale-out capacity for stateless microservices behind a load balancer.

## Skip If (ANY kills it)

- Production databases — a 2-minute interruption notice is insufficient for safe database shutdown and replication catch-up.
- Production APIs without graceful degradation — a sudden node loss will cause user-visible errors if the architecture cannot absorb it.
- Stateful workloads without checkpointing — an 18-hour ML training job without checkpoints restarts from zero on interruption, generating pure waste.
- Long-running jobs in regions with high Spot interruption rates for the required instance type — check historical interruption frequency first.

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

- parent skill: `pro/infra/cicd-engineer/`
