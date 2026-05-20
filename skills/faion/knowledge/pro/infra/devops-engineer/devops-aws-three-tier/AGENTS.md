---
slug: devops-aws-three-tier
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The three-tier pattern places the Application Load Balancer in public subnets, application workloads (ECS Fargate or EKS) in private subnets, and Aurora Serverless v2 in isolated database subnets.
content_id: "191b0a1976d3be3e"
tags: [aws, vpc, three-tier, alb, aurora]
---
# AWS Three-Tier Architecture: VPC, ALB, App, Database

## Summary

**One-sentence:** The three-tier pattern places the Application Load Balancer in public subnets, application workloads (ECS Fargate or EKS) in private subnets, and Aurora Serverless v2 in isolated database subnets.

**One-paragraph:** The three-tier pattern places the Application Load Balancer in public subnets, application workloads (ECS Fargate or EKS) in private subnets, and Aurora Serverless v2 in isolated database subnets. Security groups enforce strict least-privilege ingress between tiers. Terraform modules orchestrate the full stack.

## Applies If (ALL must hold)

- Building new cloud-native web applications that need a standard HA production baseline.
- Migrating on-premises three-tier apps to AWS with minimal architecture change.
- Designing scalable microservices that still use a shared relational database.
- Any workload requiring compliance isolation between network tiers (PCI, HIPAA).

## Skip If (ANY kills it)

- Pure serverless workloads — use devops-aws-serverless-api instead; no EC2/ECS/EKS needed.
- Single-AZ dev environments where cost matters more than HA — one NAT Gateway suffices.
- Event-driven pipelines with no persistent HTTP layer — EventBridge + Lambda + SQS is simpler.

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
