---
slug: k8s-canary-progressive
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Canary deployment gradually shifts traffic from a stable version to a new version, using metrics analysis to decide whether to promote or rollback.
content_id: "7ba3973cd09493aa"
tags: [kubernetes, canary, argo-rollouts, progressive-delivery, blue-green]
---
# Kubernetes Canary and Progressive Delivery

## Summary

**One-sentence:** Canary deployment gradually shifts traffic from a stable version to a new version, using metrics analysis to decide whether to promote or rollback.

**One-paragraph:** Canary deployment gradually shifts traffic from a stable version to a new version, using metrics analysis to decide whether to promote or rollback. Manual canary uses replica-count weighting or Nginx Ingress annotations. Argo Rollouts (2025-2026 standard) automates step-wise traffic shifts with Prometheus metric analysis and automatic rollback on threshold breach.

## Applies If (ALL must hold)

- Production releases where a rolling update's 100% exposure is too risky.
- Features that need real-traffic validation before full promotion.
- High-stakes deployments for enterprise or regulated workloads.
- GitOps workflows where automated promotion/rollback is desirable.

## Skip If (ANY kills it)

- Simple stateless services with good staging coverage — rolling update is sufficient.
- Clusters without a service mesh or Ingress controller that supports traffic splitting.
- Environments without Prometheus or equivalent metrics — analysis templates have nothing to query.
- Hot-fix deployments where speed matters more than gradual exposure.

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
