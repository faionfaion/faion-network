---
slug: microservices-inter-service-comm
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Choose the communication style (REST / gRPC / async messaging) for each inter-service call based on coupling, latency, and durability requirements.
content_id: "991f7d60c6ae2852"
complexity: medium
produces: decision-record
est_tokens: 5200
tags: [microservices, communication, sync, async, rest, grpc, messaging]
---
# Microservices Inter-Service Communication

## Summary

**One-sentence:** Choose the communication style (REST / gRPC / async messaging) for each inter-service call based on coupling, latency, and durability requirements.

**One-paragraph:** Inter-service communication style is a per-call decision, not a service-wide one. Sync REST or gRPC fits low-latency request/response between services with tight coupling; async messaging (Kafka / RabbitMQ / SQS) fits high-throughput, decoupled, eventual-consistency flows. The choice drives error handling, retry semantics, schema evolution, and observability. Mixing styles inside one call chain (e.g. sync REST in front of async queue) creates failure modes that are hard to reason about.

**Ефективно для:**

- Greenfield service-to-service interface design: REST/gRPC/async-message decision.
- Refactor of fan-out cascades, де один синхронний ланцюг блокує весь request.
- Schema-evolution rules: protobuf для gRPC, OpenAPI для REST, Avro/JSON Schema для messages.
- Observability matrix: яка комбінація tracing/logs/metrics потрібна на кожному стилі.

## Applies If (ALL must hold)

- More than 2 services need to exchange data.
- Team owns the call definition (not bound by an external API).
- Latency / durability / throughput requirements known per call.
- Schema registry available (protobuf registry, OpenAPI spec store).

## Skip If (ANY kills it)

- Monolith — no inter-service surface.
- Single owner controls both sides AND call is sub-millisecond critical — in-process call may be better.
- Cross-org integration where the contract is dictated (use vendor's style).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service inventory | list of services + owners | service catalog |
| Call SLA | latency / durability / throughput targets | SRE / product |
| Schema registry | protobuf / OpenAPI / Avro repo | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[microservices-service-boundaries]] | Boundary definition precedes communication choice. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: sync-only-if-can-wait, grpc-when-internal-typed, async-for-event-fanout, schema-registry-required, idempotency-key-on-writes | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision-record + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `list-call-attributes` | sonnet | Extract from service docs + SLAs. |
| `decide-style` | opus | Tradeoffs across coupling, durability, throughput are high-judgment. |
| `lint-inline-schemas` | haiku | Mechanical grep for inline schemas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/comm-decision-record.md` | ADR template for one inter-service communication decision |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-microservices-inter-service-comm.py` | Validate the call decision artefact against the schema | Pre-commit + CI |

## Related

- [[microservices-circuit-breaker]]
- [[microservices-saga-pattern]]
- [[microservices-service-boundaries]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
