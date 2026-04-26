# Rust Tokio Async Patterns

## Summary

Async primitives for Tokio-based Rust services: `tokio::try_join!` for parallel independent futures, `spawn_blocking` for CPU-heavy work, `futures::stream::buffer_unordered` + `Semaphore` for bounded-concurrent collection processing, and `JoinSet` for dynamic task groups. Every pattern requires an explicit concurrency bound, structured error type, and cancellation-safety annotation.

## Why

Tokio's cooperative scheduler stalls on blocking calls and panics on `std::sync::Mutex` held across `.await`. Without the four-primitive selection discipline, agents produce unbounded `join_all` that overloads pools, block the runtime with synchronous hashing, and swallow panics from `JoinHandle`. The primitives here map directly to the four workload classes (parallel IO, CPU offload, streaming batch, managed task group).

## When To Use

- Writing async services on Tokio (Axum, tonic, sqlx, reqwest) with bounded concurrency.
- Replacing sequential `.await` chains that could run in parallel with `try_join!`.
- Offloading CPU-intensive work (Argon2, image, compression) via `spawn_blocking`.
- Streaming bounded-concurrency over large collections with `buffer_unordered` + `Semaphore`.
- Migrating from `async-std` or `smol` to Tokio.

## When NOT To Use

- Single-thread CPU work — async adds no benefit; use sync code.
- Embedded / `no_std` — use `embassy` instead.
- Runtime-agnostic library code — depend on `futures`, not `tokio`.
- Hard real-time scheduling — Tokio is best-effort, not deadline-driven.

## Content

| File | What's inside |
|------|---------------|
| `content/01-primitive-selection.xml` | Four workload classes mapped to primitives, selection rules. |
| `content/02-patterns.xml` | try_join!, spawn_blocking, buffer_unordered + Semaphore, JoinSet patterns with code. |
| `content/03-rules.xml` | Cancellation-safety rules, MutexGuard-across-await antipattern, agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/map_concurrent.rs` | Generic bounded-parallel helper using buffer_unordered + Semaphore + TryStreamExt. |
| `templates/service_example.rs` | UserService with try_join!, spawn_blocking for password hashing. |
