---
slug: mq-idempotent-consumers
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: At-least-once delivery means messages arrive more than once; idempotent consumers + idempotency_key + transactional outbox guarantee one observable side-effect per business event.
content_id: "c0c3248a41f8e1a5"
complexity: medium
produces: code
est_tokens: 4400
tags: [idempotency, message-queues, deduplication, transactional-outbox, reliability]
---
# Idempotent Message Queue Consumers

## Summary

**One-sentence:** At-least-once delivery means messages arrive more than once; idempotent consumers + idempotency_key + transactional outbox guarantee one observable side-effect per business event.

**One-paragraph:** At-least-once delivery means messages arrive more than once. Idempotent consumers + payload-embedded idempotency_key + atomic reserve-before-execute + ack-after-commit + transactional outbox on the producer side together guarantee one observable side-effect per business event, no matter how many times the message is delivered. Output is a Python consumer module + deduplication store schema + outbox table DDL.

**Ефективно для:**

- Order-processing consumers where double-charge is a P0 incident.
- Webhook receivers where the sender retries on every 5xx.
- Cross-service event handlers where the broker guarantees only at-least-once.
- Producers writing to DB + publishing — use transactional outbox to prevent phantom events.

## Applies If (ALL must hold)

- Broker delivers at-least-once (RabbitMQ default, SQS, Kafka without idempotent producer).
- Consumer side-effect is observable (database write, external API call, balance change).
- Producer side-effect and publish must be atomic with respect to each other.
- Team can add an idempotency_key field to every event payload.

## Skip If (ANY kills it)

- Broker provides exactly-once with verified configuration on both ends (rare, validate first).
- Side-effect is naturally idempotent (e.g. set X = Y where Y is constant).
- Message is purely informational with no downstream effect (pure read fan-out).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Event schema | Avro / Protobuf / JSON Schema | schema registry |
| Dedup store choice | Redis / Postgres / DynamoDB | team data infra |
| Outbox capability | DB capable of transactional writes | DBA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/backend-systems/mq-patterns/AGENTS.md` | topology decision precedes implementation |
| `pro/dev/backend-systems/mq-reliability/AGENTS.md` | publisher confirms + DLQ pair with idempotency |

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
| `design-dedup-store` | sonnet | Decision between TTL store / DB unique constraint / external dedup needs judgement. |
| `draft-consumer` | sonnet | Reserve-before-execute pattern is subtle; sonnet preserves nuance. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/outbox.sql` | Transactional outbox table DDL |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mq-idempotent-consumers.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[mq-patterns]]
- [[mq-reliability]]
- [[mq-broker-implementations]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
