---
slug: kubernetes-deployment
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Kubernetes offers two built-in strategies (Recreate and Rolling Update) and three advanced strategies via Argo Rollouts (Blue-Green, Canary, A/B Testing).
content_id: "276516038785fbfe"
tags: [kubernetes, deployment, argo-rollouts, blue-green, canary]
---
# Kubernetes Deployment Strategies

## Summary

**One-sentence:** Kubernetes offers two built-in strategies (Recreate and Rolling Update) and three advanced strategies via Argo Rollouts (Blue-Green, Canary, A/B Testing).

**One-paragraph:** Kubernetes offers two built-in strategies (Recreate and Rolling Update) and three advanced strategies via Argo Rollouts (Blue-Green, Canary, A/B Testing). 80% of Kubernetes outages stem from deployment errors. The default Rolling Update is zero-downtime but has medium rollback speed; Blue-Green provides instant rollback at 2x resource cost; Canary is the most risk-averse — it shifts traffic incrementally while Prometheus/Datadog analysis gates each step.

## Applies If (ALL must hold)

- Any production Kubernetes deployment that requires zero downtime (Rolling Update minimum).
- Critical services needing instant rollback — use Blue-Green.
- High-traffic systems where a bad deploy must not reach all users — use Canary.
- GitOps workflows — Argo Rollouts integrates natively with Argo CD.

## Skip If (ANY kills it)

- Applications that cannot run two versions simultaneously (DB schema breaking change) — use Recreate or migrate schema first.
- Dev/staging environments where downtime is acceptable — Recreate is simpler.
- Teams without Prometheus metrics or observability — Canary analysis gates require metrics; fall back to Rolling Update.

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
