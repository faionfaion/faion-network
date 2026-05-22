---
slug: rust-tokio-async
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Tokio multiplexes thousands of I/O-bound connections on a small thread pool.
content_id: "3e53b31414fc5017"
tags: [tokio, async, rust, concurrency, runtime]
---
# Tokio Async Patterns

## Summary

**One-sentence:** Tokio multiplexes thousands of I/O-bound connections on a small thread pool.

**One-paragraph:** Tokio multiplexes thousands of I/O-bound connections on a small thread pool. CPU-bound work must use spawn_blocking; independent DB calls must use try_join! or JoinSet; every spawn handle must be awaited or dropped. Holding MutexGuard across .await or calling blocking syscalls directly causes cascading stalls.

## Applies If (ALL must hold)

- Rust services multiplexing thousands of network connections (HTTP, gRPC, WebSocket) on a small thread pool
- Replacing thread-per-request workers with structured concurrency (try_join!, JoinSet, select!)
- Wrapping CPU-bound work in spawn_blocking to avoid stalling the runtime
- Implementing fan-out / fan-in pipelines with channels (mpsc, broadcast, watch)
- Adding cancellation, timeouts, and graceful shutdown to long-running tasks

## Skip If (ANY kills it)

- Simple CLI that does one thing and exits — std::thread or sync code is shorter and clearer
- Heavy CPU-bound workloads (ML inference, image transforms) — Rayon / dedicated thread pools are better
- Embedded / no_std targets — Tokio requires an allocator and OS threads; use embassy instead
- Very low-latency single-shot RPC where the runtime overhead matters; consider glommio or monoio (thread-per-core) for io_uring workloads
- Teams new to Rust — async + lifetimes + Send/Sync is the steepest cliff in the language

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
