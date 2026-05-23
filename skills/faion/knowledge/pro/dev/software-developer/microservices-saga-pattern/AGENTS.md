---
slug: microservices-saga-pattern
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Manage distributed transactions across microservices as a sequence of local transactions plus paired compensation steps, with either choreography (events) or orchestration (central coordinator) coordination.
content_id: "2c42e961755e4005"
complexity: deep
produces: spec
est_tokens: 5200
tags: [microservices, saga, distributed-transactions, compensation, eventual-consistency]
---
# Saga Pattern for Distributed Transactions

## Summary

**One-sentence:** Manage distributed transactions across microservices as a sequence of local transactions plus paired compensation steps, with either choreography (events) or orchestration (central coordinator) coordination.

**One-paragraph:** The saga pattern decomposes a distributed transaction into a sequence of local transactions, each publishing an event/message triggering the next step. On failure, compensation transactions undo previously completed steps in reverse order. Every step requires a paired compensation path — partial compensation is a data-integrity incident. Two flavors: choreography (each service reacts to events; no central coordinator) and orchestration (one orchestrator service drives the sequence). Choose based on coupling, observability, and team size.

**Ефективно для:**

- Cross-service business transactions, де 2PC неможливе (полісервіс, polyglot persistence).
- Refactor sync-cascade де failure mid-flow залишає inconsistent state.
- Order/payment/inventory flows з компенсаціями (release stock, refund, cancel shipment).
- Polyglot persistence: SQL + NoSQL + external API в одній бізнес-операції.

## Applies If (ALL must hold)

- Business operation spans ≥2 services, each owning its own database.
- Each step has a meaningful compensation (logical undo).
- Eventual consistency is acceptable (seconds to minutes window).
- Existing event broker (Kafka / RabbitMQ) OR orchestrator framework (Temporal / Camunda) available.

## Skip If (ANY kills it)

- All steps live in one DB — use a local transaction.
- Step has no compensation (e.g. send irreversible email) AND happy-path failure is unacceptable.
- Strong consistency required (banking core ledger) — use a single-DB transaction or 2PC instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Saga step list | ordered (service, action, compensation) triples | domain modeling |
| Event broker | Kafka / RabbitMQ / SNS | platform |
| Orchestrator (if used) | Temporal / Camunda / Step Functions | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[microservices-inter-service-comm]] | Pick async messaging style before saga design. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: compensation-required-every-step, idempotent-steps-and-comps, outbox-not-dual-write, compensation-order-reverse, orchestrator-or-choreography-chosen | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-steps-and-comps` | opus | Domain modeling + compensation design is high-judgment. |
| `wire-outbox` | sonnet | Templated outbox + CDC setup. |
| `lint-dual-write` | haiku | Mechanical grep for db.save followed by broker.publish. |

## Templates

| File | Purpose |
|------|---------|
| `templates/saga-definition.md` | Saga spec template (steps + compensations + coordination + outbox) |
| `templates/OrderSagaWorkflow.java` | Temporal workflow skeleton with reverse-order compensations |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-microservices-saga-pattern.py` | Validate the saga definition artefact against the schema | Pre-commit + CI |

## Related

- [[microservices-inter-service-comm]]
- [[microservices-circuit-breaker]]
- [[event-sourcing-fundamentals]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
