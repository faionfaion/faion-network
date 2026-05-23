---
slug: java-spring-async
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Spring's @Async + ThreadPoolTaskExecutor pattern for running methods on a managed thread pool without blocking the HTTP thread.
content_id: "b7003a9e0a960e7a"
complexity: medium
produces: code
est_tokens: 5200
tags: [spring-boot, async, threading, concurrent, java]
---
# Spring Async

## Summary

**One-sentence:** Spring's @Async + ThreadPoolTaskExecutor pattern for running methods on a managed thread pool without blocking the HTTP thread.

**One-paragraph:** Spring's @Async + ThreadPoolTaskExecutor pattern for running methods on a managed thread pool without blocking the HTTP thread. Annotate the method with @Async("executorName"), enable globally with @EnableAsync, define a ThreadPoolTaskExecutor bean with explicit limits and TaskDecorator (MDC + SecurityContext + OTel span), and return CompletableFuture<T> so callers can observe errors. The async method must live in a different bean than the caller to avoid proxy self-invocation bypass.

**Ефективно для:**

- Fire-and-forget side effects (email, SMS, audit log) поза HTTP-потоком — без втрати p99 latency.
- Fan-out: контролер запускає N downstream-викликів та агрегує через CompletableFuture.allOf.
- @EventListener + @Async для асинхронної обробки ApplicationEventPublisher подій.
- Міграція з raw ExecutorService на Spring-managed pools (DI, metrics, graceful shutdown).
- TaskDecorator-based context propagation (MDC trace-id, SecurityContext, OTel span) у фонові threads.

## Applies If (ALL must hold)

- Background tasks that must not block HTTP threads: email/SMS, CRM sync, report generation, image transcoding.
- Fan-out: controller fires multiple downstream calls, aggregates via CompletableFuture.allOf.
- Event-driven side effects using ApplicationEventPublisher + @Async @EventListener.
- Migrating raw ExecutorService boilerplate to Spring-managed pools with proper shutdown and metrics.
- Fire-and-forget audit logging or metrics that must not impact request latency.

## Skip If (ANY kills it)

- Cross-process work needing durability, retries, or idempotency — use SQS / RabbitMQ / Kafka; @Async does not survive a JVM restart.
- High-throughput streaming — use Project Reactor / WebFlux end-to-end; mixing @Async with reactive code wastes threads.
- Latency-sensitive paths where work MUST complete before response — use synchronous code.
- Spring Boot 3.2+ apps with virtual threads enabled — @Async adds no value and may interfere with Loom schedulers.
- Exactly-once semantics, durable state, or saga workflows — use Temporal or a queue broker.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Async candidate method | Java method signature | developer / audit |
| AsyncConfig presence | @Configuration class with @EnableAsync | codebase scan |
| Executor sizing budget | corePoolSize / maxPoolSize / queueCapacity numbers | load test |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Spring Boot wiring + Actuator metrics baseline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: named-executor-required, no-self-invocation, completable-future-or-handler, no-async-with-tx, task-decorator-propagation, shutdown-drain | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-async-candidate` | sonnet | Pattern matching on method shape + transaction boundary. |
| `configure-async-pool` | opus | Sizing + TaskDecorator choices are decision-heavy. |
| `lint-async-antipatterns` | haiku | Mechanical regex audit (spring-async-audit.sh). |

## Templates

| File | Purpose |
|------|---------|
| `templates/AsyncConfig.java` | @EnableAsync configuration with TaskDecorator + shutdown drain |
| `templates/NotificationService.java` | @Async service returning CompletableFuture with fan-out pattern |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring-async.py` | Validate the async-method artefact JSON against the 02-output-contract schema | CI on each artefact change; pre-commit |
| `scripts/spring-async-audit.sh` | Lint Spring @Async antipatterns (self-invocation, bare @Async, async+tx, missing shutdown drain) | Pre-commit + CI on Spring Boot projects |

## Related

- [[java-spring-boot]]
- [[java-spring-boot-patterns]]
- [[microservices-inter-service-comm]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
