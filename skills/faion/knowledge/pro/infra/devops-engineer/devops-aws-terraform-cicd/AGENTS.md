---
slug: devops-aws-terraform-cicd
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Terraform projects for AWS follow a per-environment directory layout under infrastructure/environments/.
content_id: "ad8dc39ef2e9b869"
tags: [aws, terraform, cicd, github-actions, iac]
---
# Terraform Project Structure and GitHub Actions CI/CD for AWS

## Summary

**One-sentence:** Terraform projects for AWS follow a per-environment directory layout under infrastructure/environments/.

**One-paragraph:** Terraform projects for AWS follow a per-environment directory layout under infrastructure/environments/. State lives in S3 with DynamoDB locking. GitHub Actions deploys via OIDC (no long-lived credentials). The pipeline plans against all environments on pull request and applies sequentially after merge to main, requiring an explicit GitHub Environment approval gate for production.

## Applies If (ALL must hold)

- Starting a new AWS project with Terraform and needing a production-ready project structure.
- Adding CI/CD automation to an existing Terraform codebase without long-lived credentials.
- Setting up multi-environment infrastructure (dev/staging/prod) with isolated state per environment.
- Enforcing cost allocation tagging and provider version pinning across a team.

## Skip If (ANY kills it)

- Single-environment throwaway projects — use local state and manual apply.
- Projects using Terragrunt for DRY configuration — directory layout differs from this pattern.
- AWS CDK or Pulumi projects — different deployment model entirely.

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
