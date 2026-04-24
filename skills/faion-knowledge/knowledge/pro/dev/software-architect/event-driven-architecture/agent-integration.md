# Agent Integration — Event-Driven Architecture

## When to use
- Cross-team / cross-bounded-context integration where synchronous coupling is the documented pain (lockstep deploys, cascading outages).
- Event-replay capability is a real requirement: bootstrap new services, recover lost projections, do post-hoc analytics on past behavior.
- Asymmetric scaling: the producer's rate is variable and the consumer needs to absorb spikes without falling over.
- Long-running business processes that span hours/days/weeks (sagas, workflows, approvals).
- Streaming analytics, fraud detection, IoT, multi-step ML pipelines.
- Need natural fan-out: one event → many independent consumers (notifications, search index, audit, billing, ML feature store).

## When NOT to use
- Single-team monolith — sync calls + a function are fine; events add operational tax for no organizational gain.
- Strict request/response with low latency budget (<50ms end-to-end) — broker hop + serialization eats the budget.
- The team has never operated a broker — Kafka / RabbitMQ / SQS are real infrastructure with real on-call.
- Cross-aggregate ACID requirements — eventual consistency is the EDA default; if the domain forbids it, sagas + outbox + idempotent handlers are a lot of work for a maybe.
- Audit / compliance requires synchronous immediate confirmation of side effects (some payments, some healthcare flows).
- Schema is volatile and there is no schema registry / contract pipeline — event consumers will break silently.

## Where it fails / limitations
- **Eventual consistency surprises.** "Confirmed" UIs that read from a projection that hasn't caught up. Either show pending state or read-your-writes via the write side.
- **At-least-once delivery.** Brokers redeliver; consumers must dedupe. Agents (and humans) routinely forget the idempotency key.
- **Event versioning rot.** Once an event is in the log, it lives forever. Removing fields breaks consumers. Adding required fields on existing events is forbidden — only optional, additive changes.
- **Saga complexity.** Choreography becomes spaghetti past 3-4 services. Orchestration centralizes control but you now operate a workflow engine.
- **Debug paths get long.** A failed end-to-end flow now spans 5 spans, 3 brokers, 2 retries; without correlation IDs and distributed tracing you're blind.
- **Schema registry not optional.** Without enforced schemas, "events as a contract" becomes "events as JSON-shaped guesses."
- **DLQ rot.** Dead-letter queues fill up and nobody looks. Without alerting + tooling to triage and replay, the DLQ is the place where money goes to die.
- **Broker becomes a coupling.** "We chose Kafka" leaks API shapes (partitions, headers, retention) into application code. Use a thin abstraction.

## Agentic workflow
Drive EDA design as a four-pass pipeline: (1) an event-discovery agent runs Event Storming on the spec and produces an event catalog with producer, consumers, schema, retention; (2) a contract agent generates AsyncAPI / Avro / JSON Schema artifacts and registers them in the schema registry; (3) a scaffolding agent produces producer + consumer skeletons (Kafka / RabbitMQ / NATS) with idempotency keys, retry policies, DLQ routing, and OpenTelemetry spans baked in; (4) a topology auditor verifies that every consumer is idempotent, every event has a schema, every saga has compensations, and every cross-service call is async unless explicitly justified. The auditor is the load-bearing pass — agents over-generate sync HTTP calls if not corrected.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — implement event-driven features as SDD tasks; quality gate: every consumer PR includes idempotency key, retry config, DLQ binding, and an integration test.
- A purpose-built **event-storming agent** (worth creating): outputs `events.md` with `Event | Producer | Consumers | Trigger | Payload | Retention | DLQ policy`.
- A purpose-built **schema-evolution checker**: on PRs to `events-contracts/`, run `buf breaking` (proto) or `oasdiff` (AsyncAPI/JSON Schema); fail on non-additive changes.
- A purpose-built **saga compensator generator**: given an orchestrator definition, scaffold compensation handlers for every step; refuse to merge if any step lacks a compensation.
- `password-scrubber-agent` — events frequently carry PII; scrub before sharing fixtures or piping into 3rd-party SaaS.

### Prompt pattern
Discovery:
```
Run Event Storming on <spec>. Output a markdown event catalog
with columns Event | Producer | Consumers | Trigger | Schema fields
| Retention (days) | Ordering required (yes/no) | Idempotency key.
Reject CRUD-shaped names (UserUpdated, OrderModified). Past tense,
business outcome. Minimum 5 events.
```

Saga generation:
```
Given the multi-step process in <spec>, design as orchestration-based
saga using Temporal. Emit:
1) workflow.py with each step as activity
2) compensations.py with one compensation per step
3) failure_modes.md listing what happens if step N fails after step N-1
   has succeeded. Refuse to emit a workflow without compensations.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `kafkactl` / `rpk` / `kcat` | Inspect topics, partitions, consumer lag, replay messages | https://github.com/deviceinsight/kafkactl ; https://docs.redpanda.com ; https://github.com/edenhill/kcat |
| `buf` | Schema linting + breaking-change detection (proto / Connect-RPC) | https://buf.build |
| `apicurio-cli` / Confluent Schema Registry CLI | Manage Avro / JSON / Protobuf schemas | https://www.apicur.io/registry/ ; https://docs.confluent.io/platform/current/schema-registry/ |
| `asyncapi` (CLI) | Validate AsyncAPI specs and generate code/docs | https://www.asyncapi.com/tools/cli |
| `temporal` (CLI) | Inspect workflows, terminate, signal, replay | https://docs.temporal.io/cli |
| `nats` CLI | NATS JetStream stream/consumer management | https://github.com/nats-io/natscli |
| `aws sqs` / `aws sns` | DLQ inspection + redrive on AWS | https://docs.aws.amazon.com/cli/ |
| `kubectl logs` + `tempo` / `jaeger query` | Trace events across services | https://grafana.com/docs/tempo/ ; https://www.jaegertracing.io |
| `claude` (Anthropic CLI) | Run discovery / contract / scaffolding passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Apache Kafka (self-host) | OSS | yes | High throughput, replay, long retention. The default for serious EDA. |
| Confluent Cloud | SaaS | yes | Managed Kafka + Schema Registry + ksqlDB. |
| Redpanda | OSS + SaaS | yes | Kafka API, single binary, lower ops cost. |
| AWS MSK / EventBridge / SNS+SQS | SaaS | yes | EventBridge for routing, SNS+SQS for fan-out, MSK for Kafka. |
| RabbitMQ | OSS + SaaS (CloudAMQP) | yes | Complex routing, lower throughput than Kafka. |
| NATS / JetStream | OSS + SaaS (Synadia) | yes | Lightweight, ultra-low latency, simple replay via JetStream. |
| Apache Pulsar | OSS + SaaS (StreamNative) | yes | Multi-tenancy, geo-replication, queueing + streaming. |
| GCP Pub/Sub / Azure Service Bus / Event Grid | SaaS | yes | Cloud-native pub/sub; cheap at low scale. |
| Temporal.io | OSS + SaaS | yes | Durable orchestration; replaces brittle saga code. |
| Camunda 8 / Zeebe | OSS + SaaS | yes | BPMN orchestration with broker-backed durability. |
| Apicurio / Confluent Schema Registry / Buf BSR | OSS / SaaS | yes | Schema-first contracts. Non-negotiable for EDA at scale. |
| Debezium | OSS | yes | CDC from databases → Kafka outbox; the canonical outbox pattern. |
| AsyncAPI Studio | SaaS | yes | Design-first AsyncAPI editing + mocking. |

## Templates & scripts
The README ships pub/sub, event-sourcing, CQRS, saga, broker comparison, and reference patterns. The high-leverage missing piece is an **idempotent consumer template** that agents can drop in. Inline drop-in (≤50 lines):

```python
#!/usr/bin/env python3
# idempotent_consumer.py — template for at-least-once safe consumers.
# Backing store: Postgres processed_events table with PK on (event_id, consumer).
import asyncio, json, logging, hashlib
from contextlib import asynccontextmanager

log = logging.getLogger("consumer")

class IdempotentConsumer:
    def __init__(self, db, consumer_name: str, handler):
        self.db = db
        self.consumer = consumer_name
        self.handler = handler

    async def process(self, raw: bytes, headers: dict) -> bool:
        evt = json.loads(raw)
        eid = evt.get("event_id") or hashlib.sha256(raw).hexdigest()
        async with self.db.transaction() as tx:
            inserted = await tx.execute(
                "INSERT INTO processed_events(event_id, consumer) "
                "VALUES($1,$2) ON CONFLICT DO NOTHING RETURNING event_id",
                eid, self.consumer,
            )
            if not inserted:
                log.info("dedup skip event_id=%s", eid)
                return True  # ack: already handled
            try:
                await self.handler(evt, headers, tx)
            except RetryableError:
                raise  # let broker redeliver, dedup row rolls back
            except PoisonError as e:
                log.error("poison event_id=%s: %s", eid, e)
                await self._dlq(evt, headers, str(e))
                return True  # ack: poison goes to DLQ, do not redeliver
        return True

    async def _dlq(self, evt, headers, reason):
        # publish to DLQ topic (broker-specific; omitted)
        pass
```

Pair with: a `processed_events` table (TTL old rows), structured logs that include `event_id`/`correlation_id`, and an alert on DLQ depth.

## Best practices
- **Schemas in a registry, not in code.** Avro / Protobuf / JSON Schema, versioned, breaking-change CI gate.
- **Past-tense, business-meaningful event names.** `OrderPlaced`, not `OrderUpdated`. Matches event-sourcing discipline.
- **Idempotency keys on every consumer.** Either dedupe table or upsert key — non-optional under at-least-once delivery.
- **Outbox pattern for reliable publishing.** Write event row + business row in one DB transaction; separate worker drains to broker. Debezium for free.
- **Compensations or it didn't happen.** Every saga step has a compensating action — written before the happy path is merged.
- **Distributed tracing on day one.** OpenTelemetry, W3C Trace Context propagated through headers across producers and consumers.
- **DLQ with a triage workflow.** Auto-alert on DLQ depth > 0; have a `redrive` CLI; monthly review.
- **Backpressure-aware producers.** Don't drop in production code that calls `publish` in a tight loop with no retry/queue policy.
- **Contract tests both sides.** Pact (or AsyncAPI-driven mocks) on consumer side; producer regression tests against schema.
- **Explicit ordering vs. partition key.** If you need ordering per entity, partition by entity ID; document it.
- **Replay isn't free.** Every consumer must work correctly when re-reading history; plan for it.
- **Keep events small.** Reference IDs, not embedded objects. Big events bloat brokers and make schema evolution worse.

## AI-agent gotchas
- **Sync HTTP smuggled in.** Agents add an `httpx.AsyncClient.get(other_service)` inside an event handler "to enrich the event." That's a sync chain in EDA clothing. Reject in topology audit.
- **Missing idempotency key.** Generated handlers happily process the same `event_id` twice. Hard rule: handlers refuse events without `event_id` and use the dedup table.
- **`type(event).__name__` as the schema.** Agents skip the schema registry; rename a class, break consumers. Force `event_type=Avro/Proto/JSON-Schema` lookup.
- **Saga without compensations.** Agents emit a Temporal workflow with happy path only. Refuse to merge until each activity has a compensating activity referenced from the workflow.
- **DLQ as a black hole.** Agents wire DLQ but no alerting, no redrive CLI, no dashboards. Require a `dlq_depth` Prometheus metric and an alert rule.
- **Broker-specific code in domain.** Agents import `aio_pika` / `aiokafka` / `boto3` from `domain/` or `application/`. Banned imports list catches it.
- **Hallucinated AsyncAPI fields.** Agents invent `x-` extensions or use 2.x fields under 3.x. Validate with `asyncapi validate` in CI.
- **Schema evolution amnesia.** Agents add required fields to existing events. Wire `buf breaking` / `oasdiff` to fail PRs with non-additive changes.
- **Retry storms.** Generated retry config defaults to immediate-retry-forever; producers DDoS themselves on transient outages. Force exponential backoff + jitter + max attempts.
- **Choreography sprawl.** Agents propose 8-service choreography for what is clearly an orchestration problem. Force a saga-style review when ≥4 services participate.
- **No human checkpoint on schema deletes.** Removing an event class or field is destructive, autonomous-agent gate; require human approval and 30-day deprecation window.
- **CRUD events.** `UserUpdated`, `OrderUpdated` proliferate. Past-tense + business-outcome rule, enforced at PR review.

## References
- Hohpe, G., Woolf, B. — "Enterprise Integration Patterns." Addison-Wesley, 2003.
- Stopford, B. — "Designing Event-Driven Systems." O'Reilly, 2018. (Free from Confluent.)
- Kleppmann, M. — "Designing Data-Intensive Applications." O'Reilly, 2017 (Ch. 11).
- AsyncAPI v3 spec. https://www.asyncapi.com/docs/reference/specification/v3.0.0
- Confluent — "Apache Kafka Patterns." https://docs.confluent.io
- Debezium outbox pattern. https://debezium.io/blog/2019/02/19/reliable-microservices-data-exchange-with-the-outbox-pattern/
- Temporal docs — sagas and orchestration. https://docs.temporal.io
- Microsoft Azure Architecture — "Event-driven architecture style." https://learn.microsoft.com/azure/architecture/guide/architecture-styles/event-driven
- Sibling: `pro/dev/code-quality/event-sourcing-basics` and `event-sourcing-implementation` (this batch).
- Sibling: `pro/dev/software-architect/distributed-patterns/`.
- Sibling: `pro/dev/software-architect/microservices-architecture/`.
