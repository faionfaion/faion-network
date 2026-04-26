# Agent Integration — Spring Async

## When to use
- Background tasks that should not block HTTP threads (sending email/SMS, syncing CRM/Slack, generating reports, image/video transcoding) when a queue + worker is overkill.
- Fan-out service calls where the controller fires multiple downstream calls and needs to aggregate (parallel HTTP clients, search across shards).
- Event-driven side effects in Spring Boot apps using `ApplicationEventPublisher` + `@Async @EventListener`.
- Migrating thread-pool / `ExecutorService` boilerplate to Spring-managed `ThreadPoolTaskExecutor` with `@EnableAsync`.
- Fire-and-forget audit logging or metrics that must not impact request latency.
- Legacy code using raw `new Thread(...)` to be brought under DI / observability / shutdown management.

## When NOT to use
- Cross-process work (durable queues, retries, idempotency, cross-host fan-out) — use SQS / RabbitMQ / Kafka / Spring Cloud Stream / Temporal, not `@Async`. `@Async` does not survive a JVM restart.
- High-throughput streaming workloads — use Project Reactor / WebFlux end-to-end; mixing `@Async` (servlet-based) with reactive code blows threads.
- Latency-sensitive request paths where the work MUST complete before response — use synchronous code.
- Spring Boot apps with virtual threads enabled (`spring.threads.virtual.enabled=true`, Boot 3.2+) — `@Async` adds no value vs. just calling the method on a virtual thread, and may interfere with Loom-aware schedulers.
- Anything requiring exactly-once semantics, durable state, or saga workflows — not what `@Async` is for.

## Where it fails / limitations
- **Self-invocation no-ops.** `@Async` proxy is bypassed when calling another method of the same bean (`this.async()`). Method runs synchronously and silently. README's `NotificationService` example is fine, but agents replicate it as `this.sendEmail()` in the same class.
- **Default `SimpleAsyncTaskExecutor` doesn't pool threads.** Without an explicit `taskExecutor` bean, Spring creates a new thread per call and your app exhausts the OS thread limit. README correctly defines a `ThreadPoolTaskExecutor` — keep it.
- **`CompletableFuture` exception handling.** Uncaught `@Async` exceptions are dropped unless you set `AsyncUncaughtExceptionHandler` or return `CompletableFuture` and call `.exceptionally(...)`. Agents return `void` and lose errors.
- **`@Transactional` + `@Async` mix.** Async method runs in a separate thread → separate transaction → callers' transaction is not propagated. Reading the same DB row from inside `@Async` may not see the caller's not-yet-committed changes.
- **Security context lost.** `SecurityContextHolder` is `ThreadLocal`. `@Async` thread doesn't see the caller's principal unless you wire `DelegatingSecurityContextAsyncTaskExecutor`.
- **MDC / logging context lost.** Same root cause; trace IDs and request IDs vanish from async logs unless propagated via `TaskDecorator`.
- **Graceful shutdown ignored.** Default executor doesn't wait for in-flight tasks at JVM shutdown — emails / webhooks lost. Set `setWaitForTasksToCompleteOnShutdown(true)` + `setAwaitTerminationSeconds`.
- **Backpressure failures.** When queue fills (`QueueCapacity`), default rejection policy is `AbortPolicy` → `RejectedExecutionException` thrown to caller. README sets `CallerRunsPolicy` (degrades but doesn't drop) — better in most cases.
- **Testing pain.** Tests against `@Async` need `Awaitility` or `AsyncTestExecutor`; agents add `Thread.sleep` and produce flakes.

## Agentic workflow
Drive Spring Async adoption as a four-stage pipeline: (1) a discovery agent enumerates candidate methods (long-running, no return value needed by caller, idempotent on retry); (2) a config agent verifies / creates `ThreadPoolTaskExecutor` beans with `TaskDecorator` for MDC + Security + OTel context; (3) a refactor agent annotates methods, replaces `void` with `CompletableFuture<Void>` where errors must be observable, splits async methods to a separate bean to avoid self-invocation; (4) a test agent generates `Awaitility` + `WireMock`-based tests. Persist async-eligible inventory in `.aidocs/product_docs/async-inventory.md`. Use `faion-sdd-executor-agent` to drive each method per SDD task.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — opus model fits because async/sync trade-offs (consistency, retries, backpressure) are decision-heavy.
- `faion-feature-executor` skill — sequential mode: config → refactor → test → integration test, gating on green.
- A purpose-built **async-anti-pattern agent** (worth adding under `agents/`): linter for self-invocation, missing `@EnableAsync`, void-returning `@Async` without `AsyncUncaughtExceptionHandler`, `@Async` on method that calls `JpaRepository.save` inside a parent `@Transactional`.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — async tasks frequently log payload bodies (email content, webhook bodies) that contain PII / tokens; scrub before commit.
- For external-call durability, escalate to sibling methodologies on Kafka / RabbitMQ / Spring Cloud Stream rather than letting agents leave it on `@Async`.

### Prompt pattern
Refactor a method to async:
```
You are converting a method to Spring @Async on Spring Boot 3.4.
Constraints:
1. The async method MUST live in a different bean than the caller
   (no self-invocation). If currently same bean, extract to a new
   @Service.
2. Annotate the class @EnableAsync once (in @Configuration). Reuse
   existing AsyncConfig if present.
3. Use a named executor: @Async("taskExecutor") or "emailExecutor".
   Bean must be ThreadPoolTaskExecutor with corePoolSize, maxPoolSize,
   queueCapacity, threadNamePrefix, CallerRunsPolicy, and
   setWaitForTasksToCompleteOnShutdown(true).
4. Wrap with TaskDecorator that copies MDC + SecurityContextHolder +
   OTel current span.
5. If errors matter, return CompletableFuture<Void> and add
   .exceptionally to the caller; OR set AsyncUncaughtExceptionHandler
   in AsyncConfig that logs + increments a Prometheus counter.
6. NEVER call the @Async method from a parent @Transactional
   expecting transaction propagation; remove the parent @Transactional
   or split.
7. Test with Awaitility, never Thread.sleep.
```

Anti-pattern review:
```
You are reviewing a PR adding Spring @Async. Flag:
(1) self-invocation (`this.<asyncMethod>()` inside same class),
(2) missing executor name -> uses default SimpleAsyncTaskExecutor,
(3) void return + no AsyncUncaughtExceptionHandler,
(4) @Async on a @Transactional method, expecting same transaction,
(5) raw new Thread(...) outside Spring context,
(6) executor without setWaitForTasksToCompleteOnShutdown,
(7) test using Thread.sleep instead of Awaitility,
(8) MDC / SecurityContext drop -> missing TaskDecorator.
Cite file:line. Do not propose fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mvn` / `gradle` | Build, test, run | https://maven.apache.org , https://gradle.org |
| Spring Boot Actuator + `/actuator/threaddump` | Inspect live thread pools | https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html |
| `jcmd <pid> Thread.print` | JVM thread dump from CLI | https://docs.oracle.com/en/java/javase/21/docs/specs/man/jcmd.html |
| `async-profiler` | Sample async / blocking time | https://github.com/async-profiler/async-profiler |
| Micrometer + Prometheus | `executor.queued`, `executor.active`, `executor.completed` metrics | https://micrometer.io |
| `awaitility` | Test fluent waits | `org.awaitility:awaitility` ; https://github.com/awaitility/awaitility |
| `WireMock` CLI | Stub external HTTP for async integration tests | https://wiremock.org |
| `jstack` / `jfr` (Java Flight Recorder) | Profiling thread / lock contention | bundled with JDK |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| RabbitMQ + Spring AMQP | OSS | yes | Use when @Async outgrows in-process (durability, retries). |
| Apache Kafka + Spring Cloud Stream | OSS | yes | High-throughput async; replace @Async for event fan-out. |
| AWS SQS + spring-cloud-aws | SaaS | yes | Drop-in cloud queue. |
| Temporal | OSS / Cloud | yes | Where async needs durable state machines / saga. |
| Redis Streams + Spring Data Redis | OSS | yes | Cheap pub/sub upgrade path. |
| Hazelcast / Ignite distributed executors | OSS | yes | Cluster-wide async work. |
| Sentry / Datadog APM | SaaS | yes | Observe async tasks; trace propagation requires TaskDecorator. |
| OpenTelemetry Java agent | OSS | yes | Auto-instrumentation propagates async context if executor is wrapped. |
| Spring Batch | OSS | yes | When async grows into chunked jobs with restart semantics. |
| Quartz Scheduler | OSS | yes | Cron-like scheduled @Async; Boot integration via `spring-boot-starter-quartz`. |

## Templates & scripts

The methodology already ships AsyncConfig / NotificationService examples in `README.md` and templates in `templates.md`. Gap: a script that audits a project for `@Async` anti-patterns. Inline drop-in (≤50 lines) — `scripts/spring-async-audit.sh`:

```bash
#!/usr/bin/env bash
# spring-async-audit.sh — flag common @Async anti-patterns.
# Usage: spring-async-audit.sh <project-root>
set -euo pipefail
root="${1:?usage: spring-async-audit.sh PROJECT_ROOT}"
fail=0
echo "# Spring @Async audit ($root)"

echo "## Self-invocation (this.<asyncMethod>) inside same @Service"
for f in $(grep -rl '@Async' "$root/src/main" --include='*.java' 2>/dev/null); do
  cls=$(basename "$f" .java)
  for m in $(grep -E '@Async' "$f" -A 1 | grep -oE '[a-z][a-zA-Z0-9]+\(' | tr -d '('); do
    grep -nE "this\.${m}\(" "$f" && echo "  └ $f:$cls#$m self-invocation"
  done
done | tee /tmp/async.self || true
[[ -s /tmp/async.self ]] && fail=1

echo "## @Async without explicit executor name"
grep -rEn '@Async$|@Async\s*$|@Async\(\)' "$root/src/main" --include='*.java' \
  | tee /tmp/async.noexec || true
[[ -s /tmp/async.noexec ]] && fail=1

echo "## Void-returning @Async without AsyncUncaughtExceptionHandler"
grep -rl '@Async' "$root/src/main" --include='*.java' \
  | xargs grep -lE 'public\s+void' \
  | xargs grep -L 'AsyncUncaughtExceptionHandler' \
  | tee /tmp/async.exc || true

echo "## @Transactional combined with @Async on same method"
grep -rEn '@Async\b' "$root/src/main" --include='*.java' -B 2 \
  | grep '@Transactional' \
  | tee /tmp/async.tx || true
[[ -s /tmp/async.tx ]] && fail=1

echo "## Executor missing setWaitForTasksToCompleteOnShutdown"
grep -rEn 'new ThreadPoolTaskExecutor' "$root/src/main" --include='*.java' -A 25 \
  | grep -L 'setWaitForTasksToCompleteOnShutdown' \
  | tee /tmp/async.shutdown || true

echo "## Test using Thread.sleep with @Async"
grep -rEn 'Thread\.sleep\(' "$root/src/test" --include='*.java' \
  | tee /tmp/async.sleep || true

exit "$fail"
```

Wire into pre-commit / CI; Maven Enforcer can also block deprecated patterns at compile time.

## Best practices
- **Async method lives in a different bean than the caller.** No self-invocation. Refactor into a dedicated `AsyncEmailService` if needed.
- **Always use a named executor.** `@Async("taskExecutor")` — not just `@Async`. Default is unbounded `SimpleAsyncTaskExecutor`.
- **`ThreadPoolTaskExecutor` with explicit limits.** Core, max, queue, prefix, rejection policy, shutdown wait. README's `AsyncConfig` is a good baseline; copy it.
- **`TaskDecorator` propagates context.** MDC (logging trace IDs), SecurityContext, OTel current span, request locale. Without this, observability is broken.
- **Return `CompletableFuture<T>` if errors must be observable.** `void` async swallows exceptions unless `AsyncUncaughtExceptionHandler` is wired.
- **Don't share `@Transactional` across async boundary.** Either the parent doesn't open a tx, or the async method opens its own (and read-after-commit is needed).
- **Backpressure-friendly rejection policy.** `CallerRunsPolicy` for fire-and-forget where degradation is OK; `AbortPolicy` only when caller can handle the exception.
- **Metrics on every executor.** `Micrometer` exports `executor.queued`, `active`, `completed`, `rejected`. Alert on `rejected > 0` for any non-CallerRuns pool.
- **`setWaitForTasksToCompleteOnShutdown(true)` + bounded `setAwaitTerminationSeconds`.** No silent task loss on deploy.
- **Virtual threads on Boot 3.2+ where applicable.** `spring.threads.virtual.enabled=true` lets the platform handle scheduling; revisit per-pool sizing.
- **Test with `Awaitility`, not `Thread.sleep`.** `await().atMost(2, SECONDS).untilAsserted(...)`.
- **Boundaries with external systems = queue, not `@Async`.** Email vendor down → `@Async` retries die with the JVM. Use a queue for durability.

## AI-agent gotchas
- **Self-invocation reflex.** Agents add `@Async` to a method and call it from the same class. The proxy doesn't intercept and the method runs synchronously. Force the rule: "If the caller and `@Async` method are in the same bean, refactor."
- **Wrong executor.** Agents leave `@Async` empty and code uses `SimpleAsyncTaskExecutor` (unbounded threads). Force named executor + bean definition.
- **Lost SecurityContext.** Agents call `SecurityContextHolder.getContext()` inside the async method — null. Add `DelegatingSecurityContextAsyncTaskExecutor` or `TaskDecorator`.
- **`@Async` + `@Transactional` on same method.** Tx applied to the caller's thread, not the async thread. Misleading. Reject in review.
- **Returning `void` and losing exceptions.** Agents do not wire `AsyncUncaughtExceptionHandler`. Force one in `AsyncConfig` that logs + emits a metric.
- **`@Async` for things that need durability.** Agents use `@Async` for charging cards / sending invoices. JVM restart loses the work. Force a queue + handler.
- **Thread.sleep in tests.** Agents test async by `Thread.sleep(500); assertX()`. Flaky. Use `Awaitility` + `untilAsserted`.
- **MDC drop.** Agents log inside async method, lose trace ID, and debugging is dark. Add `TaskDecorator` that copies `MDC.getCopyOfContextMap()`.
- **Default rejection policy crashes user requests.** Default `AbortPolicy` throws `RejectedExecutionException` to caller. Pick `CallerRunsPolicy` for fire-and-forget OR a dedicated handler that logs + queues.
- **Virtual-thread confusion.** Agents wire `@Async` AND virtual threads, doubling abstraction. Decide one model per pool.
- **Memory leak via unbounded `CompletableFuture` chains.** Agents chain `.thenApplyAsync(...).thenApplyAsync(...)` indefinitely; without explicit executors, the common pool runs everything. Pin executor on each `*Async`.
- **Human-in-the-loop on parallelism numbers.** corePoolSize / maxPoolSize / queueCapacity are tuning decisions; never let an agent guess. Require benchmark + load test before merge.
- **Observability gaps.** Agents add `@Async` and forget to register Micrometer metrics on the executor (`Metrics.gauge("executor.active", taskExecutor, ThreadPoolTaskExecutor::getActiveCount)`). Force registration in the config.

## References
- Spring Framework — Task Execution and Scheduling. https://docs.spring.io/spring-framework/reference/integration/scheduling.html
- Spring Boot — Task Execution. https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html
- Spring Security — Concurrency Support. https://docs.spring.io/spring-security/reference/servlet/integrations/concurrency.html
- Awaitility — https://github.com/awaitility/awaitility
- Micrometer — Java thread pool metrics. https://docs.micrometer.io/micrometer/reference/reference/jvm.html
- OpenTelemetry Java — Async/Reactor. https://opentelemetry.io/docs/languages/java/instrumentation/
- Project Loom / Virtual threads in Spring Boot 3.2. https://spring.io/blog/2022/10/11/embracing-virtual-threads
- "Java Concurrency in Practice" — Brian Goetz (foundational executor patterns).
- Sibling methodologies in this repo: `pro/dev/software-developer/java-spring/`, `java-spring-boot/`, `java-spring-boot-patterns/`, `java-junit-testing/`, `php-laravel-queues/`, `ruby-sidekiq-jobs/`.
