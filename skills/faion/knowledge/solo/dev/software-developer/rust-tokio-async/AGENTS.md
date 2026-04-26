# Tokio Async Patterns

## Summary

Tokio is Rust's async runtime for multiplexing thousands of I/O-bound connections on a small thread pool. Core rule: CPU-bound work (password hashing, image processing) must run in `spawn_blocking` to avoid stalling the runtime; independent DB calls must use `tokio::try_join!` or `JoinSet` rather than sequential `.await`; every `tokio::spawn` handle must be awaited or explicitly dropped.

## Why

Async Rust with Tokio achieves near-zero overhead concurrency for I/O: the runtime parks tasks at `.await` and resumes them on completion instead of blocking threads. Holding a `MutexGuard` across `.await` or calling blocking syscalls directly on the async thread pool causes cascading stalls. Unstructured `spawn` without `JoinHandle` management creates memory leaks and lost errors.

## When To Use

- Rust services multiplexing thousands of network connections (HTTP, gRPC, WebSocket) on a small thread pool
- Replacing thread-per-request workers with structured concurrency (`try_join!`, `JoinSet`, `select!`)
- Wrapping CPU-bound work in `spawn_blocking` to avoid stalling the runtime
- Implementing fan-out / fan-in pipelines with channels (`mpsc`, `broadcast`, `watch`)
- Adding cancellation, timeouts, and graceful shutdown to long-running tasks

## When NOT To Use

- Simple CLI that does one thing and exits — `std::thread` or sync code is shorter and clearer
- Heavy CPU-bound workloads (ML inference, image transforms) — Rayon / dedicated thread pools are better
- Embedded / `no_std` targets — Tokio requires an allocator and OS threads; use `embassy` instead
- Teams new to Rust — async + lifetimes + `Send`/`Sync` is the steepest learning cliff

## Content

| File | What's inside |
|------|---------------|
| `content/01-async-service.xml` | Service struct with async methods, `try_join!` for parallel queries, `spawn_blocking` for CPU work |
| `content/02-concurrency.xml` | Semaphore-bounded batch processing, `JoinSet`, channel patterns (`mpsc`, `broadcast`, `watch`) |
| `content/03-antipatterns.xml` | MutexGuard across `.await`, orphaned `JoinHandle`, blocking in async context, `block_on` nesting |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-service.rs` | Reference async service with `try_join!`, `spawn_blocking`, and error propagation |
| `templates/batch-processor.rs` | Semaphore-bounded concurrent batch processor using `futures::StreamExt` |
