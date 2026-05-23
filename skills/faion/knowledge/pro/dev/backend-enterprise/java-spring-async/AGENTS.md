---
slug: java-spring-async
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Spring @Async methodology — named ThreadPoolTaskExecutors, CallerRunsPolicy backpressure, CompletableFuture return types, TaskDecorator MDC propagation, graceful shutdown.
content_id: "b7003a9e0a960e7a"
complexity: deep
produces: code
est_tokens: 4300
tags: [async, threading, spring-boot, concurrency, executor]
---
# Spring Async

## Summary

**One-sentence:** Spring @Async methodology — named ThreadPoolTaskExecutors, CallerRunsPolicy backpressure, CompletableFuture return types, TaskDecorator MDC propagation, graceful shutdown.

**One-paragraph:** Spring `@Async` offloads IO-bound work (email, SMS, webhooks, audit logs) from request threads to named `ThreadPoolTaskExecutor`s. Each pool has its own SLA (e.g. `emailExecutor`, `taskExecutor`); `@Async("emailExecutor")` is mandatory — plain `@Async` silently picks up whatever default the Boot version ships. Pools use `CallerRunsPolicy` for backpressure and `setWaitForTasksToCompleteOnShutdown(true)` + `setAwaitTerminationSeconds(30)` for graceful shutdown. Methods return `CompletableFuture<T>`, never `void`. A `TaskDecorator` propagates MDC + `SecurityContext` + tracing baggage. Self-invocation of `@Async` on `this` is forbidden — it bypasses the AOP proxy.

**Ефективно для:**

- Offloading IO-bound work (email, SMS, webhooks, audit logs) from request threads in an existing Spring Boot service.
- Fan-out parallel sub-tasks per request via `CompletableFuture.allOf` when work is short-lived and confined to one JVM.
- Fire-and-forget events that do not need cross-process durability.

## Applies If (ALL must hold)

- Spring Boot 3 service running on the blocking (Web MVC) stack.
- IO-bound work (network call, email, audit log) that should not block the request thread.
- Workload fits inside a single JVM with predictable load.

## Skip If (ANY kills it)

- Work must survive a JVM crash — use Spring Batch, Kafka, or RabbitMQ instead.
- Cross-service or cross-host coordination — use a real broker, not an in-memory `ThreadPoolTaskExecutor`.
- CPU-bound parallelism on large datasets — use `ForkJoinPool` or Project Reactor; `@Async` is sized for IO.
- Methods already inside `@Transactional` — `@Async` opens a new thread; the outer transaction does not propagate.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Workload SLA | text (latency, durability) | platform / SRE |
| Pool sizing inputs (cores, wait ratio) | numeric | perf profiling |
| MDC / tracing keys to propagate | list | observability team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Umbrella for service layering. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: named-executor, caller-runs-backpressure, completablefuture-return, taskdecorator-context, graceful-shutdown, no-self-invocation | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the async-config manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: unnamed-async, void-async-loses-exception, self-invocation-bypass, mdc-loss, async-inside-transactional | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: define pool → name executor → decorate context → wire CompletableFuture → backpressure + shutdown | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `configure-thread-pool` | sonnet | Pool sizing + decorator wiring needs judgment. |
| `wrap-method-with-async` | sonnet | CompletableFuture return shape design. |
| `audit-self-invocation` | haiku | Mechanical scan for `this.asyncMethod()` calls. |

## Templates

| File | Purpose |
|------|---------|
| `templates/AsyncConfig.java` | `ThreadPoolTaskExecutor` configuration with CallerRunsPolicy + graceful shutdown + TaskDecorator. |
| `templates/async-service.java` | Service method returning `CompletableFuture<T>` with `@Async("emailExecutor")`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring-async.py` | Validate the async-config manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[java-spring-boot]]
- [[java-spring]]
- [[java-junit-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (durability requirement, in-JVM vs cross-host, CPU vs IO) to a rule from `01-core-rules.xml`. Use it before introducing `@Async` to a service.
