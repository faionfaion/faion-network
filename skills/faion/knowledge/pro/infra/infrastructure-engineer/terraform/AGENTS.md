---
slug: terraform
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-grade Terraform covers state architecture, module design, workspace strategies, CI/CD integration, security scanning, and compliance governance.
content_id: "9289ea4b9b577eb3"
tags: [terraform, iac, infrastructure, state-management, cicd]
---
# Terraform (Advanced)

## Summary

**One-sentence:** Production-grade Terraform covers state architecture, module design, workspace strategies, CI/CD integration, security scanning, and compliance governance.

**One-paragraph:** Production-grade Terraform covers state architecture, module design, workspace strategies, CI/CD integration, security scanning, and compliance governance. The concrete rule: always save plan to file (-out=tfplan) and apply the exact saved plan in CI; always run tfsec/checkov before apply; separate state by environment AND component for minimal blast radius; use directory-per-environment over workspaces for true isolation.

## Applies If (ALL must hold)

- Designing multi-environment Terraform project layout (environments/dev|staging|prod + modules/)
- Setting up CI/CD pipelines (GitHub Actions, GitLab CI, Atlantis) with plan-then-apply gates
- Implementing security scanning (tfsec, Checkov) in the pipeline
- Using workspaces vs directory isolation — deciding and implementing
- Running native terraform test or Terratest for infrastructure testing
- Drift detection and compliance (tagging policy, audit logging)

## Skip If (ANY kills it)

- HCL syntax basics or first Terraform project — use terraform-basics
- State backend configuration and import operations — use terraform-state
- Module development and versioning patterns — use terraform-modules

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
