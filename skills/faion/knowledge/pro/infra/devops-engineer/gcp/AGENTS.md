---
slug: gcp
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GCP production deployments: use Autopilot mode for GKE (pay-per-pod, no node management) unless GPU workloads or privileged containers are required; use Workload Identity Federation to eliminate service account keys for all external workloads (GitHub Actions, GitLab CI, AWS); use Private Service Connect instead of VPC Peering for Google-managed service access.
content_id: "978bacb0d60c7800"
tags: [gcp, kubernetes, cloud-run, workload-identity, iam]
---
# GCP

## Summary

**One-sentence:** GCP production deployments: use Autopilot mode for GKE (pay-per-pod, no node management) unless GPU workloads or privileged containers are required; use Workload Identity Federation to eliminate service account keys for all external workloads (GitHub Actions, GitLab CI, AWS); use Private Service Connect instead of VPC Peering for Google-managed service access.

**One-paragraph:** GCP production deployments: use Autopilot mode for GKE (pay-per-pod, no node management) unless GPU workloads or privileged containers are required; use Workload Identity Federation to eliminate service account keys for all external workloads (GitHub Actions, GitLab CI, AWS); use Private Service Connect instead of VPC Peering for Google-managed service access. Never assign primitive IAM roles (Owner, Editor, Viewer) to service accounts.

## Applies If (ALL must hold)

- Deploying containerized workloads on GKE (prefer Autopilot)
- Running serverless containers with Cloud Run
- Authenticating GitHub Actions or other OIDC providers to GCP without long-lived keys
- Multi-project GCP organization requiring Shared VPC and centralized networking
- BigQuery/analytics workloads requiring data warehouse integration

## Skip If (ANY kills it)

- Multi-cloud architecture requiring vendor-neutral IaC — use Terraform + cloud-agnostic abstractions instead of GCP-specific tools (Deployment Manager, Cloud Build)
- Workloads requiring Windows Server containers — GKE has limited Windows node support
- Very small workload (< $50/month projected) where the Autopilot per-pod pricing exceeds a minimal VM — Cloud Run or a single e2-micro may be more cost-effective
- Team has no GCP IAM expertise — incorrect organization-level IAM bindings are hard to audit and undo

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
