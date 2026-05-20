---
slug: aws-networking
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: VPC architecture, subnet segmentation, security groups, NACLs, Transit Gateway, and VPC endpoints for AWS.
content_id: "a168aa325153c86d"
tags: [networking, vpc, aws, security-groups, transit-gateway, vpc-endpoints, zero-trust]
---
# AWS Networking: VPC Architecture, Security Controls, and Connectivity Patterns

## Summary

**One-sentence:** VPC architecture, subnet segmentation, security groups, NACLs, Transit Gateway, and VPC endpoints for AWS.

**One-paragraph:** VPC architecture, subnet segmentation, security groups, NACLs, Transit Gateway, and VPC endpoints for AWS. Concrete rule: always deploy across 3 AZs with public/private/data subnet tiers; never use 0.0.0.0/0 in security group ingress except on ALB ports 80/443; use VPC endpoints for S3/DynamoDB/Secrets Manager/SSM/ECR to eliminate NAT Gateway data charges and keep traffic on the AWS backbone.

## Applies If (ALL must hold)

- Designing a new VPC with subnet segmentation (public/private/data tiers)
- Selecting connectivity pattern: VPC Peering vs Transit Gateway vs VPC Lattice
- Auditing existing security group rules for least-privilege compliance
- Setting up VPC endpoints (Gateway for S3/DynamoDB, Interface for service APIs)
- Configuring Transit Gateway for multi-VPC or hybrid on-prem connectivity (Direct Connect / Site-to-Site VPN)
- Enabling VPC Flow Logs and GuardDuty for network visibility
- Reviewing NAT Gateway architecture for cost or HA failure modes
- Migrating from VPC Peering mesh to Transit Gateway hub-and-spoke

## Skip If (ANY kills it)

- GCP networking (VPC, Cloud NAT, firewall rules) — use gcp-networking
- ALB/NLB target group configuration — use aws-architecture-services
- Route53 DNS design — out of scope; consult AWS Route53 documentation directly
- Service-specific security groups (EKS pod SG, RDS) — covered in service methodologies
- Edge networking (CloudFront, Global Accelerator) — separate methodology

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
