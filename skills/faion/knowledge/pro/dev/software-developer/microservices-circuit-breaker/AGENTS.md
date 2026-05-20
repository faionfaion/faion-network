---
slug: microservices-circuit-breaker
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The circuit breaker wraps outbound calls to a dependency in a three-state machine: CLOSED (normal), OPEN (dependency down — fast-fail without calling it), and HALF_OPEN (recovery probe).
content_id: "11db43f7542211a3"
tags: [microservices, circuit-breaker, resilience, fault-tolerance, distributed-systems]
---
# Circuit Breaker Pattern for Microservice Resilience

## Summary

**One-sentence:** The circuit breaker wraps outbound calls to a dependency in a three-state machine: CLOSED (normal), OPEN (dependency down — fast-fail without calling it), and HALF_OPEN (recovery probe).

**One-paragraph:** The circuit breaker wraps outbound calls to a dependency in a three-state machine: CLOSED (normal), OPEN (dependency down — fast-fail without calling it), and HALF_OPEN (recovery probe). It prevents cascading failures across services when a downstream dependency degrades or fails.

## Applies If (ALL must hold)

- Any outbound HTTP or gRPC call to another service in a microservices cluster.
- Calls to external third-party APIs where availability SLOs are not guaranteed.
- Message consumers that call downstream services to process each event.
- Any call where the acceptable failure rate exceeds zero under load.

## Skip If (ANY kills it)

- Calls that must never fast-fail (idempotent writes to the primary DB of the same service) — use retries with backoff instead.
- In-process calls to the same service's domain layer — no network hop, no circuit needed.
- Calls where all failures must be surfaced immediately to the caller with no fast-fail window.

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

- parent skill: `pro/dev/software-developer/`
