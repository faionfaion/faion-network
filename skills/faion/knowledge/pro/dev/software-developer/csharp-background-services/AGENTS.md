---
slug: csharp-background-services
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Long-running in-process background workers in ASP.
content_id: "ec2c09f61ce1154b"
tags: [csharp, background-services, async, channels, aspnet-core]
---
# C# Background Services

## Summary

**One-sentence:** Long-running in-process background workers in ASP.

**One-paragraph:** Long-running in-process background workers in ASP.NET Core using BackgroundService + System.Threading.Channels for queue consumers, periodic cleanup, and cache warming with bounded channels for back-pressure, scoped DI via CreateScope(), graceful shutdown via CancellationToken, and IHealthCheck integration.

## Applies If (ALL must hold)

- Long-running in-process workers: queue consumers, periodic cleanup, cache warmers, file watchers
- In-memory work queues with back-pressure between HTTP requests and a background worker
- Scheduled tasks at moderate throughput where a separate process (Hangfire, Quartz) is overkill
- Graceful-shutdown requirements via IHostedService

## Skip If (ANY kills it)

- Jobs that must survive app restarts — use Hangfire, Quartz.NET with persistence, or a real broker
- Heavy CPU work — runs in the host process and can starve the HTTP thread pool; use a Worker host
- Distributed scheduling across replicas — BackgroundService runs on every instance; add leader election first
- Exactly-once semantics — in-memory channels are lost on shutdown

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

- parent skill: `pro/dev/software-developer/`
