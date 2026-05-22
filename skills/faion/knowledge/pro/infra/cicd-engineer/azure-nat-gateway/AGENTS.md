---
slug: azure-nat-gateway
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: NAT Gateway provides managed, zone-redundant outbound internet connectivity for private subnets.
content_id: "3d81a3dd8d6992e3"
tags: [azure, nat-gateway, outbound-connectivity, snat, terraform]
---
# Azure NAT Gateway for Outbound Connectivity

## Summary

**One-sentence:** NAT Gateway provides managed, zone-redundant outbound internet connectivity for private subnets.

**One-paragraph:** NAT Gateway provides managed, zone-redundant outbound internet connectivity for private subnets. It replaces the implicit Load Balancer outbound rules with a predictable static public IP, consistent SNAT behavior, and configurable idle timeout. Every public IP on a NAT Gateway provides ~64,000 SNAT ports — size the IP count against expected concurrent outbound connections.

## Applies If (ALL must hold)

- Any private subnet that requires outbound internet access (container registries, OS updates, external APIs).
- Workloads that must present a consistent egress IP for third-party IP allowlisting (payment gateways, SaaS APIs).
- High-availability setups requiring zone-redundant outbound — NAT Gateway supports zone-redundant public IPs.
- AKS node pools in private subnets — nodes need outbound access for node bootstrap and image pull.

## Skip If (ANY kills it)

- Subnets that have no outbound internet requirement — NAT Gateway costs even when idle; skip it for data-tier or internal-only subnets.
- Virtual WAN spoke VNets — Virtual WAN has its own managed egress; adding a NAT Gateway causes routing conflicts.
- Subnets with Azure Firewall as the egress path — do not attach NAT Gateway and Firewall UDR to the same subnet; only one egress path should control outbound routing.

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
