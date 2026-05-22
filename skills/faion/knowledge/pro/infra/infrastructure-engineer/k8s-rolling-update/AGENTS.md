---
slug: k8s-rolling-update
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Rolling update is the default and safest Kubernetes deployment strategy for most production workloads.
content_id: "268faed9f5d8b7ad"
tags: [kubernetes, rolling-update, zero-downtime, rollback, deployment]
---
# Kubernetes Rolling Update Strategy

## Summary

**One-sentence:** Rolling update is the default and safest Kubernetes deployment strategy for most production workloads.

**One-paragraph:** Rolling update is the default and safest Kubernetes deployment strategy for most production workloads. It gradually replaces old pods with new ones, keeping the service available throughout. Zero-downtime requires maxUnavailable: 0 plus a properly configured readiness probe and minReadySeconds delay. kubectl rollout undo enables fast rollback to any revision in history.

## Applies If (ALL must hold)

- Updating image versions, configuration, or environment variables on any Deployment.
- Tuning rollout speed vs. availability for high-replica Deployments.
- Debugging a stuck or failed rollout.
- Executing or documenting a rollback procedure.

## Skip If (ANY kills it)

- High-risk releases where you need percentage-based traffic control and automated metric analysis — use canary/Argo Rollouts (k8s-canary-progressive).
- StatefulSets requiring controlled partition rollouts — use updateStrategy.rollingUpdate.partition.
- Development environments where downtime is acceptable and Recreate is simpler.

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
