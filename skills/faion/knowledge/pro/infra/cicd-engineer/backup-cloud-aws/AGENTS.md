---
slug: backup-cloud-aws
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implement AWS-native backup using AWS Backup service (vaults, plans, cross-region copy rules) for managed resources (RDS, DynamoDB, EBS, EFS), and S3 lifecycle policies for object storage tiering.
content_id: "d1c9cf87d910f061"
tags: [backup, aws-backup, s3, terraform, immutable]
---
# Cloud-Native Backup with AWS Backup and S3

## Summary

**One-sentence:** Implement AWS-native backup using AWS Backup service (vaults, plans, cross-region copy rules) for managed resources (RDS, DynamoDB, EBS, EFS), and S3 lifecycle policies for object storage tiering.

**One-paragraph:** Implement AWS-native backup using AWS Backup service (vaults, plans, cross-region copy rules) for managed resources (RDS, DynamoDB, EBS, EFS), and S3 lifecycle policies for object storage tiering. Enable S3 Object Lock for immutable ransomware-resistant backups. Provision the full stack as Terraform IaC.

## Applies If (ALL must hold)

- AWS-hosted workloads with RDS, DynamoDB, EBS, or EFS resources that need centralized backup policy management.
- Compliance requirements mandating cross-region backup copies and immutable retention periods.
- Cost optimization for existing backup buckets where objects never leave Standard storage class.
- Ransomware protection requiring object lock (WORM) on backup storage.
- Consolidating fragmented per-service backup scripts into a single Terraform-managed AWS Backup plan.

## Skip If (ANY kills it)

- On-premises or non-AWS workloads — use Restic, BorgBackup, or Velero with self-managed object storage instead.
- Simple S3-bucket-to-bucket replication where S3 native replication (CRR) is sufficient and AWS Backup overhead is not justified.
- Kubernetes workload backup — use Velero which understands K8s resource state; AWS Backup only covers underlying EBS/EFS volumes.

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

- parent skill: `pro/infra/cicd-engineer/`
