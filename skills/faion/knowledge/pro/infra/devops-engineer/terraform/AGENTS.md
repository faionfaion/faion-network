---
slug: terraform
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Terraform codifies infrastructure changes in version-controlled HCL, enabling reproducible environments, drift detection, and auditable change history.
content_id: "9289ea4b9b577eb3"
tags: [terraform, infrastructure-as-code, hcl, aws, state-management]
---
# Terraform

## Summary

**One-sentence:** Terraform codifies infrastructure changes in version-controlled HCL, enabling reproducible environments, drift detection, and auditable change history.

**One-paragraph:** Terraform codifies infrastructure changes in version-controlled HCL, enabling reproducible environments, drift detection, and auditable change history. Remote state with locking (S3 + DynamoDB) prevents concurrent-apply corruption. Pin required_version and all provider versions in every project; never commit .tfvars files containing secrets.

## Applies If (ALL must hold)

- Provisioning or modifying cloud resources on AWS, GCP, or Azure
- Managing multi-environment infrastructure (dev/staging/prod) from one codebase
- Building reusable infrastructure modules shared across projects
- Setting up CI/CD pipelines that automate terraform plan and apply
- Migrating existing resources into Terraform management via import

## Skip If (ANY kills it)

- Kubernetes workloads — use Helm or Kustomize; Terraform's K8s provider is awkward for app config
- Simple one-off scripts — shell or cloud CLI is faster for ephemeral resources
- Secrets management — use Vault, AWS Secrets Manager, or similar; never store secrets in state
- Config management inside VMs — that's Ansible/Chef/Puppet territory

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
