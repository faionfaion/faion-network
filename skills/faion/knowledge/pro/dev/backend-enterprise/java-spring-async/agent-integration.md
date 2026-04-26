# Agent Integration — Spring Async

## When to use
- Offload IO-bound work (email, SMS, webhooks, slow third-party calls) from request threads inside an existing Spring Boot service.
- Fan-out parallel sub-tasks per request via `CompletableFuture.allOf` when the unit-of-work is short-lived and confined to one JVM.
- Fire-and-forget events that do not need cross-process durability (audit logs, cache warm-ups).

## When NOT to use
- Work must survive a JVM crash → use Spring Batch, Kafka, or RabbitMQ instead.
- Cross-service or cross-host coordination → use a real broker, not an in-memory `ThreadPoolTaskExecutor`.
- CPU-bound parallelism on huge datasets → use `ForkJoinPool` or Project Reactor; `@Async` is sized for IO.
- Long-running transactions: `@Async` opens a new thread, so the outer `@Transactional` does not propagate.

## Where it fails / limitations
- Self-invocation: calling `@Async` from the same bean bypasses the proxy and runs synchronously. Always inject the bean or use `AopContext.currentProxy()`.
- Default executor (`SimpleAsyncTaskExecutor`) creates an unbounded thread per call — must override with a configured `ThreadPoolTaskExecutor`.
- No `@Transactional` propagation, no `SecurityContext` propagation, no MDC propagation by default.
- Exceptions on `void` `@Async` methods are swallowed unless an `AsyncUncaughtExceptionHandler` is registered.
- Spring Boot 3.2+ default executor changed to a virtual-thread `SimpleAsyncTaskExecutor` when `spring.threads.virtual.enabled=true` — verify behavior before upgrading.

## Agentic workflow
A coding subagent should treat `@Async` as a thin wrapper around an executor, not a job queue. Drive it by: (1) detecting if the project already has `@EnableAsync` and a custom executor, (2) generating the `@Async("namedExecutor")` method with a `CompletableFuture<T>` return type, (3) adding an `AsyncUncaughtExceptionHandler` when missing, (4) writing a Spring Boot test using `@SpringBootTest` plus `Awaitility` to verify completion. Have the agent flag any call site where the caller currently relies on `@Transactional` propagation and refuse to convert it without a human checkpoint.

### Recommended subagents
- `general-purpose` Claude subagent — codegen for executor config + `@Async` method conversion.
- Code-review subagent (Sonnet) — checks for self-invocation, missing exception handler, executor pool sizing.

### Prompt pattern
```
Convert <ServiceClass.method> to use @Async("emailExecutor"). Return CompletableFuture<Void>. Verify @EnableAsync is present, ThreadPoolTaskExecutor "emailExecutor" exists, no self-invocation, no enclosing @Transactional. If any check fails, stop and ask.
```
```
Add AsyncUncaughtExceptionHandler that forwards to <existing logger / error tracker>. Update AsyncConfig to implement AsyncConfigurer and override getAsyncUncaughtExceptionHandler().
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mvn spring-boot:run` / `./gradlew bootRun` | Local run with hot reload | bundled |
| `jcmd <pid> Thread.print` | Inspect live threads, verify pool naming (`Async-N`, `Email-N`) | JDK |
| `async-profiler` | Sample CPU/wall on async pool to detect saturation | https://github.com/async-profiler/async-profiler |
| Micrometer `executor` metrics | `management.metrics.enable.executor=true` exposes pool stats to Prometheus | https://micrometer.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Spring Boot Actuator | OSS | Yes (HTTP JSON) | `/actuator/metrics/executor.active` to query pool live |
| Prometheus + Grafana | OSS | Yes | Scrape executor metrics; alert on `executor.queued` ≥ capacity-1 |
| OpenTelemetry Java agent | OSS | Yes | Automatic context propagation across `@Async` (with `otel.instrumentation.executors.enabled=true`) |
| Sentry / Honeybadger | SaaS | Yes (SDK) | Capture exceptions from `AsyncUncaughtExceptionHandler` |

## Templates & scripts
See `templates.md` for the `AsyncConfig` and `@Async` method skeletons. Inline executor health-check the agent can drop into a controller:

```java
@RestController
@RequiredArgsConstructor
public class ExecutorHealthController {
    private final ThreadPoolTaskExecutor taskExecutor;
    private final ThreadPoolTaskExecutor emailExecutor;

    @GetMapping("/internal/executors")
    public Map<String, Map<String, Integer>> stats() {
        return Map.of(
            "task",  poolStats(taskExecutor),
            "email", poolStats(emailExecutor)
        );
    }

    private Map<String, Integer> poolStats(ThreadPoolTaskExecutor e) {
        var pool = e.getThreadPoolExecutor();
        return Map.of(
            "active",   pool.getActiveCount(),
            "queue",    pool.getQueue().size(),
            "core",     pool.getCorePoolSize(),
            "max",      pool.getMaximumPoolSize(),
            "completed", (int) pool.getCompletedTaskCount()
        );
    }
}
```

## Best practices
- Always name the executor: `@Async("emailExecutor")`. Default executor is rarely what you want and changes between Boot versions.
- Set `RejectedExecutionHandler` to `CallerRunsPolicy` for backpressure unless you have a downstream queue.
- Wrap `Runnable` with a `TaskDecorator` to propagate MDC, `SecurityContext`, and tracing baggage — without it, logs lose request-id correlation.
- Return `CompletableFuture<T>` (not `Future<T>` or `void`) so callers can compose and exceptions are observable.
- Pool size: cores × (1 + wait/compute) for IO-bound; profile, do not guess.
- Shut down gracefully: `setWaitForTasksToCompleteOnShutdown(true)` and `setAwaitTerminationSeconds(...)`.

## AI-agent gotchas
- LLM commonly emits `@Async` on a method called from the same class — silently no-op. Static-analysis check or human review required before merge.
- LLM tends to omit explicit executor name; falls back to default. Force the prompt to require a named bean.
- Generated tests using `Thread.sleep` are flaky on CI. Mandate `Awaitility.await().atMost(...)`.
- LLM may suggest `@Async` to "speed up" CPU-heavy work — wrong tool. Review must reject unless workload is IO-bound.
- Virtual threads: if upgrading to Java 21 + Boot 3.2, the agent should detect `spring.threads.virtual.enabled` and rewrite executor sizing, not blindly keep `corePoolSize=4`.
- Human-in-loop checkpoint: any conversion of a method currently inside `@Transactional` must pause for review — silent transaction loss is a high-severity regression.

## References
- https://docs.spring.io/spring-framework/reference/integration/scheduling.html#scheduling-annotation-support-async
- https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html
- https://github.com/spring-projects/spring-framework/wiki/Async-Annotation-Caveats
- "Java Concurrency in Practice" — Goetz, ch. 6 (executors), ch. 8 (pool sizing)
