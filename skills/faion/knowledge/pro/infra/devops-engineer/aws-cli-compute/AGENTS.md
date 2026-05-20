---
slug: aws-cli-compute
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reference for AWS CLI commands covering EC2 instance lifecycle, S3 object and bucket management, Lambda function management and invocation, and shared credential configuration patterns.
content_id: "d6072c8a9080dc35"
tags: [aws, cli, ec2, s3, lambda]
---
# AWS CLI — Compute and Storage Operations (EC2, S3, Lambda)

## Summary

**One-sentence:** Reference for AWS CLI commands covering EC2 instance lifecycle, S3 object and bucket management, Lambda function management and invocation, and shared credential configuration patterns.

**One-paragraph:** Reference for AWS CLI commands covering EC2 instance lifecycle, S3 object and bucket management, Lambda function management and invocation, and shared credential configuration patterns.

## Applies If (ALL must hold)

- Scripting EC2 instance launch, stop, terminate, or AMI creation workflows.
- Managing S3 bucket lifecycle, versioning, policies, and object sync operations.
- Deploying, updating, or invoking Lambda functions and managing layers and aliases.
- Setting up local AWS CLI profiles and environment variable authentication.

## Skip If (ANY kills it)

- Standing up multi-resource infrastructure — use CloudFormation or Terraform instead; see aws-cfn-terraform-templates.
- Container workloads (ECS, EKS, ECR) — see aws-cli-containers-iac for those commands.
- CI/CD automation at scale — wire CLI calls through GitHub Actions or GitLab CI rather than bare shell scripts.

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
