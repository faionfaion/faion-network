---
slug: azure-app-gateway-waf
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Application Gateway v2 is a regional Layer 7 load balancer with integrated WAF (Web Application Firewall).
content_id: "ce41a9b3143a53d6"
tags: [azure, application-gateway, waf, load-balancer, terraform]
---
# Azure Application Gateway v2 with WAF

## Summary

**One-sentence:** Application Gateway v2 is a regional Layer 7 load balancer with integrated WAF (Web Application Firewall).

**One-paragraph:** Application Gateway v2 is a regional Layer 7 load balancer with integrated WAF (Web Application Firewall). It handles SSL termination, URL path-based routing, and health probes. WAF_v2 SKU with OWASP 3.2 managed ruleset protects backends from OWASP Top 10 attacks. As of 2025, its subnet requires delegation to `Microsoft.Network/applicationGateways`.

## Applies If (ALL must hold)

- Regional Layer 7 load balancing for AKS, App Service, or VM backends within a single Azure region.
- SSL/TLS termination at the edge with certificate management via Key Vault.
- OWASP protection for web applications and APIs exposed to the internet or corporate networks.
- URL path-based routing (e.g., /api/* to one backend, /static/* to another).
- When chained with Azure Front Door Premium via Private Link for global + regional WAF layering.

## Skip If (ANY kills it)

- Pure TCP/UDP load balancing — use Azure Load Balancer (Standard) instead; App Gateway only speaks HTTP/HTTPS.
- Global load balancing across regions — use Front Door for that; App Gateway is regional only.
- Cost-sensitive POCs — WAF_v2 costs hundreds USD/month idle (two minimum instances).

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
