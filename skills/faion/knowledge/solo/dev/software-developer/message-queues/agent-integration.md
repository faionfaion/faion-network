# Agent Integration — Message Queues

## When to use
- Decoupling producer and consumer services with very different throughput or availability profiles.
- Background work: emails, image/video processing, PDF generation, LLM calls, webhook fan-out.
- Load leveling during traffic spikes (sign-ups, cron job storms, marketing pushes).
- Event-driven architectures: order placed → invoice + shipping + analytics consumers.
- Fan-out / pub-sub: one publish hits many independent subscribers.
- Reliable delivery with retry + dead-letter for at-least-once processing.

## When NOT to use
- Hard real-time request/response (chat sends, payment confirmation in user UI) — use sync HTTP/RPC.
- Single-process workers — `asyncio.Queue` / Goroutines are simpler.
- Coordination of multi-step transactional flows where ordering and exactly-once matter — use a workflow engine (Temporal, Airflow, Prefect) instead.
- Streaming analytics with windowing — use Kafka + Flink/ksqlDB, not a queue.
- Storing large blobs — queues are for **references**; put bytes in S3/object storage.

## Where it fails / limitations
- "Exactly once" is a marketing promise; in practice plan for at-least-once and design idempotent consumers.
- DLQ without an alerting + replay process becomes a black hole.
- Unbounded retries on a poison message stop the queue for everyone (head-of-line blocking on FIFO queues).
- Queues don't enforce ordering across partitions/shards; if you need global order, throughput is capped at one consumer.
- RabbitMQ TTL+DLX patterns silently lose messages if exchange/queue not declared exactly right.
- Redis Streams are great until memory pressure → maxlen trims unread messages.
- Celery + Redis broker has no transactional guarantees for `apply_async` from inside a DB transaction — use `transaction.on_commit()`.
- SQS: 256 KB hard message limit; visibility timeout misconfig → duplicate processing.
- Kafka adds operational cost (Zookeeper/KRaft, ZK upgrades, partition rebalancing); overkill for solo SaaS.

## Agentic workflow
A planner subagent picks the broker (RabbitMQ vs Redis Streams vs Celery vs SQS vs Kafka) based on guarantees needed (at-least-once / ordering / fan-out / TTL / size). An implementer subagent writes producer + consumer + DLQ wiring + retry policy. A reliability subagent generates idempotency tests (replay same message N times) and chaos tests (kill consumer mid-process, restart, verify no duplicate effect). A monitoring subagent provisions queue-depth + age-of-oldest-message dashboards + alerts.

### Recommended subagents
- `faion-sdd-executor-agent` — runs spec → code → idempotency-tests → review.
- A user-defined `chaos-runner` (model: haiku) — simulates consumer crash mid-handler, verifies replay safety.
- A user-defined `idempotency-auditor` (model: sonnet) — reads handler code, flags non-idempotent operations (raw INSERTs, non-conditional emails, charges without idempotency key).
- `password-scrubber-agent` — sweep messages and tests for embedded credentials.

### Prompt pattern
- "Read `message-queues/README.md`. Given workload `<X>` (rate, payload size, ordering, retry semantics), pick a broker and justify in 5 bullets. Output a YAML config: queue names, DLQ name, max receive count, TTL, prefetch."
- "Implement RabbitMQ producer + consumer for `orders` with DLQ, persistent delivery, prefetch=10, manual ack. Add a unit test that proves replaying the same message twice causes exactly one DB row. Use the `idempotency_key` column."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rabbitmqadmin` | Declare queues/exchanges, publish, consume from CLI | bundled with RabbitMQ |
| `redis-cli` / `valkey-cli` | `XADD`, `XREADGROUP`, `XPENDING` for Streams ops | bundled |
| `awscli` (`aws sqs`) | Send/receive/inspect SQS queues | `pip install awscli` |
| `kcat` (former `kafkacat`) | Kafka producer/consumer/inspector | https://github.com/edenhill/kcat |
| `kaf` | Friendlier Kafka CLI | https://github.com/birdayz/kaf |
| `celery` CLI | `celery -A app inspect active` / `purge` / `events` | `pip install celery` |
| `flower` | Celery monitoring dashboard | `pip install flower` |
| `pulsar-admin` | Pulsar topic ops | bundled |
| `nats` CLI | NATS / JetStream ops | https://docs.nats.io/using-nats/nats-tools/nats_cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| RabbitMQ | OSS | Yes | Mature; classic, quorum, streams queues; great DLX/TTL. |
| Redis Streams / Valkey | OSS | Yes | Lightweight, consumer groups, ack model. |
| AWS SQS | SaaS | Yes (boto3, IaC) | Standard + FIFO; built-in DLQ; trivial to scale. |
| AWS SNS + SQS fan-out | SaaS | Yes | Cheap pub-sub; combine with SQS for durable subscribers. |
| Google Pub/Sub | SaaS | Yes | At-least-once, dead-letter topics, filters. |
| Kafka / Redpanda | OSS / SaaS | Yes | Heavy; pick when ordering + replay across consumers is critical. |
| Pulsar | OSS / SaaS | Yes | Tiered storage; multi-tenant; geo-replication. |
| NATS / JetStream | OSS | Yes | Low-latency, simple ops; good for edge / IoT. |
| Celery (broker: Redis/RabbitMQ) | OSS | Yes | Python task queue; chains/groups/chords. |
| Sidekiq | OSS / SaaS | Partial | Ruby/Rails ecosystem; Redis-backed. |
| RQ / Dramatiq / Arq | OSS | Yes | Lighter Python alternatives to Celery. |
| Inngest / Trigger.dev | SaaS | Yes | TS-native event-driven workflows; great for solo. |
| Temporal | OSS / SaaS | Yes | Workflow engine, not a queue — pick when you need state machines. |

## Templates & scripts
See `templates.md` and the README for RabbitMQ, Redis Streams, Celery, SQS templates. Idempotent-handler skeleton an agent should reuse:

```python
# idempotent_handler.py
import hashlib
from contextlib import contextmanager

def message_idempotency_key(msg: dict) -> str:
    # Prefer producer-supplied id; fall back to deterministic hash.
    if mid := msg.get("idempotency_key"):
        return mid
    body = repr(sorted(msg.items())).encode()
    return hashlib.sha256(body).hexdigest()

@contextmanager
def claim_once(db, key: str):
    # Postgres example: UNIQUE(idempotency_key) on processed_messages.
    inserted = db.execute(
        "INSERT INTO processed_messages(key) VALUES (%s) ON CONFLICT DO NOTHING RETURNING 1",
        (key,),
    ).fetchone()
    if not inserted:
        yield False  # duplicate, skip
        return
    try:
        yield True
        db.commit()
    except Exception:
        db.rollback()
        # row stays unless caller deletes — choose: delete on failure for retry, keep for poison-stop
        db.execute("DELETE FROM processed_messages WHERE key = %s", (key,))
        db.commit()
        raise

# Usage inside consumer callback:
def handler(msg, db):
    key = message_idempotency_key(msg)
    with claim_once(db, key) as fresh:
        if not fresh:
            return  # silently ack
        do_work(msg, db)
```

## Best practices
- Make every consumer **idempotent** (DB unique key, `ON CONFLICT DO NOTHING`, conditional updates with `version`/`updated_at`).
- Always wire a DLQ with `max_receive_count` (3-5). Add an alert when DLQ > 0.
- Set `prefetch_count` (RabbitMQ) / `worker_prefetch_multiplier=1` (Celery) for slow handlers; otherwise one worker hogs messages.
- Use **manual ack** + ack-after-success; never `auto_ack` for anything important.
- Persist messages (`delivery_mode=2`) for durable queues; mirror or use quorum queues for HA.
- Include `correlation_id` and `causation_id` headers for tracing through fan-out trees.
- Use `transaction.on_commit()` (Django) / outbox pattern when enqueuing from inside DB transactions, otherwise consumers race the writer.
- Keep payloads small (<10 KB ideal, <100 KB hard limit, <256 KB SQS limit). Put blobs in S3, send the URL.
- Set `MessageRetentionPeriod` on DLQs ≥14 days so you have time to triage.
- For Kafka: pick `key` deliberately — wrong key = wrong partition = lost ordering guarantees.
- Prefer **producer-supplied idempotency keys** (UUIDv7 tied to a domain action) over content hashes.
- Add jitter to retry backoff to avoid thundering herds on transient failures.

## AI-agent gotchas
- LLMs paste the README's `auto_ack=False` example then forget to actually `basic_ack` in the success path; messages get re-delivered on prefetch refill.
- Agents emit consumers without idempotency. Force the `idempotency_key` table + `ON CONFLICT` in every plan.
- DLQ wiring with RabbitMQ `dead-letter-exchange`/`dead-letter-routing-key`: agents declare queues with mismatched arguments and silently get a different queue. Always test by publishing a known-bad message and checking the DLQ.
- Celery `task_acks_late=True` is required for safe replay but agents skip it because the default is `False`.
- For AWS SQS, agents forget visibility timeout > p99 handler runtime → message processed twice in parallel.
- Redis Streams `XCLAIM` for stuck-consumer recovery is omitted by default; without it, crashed consumers block messages forever.
- Agents fan-out via app code (`for sub in subs: queue.publish(...)`) instead of using exchange/topic — this loses durability if the publisher crashes mid-loop.
- Outbox pattern is rarely emitted by default; LLMs publish from inside the DB transaction and you lose messages if the broker is briefly down.
- Human-in-loop checkpoint: any change to retry counts, visibility timeout, or DLQ wiring on production-payment / production-email queues must be human-approved.
- Watch for log-spam: agents log every consumed message at INFO; in production, sample or move to DEBUG.

## References
- RabbitMQ tutorials — https://www.rabbitmq.com/tutorials
- Redis Streams — https://redis.io/docs/data-types/streams/
- Celery best practices — https://docs.celeryq.dev/en/stable/userguide/tasks.html#best-practices
- AWS SQS DLQs — https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
- Kafka design — https://kafka.apache.org/documentation/#design
- Outbox pattern — https://microservices.io/patterns/data/transactional-outbox.html
- Enterprise Integration Patterns — https://www.enterpriseintegrationpatterns.com/
- Idempotent receivers — https://en.wikipedia.org/wiki/Idempotence#Computer_science_meaning
