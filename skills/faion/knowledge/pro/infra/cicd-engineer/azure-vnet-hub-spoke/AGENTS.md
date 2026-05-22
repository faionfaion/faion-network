---
slug: azure-vnet-hub-spoke
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Foundation of Azure networking: Virtual Network (VNet) provides network isolation with subnets, peering, and delegations.
content_id: "eff8d00fd54e802e"
tags: [azure, vnet, hub-spoke, networking, terraform]
---
# Azure VNet and Hub-Spoke Topology

## Summary

**One-sentence:** Foundation of Azure networking: Virtual Network (VNet) provides network isolation with subnets, peering, and delegations.

**One-paragraph:** Foundation of Azure networking: Virtual Network (VNet) provides network isolation with subnets, peering, and delegations. Hub-spoke topology centralises shared services (Firewall, Bastion, DNS) in a hub VNet while workloads live in spoke VNets connected via peering.

## Applies If (ALL must hold)

- Designing landing-zone networks for new Azure subscriptions with multiple workloads or environments.
- Multi-team environments where workloads share Firewall, Bastion, DNS, or VPN Gateway.
- Compliance scenarios (HIPAA, PCI-DSS) requiring strict east-west traffic inspection between VNets.
- Any setup with on-premises connectivity via VPN Gateway or ExpressRoute — the Gateway lives in the hub.

## Skip If (ANY kills it)

- Single-region, single-VNet, single-team workload that does not cross subscriptions — full hub-spoke is overkill, use a flat VNet.
- Cost-sensitive POCs — hub-spoke with Firewall + Bastion combined runs hundreds USD/month idle.
- Throwaway dev environments — a flat VNet with NSG is sufficient.

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
