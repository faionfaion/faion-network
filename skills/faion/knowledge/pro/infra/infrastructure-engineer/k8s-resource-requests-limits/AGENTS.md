---
slug: k8s-resource-requests-limits
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every container in production MUST declare CPU and memory requests and limits.
content_id: "aa3869a862b7dbd6"
tags: [kubernetes, resource-management, qos, cpu-limits, memory-limits]
---
# Kubernetes Resource Requests, Limits, and QoS Classes

## Summary

**One-sentence:** Every container in production MUST declare CPU and memory requests and limits.

**One-paragraph:** Every container in production MUST declare CPU and memory requests and limits. Requests drive scheduler placement (guaranteed minimum); limits drive kubelet enforcement (maximum). The ratio of requests to limits determines the pod's QoS class, which controls eviction order under node pressure. According to 2025 benchmarks, 99.94% of clusters are over-provisioned with average CPU utilization at just 10% — right-sizing is the single biggest lever for cost and stability.

## Applies If (ALL must hold)

- Every container in every Deployment, StatefulSet, DaemonSet, or Job in a non-trivial environment.
- When a pod is OOMKilled repeatedly — diagnose and raise memory limit.
- When CPU throttling metrics show >10% throttled periods — raise or remove CPU limit.
- When pods fail to schedule with "Insufficient resources" — lower requests or add nodes.
- When right-sizing using VPA in recommendation mode before locking values.

## Skip If (ANY kills it)

- Throwaway local dev containers — overhead of tuning exceeds value; use a LimitRange default instead.
- Init containers in simple scenarios — they run once and exit; defaults from LimitRange suffice unless they do heavy work.

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
