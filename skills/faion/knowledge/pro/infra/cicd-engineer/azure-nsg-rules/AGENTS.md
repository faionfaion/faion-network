---
slug: azure-nsg-rules
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: NSGs perform stateful packet inspection using a 5-tuple (source IP, source port, destination IP, destination port, protocol).
content_id: "cf012d8f32c90760"
tags: [azure, nsg, network-security, firewall, terraform]
---
# Azure Network Security Groups (NSG)

## Summary

**One-sentence:** NSGs perform stateful packet inspection using a 5-tuple (source IP, source port, destination IP, destination port, protocol).

**One-paragraph:** NSGs perform stateful packet inspection using a 5-tuple (source IP, source port, destination IP, destination port, protocol). Rules are evaluated by priority (100–4095); first match wins. The architectural principle is deny-by-default: add explicit allow rules for required traffic and close everything else with a priority-4096 DenyAll rule.

## Applies If (ALL must hold)

- Every subnet in a production VNet (except GatewaySubnet which cannot have an NSG).
- Any subnet holding compute (VMs, AKS nodes, App Service Integration) or PaaS endpoints.
- When implementing zero-trust east-west controls between tiers (web, app, data).
- Compliance requirements (HIPAA, PCI-DSS, SOC2) mandating network segmentation evidence.

## Skip If (ANY kills it)

- GatewaySubnet — Azure blocks NSG association; use route tables instead.
- AzureFirewallSubnet — Firewall has its own rule engine; NSG is not supported there.
- POC environments where full deny-by-default adds friction without security value.

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
