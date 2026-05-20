---
slug: gcp-terraform-templates
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-ready Terraform HCL module set for GCP infrastructure (2025-2026): VPC with four subnet tiers and Cloud NAT, least-privilege firewall rules, per-workload service accounts, Cloud Run v2 service with probes, GKE Autopilot with Workload Identity, Cloud SQL PostgreSQL with private IP and PITR, and a complete example composing all modules.
content_id: "ff029357753bcfbc"
tags: [gcp, terraform, iac, modules, hcl]
---
# GCP Terraform Templates

## Summary

**One-sentence:** Production-ready Terraform HCL module set for GCP infrastructure (2025-2026): VPC with four subnet tiers and Cloud NAT, least-privilege firewall rules, per-workload service accounts, Cloud Run v2 service with probes, GKE Autopilot with Workload Identity, Cloud SQL PostgreSQL with private IP and PITR, and a complete example composing all modules.

**One-paragraph:** Production-ready Terraform HCL module set for GCP infrastructure (2025-2026): VPC with four subnet tiers and Cloud NAT, least-privilege firewall rules, per-workload service accounts, Cloud Run v2 service with probes, GKE Autopilot with Workload Identity, Cloud SQL PostgreSQL with private IP and PITR, and a complete example composing all modules.

## Applies If (ALL must hold)

- Bootstrapping a new GCP project with production-ready infrastructure via Terraform.
- Adding a Cloud Run service, GKE cluster, or Cloud SQL instance to an existing Terraform root.
- Standardizing service account and IAM patterns across teams via shared modules.
- Generating LLM-assisted Terraform for GCP (use gcp-llm-prompts for prompt templates).

## Skip If (ANY kills it)

- One-off exploratory deployments — use gcloud commands (gcp-overview-cli or gcp-compute-gke) and destroy after.
- Existing infrastructure managed outside Terraform — import first, then adopt modules incrementally.

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
