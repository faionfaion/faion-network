---
slug: finops-devops-cost-kubernetes
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Kubernetes clusters default to uniform over-provisioned node pools with no autoscaling and no workload-aware placement — the result is 25% average CPU and 40% average memory utilization.
content_id: "819f50b3e2e95b0d"
tags: [finops, kubernetes, cost-optimization, node-pools, vpa]
---
# Kubernetes Cost Optimization: Node Pools, VPA, and Spot

## Summary

**One-sentence:** Kubernetes clusters default to uniform over-provisioned node pools with no autoscaling and no workload-aware placement — the result is 25% average CPU and 40% average memory utilization.

**One-paragraph:** Kubernetes clusters default to uniform over-provisioned node pools with no autoscaling and no workload-aware placement — the result is 25% average CPU and 40% average memory utilization. Four levers reduce this to 55% CPU / 65% memory utilization and cut cluster costs by 48-60%: workload-specific node pools (CPU-intensive, memory-intensive, general), Vertical Pod Autoscaler for right-pod-sizing, Spot node pools for batch/preemptible work, and Committed Use Discounts on the stable baseline.

## Applies If (ALL must hold)

- Kubernetes cluster average CPU utilization below 40% or memory below 50% — the cluster is significantly underutilized and Spot/VPA/node-pool splits will have high impact.
- Single node pool for all workloads — replacing with workload-specific pools reduces node count 30-50%.
- Batch workloads (ML training, data processing, CI/CD runners) co-located with services — separate Spot node pool saves 70-90% on batch compute without affecting services.
- Pod resource requests set to static values from initial deployment without production tuning — VPA in recommendation mode will show the gap.
- Cluster running 24/7 at stable size — Committed Use Discounts (GKE) or Reserved Node Groups (EKS) cover the baseline at 37-40% discount.

## Skip If (ANY kills it)

- Clusters under 10 nodes — optimization overhead (VPA, multiple node pools) exceeds savings on small clusters.
- VPA in Auto mode on stateful workloads (databases) — pod restarts during request adjustments cause brief unavailability.
- Spot node pools for services with no pod disruption budget or no horizontal replicas — a single-pod service on a Spot node will have downtime on preemption.

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

- parent skill: `pro/infra/devops-engineer/`
