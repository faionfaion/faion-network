---
slug: message-queues
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Implement async message passing with idempotent consumers, DLQ + alerts, manual acknowledgement, and explicit retry policy per queue.
content_id: "2d111252aba48685"
complexity: medium
produces: code
est_tokens: 4200
tags: [message-queues, async, idempotency, dlq, reliability]
---
# Message Queue Patterns

## Summary

**One-sentence:** Implement async message passing with idempotent consumers, DLQ + alerts, manual acknowledgement, and explicit retry policy per queue.

**One-paragraph:** Asynchronous message passing between services using brokers (RabbitMQ, Redis Streams, Celery, SQS) with mandatory idempotent consumers, dead-letter queues (DLQ) with alerts, manual acknowledgment, and explicit retry policies. Producers serialise via a versioned schema; consumers tolerate at-least-once delivery. Output is the broker config + consumer module + DLQ alerting.

**Ефективно для:**

- Decoupling producers from consumers across services.
- Smoothing bursty traffic with a buffered queue.
- Adding async retries to flaky integrations.
- Replacing in-process queues with a durable broker.

## Applies If (ALL must hold)

- Producer and consumer can be decoupled (work need not be synchronous to producer).
- Broker is RabbitMQ, Redis Streams, SQS, NATS, or equivalent.
- Workloads tolerate at-least-once delivery semantics (idempotency feasible).
- Operations team can monitor queue depth + DLQ + consumer lag.

## Skip If (ANY kills it)

- Strict in-order, exactly-once requirement that broker cannot satisfy.
- Tight-latency RPC where queue overhead exceeds payoff.
- Use case is purely fan-out broadcast — pub/sub channels are simpler.
- Project already uses Celery — apply django-celery methodology instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Broker choice + version + topology (queues vs streams) | config | platform |
| Message schema with version field + payload contract | schema | tech-lead |
| Consumer idempotency strategy per queue | ADR | tech-lead |
| DLQ + alert routing (PagerDuty, Slack) | endpoint | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[logging-patterns]] | Consumer events log structured fields. |
| [[api-error-handling]] | Retry decisions consume error classifications. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (idempotent consumer, manual ack, DLQ wired, retry policy explicit, versioned message schema, no infinite retries) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for queue config + consumer spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: schema → producer → consumer → DLQ → alerts | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schema_authoring` | sonnet | Message schema with version + payload. |
| `consumer_authoring` | sonnet | Idempotent + manual-ack + retry policy. |
| `dlq_alerts_wiring` | sonnet | Threshold-based alert on DLQ depth. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rabbitmq-client.py` | RabbitMQ producer + consumer pattern with manual ack + DLQ |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/idempotent-handler.py` | Idempotent handler pattern for queue consumers | Wave 3 of procedure: wire into consumer |
| `scripts/validate-message-queues.py` | Validate queue + consumer spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[django-celery]]
- [[logging-patterns]]
- [[api-error-handling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps broker capability, idempotency feasibility, and operations readiness to a rule from `01-core-rules.xml`, telling the agent whether to apply queue conventions or skip for unsuitable cases. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
