# Spring Async

## Summary

Spring's `@Async` annotation offloads IO-bound work (email, SMS, webhooks, slow third-party calls) from request threads onto a named `ThreadPoolTaskExecutor`. Return `CompletableFuture<T>` from every async method for composability and observable exceptions. Always name the executor explicitly (`@Async("emailExecutor")`) — the default changes between Boot versions.

## Why

Request threads are a scarce resource; blocking them on slow IO degrades throughput and increases p99 latency. `@Async` delegates to a tuned thread pool without the operational overhead of a full message broker. Named executors allow independent pool sizing (email vs general task), backpressure via `CallerRunsPolicy`, and Micrometer metrics per pool. `CompletableFuture` composition replaces nested callbacks and makes exception propagation explicit.

## When To Use

- Offloading IO-bound work (email, SMS, webhooks, audit logs) from request threads in an existing Spring Boot service.
- Fan-out parallel sub-tasks per request via `CompletableFuture.allOf` when work is short-lived and confined to one JVM.
- Fire-and-forget events that do not need cross-process durability.

## When NOT To Use

- Work must survive a JVM crash — use Spring Batch, Kafka, or RabbitMQ instead.
- Cross-service or cross-host coordination — use a real broker, not an in-memory `ThreadPoolTaskExecutor`.
- CPU-bound parallelism on large datasets — use `ForkJoinPool` or Project Reactor; `@Async` is sized for IO.
- Methods already inside `@Transactional` — `@Async` opens a new thread; the outer transaction does not propagate.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Executor naming, pool sizing formula, MDC/SecurityContext propagation, graceful shutdown. |
| `content/02-examples.xml` | `AsyncConfig` with two named executors, `@Async` service method returning `CompletableFuture`. |
| `content/03-antipatterns.xml` | Self-invocation no-op, default executor hazard, `void` exception swallowing, virtual-thread upgrade trap. |

## Templates

| File | Purpose |
|------|---------|
| `templates/AsyncConfig.java` | `ThreadPoolTaskExecutor` config with `CallerRunsPolicy`, graceful shutdown, `TaskDecorator` hook. |
| `templates/async-service.java` | `@Async` method skeleton returning `CompletableFuture<Void>` with error handling. |
