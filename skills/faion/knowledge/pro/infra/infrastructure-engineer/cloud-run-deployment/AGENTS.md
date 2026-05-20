---
slug: cloud-run-deployment
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cloud Run services accept HTTP requests and scale automatically.
content_id: "92ded1ff88c1f098"
tags: [gcp, cloud-run, deployment, containers, terraform]
---
# Cloud Run Service Deployment

## Summary

**One-sentence:** Cloud Run services accept HTTP requests and scale automatically.

**One-paragraph:** Cloud Run services accept HTTP requests and scale automatically. Deploy from a container image or source, set resource limits, configure health checks, and use Secret Manager for credentials. The container MUST listen on the PORT environment variable.

## Applies If (ALL must hold)

- Deploying a stateless HTTP API or web application as a containerized service.
- Migrating from Cloud Functions to a container-based runtime.
- Setting up a new Cloud Run service with Terraform or gcloud in production.
- Configuring health check probes for a Cloud Run service.
- Building a Dockerfile for a Cloud Run target container.

## Skip If (ANY kills it)

- Long-running background tasks without HTTP triggers — use Cloud Run Jobs instead.
- Stateful services requiring persistent local disk — use Compute Engine or GKE.
- Workloads exceeding 8 vCPU or 32 GB memory — use GKE.
- Autoscaling configuration details — see cloud-run-autoscaling.
- Traffic splitting and canary patterns — see cloud-run-traffic-management.

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
