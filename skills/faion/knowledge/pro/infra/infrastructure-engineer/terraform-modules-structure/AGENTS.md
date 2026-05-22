---
slug: terraform-modules-structure
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Terraform modules are self-contained packages of Terraform configurations that encapsulate reusable infrastructure components.
content_id: "d02801b160046cc7"
tags: [terraform, modules, iac, structure, design]
---
# Terraform Module Structure and Design

## Summary

**One-sentence:** Terraform modules are self-contained packages of Terraform configurations that encapsulate reusable infrastructure components.

**One-paragraph:** Terraform modules are self-contained packages of Terraform configurations that encapsulate reusable infrastructure components. Well-designed modules reduce code duplication, improve maintainability, and enable team collaboration at scale. Every module must have a single responsibility, a clear inputs/outputs contract, and comprehensive documentation.

## Applies If (ALL must hold)

- Authoring a new reusable Terraform module for a specific resource type (VPC, ECS service, RDS instance).
- Refactoring an existing flat Terraform root that is growing beyond a single concern.
- Onboarding a new engineer or agent to an existing module — use this as the canonical layout reference.
- Publishing a module to the Terraform Registry or an internal registry.

## Skip If (ANY kills it)

- One-off scripts or environment-specific configs — a root module with inline resources is simpler and sufficient.
- Prototype repos with fewer than 5 resources — the overhead of a full module structure exceeds the value.

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
