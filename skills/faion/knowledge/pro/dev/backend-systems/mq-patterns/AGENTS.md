---
slug: mq-patterns
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a queue-topology contract picking among work-queue / fan-out / request-reply / DLQ with idempotency + monitoring spec.
content_id: "75f1e47d15cb309e"
complexity: medium
produces: spec
est_tokens: 4400
tags: [message-queues, async, distributed-systems, event-driven, patterns]
---
# Message Queue Patterns

## Summary

**One-sentence:** Produces a queue-topology contract picking among work-queue / fan-out / request-reply / DLQ with idempotency + monitoring spec.

**One-paragraph:** Message queues enable asynchronous communication between services, providing decoupling, load leveling, and reliability. Four foundational topologies cover the vast majority of use cases: point-to-point work queue, publish/subscribe fan-out, request/reply, and dead-letter queue for failed messages. Output is a topology-contract YAML naming queue/exchange names, schema, partition key, retry policy, DLQ target, idempotency strategy, and monitoring spec.

**Ефективно для:**

- Service-to-service decoupling so failures isolate (orders ↛ email).
- Async background jobs (image resize, ETL, ML inference).
- Event-driven architectures with multiple independent consumers.
- Load leveling for spiky traffic the downstream cannot absorb synchronously.

## Applies If (ALL must hold)

- Decoupling services in distributed systems so failures isolate — the order service should not block when the email service is down.
- Async background jobs (image resize, ETL, ML inference) where users should not wait on the response path.
- Load leveling — absorb traffic spikes that the downstream cannot handle synchronously.
- Event-driven architectures with multiple consumers (audit, analytics, search index) per published event.
- Reliable hand-off across process or network boundaries with at-least-once or exactly-once delivery semantics.

## Skip If (ANY kills it)

- Request/response with low latency requirement under 50 ms end-to-end — synchronous gRPC or HTTP wins.
- Strong-consistency transactional flows that span multiple services — use SAGA or 2PC instead.
- Adding queues just to scale without measuring backpressure or queue depth — operational burden with no benefit.
- Pure fan-out logging — use a log shipper instead.
- Tiny apps that fit on one box — a goroutine with a channel or queue.Queue is simpler.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service interaction list | yaml / md | team — what calls what async |
| Throughput + latency budget | SLO doc | ops |
| Schema registry | Avro / Protobuf / JSON Schema | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

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
| `pick-topology` | sonnet | Topology decision needs judgement on consumer relationship. |
| `draft-contract` | sonnet | Contract writing benefits from sonnet. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/topology-contract.yaml` | Queue topology contract skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mq-patterns.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[mq-broker-implementations]]
- [[mq-idempotent-consumers]]
- [[mq-reliability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
