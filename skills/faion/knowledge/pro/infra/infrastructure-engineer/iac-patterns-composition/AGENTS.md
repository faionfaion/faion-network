---
slug: iac-patterns-composition
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Four composition patterns for structuring Terraform across multiple environments and teams: Terramod (environment definitions compose from modules), Landing Zone (self-service pre-configured environment framework), Service Catalog (vetted patterns for complex deployments), and Hub-Spoke (central shared services with isolated workloads).
content_id: "7bba72cb0b105d45"
tags: [terraform, iac, composition, landing-zone, state-management]
---
# IaC Composition Patterns

## Summary

**One-sentence:** Four composition patterns for structuring Terraform across multiple environments and teams: Terramod (environment definitions compose from modules), Landing Zone (self-service pre-configured environment framework), Service Catalog (vetted patterns for complex deployments), and Hub-Spoke (central shared services with isolated workloads).

**One-paragraph:** Four composition patterns for structuring Terraform across multiple environments and teams: Terramod (environment definitions compose from modules), Landing Zone (self-service pre-configured environment framework), Service Catalog (vetted patterns for complex deployments), and Hub-Spoke (central shared services with isolated workloads).

## Applies If (ALL must hold)

- Multiple environments (dev/staging/prod) sharing the same module graph — use Terramod or Terragrunt composition.
- Multiple teams self-provisioning standardized infrastructure — use Landing Zone or Service Catalog.
- Shared networking/security services consumed by isolated workload accounts — use Hub-Spoke.
- Designing state isolation boundaries before a new project starts.

## Skip If (ANY kills it)

- Single-environment projects — composition patterns add directory structure overhead without benefit.
- Single-team projects with 1-2 modules — direct module composition in a flat root module is simpler.
- Service Catalog when teams don't have distinct infrastructure needs — standardize in modules instead.

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
