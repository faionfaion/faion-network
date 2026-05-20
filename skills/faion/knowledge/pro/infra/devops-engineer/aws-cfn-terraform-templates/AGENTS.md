---
slug: aws-cfn-terraform-templates
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-ready CloudFormation YAML and Terraform HCL templates for common AWS infrastructure patterns: VPC networking, ECS Fargate services, serverless Lambda stacks, RDS PostgreSQL with Secrets Manager, and supporting IAM/S3/ECS configuration JSON.
content_id: "2d087b7b3af7acd9"
tags: [aws, cloudformation, terraform, iac, templates]
---
# AWS Infrastructure-as-Code Templates (CloudFormation and Terraform)

## Summary

**One-sentence:** Production-ready CloudFormation YAML and Terraform HCL templates for common AWS infrastructure patterns: VPC networking, ECS Fargate services, serverless Lambda stacks, RDS PostgreSQL with Secrets Manager, and supporting IAM/S3/ECS configuration JSON.

**One-paragraph:** Production-ready CloudFormation YAML and Terraform HCL templates for common AWS infrastructure patterns: VPC networking, ECS Fargate services, serverless Lambda stacks, RDS PostgreSQL with Secrets Manager, and supporting IAM/S3/ECS configuration JSON.

## Applies If (ALL must hold)

- Deploying a new VPC with multi-AZ public and private subnets.
- Launching an ECS Fargate service behind an Application Load Balancer.
- Setting up a serverless API with Lambda, API Gateway, and DynamoDB.
- Provisioning RDS PostgreSQL with auto-rotating credentials via Secrets Manager.
- Creating reusable Terraform modules for VPC or ECS service resources.

## Skip If (ANY kills it)

- One-off CLI operations — use aws-cli-compute or aws-cli-containers-iac commands.
- Highly customized environments where a module's defaults diverge significantly — fork and adapt rather than fight the template.
- Simple single-resource changes — use aws cloudformation update-stack with a targeted parameter override.

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
