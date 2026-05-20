---
slug: gitops-progressive-delivery
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Progressive delivery extends GitOps with automated canary and blue-green deployments.
content_id: "ea6db0a6bdb4d31e"
tags: [progressive-delivery, canary, flagger, argo-rollouts, gitops]
---
# Progressive Delivery with GitOps

## Summary

**One-sentence:** Progressive delivery extends GitOps with automated canary and blue-green deployments.

**One-paragraph:** Progressive delivery extends GitOps with automated canary and blue-green deployments. Flagger and Argo Rollouts integrate with ArgoCD or Flux to shift traffic incrementally, analyze metrics (success rate, latency), and automatically roll back on threshold violations — without human intervention in the happy path.

## Applies If (ALL must hold)

- High-traffic production services where a bad deploy affects many users before it's caught.
- Services with reliable Prometheus metrics (success rate, latency) that can serve as rollback signals.
- Teams that have adopted GitOps and want to add automated rollback to their CD pipeline.
- Environments where blue-green switchover needs to be controlled without downtime.

## Skip If (ANY kills it)

- Services without meaningful Prometheus metrics — canary analysis has nothing to trigger rollback on; use standard rolling updates.
- Environments without a traffic management layer (service mesh or capable ingress) — Flagger/Rollouts require traffic splitting support.
- Stateful services with schema migrations that can't run with two versions simultaneously.
- Low-traffic internal tools where a bad deploy affects 1-2 users — standard rollout with fast rollback is simpler.

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
