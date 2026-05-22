---
slug: terraform-state
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Remote state configuration, locking, encryption, import, and migration patterns for Terraform.
content_id: "522b86188f29045a"
tags: [terraform, state-management, remote-backend, iac, import]
---
# Terraform State

## Summary

**One-sentence:** Remote state configuration, locking, encryption, import, and migration patterns for Terraform.

**One-paragraph:** Remote state configuration, locking, encryption, import, and migration patterns for Terraform. The concrete rule is: always use a remote backend with locking enabled (S3+DynamoDB for AWS, GCS for GCP); separate state files per environment and per component to minimize blast radius; prefer import blocks (Terraform 1.5+) and moved blocks over CLI state commands for declarative refactoring.

## Applies If (ALL must hold)

- Setting up a remote backend for a new project or migrating from local state.
- Importing existing cloud resources into Terraform management.
- Refactoring resource names or moving resources between modules.
- Recovering from state corruption or lock issues.
- Designing multi-environment state isolation strategy.

## Skip If (ANY kills it)

- Basic HCL syntax or provider configuration — use terraform-basics instead.
- CI/CD pipeline design — use terraform (advanced methodology) instead.
- Module structure design — use terraform-modules instead.
- Emergency force-unlock without understanding lock cause — diagnose first, unlock last resort.

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
