---
slug: k8s-scaling-availability
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: HorizontalPodAutoscaler (autoscaling/v2) automatically scales Deployment replicas based on CPU, memory, or custom metrics.
content_id: "b3be9b127710daff"
tags: [kubernetes, hpa, autoscaling, pdb, availability]
---
# Kubernetes Scaling and Availability: HPA and PDB

## Summary

**One-sentence:** HorizontalPodAutoscaler (autoscaling/v2) automatically scales Deployment replicas based on CPU, memory, or custom metrics.

**One-paragraph:** HorizontalPodAutoscaler (autoscaling/v2) automatically scales Deployment replicas based on CPU, memory, or custom metrics. PodDisruptionBudget protects a minimum number of running pods during voluntary disruptions such as node drains or cluster upgrades. Both are required for production deployments: HPA handles load changes, PDB handles maintenance.

## Applies If (ALL must hold)

- Adding autoscaling to a production Deployment or StatefulSet.
- Protecting a service during cluster maintenance, node drain, or voluntary disruption.
- Tuning scale-down conservatism to prevent flapping.
- Setting up event-driven autoscaling with KEDA (queue depth, HTTP request count).

## Skip If (ANY kills it)

- Development/staging single-replica Deployments — HPA complexity without HA benefit.
- Batch jobs and CronJobs — use KEDA or manual scaling on completion events instead.
- StatefulSets with ordered provisioning where rapid scale-up risks data consistency — review before applying aggressive scale policies.

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
