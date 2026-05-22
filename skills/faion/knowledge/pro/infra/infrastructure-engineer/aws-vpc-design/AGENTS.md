---
slug: aws-vpc-design
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A production VPC uses a three-tier subnet layout (public/private/database) across a minimum of 3 Availability Zones, per-AZ NAT Gateways for high availability, VPC endpoints for cost-free private AWS service access, and VPC Flow Logs to S3 for security auditing.
content_id: "cf6d3dd7ce7b9165"
tags: [aws, vpc, networking, subnets, terraform]
---
# AWS VPC Architecture Design

## Summary

**One-sentence:** A production VPC uses a three-tier subnet layout (public/private/database) across a minimum of 3 Availability Zones, per-AZ NAT Gateways for high availability, VPC endpoints for cost-free private AWS service access, and VPC Flow Logs to S3 for security auditing.

**One-paragraph:** A production VPC uses a three-tier subnet layout (public/private/database) across a minimum of 3 Availability Zones, per-AZ NAT Gateways for high availability, VPC endpoints for cost-free private AWS service access, and VPC Flow Logs to S3 for security auditing. All configuration is Terraform-managed via the terraform-aws-modules/vpc module.

## Applies If (ALL must hold)

- Any new workload requiring an isolated network environment on AWS.
- Migrating a workload from a flat or poorly segmented network to a properly tiered architecture.
- When adding EKS or ECS to an existing VPC — requires specific subnet tagging for load balancer discovery.
- Multi-VPC architectures where Transit Gateway connects spoke VPCs to a shared hub.

## Skip If (ANY kills it)

- Lambda-only workloads with no VPC requirements — attaching Lambda to a VPC adds cold-start overhead without benefit if no private resources need access.
- Purely serverless architectures where all backends are public AWS APIs — VPC endpoints add cost without value.

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
