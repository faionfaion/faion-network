# Message Broker Implementations

## Summary

**One-sentence:** Production-ready Python implementations for the four most common message brokers: RabbitMQ (pika), Redis Streams (redis-py), Celery, and AWS SQS (boto3).

**One-paragraph:** Production-ready Python implementations for the four most common message brokers: RabbitMQ (pika), Redis Streams (redis-py), Celery (task queue with chains/groups/chords), and AWS SQS (boto3). Each implementation covers queue declaration, persistent publishing with confirms, consumer with explicit ack/nack, and DLQ wiring. Output is a Python module plus a deployment manifest naming the broker + topology + DLQ + alert thresholds.

**Ефективно для:**

- Standing up RabbitMQ with publisher confirms and topic routing for cross-team events.
- Building a Redis Streams consumer group with replayable history on existing Redis.
- Migrating ad-hoc cron jobs to Celery chains/groups with proper DLQ + retry policy.
- Wiring AWS SQS with FIFO ordering or DLQ-on-poison for serverless workloads.

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

| Artefact | Format | Source |
|----------|--------|--------|
| Broker choice + topology | yaml / md | team — picked via mq-patterns |
| Connection credentials | secret manager ref | vault |
| DLQ + alert thresholds | yaml / config | team SLO catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/backend-systems/mq-patterns/AGENTS.md` | topology decision precedes implementation |
| `pro/dev/backend-systems/mq-reliability/AGENTS.md` | reliability practices apply to every impl |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-broker` | sonnet | Decision tree application against constraints. |
| `draft-impl` | sonnet | Each broker requires light judgement on retry + ack timing. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | Broker connection + topology + DLQ + alert manifest |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mq-broker-implementations.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[mq-patterns]]
- [[mq-reliability]]
- [[mq-idempotent-consumers]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
