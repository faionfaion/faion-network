---
slug: lb-health-checks
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Health checks are the mechanism by which LBs remove dead backends from rotation.
content_id: "dc5b9742a2b2d772"
tags: [load-balancing, health-checks, kubernetes, haproxy, nginx]
---
# Load Balancer Health Check Implementation

## Summary

**One-sentence:** Health checks are the mechanism by which LBs remove dead backends from rotation.

**One-paragraph:** Health checks are the mechanism by which LBs remove dead backends from rotation. Implement three endpoints: /health (basic process alive), /health/live (Kubernetes liveness), /health/ready (readiness + deep dependency probe). Configure check intervals between 10-30s with tuned healthy/unhealthy thresholds per backend type.

## Applies If (ALL must hold)

- Implementing a new backend service that will sit behind a load balancer.
- Adding Kubernetes liveness and readiness probes to an existing service.
- Debugging flapping services being incorrectly removed from the LB pool.
- Hardening a service so the LB accurately reflects dependency health.

## Skip If (ANY kills it)

- TCP-only services — use tcp-check in HAProxy or TCP probe in Kubernetes; HTTP health endpoints are not applicable.
- Stateless functions (FaaS/Lambda) — the platform manages health; custom endpoints add no value.
- Database load balancing — use database-protocol health checks (mysql-check, pgsql-check) not HTTP endpoints.

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
