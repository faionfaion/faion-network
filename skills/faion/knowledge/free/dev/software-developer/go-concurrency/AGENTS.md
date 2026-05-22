---
slug: go-concurrency
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Canonical Go goroutine and concurrency patterns: worker pool, rate limiter, semaphore, RWMutex cache, and sync.
content_id: "5a2df46fd2085f66"
tags: [go, concurrency, goroutines, channels, worker-pool]
---
# Go Concurrency Patterns

## Summary

**One-sentence:** Canonical Go goroutine and concurrency patterns: worker pool, rate limiter, semaphore, RWMutex cache, and sync.

**One-paragraph:** Canonical Go goroutine and concurrency patterns: worker pool, rate limiter, semaphore, RWMutex cache, and sync.Once. The invariant: every goroutine must have an explicit exit condition (context.Done() or channel close), and the goroutine that writes to a channel is the one that closes it. Tests must pass go test -race.

## Applies If (ALL must hold)

- Generating a Go service that processes jobs in parallel (HTTP fan-out, batch ETL, queue consumer).
- Refactoring sequential Go code into a worker pool with bounded concurrency.
- Writing pipelines where stage N feeds stage N+1 via channels.
- Adding context-based cancellation to existing goroutines.
- Building rate limiters or semaphores around external APIs.

## Skip If (ANY kills it)

- Single-threaded scripts or one-shot CLIs where startup cost dominates.
- Code that needs to share mutable state without a clear ownership boundary — refactor the data model first.
- Pure CPU-bound work with GOMAXPROCS=1 — goroutines add scheduling overhead with no parallelism.
- When "concurrency" is really async I/O against one source — a single goroutine with select suffices.

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

- parent skill: `free/dev/software-developer/`
