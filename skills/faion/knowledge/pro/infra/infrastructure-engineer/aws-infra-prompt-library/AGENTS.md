---
slug: aws-infra-prompt-library
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Parameterized prompt templates for generating, auditing, troubleshooting, and documenting AWS infrastructure.
content_id: "3d2a91245cd23346"
tags: [aws, prompts, llm, infrastructure]
---
# AWS Infrastructure LLM Prompt Library

## Summary

**One-sentence:** Parameterized prompt templates for generating, auditing, troubleshooting, and documenting AWS infrastructure.

**One-paragraph:** Parameterized prompt templates for generating, auditing, troubleshooting, and documenting AWS infrastructure. Each prompt targets a specific task category: generation (VPC, IAM, ASG), security analysis, troubleshooting, cost optimization, migration planning, documentation, and compliance verification.

## Applies If (ALL must hold)

- Generating Terraform or CloudFormation for a new VPC, security group set, or IAM role.
- Auditing an existing IAM policy or security group configuration for least-privilege violations.
- Troubleshooting connectivity failures between EC2 instances, ECS tasks, or Lambda functions.
- Planning Reserved Instance purchases or identifying cost optimization opportunities.
- Planning a workload or database migration to AWS.
- Preparing compliance evidence or generating operational runbooks.

## Skip If (ANY kills it)

- Production infrastructure changes without human review — always validate generated IaC in a staging environment first.
- Compliance audit sign-off — prompts assist investigation, but formal compliance requires authoritative tooling (AWS Config rules, Security Hub).

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
