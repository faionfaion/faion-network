---
slug: azure-private-link
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Private Endpoints inject a NIC with a private IP from your VNet into an Azure PaaS service (Storage, Key Vault, SQL, PostgreSQL, ACR, App Service, etc.
content_id: "5139f8246867ecad"
tags: [azure, private-link, private-endpoint, private-dns, terraform]
---
# Azure Private Link and Private Endpoints

## Summary

**One-sentence:** Private Endpoints inject a NIC with a private IP from your VNet into an Azure PaaS service (Storage, Key Vault, SQL, PostgreSQL, ACR, App Service, etc.

**One-paragraph:** Private Endpoints inject a NIC with a private IP from your VNet into an Azure PaaS service (Storage, Key Vault, SQL, PostgreSQL, ACR, App Service, etc.). Combined with a Private DNS zone and a VNet link, DNS resolution for the service FQDN returns the private IP instead of the public one — all traffic stays on the Azure backbone. Public access on the target resource MUST be disabled to eliminate the public endpoint.

## Applies If (ALL must hold)

- All PaaS services (Storage, Key Vault, SQL, PostgreSQL, ACR, App Service) in production environments.
- Compliance requirements (HIPAA, PCI-DSS, SOC2) mandating data exfiltration controls and private connectivity.
- Migrating from Service Endpoints to Private Endpoints for stronger isolation guarantees.
- Exposing internal services to other VNets or subscriptions via Private Link Service (your own service behind an internal load balancer).

## Skip If (ANY kills it)

- Dev/test environments where the Private DNS zone complexity adds debugging overhead for no compliance value.
- When the platform team cannot reliably operate Private DNS zones — broken DNS makes Private Link a debugging nightmare with no obvious error.
- Services that have no private endpoint support (some preview services, some third-party Azure Marketplace offerings).

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
