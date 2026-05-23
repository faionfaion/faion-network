---
slug: mq-reliability
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Reliability config bundle: publisher confirms, DLQ + alert, exponential backoff + jitter, prefetch limits, schema registry — produces a reliability-config YAML.
content_id: "749271e8581e8875"
complexity: medium
produces: config
est_tokens: 4500
tags: [message-queues, reliability, dead-letter-queue, backpressure, schema-versioning]
---
# Message Queue Reliability

## Summary

**One-sentence:** Reliability config bundle: publisher confirms, DLQ + alert, exponential backoff + jitter, prefetch limits, schema registry — produces a reliability-config YAML.

**One-paragraph:** Reliable message queues require four complementary practices: publisher confirms so 'published' means durably stored (not just buffered); DLQ with alerting so poison messages are isolated rather than lost silently; exponential backoff with jitter so retry storms do not DoS the broker; and backpressure via prefetch limits so slow consumers do not starve siblings or OOM the broker. Output is a reliability-config YAML covering all four plus schema registry + queue length cap.

**Ефективно для:**

- Hardening existing queues that lose messages on broker restart.
- Adding DLQ + replay runbook to queues that retry forever silently.
- Tuning prefetch + backoff to avoid retry-storm outages.
- Pinning schemas so a producer field rename does not crash consumers.

## Applies If (ALL must hold)

- Queue is in production and message loss is unacceptable.
- Broker supports publisher confirms (RabbitMQ / Kafka idempotent producer / SQS SendMessage response).
- Team owns both producer and consumer config or can mandate them via platform standards.
- Schema registry is available (or can be stood up).

## Skip If (ANY kills it)

- Queue is best-effort fan-out where message loss is acceptable.
- Throughput exceeds 1M msg/sec — different reliability model (Kafka tuned, Kinesis).
- Broker is a toy / dev-only queue (in-memory channel).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Broker config access | admin token | platform |
| Alert system | Prometheus / Datadog | ops |
| Schema registry | Confluent / Glue / Apicurio | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/backend-systems/mq-patterns/AGENTS.md` | topology choice precedes reliability tuning |

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
| `audit-existing-queues` | sonnet | Pulling current settings + comparing to policy needs judgement. |
| `draft-config` | sonnet | Reliability config requires nuance. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/reliability-config.yaml` | Reliability config skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mq-reliability.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[mq-patterns]]
- [[mq-broker-implementations]]
- [[mq-idempotent-consumers]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
