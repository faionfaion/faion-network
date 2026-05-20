---
slug: event-driven-architecture
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Event-Driven Architecture (EDA) structures inter-service communication as asynchronous events flowing through a broker (Kafka, RabbitMQ, SQS) rather than synchronous HTTP calls.
content_id: "2b7648484f74ed20"
tags: [event-driven-architecture, async-messaging, kafka, distributed-systems, saga-pattern]
---
# Event-Driven Architecture

## Summary

**One-sentence:** Event-Driven Architecture (EDA) structures inter-service communication as asynchronous events flowing through a broker (Kafka, RabbitMQ, SQS) rather than synchronous HTTP calls.

**One-paragraph:** Event-Driven Architecture (EDA) structures inter-service communication as asynchronous events flowing through a broker (Kafka, RabbitMQ, SQS) rather than synchronous HTTP calls. The concrete rules: every consumer must be idempotent (dedup by event_id); every event name is past-tense describing a business outcome (OrderPlaced, not OrderUpdated); every saga step has a compensating action written before the happy path is merged.

## Applies If (ALL must hold)

- Cross-team / cross-bounded-context integration where synchronous coupling causes lockstep deploys or cascading outages
- Event-replay capability is a real requirement (new service bootstrap, projection recovery, post-hoc analytics)
- Asymmetric scaling: producer rate is variable, consumer must absorb spikes without falling over
- Long-running business processes spanning hours/days/weeks (sagas, approvals, workflows)
- Natural fan-out: one event drives notifications, search index, audit, billing, ML feature store independently

## Skip If (ANY kills it)

- Single-team monolith — sync calls are fine; events add operational tax (broker, schemas, DLQs) for no organizational gain
- Strict latency budget below ~50ms end-to-end — broker hop + serialization eats the budget
- Team has never operated a broker — Kafka / RabbitMQ / SQS require real on-call experience
- Cross-aggregate ACID requirements — sagas + outbox + idempotent handlers are a lot of work for eventual consistency
- Schema is volatile with no schema registry — event consumers will break silently on field renames

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/dev/software-architect/`
