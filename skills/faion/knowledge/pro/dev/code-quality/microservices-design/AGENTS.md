---
slug: microservices-design
tier: pro
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Microservices architecture structures an application as independently deployable services where each service owns its data, exposes a well-defined API, and communicates through HTTP or async messaging.
content_id: "81a5166177c7a679"
tags: [microservices, architecture, distributed-systems, async-messaging, fastapi]
---
# Microservices Design

## Summary

**One-sentence:** Microservices architecture structures an application as independently deployable services where each service owns its data, exposes a well-defined API, and communicates through HTTP or async messaging.

**One-paragraph:** Microservices architecture structures an application as independently deployable services where each service owns its data, exposes a well-defined API, and communicates through HTTP or async messaging. The core rules: each service has exactly one database (no shared tables); services never import each other's code directly; failures in one service must not cascade to others.

## Applies If (ALL must hold)

- Large application where multiple teams work on different features simultaneously
- Systems requiring independent scaling (checkout scales at 10x normal during flash sales; user service does not)
- Organizations practicing continuous deployment where lockstep releases are a bottleneck
- Technology diversity is justified (ML service in Python, billing in Java, web frontend in Node)
- High availability requirement where a single service failure must not take down the whole product

## Skip If (ANY kills it)

- Single team or early-stage startup — operational overhead (observability, CI/CD per service, networking) exceeds benefit
- Domain not yet stable — premature service boundaries become costly to re-draw as the model evolves
- Team lacks experience with distributed systems — eventual consistency, network failures, and distributed tracing require operational maturity
- Transactions must be ACID across multiple business entities — sagas add significant complexity compared to a monolith with a single DB
- Tight latency budget — each service hop adds network round-trip time

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

- parent skill: `pro/dev/code-quality/`
