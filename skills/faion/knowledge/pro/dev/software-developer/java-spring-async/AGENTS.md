# Spring Async

## Summary

Spring's `@Async` + `ThreadPoolTaskExecutor` pattern for running methods on a managed thread pool without blocking the HTTP thread. Annotate a method `@Async("executorName")`, enable with `@EnableAsync`, define a `ThreadPoolTaskExecutor` bean, and return `CompletableFuture<T>` so callers can observe errors. The async method must live in a different bean than the caller to avoid proxy self-invocation bypass.

## Why

Offloading fire-and-forget work (email, SMS, audit logging, webhook delivery) to a named pool removes it from the request thread, reducing p99 latency. Named executors with bounded queues and `CallerRunsPolicy` provide backpressure without dropping tasks. Unlike raw `ExecutorService`, Spring-managed pools participate in DI, observability (Micrometer metrics), graceful shutdown, and context propagation (MDC, SecurityContext, OTel span) via `TaskDecorator`.

## When To Use

- Background tasks that must not block HTTP threads: email/SMS, CRM sync, report generation, image transcoding.
- Fan-out: controller fires multiple downstream calls, aggregates via `CompletableFuture.allOf`.
- Event-driven side effects using `ApplicationEventPublisher` + `@Async @EventListener`.
- Migrating raw `ExecutorService` boilerplate to Spring-managed pools with proper shutdown and metrics.
- Fire-and-forget audit logging or metrics that must not impact request latency.

## When NOT To Use

- Cross-process work needing durability, retries, or idempotency — use SQS / RabbitMQ / Kafka instead; `@Async` does not survive a JVM restart.
- High-throughput streaming — use Project Reactor / WebFlux end-to-end; mixing `@Async` with reactive code wastes threads.
- Latency-sensitive paths where work MUST complete before response — use synchronous code.
- Spring Boot 3.2+ apps with virtual threads enabled — `@Async` adds no value and may interfere with Loom schedulers.
- Exactly-once semantics, durable state, or saga workflows — use Temporal or a queue broker.

## Content

| File | What's inside |
|------|---------------|
| `content/01-async-config.xml` | ThreadPoolTaskExecutor setup, TaskDecorator for MDC/Security/OTel, graceful shutdown rules |
| `content/02-async-service.xml` | @Async method rules, CompletableFuture error handling, self-invocation antipattern |
| `content/03-antipatterns.xml` | Self-invocation, missing executor name, void without handler, tx/async mix, Thread.sleep in tests |

## Templates

| File | Purpose |
|------|---------|
| `templates/async-config.java` | ThreadPoolTaskExecutor bean with CallerRunsPolicy, TaskDecorator, shutdown wait |
| `templates/async-service.java` | @Async service with CompletableFuture, error handling, fan-out pattern |
| `templates/spring-async-audit.sh` | Shell auditor: self-invocation, missing executor, void without handler, tx+async, sleep-in-tests |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/spring-async-audit.sh` | Flag common @Async anti-patterns across a project src tree |
