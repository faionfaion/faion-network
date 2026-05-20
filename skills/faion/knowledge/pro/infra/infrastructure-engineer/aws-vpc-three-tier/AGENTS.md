---
slug: aws-vpc-three-tier
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Build a production three-tier VPC: 9 subnets (3 AZs x public/private/database), per-AZ NAT gateways, free S3 gateway endpoint, interface endpoints for ECR and Secrets Manager, an internet-facing Application Load Balancer with HTTPS, VPC Flow Logs, and Transit Gateway attachment for multi-VPC connectivity.
content_id: "c3858e72c3a25def"
tags: [aws, vpc, networking, nat-gateway]
---
# AWS VPC Three-Tier Architecture: Subnets, NAT, Endpoints, ALB, Transit Gateway

## Summary

**One-sentence:** Build a production three-tier VPC: 9 subnets (3 AZs x public/private/database), per-AZ NAT gateways, free S3 gateway endpoint, interface endpoints for ECR and Secrets Manager, an internet-facing Application Load Balancer with HTTPS, VPC Flow Logs, and Transit Gateway attachment for multi-VPC connectivity.

**One-paragraph:** Build a production three-tier VPC: 9 subnets (3 AZs x public/private/database), per-AZ NAT gateways, free S3 gateway endpoint, interface endpoints for ECR and Secrets Manager, an internet-facing Application Load Balancer with HTTPS, VPC Flow Logs, and Transit Gateway attachment for multi-VPC connectivity. All CLI commands are reproducible and environment-parameterized.

## Applies If (ALL must hold)

- Setting up a new production VPC from scratch.
- Adding private and database subnet tiers to an existing single-tier VPC.
- Connecting multiple VPCs (prod, staging, shared-services) via Transit Gateway.
- Reducing NAT gateway costs by adding S3 and ECR VPC endpoints.

## Skip If (ANY kills it)

- Proof-of-concept or dev-only environments — a single public subnet with restrictive security groups is sufficient; NAT gateway costs $32/month minimum.
- Serverless-only workloads (Lambda + API Gateway + DynamoDB) with no VPC dependency — attaching Lambda to a VPC adds cold start latency and requires NAT for internet access.

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
