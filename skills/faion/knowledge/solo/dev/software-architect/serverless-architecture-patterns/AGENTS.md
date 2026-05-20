---
slug: serverless-architecture-patterns
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Six core serverless patterns — API backend, event processing, saga/orchestration, fan-out/fan-in, CQRS with event sourcing, and edge computing — plus the most common anti-patterns and real-world examples from e-commerce, data pipelines, SaaS multi-tenant, and document processing use cases.
content_id: "2ef37eed60cd4a67"
tags: [serverless, patterns, event-driven, step-functions, lambda]
---
# Serverless Architecture Patterns

## Summary

**One-sentence:** Six core serverless patterns — API backend, event processing, saga/orchestration, fan-out/fan-in, CQRS with event sourcing, and edge computing — plus the most common anti-patterns and real-world examples from e-commerce, data pipelines, SaaS multi-tenant, and document processing use cases.

**One-paragraph:** Six core serverless patterns — API backend, event processing, saga/orchestration, fan-out/fan-in, CQRS with event sourcing, and edge computing — plus the most common anti-patterns and real-world examples from e-commerce, data pipelines, SaaS multi-tenant, and document processing use cases.

## Applies If (ALL must hold)

- Composing Lambda functions into multi-step workflows requiring retry and error handling.
- Building event-driven pipelines across SQS, SNS, EventBridge, and Kinesis.
- Designing parallel processing with fan-out to multiple workers.
- Implementing CQRS or event sourcing with separate read/write paths.
- Reviewing existing serverless architecture for anti-patterns.

## Skip If (ANY kills it)

- Greenfield non-serverless design — these patterns are Lambda/FaaS specific.
- Simple CRUD endpoints without event-driven requirements — a plain API Gateway + Lambda suffices without pattern overhead.

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
