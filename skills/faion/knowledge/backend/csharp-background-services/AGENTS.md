# C# Background Services

## Summary

**One-sentence:** Long-running in-process workers via `BackgroundService` + Channels with bounded back-pressure, scoped DI, graceful shutdown, idempotent retry and health checks.

**One-paragraph:** Ad-hoc `Task.Run` loops bypass the `IHost` lifecycle, ignore `CancellationToken`, and capture scoped DI as singletons. `BackgroundService` extends `IHostedService` and integrates with graceful shutdown, `IHealthCheck`, and `System.Threading.Channels` for in-memory queues with back-pressure. This methodology pins seven testable rules: extend `BackgroundService` (never `Task.Run`), pass `stoppingToken` everywhere, catch per item inside `ExecuteAsync`, `CreateScope()` for scoped access, `Channel.CreateBounded` with an explicit `FullMode`, `PeriodicTimer` instead of a delay loop, and a per-item log scope. Output: a worker class + DI registration + xUnit test conforming to the contract in `02-output-contract.xml`.

**Ефективно для:**

- Queue consumer / scheduler / file watcher з graceful shutdown і bounded drain.
- Idempotent work units під at-least-once delivery.
- In-memory back-pressure between HTTP and background workers.
- Observability як first-class concern (metrics + tracing + per-item log scope).
- Moderate-throughput scheduled tasks where Hangfire/Quartz is overkill.

## Applies If (ALL must hold)

- Service runs a long-lived background loop (queue consumer, scheduler, watcher) inside the API host process.
- Process must shut down gracefully on SIGTERM with bounded drain time.
- Work units must be idempotent to survive at-least-once delivery.
- Throughput fits on a single replica or a leader-elected replica.

## Skip If (ANY kills it)

- Jobs MUST survive restarts — use Hangfire, Quartz.NET, or a durable broker; channels are in-memory only.
- Heavy CPU work per item — would starve the HTTP thread pool; isolate to a separate Worker host.
- Distributed scheduling across replicas without leader election.
- Exactly-once semantics required — in-memory channels lose state on shutdown.
- One-shot CLI / job runner, or a periodic job better expressed as a cron-triggered Function / Lambda.
- Hosted in IIS in-process — BackgroundService lifecycle does not align cleanly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Worker scope / job spec (queue / scheduler / watcher) | markdown | product / ticket |
| Idempotency key strategy | markdown | architecture |
| ASP.NET Core 6+ project | csproj | repo |
| DbContext or downstream service contract | C# interface | repo |
| Observability stack (metrics + tracing) | config | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[csharp-aspnet-core]] | Hosted service runs inside the same Generic Host as the API |
| [[csharp-dotnet]] | Base .NET wiring, DI, hosting model |
| [[csharp-entity-framework]] | Scoped DbContext lifecycle the worker depends on |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: extend-backgroundservice, pass-stoppingtoken, per-item-trycatch, scope-per-item, bounded-channel, periodic-timer-not-delay-loop, structured-per-item-logging | 1300 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the worker spec + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: task-run-loop, unbounded-channel, captive-dbcontext, no-stoppingtoken, uncorrelated-worker-logs | 900 |
| `content/04-procedure.xml` | essential | 7-step procedure with input/action/output per step | 1100 |
| `content/06-decision-tree.xml` | essential | Routing tree on durability / CPU / queue / schedule → conclusion(ref=rule-id) | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-job-shape` | sonnet | Apply the decision tree on durability / throughput / CPU |
| `scaffold-skeleton` | haiku | Mechanical template emission |
| `wire-feature-logic` | sonnet | Per-feature judgment with bounded inputs |
| `write-xunit-test` | haiku | Mechanical AAA test against the IHostedService API |
| `audit-output` | sonnet | Verify rules in 01-core-rules.xml hold |

## Templates

| File | Purpose |
|------|---------|
| `templates/queue-consumer.cs` | BackgroundService queue-consumer skeleton with retry + idempotency |
| `templates/registration.cs` | Channel + worker + health-check registration snippet for Program.cs |
| `templates/prompt-worker.txt` | Subagent prompt generating worker + registration + xUnit test |
| `templates/_smoke-test.cs` | Filled-in minimal queue consumer for a Users.Created topic |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-background-services.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[csharp-aspnet-core]]
- [[csharp-dotnet]]
- [[csharp-entity-framework]]
- [[csharp-xunit-testing]]
- [[audit-grade-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable job-shape signals (durability requirement, CPU profile, queue vs schedule) to a rule from `01-core-rules.xml`, and either approves BackgroundService or redirects to a durable broker / separate Worker host. Use it whenever an engineer reaches for `Task.Run` or considers a hosted service for periodic work.
