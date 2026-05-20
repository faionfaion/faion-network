---
slug: go-concurrency-patterns
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Four battle-tested Go concurrency primitives — worker pool, fan-out/fan-in, errgroup with semaphore, and pipeline — selected by workload type (IO-bound vs CPU-bound vs streaming vs fail fast).
content_id: "07220ddb2d1d598e"
tags: [go, concurrency, goroutines, patterns, performance]
---
# Go Concurrency Patterns

## Summary

**One-sentence:** Four battle-tested Go concurrency primitives — worker pool, fan-out/fan-in, errgroup with semaphore, and pipeline — selected by workload type (IO-bound vs CPU-bound vs streaming vs fail fast).

**One-paragraph:** Four battle-tested Go concurrency primitives — worker pool, fan-out/fan-in, errgroup with semaphore, and pipeline — selected by workload type (IO-bound vs CPU-bound vs streaming vs fail fast). Every pattern requires context propagation, panic recovery, and a goleak-based goroutine-leak test.

## Applies If (ALL must hold)

- Building a worker pool to consume from a queue (Kafka, NATS, SQS) with bounded parallelism.
- Fan-out/fan-in over a slice where each item has independent IO.
- Pipelines of transforming stages joined by channels.
- Replacing ad-hoc goroutine launches lacking Context/WaitGroup discipline.
- Rate-limiting outbound calls.

## Skip If (ANY kills it)

- Pure CPU-bound number crunching — simple parallel for without channels.
- Single-flight de-duplication — use golang.org/x/sync/singleflight.
- First error cancels siblings — use errgroup directly, not a custom pool.
- Hot path with billions of tiny tasks — goroutine-per-request already in the runtime.
- Libraries exposing their own concurrency (e.g., DB pool) — don't double-wrap.

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
