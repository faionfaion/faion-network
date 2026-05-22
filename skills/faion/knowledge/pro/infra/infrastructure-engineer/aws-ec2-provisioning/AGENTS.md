---
slug: aws-ec2-provisioning
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Provision EC2 instances with IMDSv2 enforced, encrypted gp3 EBS volumes, and SSM Session Manager (no SSH keys).
content_id: "6601feaf6af7d8ea"
tags: [aws, ec2, auto-scaling, launch-template]
---
# EC2 Provisioning: Launch Templates, Auto Scaling, and Security Groups

## Summary

**One-sentence:** Provision EC2 instances with IMDSv2 enforced, encrypted gp3 EBS volumes, and SSM Session Manager (no SSH keys).

**One-paragraph:** Provision EC2 instances with IMDSv2 enforced, encrypted gp3 EBS volumes, and SSM Session Manager (no SSH keys). Use launch templates for reproducible configuration and Auto Scaling Groups with target tracking scaling to handle variable load. Create security groups per application tier — web, app, database — referencing each other by group ID rather than CIDR.

## Applies If (ALL must hold)

- Provisioning EC2-backed services that need horizontal scaling.
- Creating reproducible instance configurations for multiple environments.
- Setting up role-based three-tier security group topology (ALB → app → database).
- Migrating existing instances to launch template + ASG pattern for zero-downtime instance refresh.

## Skip If (ANY kills it)

- Single throwaway instances — use `aws ec2 run-instances` directly; launch template overhead not justified.
- Containerized workloads at scale — use ECS Fargate or EKS instead of EC2-backed ASGs.
- Stateful single-instance workloads — ASG with min=1 is fine, but target tracking scaling does not apply.

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
