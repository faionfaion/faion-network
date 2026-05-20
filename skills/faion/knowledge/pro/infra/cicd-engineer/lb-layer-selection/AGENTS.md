---
slug: lb-layer-selection
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Choosing between L4 (transport layer) and L7 (application layer) load balancing is the first architectural decision when deploying a load balancer.
content_id: "c75582692f989851"
tags: [load-balancing, networking, l4, l7, infrastructure]
---
# Load Balancer Layer Selection: L4 vs L7

## Summary

**One-sentence:** Choosing between L4 (transport layer) and L7 (application layer) load balancing is the first architectural decision when deploying a load balancer.

**One-paragraph:** Choosing between L4 (transport layer) and L7 (application layer) load balancing is the first architectural decision when deploying a load balancer. L4 routes TCP/UDP by IP and port with minimal CPU cost; L7 routes by HTTP headers, URL, cookies, and content — enabling SSL termination, path routing, and header manipulation at the cost of more resources. Modern stacks often use both layers together.

## Applies If (ALL must hold)

- Choosing or reviewing a load balancer type at the start of an infrastructure design.
- Traffic profile is purely TCP/UDP (gaming, streaming, database proxies) — L4 is sufficient.
- Content-based routing, SSL termination at the load balancer, or HTTP header manipulation is needed — L7 is required.
- A/B testing, canary deployments, or API gateway functionality is in scope — L7 is required.
- Architecture review catches an agent proposing L4 but listing L7 features — reject the inconsistency.

## Skip If (ANY kills it)

- Vendor/tool selection — use load-balancing-implementation for HAProxy/NGINX/cloud LB specifics.
- TLS cipher suite decisions — see ssl-tls-setup.
- Service-mesh internal routing (mTLS, sidecar/sidecarless) — different concern entirely.
- Database read-replica or write-splitter routing — use DB-specific guidance.
- API gateway feature decisions (auth, quotas, transformations) — a gateway is more than a load balancer.

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
