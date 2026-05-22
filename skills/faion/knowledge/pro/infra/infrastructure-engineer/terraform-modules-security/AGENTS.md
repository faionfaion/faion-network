---
slug: terraform-modules-security
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Terraform modules must never embed secrets, must follow IAM and network least-privilege, and must be tested with terraform validate, terraform test (native), and optionally Terratest before release.
content_id: "a64b52eccd97f559"
tags: [terraform, modules, security, testing, cicd]
---
# Terraform Module Security and Testing

## Summary

**One-sentence:** Terraform modules must never embed secrets, must follow IAM and network least-privilege, and must be tested with terraform validate, terraform test (native), and optionally Terratest before release.

**One-paragraph:** Terraform modules must never embed secrets, must follow IAM and network least-privilege, and must be tested with terraform validate, terraform test (native), and optionally Terratest before release. A CI/CD pipeline with format check, validation, lint, security scan, plan, and gated apply stages is the minimum quality bar for production modules.

## Applies If (ALL must hold)

- Writing or reviewing a Terraform module that manages IAM, networking, encryption, or secret references.
- Setting up a CI/CD pipeline for a Terraform module or environment.
- Adding tests to an existing module that lacks automated validation.
- Conducting a security review of a module before promoting it to production.

## Skip If (ANY kills it)

- Prototype or throwaway environments — apply a lighter checklist; skip Terratest.
- Read-only modules that only expose data sources — security scan for secrets is still required.

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
