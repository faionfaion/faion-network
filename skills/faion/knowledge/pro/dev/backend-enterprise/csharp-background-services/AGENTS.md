---
slug: csharp-background-services
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implement in-process background work via BackgroundService and Channel<T>.
content_id: "ec2c09f61ce1154b"
tags: [background-service, aspnet-core, csharp, hosted-service, async]
---
# C# Background Services

## Summary

**One-sentence:** Implement in-process background work via BackgroundService and Channel<T>.

**One-paragraph:** Implement in-process background work via BackgroundService and Channel<T>. Pattern covers two patterns: (1) queue consumers that bridge HTTP requests to async post-processing, and (2) periodic tasks running at fixed intervals. Always use bounded channels with explicit capacity and FullMode to prevent memory leaks. Resolve scoped dependencies (DbContext, repositories) inside ExecuteAsync via IServiceProvider.CreateScope(), never injected directly. Wrap per-item processing in try/catch and use PeriodicTimer for fixed-interval work, never Task.Delay loops.

## Applies If (ALL must hold)

- In-process queue consumer that bridges an HTTP request to async post-processing.
- Periodic cleanup or sync job running every few minutes on a single replica (no leader election needed).
- Lightweight scheduled work where Hangfire/Quartz overhead is not justified.
- Wiring IHostApplicationLifetime, structured logging, and OpenTelemetry around background work.

## Skip If (ANY kills it)

- Distributed scheduling across multiple replicas — use Hangfire, Quartz.NET, or a platform CronJob (requires leader election).
- Durable, retry-able jobs — use Hangfire, MassTransit, or a real message queue (RabbitMQ, SQS, Service Bus).
- Long-running CPU-bound work that should not share the host thread pool — deploy a separate Worker Service.
- Cron-style "every Tuesday at 3 AM" — PeriodicTimer is fixed-interval only; use Quartz.NET or a platform scheduler.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/dev/backend-enterprise/`
