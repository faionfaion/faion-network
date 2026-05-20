---
slug: java-spring-async
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Spring @Async offloads IO-bound work from request threads to ThreadPoolTaskExecutor.
content_id: "0570b97e2c843ec8"
tags: [async, threading, spring-boot, concurrency, executor]
---
# Spring Async

## Summary

**One-sentence:** Spring @Async offloads IO-bound work from request threads to ThreadPoolTaskExecutor.

**One-paragraph:** Spring @Async offloads IO-bound work from request threads to ThreadPoolTaskExecutor. Name executors explicitly.

## Applies If (ALL must hold)

- Offloading IO-bound work (email, SMS, webhooks, audit logs) from request threads in an existing Spring Boot service.
- Fan-out parallel sub-tasks per request via `CompletableFuture.allOf` when work is short-lived and confined to one JVM.
- Fire-and-forget events that do not need cross-process durability.

## Skip If (ANY kills it)

- Work must survive a JVM crash — use Spring Batch, Kafka, or RabbitMQ instead.
- Cross-service or cross-host coordination — use a real broker, not an in-memory `ThreadPoolTaskExecutor`.
- CPU-bound parallelism on large datasets — use `ForkJoinPool` or Project Reactor; `@Async` is sized for IO.
- Methods already inside `@Transactional` — `@Async` opens a new thread; the outer transaction does not propagate.

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

- parent skill: `pro/dev/backend-enterprise/`
