# C# Background Services

## Summary

ASP.NET Core in-process background workers using `BackgroundService` + `System.Threading.Channels`: queue consumers, periodic cleaners, and cache warmers with bounded channels for back-pressure, scoped DI via `CreateScope()`, graceful shutdown via `CancellationToken`, and `IHealthCheck` integration.

## Why

Ad-hoc `Task.Run` loops are not lifecycle-managed, ignore cancellation, and bypass DI scoping. `BackgroundService` integrates with `IHost` shutdown, surfaces health via `IHealthCheck`, and makes channels first-class. Bounded channels prevent memory bombs; `PeriodicTimer` prevents drift. Scoped DI via `CreateScope()` prevents captive-dependency bugs with `DbContext`.

## When To Use

- Long-running in-process workers: queue consumers, periodic cleanup, cache warmers, file watchers
- In-memory work queues with back-pressure between HTTP requests and a background worker
- Scheduled tasks at moderate throughput where a separate process (Hangfire, Quartz) is overkill
- Graceful-shutdown requirements via `IHostedService`

## When NOT To Use

- Jobs that must survive app restarts — use Hangfire, Quartz.NET with persistence, or a real broker
- Heavy CPU work — runs in the host process and can starve the HTTP thread pool; use a Worker host
- Distributed scheduling across replicas — `BackgroundService` runs on every instance; add leader election first
- "Exactly-once" semantics — in-memory channels are lost on shutdown

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | BackgroundService + Channel wiring rules, scoped DI, PeriodicTimer, health check integration |
| `content/02-examples.xml` | Queue consumer, timed cleanup, health check, DI registration examples and antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-worker.txt` | Subagent prompt template for generating BackgroundService + queue + DI registration + xUnit test |
