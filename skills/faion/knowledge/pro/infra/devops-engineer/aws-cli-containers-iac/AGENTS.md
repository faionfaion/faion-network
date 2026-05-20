---
slug: aws-cli-containers-iac
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reference for AWS CLI commands covering RDS and Aurora databases, ECS/EKS/ECR container services, CloudFormation stack management, IAM user/role/policy operations, CloudWatch logs and alarms, and common deployment patterns including blue-green and disaster recovery.
content_id: "56b58c33435b18cd"
tags: [aws, cli, ecs, eks, cloudformation]
---
# AWS CLI — Containers, Databases, IaC, Identity and Monitoring

## Summary

**One-sentence:** Reference for AWS CLI commands covering RDS and Aurora databases, ECS/EKS/ECR container services, CloudFormation stack management, IAM user/role/policy operations, CloudWatch logs and alarms, and common deployment patterns including blue-green and disaster recovery.

**One-paragraph:** Reference for AWS CLI commands covering RDS and Aurora databases, ECS/EKS/ECR container services, CloudFormation stack management, IAM user/role/policy operations, CloudWatch logs and alarms, and common deployment patterns including blue-green and disaster recovery.

## Applies If (ALL must hold)

- Managing RDS instances, snapshots, parameter groups, and Aurora clusters via CLI.
- ECS cluster, task definition, service, and ECR image lifecycle operations.
- EKS cluster creation, node group scaling, and add-on management.
- CloudFormation stack create/update/delete with change sets and output extraction.
- IAM user, role, policy, and permission boundary management.
- CloudWatch log querying, metric retrieval, alarm management, and dashboards.

## Skip If (ANY kills it)

- EC2, S3, and Lambda operations — see aws-cli-compute for those commands.
- Repeatable multi-resource deployments — use templates from aws-cfn-terraform-templates instead.
- Production IAM changes without peer review — IAM modifications are high-risk; use IaC with version control.

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
