---
slug: go-goroutines
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Goroutines are lightweight threads managed by Go runtime.
content_id: "249c25f2cec17c32"
tags: [go, concurrency, goroutines, worker-pools, synchronization]
---
# Go Goroutines and Worker Patterns

## Summary

**One-sentence:** Goroutines are lightweight threads managed by Go runtime.

**One-paragraph:** Goroutines are lightweight threads managed by Go runtime. Use for parallel processing, HTTP servers, background tasks, and I/O-bound work. Key principle: don't share memory; communicate via channels. Keep lock sections small. Avoid leaks with exit conditions. Use context for cancellation.

## Applies If (ALL must hold)

- Parallel processing of data where goroutines can work independently.
- HTTP servers handling concurrent requests, where each request gets its own goroutine.
- Background task processing and job queues, dispatching work to worker pools.
- I/O-bound operations where waiting for network or disk does not block other work.
- CPU-bound parallel computation on multi-core systems.

## Skip If (ANY kills it)

- Simple sequential programs where concurrency adds unnecessary complexity.
- Very hot inner loops where goroutine scheduling overhead is significant compared to work done.
- Systems where you cannot use channels (e.g., certain legacy C bindings) and must use raw locks.
- Scenarios where the cost of context propagation (setup, cleanup) exceeds the parallelism benefit.

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

- parent skill: `pro/dev/backend-systems/`
