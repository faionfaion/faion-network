---
slug: lb-technology-selection
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Choose the right load balancer for production using a decision matrix covering HAProxy, Nginx, AWS/GCP/Azure managed LBs, and Kubernetes Ingress controllers.
content_id: "addb50b6e4fdf575"
tags: [load-balancing, haproxy, nginx, kubernetes, infrastructure]
---
# Load Balancer Technology Selection

## Summary

**One-sentence:** Choose the right load balancer for production using a decision matrix covering HAProxy, Nginx, AWS/GCP/Azure managed LBs, and Kubernetes Ingress controllers.

**One-paragraph:** Choose the right load balancer for production using a decision matrix covering HAProxy, Nginx, AWS/GCP/Azure managed LBs, and Kubernetes Ingress controllers. Selection criteria: traffic type (L4/L7), environment (bare-metal/cloud/K8s), concurrency, and operational complexity.

## Applies If (ALL must hold)

- Starting a new service fleet and selecting the LB stack from scratch.
- Migrating from a single-instance setup to a multi-backend load-balanced architecture.
- Evaluating whether to use a managed cloud LB or a self-hosted solution.
- Choosing a Kubernetes Ingress controller for a new cluster.

## Skip If (ANY kills it)

- Internal service-to-service mesh routing — use a service mesh (Linkerd, Istio, Cilium) instead; LB selection does not apply.
- Static-site CDN — CloudFront, Cloudflare, or Fastly serve this role; no LB configuration needed.
- Single-instance dev workloads — nginx -t and docker run -p are sufficient.
- Database load balancing (PgBouncer, ProxySQL, Vitess) — generic LB rules do not fit; use database-specific patterns.

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
