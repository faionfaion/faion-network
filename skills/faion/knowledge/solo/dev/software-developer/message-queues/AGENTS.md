---
slug: message-queues
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Asynchronous message passing between services using brokers (RabbitMQ, Redis Streams, Celery, SQS) with mandatory idempotent consumers, dead-letter queues (DLQ) with alerts, manual acknowledgment, and explicit retry policies.
content_id: "2d111252aba48685"
tags: [message-queues, async, idempotency, dlq, reliability]
---
# Message Queue Patterns and Implementation

## Summary

**One-sentence:** Asynchronous message passing between services using brokers (RabbitMQ, Redis Streams, Celery, SQS) with mandatory idempotent consumers, dead-letter queues (DLQ) with alerts, manual acknowledgment, and explicit retry policies.

**One-paragraph:** Asynchronous message passing between services using brokers (RabbitMQ, Redis Streams, Celery, SQS) with mandatory idempotent consumers, dead-letter queues (DLQ) with alerts, manual acknowledgment, and explicit retry policies. Every consumer must implement an idempotency key check before processing; every queue must have a paired DLQ with max-receive-count 3-5.

## Applies If (ALL must hold)

- Decoupling producer and consumer services with different throughput or availability profiles.
- Background work: emails, image processing, LLM calls, webhook fan-out.
- Load leveling during traffic spikes.
- Event-driven architectures: one publish to multiple independent subscribers.
- Reliable delivery with retry + dead-letter for at-least-once processing.
- Decoupling producer and consumer services with very different throughput or availability profiles.
- Background work: emails, image/video processing, PDF generation, LLM calls, webhook fan-out.
- Load leveling during traffic spikes (sign-ups, cron job storms, marketing pushes).
- Event-driven architectures: order placed to invoice + shipping + analytics consumers.
- Fan-out / pub-sub: one publish hits many independent subscribers.

## Skip If (ANY kills it)

- Hard real-time request/response (chat, payment confirmation in user UI) — use sync HTTP/RPC.
- Single-process workers — asyncio.Queue or goroutines are simpler.
- Multi-step transactional flows where ordering and exactly-once matter — use a workflow engine (Temporal, Airflow).
- Streaming analytics with windowing — use Kafka + Flink/ksqlDB.
- Storing large blobs — queues are for references; put bytes in S3/object storage.
- Coordination of multi-step transactional flows where ordering and exactly-once matter — use a workflow engine (Temporal, Airflow, Prefect) instead.
- Streaming analytics with windowing — use Kafka + Flink/ksqlDB, not a queue.

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

- parent skill: `solo/dev/software-developer/`
