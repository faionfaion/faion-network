---
slug: k8s-resource-quota
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: ResourceQuota enforces hard aggregate limits on the total resources a namespace can consume: CPU requests/limits, memory requests/limits, storage, and object counts (pods, services, secrets, configmaps, PersistentVolumeClaims).
content_id: "1ed866f43d2b8bf7"
tags: [kubernetes, resource-quota, namespace-governance, multi-tenancy, cluster-policy]
---
# Kubernetes ResourceQuota — Namespace-Level Aggregate Caps

## Summary

**One-sentence:** ResourceQuota enforces hard aggregate limits on the total resources a namespace can consume: CPU requests/limits, memory requests/limits, storage, and object counts (pods, services, secrets, configmaps, PersistentVolumeClaims).

**One-paragraph:** ResourceQuota enforces hard aggregate limits on the total resources a namespace can consume: CPU requests/limits, memory requests/limits, storage, and object counts (pods, services, secrets, configmaps, PersistentVolumeClaims). Where LimitRange governs individual containers, ResourceQuota governs the namespace as a whole. Every shared or production namespace MUST have a ResourceQuota to prevent a single team or runaway workload from consuming all cluster resources (the noisy-neighbor problem).

## Applies If (ALL must hold)

- Every shared, production, staging, or team namespace in a multi-tenant cluster.
- When a deployment scaling incident exhausted all node resources in a namespace — add ResourceQuota immediately after recovery.
- When implementing chargeback or cost attribution by team — use ResourceQuota as the governance contract.
- When a namespace needs object count limits (e.g., prevent service proliferation or secret sprawl).
- When scoping quotas to QoS class or PriorityClass — use scopeSelector.

## Skip If (ANY kills it)

- Single-team clusters with a single namespace — ResourceQuota overhead is administrative cost with no isolation benefit.
- Ephemeral test namespaces with a short TTL — spend time on automation to clean them up instead of quota governance.

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
