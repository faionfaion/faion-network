# Message Queues

## Summary

Asynchronous message passing between services using brokers (RabbitMQ, Redis Streams, Celery, SQS) with mandatory idempotent consumers, dead-letter queues (DLQ) with alerts, manual acknowledgment, and explicit retry policies. Every consumer must implement an idempotency key check before processing; every queue must have a paired DLQ with max-receive-count 3-5.

## Why

Distributed async processing fails silently when consumers are not idempotent and DLQs are absent. "At-least-once" delivery is the practical guarantee of every broker; without idempotency, duplicate messages corrupt data. Without DLQ + alert, poison messages block queues indefinitely. The outbox pattern prevents message loss when publishing inside DB transactions.

## When To Use

- Decoupling producer and consumer services with different throughput or availability profiles.
- Background work: emails, image processing, LLM calls, webhook fan-out.
- Load leveling during traffic spikes.
- Event-driven architectures: one publish → multiple independent subscribers.
- Reliable delivery with retry + dead-letter for at-least-once processing.

## When NOT To Use

- Hard real-time request/response (chat, payment confirmation in user UI) — use sync HTTP/RPC.
- Single-process workers — `asyncio.Queue` or goroutines are simpler.
- Multi-step transactional flows where ordering and exactly-once matter — use a workflow engine (Temporal, Airflow).
- Streaming analytics with windowing — use Kafka + Flink/ksqlDB.
- Storing large blobs — queues are for references; put bytes in S3/object storage.

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Work queue, pub/sub, request/reply, DLQ patterns; broker selection guide. |
| `content/02-implementations.xml` | RabbitMQ, Redis Streams, Celery, SQS code with DLQ wiring and retry policy. |
| `content/03-antipatterns.xml` | No idempotency, missing DLQ, auto-ack, Celery transaction race, SQS visibility timeout. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rabbitmq-client.py` | RabbitMQ producer + consumer with DLQ, persistent delivery, prefetch, manual ack. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/idempotent-handler.py` | DB-backed idempotency key claim with ON CONFLICT DO NOTHING; reusable in any consumer. |
