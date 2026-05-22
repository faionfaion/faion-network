---
slug: devops-lb-health-checks
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Health checks allow the load balancer to remove unhealthy backends from rotation automatically.
content_id: "bae1e90dd49345aa"
tags: [load-balancing, health-checks, liveness, readiness, observability]
---
# Load Balancer Health Checks

## Summary

**One-sentence:** Health checks allow the load balancer to remove unhealthy backends from rotation automatically.

**One-paragraph:** Health checks allow the load balancer to remove unhealthy backends from rotation automatically. Proper design separates liveness (process alive) from readiness (can serve traffic), uses dedicated endpoints, and checks real dependencies — not just HTTP 200.

## Applies If (ALL must hold)

- Any production load-balanced service — health checks are mandatory, not optional.
- Services with external dependencies (database, cache, upstream APIs) that can fail independently.
- Kubernetes deployments requiring liveness and readiness probes.
- Blue-green or rolling deployments where new instances must pass checks before receiving traffic.

## Skip If (ANY kills it)

- Health check path must not execute expensive operations (full DB query, large file load) — it will add latency to every check interval.
- Do not use the same endpoint for liveness and readiness — liveness failing restarts the pod; readiness failing only removes it from rotation.

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
