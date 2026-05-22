---
slug: serverless-iac-and-templates
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Framework selection guide (SAM for AWS-native simplicity, Serverless Framework for multi-cloud plugins, SST for TypeScript full-stack DX, CDK for complex type-safe infra) plus production-ready templates for REST APIs, SQS event processing, Step Functions workflows, scheduled jobs, and Lambda handlers (Python Powertools and TypeScript).
content_id: "78c0522112227665"
tags: [serverless, iac, sam, cdk, lambda]
---
# Serverless IaC Frameworks and Templates

## Summary

**One-sentence:** Framework selection guide (SAM for AWS-native simplicity, Serverless Framework for multi-cloud plugins, SST for TypeScript full-stack DX, CDK for complex type-safe infra) plus production-ready templates for REST APIs, SQS event processing, Step Functions workflows, scheduled jobs, and Lambda handlers (Python Powertools and TypeScript).

**One-paragraph:** Framework selection guide (SAM for AWS-native simplicity, Serverless Framework for multi-cloud plugins, SST for TypeScript full-stack DX, CDK for complex type-safe infra) plus production-ready templates for REST APIs, SQS event processing, Step Functions workflows, scheduled jobs, and Lambda handlers (Python Powertools and TypeScript).

## Applies If (ALL must hold)

- Starting a new serverless project and selecting an IaC framework.
- Scaffolding a Lambda REST API, SQS processor, Step Functions workflow, or scheduled job.
- Generating production-ready Lambda handler code with structured logging, tracing, and idempotency.
- Setting up IAM least-privilege policies for DynamoDB, S3, EventBridge, or Secrets Manager access.

## Skip If (ANY kills it)

- Existing projects with established IaC — switching frameworks mid-project requires full resource migration.
- Non-AWS serverless targets (Cloudflare Workers, Vercel) — use Wrangler or Vercel CLI instead of SAM/CDK.

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

- parent skill: `solo/dev/software-architect/`
