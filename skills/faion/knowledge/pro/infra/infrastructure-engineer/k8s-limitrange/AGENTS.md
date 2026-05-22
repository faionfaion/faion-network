---
slug: k8s-limitrange
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A LimitRange is a namespace-scoped policy that enforces resource constraints at the individual container or pod level.
content_id: "983c817fffb6440a"
tags: [kubernetes, limitrange, namespace-policy, resource-governance, multi-tenancy]
---
# Kubernetes LimitRange — Per-Container Resource Governance

## Summary

**One-sentence:** A LimitRange is a namespace-scoped policy that enforces resource constraints at the individual container or pod level.

**One-paragraph:** A LimitRange is a namespace-scoped policy that enforces resource constraints at the individual container or pod level. It provides automatic defaults (so containers without explicit resources still get sensible values), minimum/maximum bounds (preventing extremes), and optional limit-to-request ratio caps. Every namespace in a multi-tenant or production cluster MUST have a LimitRange. Without one, containers that omit the resources block receive BestEffort QoS and can consume unlimited node resources.

## Applies If (ALL must hold)

- Every namespace in a production or shared cluster — create LimitRange as part of namespace provisioning.
- When developers frequently forget to set resources on containers (defaults solve this automatically).
- When a container is being OOMKilled immediately at startup — check if LimitRange max is lower than the required memory.
- When a single container is consuming an entire node — set LimitRange max.cpu and max.memory.
- When enforcing commit to a CPU overcommit policy — use maxLimitRequestRatio.

## Skip If (ANY kills it)

- Single-pod test namespaces where you explicitly manage every container's resources — LimitRange adds admission overhead with no value.
- When all workloads already have explicit resources and you only need aggregate caps — use ResourceQuota alone.

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
