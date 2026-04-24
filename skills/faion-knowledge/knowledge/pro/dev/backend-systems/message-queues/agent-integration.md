# Agent Integration — Message Queues

## When to use
- Decoupling producer/consumer services so failures isolate (the order service shouldn't block when the email service is down).
- Async background jobs (image resize, ETL, ML inference) where users shouldn't wait on the response path.
- Load leveling — absorb traffic spikes that the downstream can't handle synchronously.
- Event-driven architectures with multiple consumers (audit, analytics, search index) per published event.
- Reliable hand-off across process / network boundaries with at-least-once or exactly-once delivery semantics.

## When NOT to use
- Request/response with low latency requirement (<50 ms end-to-end) — synchronous gRPC/HTTP wins.
- Strong-consistency, transactional flows that span multiple services — use SAGA or 2PC, but understand the trade-offs first.
- "Just to scale" without measuring backpressure or queue depth — adds operational burden.
- Cache invalidation chains (use pub/sub on Redis) or pure fan-out logging (use a log shipper).
- Tiny apps that fit on one box — a goroutine + channel or a Python `queue.Queue` is simpler and faster.

## Where it fails / limitations
- The README's `RabbitMQClient` opens the connection lazily on every channel access — under load this thrashes connections; agents should hold one connection per process.
- DLQ without alerting is silent failure: messages pile up, nobody notices, business logic stops working.
- "Exactly once" is mostly a marketing claim. Build idempotent consumers and accept at-least-once unless your broker explicitly supports transactions (Kafka EOS, RabbitMQ confirms + dedup).
- Ordering guarantees are partition-scoped (Kafka, Kinesis) or queue-scoped (RabbitMQ); agents assume global order and write code that breaks under sharding.
- Poison messages: a single malformed payload retried infinitely consumes a worker. DLQ + max-retry is mandatory.
- Backpressure: producers without flow control fill brokers and OOM them. Set queue length limits + producer-side acks.

## Agentic workflow
Treat the contract (topic name, schema, partition key, retry/DLQ policy, ordering, idempotency strategy) as the primary deliverable — write it before code. One agent designs the contract; another implements producer + consumer with structured logging, metrics, and a deterministic test that drains the DLQ. Always include a chaos test: kill the broker mid-flight, restart, and verify zero loss + zero duplicate side effects.

### Recommended subagents
- `faion-sdd-executor-agent` — runs SDD; quality gates should require an integration test that publishes + consumes against a containerized broker.
- A custom `mq-contract-reviewer` (Opus, read-only) — checks that schema, partition key, retries, DLQ, and idempotency are all defined before approval.
- `password-scrubber-agent` — broker URLs, SASL credentials, and AWS keys often leak into config files.

### Prompt pattern
```
Add an async path: producer publishes <event_name> on <topic>, consumer in <service> processes it.
Deliver: (1) contract.md (schema, partition key, ordering, retry policy, DLQ, idempotency key, replay strategy),
(2) producer code (with confirms/acks, structured log per publish),
(3) consumer code (idempotent, ctx-driven shutdown, metrics: consumed/failed/dlq/lag),
(4) integration test (testcontainers Kafka/RabbitMQ),
(5) chaos test (broker restart mid-flight).
Forbid: auto-ack, infinite retry without DLQ, consumer that mutates DB without idempotency check.
```

```
Audit consumer.go: confirm idempotency key, ack-after-commit ordering, DLQ on terminal failure, max-retry ceiling. Output JSON {findings: [{file:line, rule, severity}]}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rabbitmqctl` / `rabbitmqadmin` | RabbitMQ admin: queues, bindings, consumers, dead-letter | https://www.rabbitmq.com/cli.html |
| `rabbitmq-diagnostics` | Health checks, memory pressure | https://www.rabbitmq.com/rabbitmq-diagnostics.8.html |
| `kafka-topics.sh` / `kafka-consumer-groups.sh` | Kafka admin, lag, reset | https://kafka.apache.org/documentation/#basic_ops |
| `kcat` (was kafkacat) | Produce/consume from CLI; dump partitions | https://github.com/edenhill/kcat |
| `redpanda rpk` | Kafka-API admin with cleaner UX | https://docs.redpanda.com/current/reference/rpk/ |
| `aws sqs` | Send/receive/purge queues, DLQ inspection | https://docs.aws.amazon.com/cli/latest/reference/sqs/ |
| `aws sns` | Publish/topic/subscription mgmt | https://docs.aws.amazon.com/cli/latest/reference/sns/ |
| `nats` CLI | NATS streams, JetStream consumers | https://docs.nats.io/using-nats/nats-tools/nats_cli |
| `gcloud pubsub` | GCP Pub/Sub admin | https://cloud.google.com/sdk/gcloud/reference/pubsub |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| RabbitMQ | OSS / SaaS (CloudAMQP) | Yes | Best for routing topology (topic exchange + headers); confirms+publisher acks for reliability. |
| Apache Kafka | OSS | Yes | High throughput, partition-ordered; agents must understand consumer groups + offsets. |
| Confluent Cloud | SaaS | Yes | Hosted Kafka + Schema Registry + KSQL — agent-friendly REST API. |
| Redpanda | OSS / SaaS | Yes | Kafka API, no JVM/ZK; `rpk` is more agent-friendly than Kafka tools. |
| AWS SQS / SNS | SaaS | Yes | Boring, reliable; SQS FIFO for order; DLQ first-class. |
| AWS Kinesis | SaaS | Yes | Kafka-like; shard mgmt is the gotcha. |
| GCP Pub/Sub | SaaS | Yes | Push or pull; ordering keys + dead-letter native. |
| NATS / JetStream | OSS | Yes | Lightweight; JetStream gives durable streams + consumers. |
| Temporal | OSS / SaaS | Yes | Not a queue, but often replaces hand-rolled saga + retry on top of MQs. |
| RabbitMQ Streams | OSS | Partial | New stream protocol; agent training data is thin — verify outputs. |

## Templates & scripts
See `templates.md` and `examples.md` for RabbitMQ/Kafka/SQS producer + consumer scaffolds. Idempotent consumer skeleton (≤40 lines):

```python
# consumers/idempotent.py
import json, hashlib, redis, logging
log = logging.getLogger(__name__)
r = redis.Redis(decode_responses=True)
DEDUP_TTL = 7 * 24 * 3600  # 7 days

def handle(message_bytes: bytes, process):
    msg = json.loads(message_bytes)
    key = msg.get("idempotency_key") or hashlib.sha256(message_bytes).hexdigest()
    dedup_key = f"mq:dedup:{key}"

    # Reserve the slot atomically; if already taken, skip.
    if not r.set(dedup_key, "1", nx=True, ex=DEDUP_TTL):
        log.info("duplicate message, skipping", extra={"key": key})
        return "ack"

    try:
        process(msg)
        return "ack"
    except TransientError:
        r.delete(dedup_key)        # Allow retry to re-process.
        return "nack-requeue"
    except Exception:               # noqa: BLE001
        log.exception("terminal failure, sending to DLQ", extra={"key": key})
        return "nack-dlq"
```

## Best practices
- Define the message schema in a registry (Avro/Protobuf/JSON Schema) and version it. Consumers must be backward-compatible across at least one version.
- Idempotency key on every message; consumer dedups via Redis/DB unique index. Don't trust "exactly once".
- Set max retries + exponential backoff + jitter; on terminal failure, route to a DLQ with the original payload + error metadata.
- Alert on queue depth, consumer lag (Kafka), DLQ size, oldest-unacked-age. These are your earliest incident signals.
- Producers use confirms (RabbitMQ) / `acks=all` (Kafka). Without confirms, "published" means "buffered locally".
- Consumers ack only after the side-effect is committed (DB write, downstream call). Acking before commit is the #1 source of message loss.
- Limit prefetch / max-in-flight so a slow consumer doesn't gobble the queue and starve siblings.

## AI-agent gotchas
- LLMs default to `auto_ack=True` because the SDK examples do. This silently loses messages on consumer crash. Force `auto_ack=False`.
- Agents publish before the DB transaction commits — if the DB rolls back, the consumer sees a phantom event. Use the transactional outbox pattern.
- "Exactly once" is requested constantly; agents will claim Kafka EOS gives it without enabling the right configs (`enable.idempotence`, transactional producer, `read_committed`). Force a config audit.
- Schemas drift: agents add fields without bumping version; old consumers crash. Block additions without a migration note.
- Retry storms: on broker hiccup, agents add naive `while True: retry()` and DOS the broker. Require backoff + circuit breaker.
- DLQ becomes a graveyard if no one drains it. Always include a tooling task (`scripts/replay_dlq.py`) and a runbook.
- Human-in-loop checkpoint: any new topic / queue, schema change, or retry-policy change in production needs explicit reviewer approval — they have long tails.

## References
- "Enterprise Integration Patterns" (Hohpe, Woolf) — canonical pattern catalog.
- "Designing Data-Intensive Applications" (Kleppmann) — chapters 4, 11.
- RabbitMQ in Depth (Roy) — implementation detail.
- Kafka docs: consumer groups, EOS — https://kafka.apache.org/documentation/
- Confluent: idempotent producer — https://docs.confluent.io/platform/current/clients/producer.html#idempotent-producer
- AWS SQS DLQ — https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
- Transactional outbox pattern — https://microservices.io/patterns/data/transactional-outbox.html
