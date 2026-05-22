---
slug: php-laravel-queues
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Laravel's queue system for offloading background work: job classes implementing ShouldQueue, named queues for priority, WithoutOverlapping middleware for deduplication, retry/backoff/timeout configuration, and Bus::batch for parallel dataset processing.
content_id: "302900c45e681bd9"
tags: [laravel, queues, jobs, background-processing, async]
---
# Laravel Queues

## Summary

**One-sentence:** Laravel's queue system for offloading background work: job classes implementing ShouldQueue, named queues for priority, WithoutOverlapping middleware for deduplication, retry/backoff/timeout configuration, and Bus::batch for parallel dataset processing.

**One-paragraph:** Laravel's queue system for offloading background work: job classes implementing ShouldQueue, named queues for priority, WithoutOverlapping middleware for deduplication, retry/backoff/timeout configuration, and Bus::batch for parallel dataset processing. Jobs must be idempotent (check isProcessed() early), pass primitive IDs only (not Eloquent models), and implement failed() to surface failures to operators.

## Applies If (ALL must hold)

- Any work taking >200ms from HTTP: email, PDF/CSV generation, third-party API calls, image processing.
- Fan-out: one user action triggers many side-effects (notify N subscribers).
- Batch jobs (Bus::batch) with then/catch/finally callbacks for large dataset processing.
- Webhook processing where you must ack the sender quickly and process asynchronously.
- Scheduled retries with exponential backoff for unreliable downstream services.

## Skip If (ANY kills it)

- Hard real-time requirements (<1s end-to-end) — queue overhead and worker polling add latency.
- When the DB write IS the result the user is waiting for.
- Single-host deployments without a daemonized worker (queue:work must run continuously).
- Jobs that depend on request-scoped state (auth user, session) — pass primitive IDs only.
- When there is no Horizon/supervisor plan and no failed_jobs monitoring.

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
