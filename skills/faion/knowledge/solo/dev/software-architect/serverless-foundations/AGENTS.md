---
slug: serverless-foundations
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Serverless computing abstracts infrastructure management, allowing developers to focus on code.
content_id: "781d4ef155972ec9"
tags: [serverless, faas, cloud, aws-lambda, architecture]
---
# Serverless Architecture — Foundations

## Summary

**One-sentence:** Serverless computing abstracts infrastructure management, allowing developers to focus on code.

**One-paragraph:** Serverless computing abstracts infrastructure management, allowing developers to focus on code. Functions scale from zero to thousands of instances automatically, are billed per execution (millisecond granularity), and are stateless by design — all state lives in external storage.

## Applies If (ALL must hold)

- REST/GraphQL APIs with auto-scaling, pay-per-request, and easy deployment needs.
- Event processing with native integration with queues, streams, and storage.
- Webhooks handling spiky, unpredictable traffic.
- Scheduled jobs (cron) with no idle costs between executions.
- Image/video processing requiring horizontal scale for parallel processing.
- Data transformations: ETL pipelines, real-time processing.
- MVPs and prototypes needing fast iteration with minimal ops overhead.
- Chatbots and AI workloads with burst traffic patterns and API integrations.
- IoT backends handling millions of device events.

## Skip If (ANY kills it)

- Long-running tasks (>15 min) — Lambda timeout limit; use ECS/Fargate or Step Functions instead.
- Consistent high load — cost-inefficient at scale; containers or EC2 are cheaper.
- Low latency requirements (<50ms) — cold starts add latency; use containers or keep-warm strategies.
- Complex stateful applications — requires external state management; consider Kubernetes or traditional servers.
- GPU/specialized hardware — limited instance types; use EC2 with GPU or SageMaker.
- WebSockets (persistent connections) — use API Gateway WebSocket or AppSync instead.
- Heavy compute (video encoding) — memory/CPU limits and cost; use EC2 Spot or dedicated instances.
- Compliance requiring physical isolation — multi-tenancy concerns; use dedicated infrastructure.

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
