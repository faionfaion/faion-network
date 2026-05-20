---
slug: azure-architecture
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Azure enterprise architecture is organized around the Well-Architected Framework (five pillars: Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency) and Landing Zones (eight design areas).
content_id: "af0f2f74732393f6"
tags: [azure, cloud-architecture, landing-zones, well-architected, governance]
---
# Azure Architecture

## Summary

**One-sentence:** Azure enterprise architecture is organized around the Well-Architected Framework (five pillars: Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency) and Landing Zones (eight design areas).

**One-paragraph:** Azure enterprise architecture is organized around the Well-Architected Framework (five pillars: Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency) and Landing Zones (eight design areas). Use Azure Verified Modules (AVM) and Bicep for new deployments; the legacy ESLZ Terraform module is deprecated as of August 2026.

## Applies If (ALL must hold)

- Designing new Azure workload from scratch and need governance baseline
- Organization is adopting Azure at scale (multiple subscriptions, multiple teams)
- Evaluating Well-Architected Framework pillars against an existing Azure deployment
- Setting up hub-spoke networking, Entra ID integration, or PIM-based privileged access
- Migrating on-premises workloads following Cloud Adoption Framework patterns

## Skip If (ANY kills it)

- Single-subscription, single-team project without compliance requirements — Landing Zone overhead is not justified; use a simple resource group structure
- Non-Azure cloud (AWS, GCP) — framework is Azure-specific; use respective cloud frameworks
- Proof-of-concept or sandbox environment — apply minimal governance, not full Landing Zone

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

- parent skill: `pro/infra/devops-engineer/`
