---
slug: gcp-security-iam
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GCP security framework covering IAM least privilege with Workload Identity Federation (no service account keys), VPC Service Controls perimeters for data exfiltration prevention, CMEK encryption, and audit logging.
content_id: "cfa58a7cc5a07a6a"
tags: [gcp, iam, security, workload-identity, vpc-service-controls]
---
# GCP Security and IAM

## Summary

**One-sentence:** GCP security framework covering IAM least privilege with Workload Identity Federation (no service account keys), VPC Service Controls perimeters for data exfiltration prevention, CMEK encryption, and audit logging.

**One-paragraph:** GCP security framework covering IAM least privilege with Workload Identity Federation (no service account keys), VPC Service Controls perimeters for data exfiltration prevention, CMEK encryption, and audit logging. Includes full IAM and data security checklists.

## Applies If (ALL must hold)

- Configuring IAM roles and service accounts for a new GCP project.
- Eliminating service account key files from CI/CD pipelines (Workload Identity Federation).
- Implementing data exfiltration prevention around Cloud Storage or BigQuery (VPC-SC).
- Conducting a security audit or quarterly IAM review.
- Setting up CMEK key rotation for sensitive workloads.

## Skip If (ANY kills it)

- Network topology design — use gcp-networking-vpc for VPC, firewall, and Cloud Armor.
- Compute or GKE cluster provisioning — use gcp-compute-gke.

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
