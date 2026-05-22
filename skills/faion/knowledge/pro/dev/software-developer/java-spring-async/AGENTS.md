---
slug: java-spring-async
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Spring's @Async + ThreadPoolTaskExecutor pattern for running methods on a managed thread pool without blocking the HTTP thread.
content_id: "0570b97e2c843ec8"
tags: [spring-boot, async, threading, concurrent, java]
---
# Spring Async

## Summary

**One-sentence:** Spring's @Async + ThreadPoolTaskExecutor pattern for running methods on a managed thread pool without blocking the HTTP thread.

**One-paragraph:** Spring's @Async + ThreadPoolTaskExecutor pattern for running methods on a managed thread pool without blocking the HTTP thread. Annotate a method @Async("executorName"), enable with @EnableAsync, define a ThreadPoolTaskExecutor bean, and return CompletableFuture<T> so callers can observe errors. The async method must live in a different bean than the caller to avoid proxy self-invocation bypass.

## Applies If (ALL must hold)

- Background tasks that must not block HTTP threads: email/SMS, CRM sync, report generation, image transcoding.
- Fan-out: controller fires multiple downstream calls, aggregates via CompletableFuture.allOf.
- Event-driven side effects using ApplicationEventPublisher + @Async @EventListener.
- Migrating raw ExecutorService boilerplate to Spring-managed pools with proper shutdown and metrics.
- Fire-and-forget audit logging or metrics that must not impact request latency.

## Skip If (ANY kills it)

- Cross-process work needing durability, retries, or idempotency — use SQS / RabbitMQ / Kafka instead; @Async does not survive a JVM restart.
- High-throughput streaming — use Project Reactor / WebFlux end-to-end; mixing @Async with reactive code wastes threads.
- Latency-sensitive paths where work MUST complete before response — use synchronous code.
- Spring Boot 3.2+ apps with virtual threads enabled — @Async adds no value and may interfere with Loom schedulers.
- Exactly-once semantics, durable state, or saga workflows — use Temporal or a queue broker.

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
