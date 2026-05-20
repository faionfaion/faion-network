---
slug: aws-lambda
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Serverless function design, cold start optimization, layer management, and event source configuration for AWS Lambda.
content_id: "b058a3dc8d8ee90d"
tags: [serverless, lambda, aws, cold-start, event-sources]
---
# AWS Lambda: Serverless Function Design, Optimization, and Event Source Configuration

## Summary

**One-sentence:** Serverless function design, cold start optimization, layer management, and event source configuration for AWS Lambda.

**One-paragraph:** Serverless function design, cold start optimization, layer management, and event source configuration for AWS Lambda. The concrete rule is: initialize all SDK clients and database connections outside the handler; use ReportBatchItemFailures for all polling event sources (SQS, Kinesis, DynamoDB Streams); use ARM64 (Graviton2) architecture by default for 20% cost reduction; enable SnapStart for Java/Python/.NET to reduce cold starts by 58-94%.

## Applies If (ALL must hold)

- Writing a new Lambda handler (Python, Node.js, Java) for any event source
- Optimizing cold start latency for latency-sensitive APIs
- Configuring SQS, Kinesis, or DynamoDB Streams event source mappings
- Packaging shared dependencies as Lambda layers
- Setting up blue-green or canary deployments with Lambda aliases
- Creating SAM or Terraform IaC for Lambda infrastructure

## Skip If (ANY kills it)

- Workloads running longer than 15 minutes — use ECS/Fargate containers instead
- Functions requiring GPU — Lambda has no GPU support; use SageMaker or ECS
- Steady-state high-concurrency APIs where provisioned concurrency cost exceeds container cost
- Kubernetes or containerized architecture decisions — use aws-architecture-services

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
