---
slug: go-concurrency-patterns
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Safe, leak-free concurrency in Go using bounded worker pools, fan-out/fan-in pipelines, and context.
content_id: "07220ddb2d1d598e"
tags: [go, concurrency, goroutines, channels, patterns]
---
# Go Concurrency Patterns

## Summary

**One-sentence:** Safe, leak-free concurrency in Go using bounded worker pools, fan-out/fan-in pipelines, and context.

**One-paragraph:** Safe, leak-free concurrency in Go using bounded worker pools, fan-out/fan-in pipelines, and context.Context cancellation. All goroutines have explicit termination paths. Channels have documented ownership (one writer, one closer). go test -race is non-negotiable for any concurrent code.

## Applies If (ALL must hold)

- Fan-out work over goroutines: HTTP request batchers, ETL pipelines, scrapers, queue workers
- CPU-bound parallel processing with runtime.NumCPU() workers
- I/O-bound parallel work (HTTP fetches, DB calls) where bounded pools cap concurrency
- Streaming pipelines needing backpressure (bounded channels) and clean shutdown via context

## Skip If (ANY kills it)

- Single-threaded request handlers — Go's net/http already goroutine-per-request; adding pools is overkill
- Trivial sequential loops — concurrency adds complexity (panic recovery, error aggregation) that often outweighs gains
- When errgroup.Group already covers the use case — prefer stdlib over hand-rolled pools
- Long-running stateful tasks needing crash recovery — use a real queue (NATS, SQS) instead of in-memory channels

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

- parent skill: `solo/dev/software-developer/`
