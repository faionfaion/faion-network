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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/idempotent-handler.py` | Idempotent handler pattern for queue consumers | Wave 3 of procedure: wire into consumer |
| `scripts/validate-message-queues.py` | Validate queue + consumer spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-celery]]
- [[logging-patterns]]
- [[api-error-handling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps broker capability, idempotency feasibility, and operations readiness to a rule from `01-core-rules.xml`, telling the agent whether to apply queue conventions or skip for unsuitable cases. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rabbitmq-client.py`

```python
"""rabbitmq-client.py — RabbitMQ producer + consumer with DLQ wiring.

Features:
  - Persistent delivery (delivery_mode=2)
  - Durable queues with dead-letter exchange
  - prefetch_count=10 for fair dispatch
  - Manual ack after successful processing
  - basic_nack(requeue=False) on failure → routes to DLQ

Usage:
    client = RabbitMQClient()
    client.declare_queue(QueueConfig(name="orders", durable=True,
                                     dead_letter_exchange="", dead_letter_routing_key="orders.dlq"))
    client.publish("orders", {"order_id": "123"})
    client.consume("orders", lambda msg: process(msg))
"""
import json
from dataclasses import dataclass, field
from typing import Callable, Optional

import pika


@dataclass
class QueueConfig:
    name: str
    durable: bool = True
    dead_letter_exchange: Optional[str] = None
    dead_letter_routing_key: Optional[str] = None
    message_ttl: Optional[int] = None  # milliseconds


class RabbitMQClient:
    def __init__(self, host: str = "localhost", port: int = 5672):
        params = pika.ConnectionParameters(
            host=host, port=port, heartbeat=600, blocked_connection_timeout=300
        )
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._channel.basic_qos(prefetch_count=10)

    def declare_queue(self, config: QueueConfig) -> None:
        args: dict = {}
        if config.dead_letter_exchange is not None:
            args["x-dead-letter-exchange"] = config.dead_letter_exchange
        if config.dead_letter_routing_key:
            args["x-dead-letter-routing-key"] = config.dead_letter_routing_key
        if config.message_ttl:
            args["x-message-ttl"] = config.message_ttl

        self._channel.queue_declare(
            queue=config.name,
            durable=config.durable,
            arguments=args or None,
        )

    def publish(self, queue: str, message: dict) -> None:
        self._channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent
                content_type="application/json",
            ),
        )

    def consume(self, queue: str, callback: Callable[[dict], None]) -> None:
        def _wrapper(ch, method, properties, body):
            try:
                msg = json.loads(body)
                callback(msg)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception:
                # nack without requeue → routes to DLQ
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                raise

        self._channel.basic_consume(queue=queue, on_message_callback=_wrapper, auto_ack=False)
        self._channel.start_consuming()
```
