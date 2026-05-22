---
slug: aws-architecture-services
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-ready patterns for AWS service selection, integration, and deployment.
content_id: "89e2a94a55ae4810"
tags: [aws, architecture, serverless, containers, well-architected, terraform, eventbridge]
---
# AWS Architecture Services

## Summary

**One-sentence:** Production-ready patterns for AWS service selection, integration, and deployment.

**One-paragraph:** Production-ready patterns for AWS service selection, integration, and deployment. Covers serverless vs containers, EventBridge event-driven design, the Well-Architected six pillars, and Terraform configurations for EKS, RDS Aurora, ALB, S3+CloudFront, and API Gateway. The default rule: Lambda for variable/spiky traffic under 15 minutes; containers for steady high-volume 24/7 workloads; hybrid for everything in between.

## Applies If (ALL must hold)

- Selecting compute service (Lambda vs ECS Fargate vs EKS) for a new workload
- Designing event-driven architectures with EventBridge, SNS, SQS, or Step Functions
- Applying AWS Well-Architected Framework review to existing infrastructure
- Writing Terraform for EKS clusters, Aurora, ALB, CloudFront, or API Gateway
- Performing cost optimization (Graviton migration, Spot, Reserved, Instance Scheduler)
- Reviewing a pull request that adds or modifies AWS infrastructure
- Onboarding a new account and applying baseline tags, CloudTrail, and AWS Config

## Skip If (ANY kills it)

- GCP or Azure architecture decisions — use gcp-arch-patterns or the Azure methodology instead
- Terraform syntax basics — use terraform-basics for HCL fundamentals
- VPC and networking design — use aws-networking for subnet, SG, and TGW patterns
- S3 bucket policies and lifecycle rules — use aws-s3-storage for storage-specific patterns
- Lambda function packaging and cold start tuning — use aws-lambda
- EC2 or ECS task definitions and capacity providers — use aws-ec2-ecs

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
