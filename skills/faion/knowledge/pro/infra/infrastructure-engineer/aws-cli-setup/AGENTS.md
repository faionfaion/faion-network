---
slug: aws-cli-setup
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Install AWS CLI v2 on Linux, configure named profiles and credential files, and manage authentication via environment variables for multi-account, multi-region workflows.
content_id: "bc6731f3864a7f89"
tags: [aws, cli, credentials, profiles]
---
# AWS CLI v2 Setup and Profile Management

## Summary

**One-sentence:** Install AWS CLI v2 on Linux, configure named profiles and credential files, and manage authentication via environment variables for multi-account, multi-region workflows.

**One-paragraph:** Install AWS CLI v2 on Linux, configure named profiles and credential files, and manage authentication via environment variables for multi-account, multi-region workflows. Profile-per-environment isolation prevents credential leaks between dev and production.

## Applies If (ALL must hold)

- Setting up a new developer workstation or CI runner for AWS access.
- Adding a new AWS account (dev, staging, prod) to an existing workflow.
- Configuring assume-role profiles for cross-account access.
- Debugging authentication failures (wrong profile, expired tokens).

## Skip If (ANY kills it)

- EC2 instances and ECS tasks — use IAM instance roles/task roles; no CLI credentials file needed.
- Lambda functions — use execution roles; never embed credentials.
- Production automation — prefer IAM roles with STS AssumeRole over long-lived access keys.

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
