---
slug: gcp-llm-prompts
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Parameterized LLM prompt templates for GCP infrastructure work: generating Terraform HCL for VPC, firewall, service accounts, Cloud Run, and GKE; security audits and IAM policy reviews; connectivity and Cloud Run troubleshooting; cost optimization and committed-use analysis; architecture documentation, runbooks, and compliance checks.
content_id: "d0bb056ea16b25a5"
tags: [gcp, llm-prompts, terraform, security-audit, troubleshooting]
---
# GCP LLM Prompts

## Summary

**One-sentence:** Parameterized LLM prompt templates for GCP infrastructure work: generating Terraform HCL for VPC, firewall, service accounts, Cloud Run, and GKE; security audits and IAM policy reviews; connectivity and Cloud Run troubleshooting; cost optimization and committed-use analysis; architecture documentation, runbooks, and compliance checks.

**One-paragraph:** Parameterized LLM prompt templates for GCP infrastructure work: generating Terraform HCL for VPC, firewall, service accounts, Cloud Run, and GKE; security audits and IAM policy reviews; connectivity and Cloud Run troubleshooting; cost optimization and committed-use analysis; architecture documentation, runbooks, and compliance checks.

## Applies If (ALL must hold)

- Generating Terraform HCL for a new GCP resource (VPC, Cloud Run, GKE, Cloud SQL).
- Auditing an existing GCP configuration for security issues.
- Troubleshooting connectivity (firewall, NAT, VPC-SC) or IAM permission denied errors.
- Planning cost optimization or committed-use discount purchases.
- Generating architecture documentation, runbooks, or change requests.
- Planning a workload or database migration to GCP.
- Preparing evidence for compliance audits (CIS, SOC2, PCI-DSS, HIPAA).

## Skip If (ANY kills it)

- Actual Terraform module bodies — use gcp-terraform-templates for ready-made HCL.
- gcloud CLI commands for one-off tasks — use gcp-overview-cli, gcp-compute-gke, etc.

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
