# Event-Driven Architecture

## Summary

Event-Driven Architecture (EDA) structures inter-service communication as asynchronous events flowing through a broker (Kafka, RabbitMQ, SQS) rather than synchronous HTTP calls. The concrete rules: every consumer must be idempotent (dedup by event_id); every event name is past-tense describing a business outcome (OrderPlaced, not OrderUpdated); every saga step has a compensating action written before the happy path is merged.

## Why

Synchronous point-to-point calls create a distributed monolith: every service must be up for any request to succeed, and latency stacks multiplicatively. EDA breaks this by making producers unaware of consumers, allowing consumers to scale and fail independently, and enabling event replay to bootstrap new services or recover lost projections. Fan-out (one event → N independent consumers) is free.

## When To Use

- Cross-team / cross-bounded-context integration where synchronous coupling causes lockstep deploys or cascading outages
- Event-replay capability is a real requirement (new service bootstrap, projection recovery, post-hoc analytics)
- Asymmetric scaling: producer rate is variable, consumer must absorb spikes without falling over
- Long-running business processes spanning hours/days/weeks (sagas, approvals, workflows)
- Natural fan-out: one event drives notifications, search index, audit, billing, ML feature store independently

## When NOT To Use

- Single-team monolith — sync calls are fine; events add operational tax (broker, schemas, DLQs) for no organizational gain
- Strict latency budget below ~50ms end-to-end — broker hop + serialization eats the budget
- Team has never operated a broker — Kafka / RabbitMQ / SQS require real on-call experience
- Cross-aggregate ACID requirements — sagas + outbox + idempotent handlers are a lot of work for eventual consistency
- Schema is volatile with no schema registry — event consumers will break silently on field renames

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-patterns.xml` | Pub/Sub, Event Sourcing, CQRS, Saga (choreography + orchestration) — rules and trade-offs |
| `content/02-broker-comparison.xml` | Kafka, Pulsar, RabbitMQ, AWS SQS/SNS — throughput, latency, use-when |
| `content/03-event-schema.xml` | CloudEvents standard, naming conventions, versioning strategies, schema evolution rules |
| `content/04-delivery-guarantees.xml` | At-most/at-least/exactly-once, idempotency techniques, dedup table pattern |
| `content/05-antipatterns.xml` | Event as command, oversized events, missing correlation ID, CRUD event names |

## Templates

| File | Purpose |
|------|---------|
| `templates/idempotent-consumer.py` | At-least-once safe consumer with dedup table, DLQ routing, RetryableError handling |
| `templates/cloudevent.json` | CloudEvents v1.0 example with required + optional attributes |
| `templates/eda-prompt.txt` | LLM prompt pattern for event storming and saga generation |
