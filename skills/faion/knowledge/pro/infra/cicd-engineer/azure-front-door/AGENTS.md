---
slug: azure-front-door
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Azure Front Door Premium is a global Layer 7 load balancer, CDN, and WAF service.
content_id: "d993764492c14fef"
tags: [azure, front-door, cdn, global-load-balancing, terraform]
---
# Azure Front Door Premium (Global LB, CDN, WAF)

## Summary

**One-sentence:** Azure Front Door Premium is a global Layer 7 load balancer, CDN, and WAF service.

**One-paragraph:** Azure Front Door Premium is a global Layer 7 load balancer, CDN, and WAF service. It routes traffic to the nearest healthy origin, caches static content at PoPs, and optionally connects to origins via Private Link over the Azure backbone (no public internet between Front Door and backend). Premium tier is required for Private Link and advanced WAF with bot protection. Config propagation takes 5-15 minutes — plan for this in deployment pipelines.

## Applies If (ALL must hold)

- Global distribution across multiple regions with health-aware failover.
- CDN caching for static assets at Azure PoPs close to end users.
- Outer WAF layer in a Front Door + App Gateway two-tier architecture.
- When origins must remain private — Front Door Premium with Private Link keeps traffic on Azure backbone.
- DDoS protection at the edge for high-traffic internet-facing applications.

## Skip If (ANY kills it)

- Single-region applications with no CDN or global routing needs — App Gateway alone is simpler and cheaper.
- Dev/test environments where Front Door's 5-15 minute config propagation slows iteration cycles.
- Standard tier if Private Link to origins is needed — Premium is required for Private Link.
- Cost-sensitive workloads — Front Door Premium combined with App Gateway v2 can cost hundreds USD/month idle.

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
