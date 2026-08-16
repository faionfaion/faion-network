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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Umbrella for service layering. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: named-executor, caller-runs-backpressure, completablefuture-return, taskdecorator-context, graceful-shutdown, no-self-invocation | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the async-config manifest (+ uncaught-handler / executor-metrics / transactional-on-method fields) + valid/invalid examples | 1100 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: unnamed-async, void-async-loses-exception, self-invocation-bypass, mdc-loss, async-inside-transactional | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: define pool → decorate context → annotate methods → shutdown + Micrometer metrics + uncaught handler → Awaitility tests and audit | 1000 |
| `content/05-examples.xml` | essential | Worked sync→@Async conversion (latency, metrics, audit) + CompletableFuture.allOf fan-out | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 800 |

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring-async.py` | Validate the async-config manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |
| `scripts/spring-async-audit.sh` | Grep-based audit of a target project for self-invocation, bare `@Async`, `@Async`+`@Transactional`, and missing shutdown drain. | Before merging any change that adds or edits an `@Async` method. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[java-spring-boot]]
- [[java-spring]]
- [[java-junit-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (durability requirement, in-JVM vs cross-host, CPU vs IO) to a rule from `01-core-rules.xml`. Use it before introducing `@Async` to a service.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/AsyncConfig.java`

```java
// AsyncConfig.java — Spring @Async executor configuration skeleton
// Replace pool sizes with profiled values: cores * (1 + wait/compute) for IO-bound

package com.example.config;

import org.springframework.aop.interceptor.AsyncUncaughtExceptionHandler;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.task.TaskDecorator;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;

@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(8);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("Task-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.setWaitForTasksToCompleteOnShutdown(true);
        executor.setAwaitTerminationSeconds(30);
        executor.setTaskDecorator(new MdcTaskDecorator()); // propagates MDC, SecurityContext
        executor.initialize();
        return executor;
    }

    @Bean(name = "emailExecutor")
    public Executor emailExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(4);
        executor.setQueueCapacity(50);
        executor.setThreadNamePrefix("Email-");
        executor.setWaitForTasksToCompleteOnShutdown(true);
        executor.setAwaitTerminationSeconds(30);
        executor.initialize();
        return executor;
    }

    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (ex, method, params) ->
            LoggerFactory.getLogger(AsyncConfig.class)
                .error("Uncaught async exception in {}", method.getName(), ex);
    }
}
```

### `templates/async-service.java`

```java
// @Async service method skeleton — returns CompletableFuture<Void>
// Replace: NotificationService, emailExecutor, EmailService, Order

package com.example.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;

@Service
@RequiredArgsConstructor
@Slf4j
public class NotificationService {

    private final EmailService emailService;

    /**
     * Sends order confirmation email asynchronously on the "emailExecutor" pool.
     * Returns CompletableFuture<Void> — callers can chain or await.
     *
     * @param order the order to confirm (pass ID in production — re-fetch here)
     * @return completed future on success, failed future on error
     */
    @Async("emailExecutor")
    public CompletableFuture<Void> sendOrderConfirmation(Order order) {
        log.info("Sending order confirmation for order {}", order.getId());
        try {
            emailService.send(
                order.getUser().getEmail(),
                "Order Confirmation #" + order.getId(),
                buildEmailBody(order)
            );
            return CompletableFuture.completedFuture(null);
        } catch (Exception e) {
            log.error("Failed to send confirmation for order {}", order.getId(), e);
            return CompletableFuture.failedFuture(e);
        }
    }

    private String buildEmailBody(Order order) {
        return "Your order #" + order.getId() + " has been confirmed.";
    }
}
```
