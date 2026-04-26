# C# Background Services

## Summary

Pattern for in-process background processing in ASP.NET Core using `BackgroundService` + `Channel<T>`. Covers queue consumers (producer/consumer via bounded `Channel<T>`), periodic tasks (via `PeriodicTimer`), and graceful shutdown under `CancellationToken`. Scoped dependencies must be resolved per-item via `IServiceProvider.CreateScope()` — never injected directly into the singleton `BackgroundService`.

## Why

`IHostedService` / `BackgroundService` is the idiomatic .NET way to run in-process background work without a separate process or external scheduler. `Channel<T>` gives a thread-safe, backpressure-aware queue. `PeriodicTimer` fires at fixed intervals and cancels cleanly on host shutdown — unlike `Task.Delay` loops, which leak on SIGTERM.

## When To Use

- In-process queue consumer that bridges an HTTP request to async post-processing.
- Periodic cleanup or sync job running every few minutes on a single replica (no leader election needed).
- Lightweight scheduled work where Hangfire/Quartz overhead is not justified.
- Wiring `IHostApplicationLifetime`, structured logging, and OpenTelemetry around background work.

## When NOT To Use

- Distributed scheduling across multiple replicas — use Hangfire, Quartz.NET, or a platform CronJob (requires leader election).
- Durable, retry-able jobs — use Hangfire, MassTransit, or a real message queue (RabbitMQ, SQS, Service Bus).
- Long-running CPU-bound work that should not share the host thread pool — deploy a separate Worker Service.
- Cron-style "every Tuesday at 3 AM" — `PeriodicTimer` is fixed-interval only; use Quartz.NET or a platform scheduler.

## Content

| File | What's inside |
|------|---------------|
| `content/01-queue-consumer.xml` | `BackgroundService` + bounded `Channel<T>` producer/consumer pattern with per-item scope and try/catch. |
| `content/02-periodic-timer.xml` | `PeriodicTimer`-based timed background service with scoped DI resolution. |
| `content/03-rules-and-gotchas.xml` | Mandatory rules, common AI-agent mistakes, and registration snippet. |

## Templates

| File | Purpose |
|------|---------|
| `templates/queue-consumer.cs` | `BackgroundService` + `Channel<T>` producer/consumer skeleton with bounded channel, scoped DI, and per-item try/catch. |
| `templates/registration.cs` | `Program.cs` registration snippet for channel, queue abstraction, and hosted services. |
