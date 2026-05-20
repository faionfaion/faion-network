---
slug: api-monitoring-health-checks
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every API must expose two distinct health endpoints: /healthz (liveness — process alive, no downstream calls) and /readyz (readiness — all dependencies reachable).
content_id: "6f3abd7a378340d0"
tags: [api-monitoring, health-checks, kubernetes, fastapi, observability]
---
# API Health Check Endpoints: Liveness vs. Readiness

## Summary

**One-sentence:** Every API must expose two distinct health endpoints: /healthz (liveness — process alive, no downstream calls) and /readyz (readiness — all dependencies reachable).

**One-paragraph:** Every API must expose two distinct health endpoints: /healthz (liveness — process alive, no downstream calls) and /readyz (readiness — all dependencies reachable). Conflating the two causes cascade restart loops under Kubernetes.

## Applies If (ALL must hold)

- Any API service deployed under Kubernetes, Docker Swarm, ECS, or any orchestrator that uses liveness/readiness distinctions.
- When adding observability to a new Python/Node/Go/Java API for the first time.
- Before a planned launch or scale event — health probes must exist before load balancers are configured.
- When migrating from a single /health endpoint to a split liveness/readiness pattern.

## Skip If (ANY kills it)

- Pre-product-fit prototypes — /health returning 200 with log-to-stdout is enough; full probe separation adds overhead without value.
- Static sites and CDN-only deployments — the CDN provider's health checks already cover availability.
- One-shot batch jobs and cron tasks — use job-completion alerts (Healthchecks.io, Dead Man's Snitch) instead.

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

- parent skill: `pro/dev/software-developer/`
