# Agent Integration — Rust Tokio Async Patterns

## When to use
- Writing async services on Tokio (Axum, Actix, tonic, sqlx, reqwest) with bounded concurrency.
- Replacing nested `.await` chains that could run in parallel with `tokio::try_join!` / `tokio::join!`.
- Offloading CPU-intensive work (Argon2, image, compression, regex) from the runtime via `spawn_blocking`.
- Streaming bounded-concurrency over large input collections with `futures::stream::buffer_unordered` + `Semaphore`.
- Migrating from `async-std` or `smol` to Tokio for ecosystem compatibility.

## When NOT to use
- Single-thread CPU work — async adds no benefit and obscures stacks; use sync code.
- Embedded / `no_std` — pick `embassy` instead.
- Library code that should be runtime-agnostic — depend on `futures`, not `tokio`, and let callers pick.
- Hard real-time scheduling — Tokio's scheduler is best-effort, not deadline-driven.
- Pure FFI / blocking C — wrap once with `spawn_blocking` and treat the rest as sync.

## Where it fails / limitations
- Holding a `MutexGuard` across `.await` deadlocks the executor; use `tokio::sync::Mutex` only when needed, prefer message passing.
- `spawn_blocking` has a default capacity of 512 threads; flooding it causes queueing not parallelism.
- `tokio::select!` cancels the losing future at any await point — partial work and dropped resources surface as subtle bugs.
- `Semaphore::acquire` returns a permit tied to a lifetime; agents often `unwrap` it and lose the cancellation propagation.
- `JoinHandle` errors come in two flavors (panic vs cancellation); ignoring `.await??` swallows panics silently.
- `try_join!` cancels siblings on first error — fine for "all or none", wrong when partial results are valuable.
- Buffered streams (`buffer_unordered(N)`) can starve fairness when one item takes 100x longer; consider `buffered`.

## Agentic workflow
The agent should (1) classify the workload (parallelizable independent IO vs sequential dependency vs CPU-bound vs blocking-IO), (2) pick the primitive (`try_join!`, `join_all`, `buffer_unordered`, `spawn_blocking`, `JoinSet`), (3) implement with explicit concurrency bound, structured error type, and cancellation safety, (4) add a test that exercises a panic and an early-error path. Force `cargo clippy -- -D warnings` (catches `MutexGuard` across await via `clippy::await_holding_lock`) and `cargo test` with `--features tokio/test-util` for time control. For services using sqlx/sea-orm, agent must read the existing `Database` struct first — wrapping pooled queries in extra `spawn` is a common anti-pattern.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the change as an SDD task; gates: `cargo clippy -- -D warnings`, `cargo nextest run`, `cargo test --doc`.
- A general implementer (Sonnet) for boilerplate; an architect (Opus) to choose between `tokio::spawn` (independent task) and `JoinSet` (managed group) and to design `AppError` cancellation behavior.

### Prompt pattern
```
Implement <fn> in src/services/<x>.rs. Inputs: <type>, expected size: <N>, latency: <ms>,
each item is independent and IO-bound (HTTP/DB). Use futures::stream::buffer_unordered
with tokio::sync::Semaphore at concurrency=<C>. Errors: short-circuit via try_join /
collect into Vec<Result<_>>? Pick one and justify. Cover panic in a worker with a test.
```

```
Audit this async code for: MutexGuard held across .await, missing spawn_blocking on
CPU-heavy ops (argon2/compress/regex), unbounded spawn, JoinHandle errors swallowed,
and use of std::sync::Mutex inside async. List file:line for each.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo nextest` | Faster test runner; better async output | https://nexte.st |
| `cargo flamegraph` | Async-aware flamegraphs (with `--cfg=tokio_unstable` + tokio-console) | https://github.com/flamegraph-rs/flamegraph |
| `tokio-console` | Live view of tasks, polls, blocked time | https://github.com/tokio-rs/console |
| `cargo-llvm-cov` | Coverage for async code | https://github.com/taiki-e/cargo-llvm-cov |
| `clippy` | `await_holding_lock`, `unused_async`, etc. | rustup component |
| `loom` | Permutation-test of concurrent code | https://github.com/tokio-rs/loom |
| `criterion` | Benchmarks for async fns | https://bheisler.github.io/criterion.rs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokio Console | OSS | Yes | Attach via `RUSTFLAGS="--cfg tokio_unstable"`; agent can read its output. |
| OpenTelemetry Rust | OSS | Yes | `tracing-opentelemetry` propagates spans across `.await`. |
| Datadog APM | SaaS | Indirect | Via OTel exporter. |
| Sentry | SaaS | Yes | `sentry-tracing` ships panic capture for tasks. |
| Tokio (rt + macros features) | OSS | — | The runtime; pin features deliberately. |
| sqlx Pool | OSS | Yes | Don't wrap pool calls in extra `spawn`. |

## Templates & scripts
See `templates.md`. Inline bounded-parallel template (the canonical pattern):

```rust
use futures::{stream, StreamExt, TryStreamExt};
use std::sync::Arc;
use tokio::sync::Semaphore;

pub async fn map_concurrent<T, R, E, F, Fut>(
    items: Vec<T>, concurrency: usize, f: F,
) -> Result<Vec<R>, E>
where
    T: Send + 'static,
    F: Fn(T) -> Fut + Send + Sync + 'static,
    Fut: std::future::Future<Output = Result<R, E>> + Send,
    R: Send + 'static,
    E: Send + 'static,
{
    let sem = Arc::new(Semaphore::new(concurrency));
    let f = Arc::new(f);
    stream::iter(items)
        .map(|item| {
            let sem = sem.clone();
            let f = f.clone();
            async move {
                let _permit = sem.acquire_owned().await.expect("sem closed");
                f(item).await
            }
        })
        .buffer_unordered(concurrency)
        .try_collect()
        .await
}
```

## Best practices
- Never hold `std::sync::Mutex` across `.await`; either drop the guard before awaiting or switch to `tokio::sync::Mutex`.
- Always bound concurrency with `Semaphore` or `buffer_unordered(N)`; unbounded `join_all` will overload pools and remote services.
- Wrap CPU-heavy operations in `tokio::task::spawn_blocking` and `await??` (joins panic propagation + inner Result).
- Prefer `JoinSet` over `Vec<JoinHandle<T>>` for dynamic groups — it gives drop-time cancellation and ordered consumption.
- Use `tokio::time::timeout` on every external IO call; default-no-timeout is the most common production incident.
- Propagate `tracing::Span::current()` into spawned tasks via `.instrument(span.clone())` so traces survive `tokio::spawn`.
- Configure runtime threads explicitly in `main.rs` (`#[tokio::main(flavor = "multi_thread", worker_threads = N)]`) for predictable benchmarks.
- For sqlx, rely on the pool — do not `spawn` per-query; it doubles the scheduling cost.

## AI-agent gotchas
- `tokio::spawn` requires `Send + 'static`. Agents trying to capture `&Database` will get cryptic errors and respond by adding `Arc::new` everywhere — review for over-Arc'd state.
- `spawn_blocking` closure captures must be owned; LLMs forget to clone `String` and emit confusing lifetime errors.
- `tokio::select!` on a non-cancellation-safe future (e.g., `tokio::io::AsyncReadExt::read_to_end`) drops partial state on the loser branch — silent data loss. Require a comment per branch documenting cancel-safety.
- LLMs use `futures::executor::block_on` inside async to "fix" lifetime issues — this deadlocks the runtime. Forbid it explicitly.
- Mixing `async-std::task::spawn` and `tokio::spawn` from outdated examples is a common cross-runtime bug; pin Tokio in the prompt.
- Agents instinctively wrap `Mutex<T>` around sqlx pools or reqwest clients — both are already Send/Sync. Reject any such wrapper.
- Human-in-loop checkpoint: review changes to runtime config (`worker_threads`, `max_blocking_threads`); they have global effects.
- Generated tests rarely cover panic-in-task — require a `#[tokio::test]` that asserts `.await??` returns `JoinError::is_panic()`.

## References
- Tokio tutorial: https://tokio.rs/tokio/tutorial
- Tokio docs: https://docs.rs/tokio
- futures crate: https://docs.rs/futures
- Tokio Console: https://github.com/tokio-rs/console
- Async Rust book (Programming Rust, Blandy/Orendorff/Tindall, ch. 20)
- Alice Ryhl — "Actors with Tokio": https://ryhl.io/blog/actors-with-tokio/
- Withoutboats — "Async cancellation": https://without.boats/blog/poll-next/
