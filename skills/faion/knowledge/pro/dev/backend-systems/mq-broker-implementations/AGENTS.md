---
slug: mq-broker-implementations
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-ready Python implementations for the four most common message brokers: RabbitMQ (pika), Redis Streams (redis-py), Celery (task queue with chains/groups/chords), and AWS SQS (boto3).
content_id: "2008697d50f64d41"
tags: [rabbitmq, redis-streams, celery, sqs, message-queues]
---
# Message Broker Implementations

## Summary

**One-sentence:** Production-ready Python implementations for the four most common message brokers: RabbitMQ (pika), Redis Streams (redis-py), Celery (task queue with chains/groups/chords), and AWS SQS (boto3).

**One-paragraph:** Production-ready Python implementations for the four most common message brokers: RabbitMQ (pika), Redis Streams (redis-py), Celery (task queue with chains/groups/chords), and AWS SQS (boto3). Each includes queue declaration, persistent publishing, consumer with explicit ack/nack, and DLQ wiring.

## Applies If (ALL must hold)

- RabbitMQ — when routing topology matters (topic exchange, headers exchange) or when publisher confirms are required for guaranteed delivery.
- Redis Streams — when you already run Redis and need lightweight event sourcing with consumer groups; shard-level ordering is acceptable.
- Celery — when you need a task queue abstraction over Redis or RabbitMQ with built-in retry, periodic tasks, and workflow primitives (chain, group, chord).
- AWS SQS — when running on AWS and wanting a managed, boring queue with first-class DLQ support and FIFO ordering option.

## Skip If (ANY kills it)

- RabbitMQ — when throughput exceeds millions of messages per second; use Kafka or Kinesis instead.
- Redis Streams — when ordering must be global across all partitions, not just per-stream; and when persistence must survive Redis restart without AOF/RDB.
- Celery — when you need strict exactly-once or when the Celery abstraction hides broker behavior you must control precisely.
- SQS — when running outside AWS or when message retention beyond 14 days is required.

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

- parent skill: `pro/dev/backend-systems/`
