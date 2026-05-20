---
slug: devops-aws-serverless-api
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The serverless API pattern uses API Gateway HTTP API as the entry point, Lambda on arm64 (Graviton) for compute, DynamoDB (single-table, on-demand) for state, EventBridge for event routing, SQS with DLQ for async buffering, and Step Functions for multi-step orchestration.
content_id: "eea5548fcf0edc14"
tags: [aws, serverless, lambda, api-gateway, dynamodb]
---
# AWS Serverless API: Lambda + API Gateway + DynamoDB + EventBridge

## Summary

**One-sentence:** The serverless API pattern uses API Gateway HTTP API as the entry point, Lambda on arm64 (Graviton) for compute, DynamoDB (single-table, on-demand) for state, EventBridge for event routing, SQS with DLQ for async buffering, and Step Functions for multi-step orchestration.

**One-paragraph:** The serverless API pattern uses API Gateway HTTP API as the entry point, Lambda on arm64 (Graviton) for compute, DynamoDB (single-table, on-demand) for state, EventBridge for event routing, SQS with DLQ for async buffering, and Step Functions for multi-step orchestration. All resources are managed with terraform-aws-modules. 60–80% cost reduction vs always-on containers for variable traffic.

## Applies If (ALL must hold)

- REST/GraphQL APIs with variable or spiky traffic (dev tools, internal dashboards, webhook handlers).
- Event-driven async processing where tasks complete in under 15 minutes.
- Workloads that need to scale to zero overnight to minimize cost.
- New greenfield services where container orchestration overhead is not justified.
- GenAI RAG pipelines on Bedrock — Lambda + API Gateway + DynamoDB is the standard glue layer.

## Skip If (ANY kills it)

- Long-running tasks exceeding 15 minutes — use Fargate or EKS instead.
- High-throughput workloads with steady baseline traffic — always-on containers are cheaper above ~80% CPU.
- Applications requiring in-process state or shared memory — Lambda is stateless per invocation.
- Complex relational queries — DynamoDB is key-value; use Aurora Serverless v2 via devops-aws-three-tier.

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
