# Agent Integration — Tokio Async Patterns

## When to use
- Building Rust services that need to multiplex thousands of network connections (HTTP, gRPC, WebSocket, MQTT) on a small thread pool.
- Replacing a thread-per-request worker with a structured concurrency model (`tokio::spawn`, `JoinSet`, `select!`).
- Wrapping CPU-bound work in `spawn_blocking` so it does not stall the runtime.
- Adding cancellation, timeouts, and graceful shutdown to long-running tasks.
- Implementing fan-out / fan-in pipelines with channels (`mpsc`, `broadcast`, `watch`).

## When NOT to use
- A simple CLI that does one thing and exits — `std::thread` or sync code is shorter and clearer.
- Heavy CPU-bound workloads (image transforms, ML inference) — Rayon / dedicated thread pools are better; tokio is for I/O.
- Embedded / `no_std` targets — Tokio assumes an allocator and OS threads. Use `embassy` instead.
- Very low-latency single-shot RPC where the runtime overhead matters; consider `glommio` or `monoio` (thread-per-core) for `io_uring` workloads.
- When the team is new to Rust — async + lifetimes + `Send`/`Sync` is the steepest cliff in the language.

## Where it fails / limitations
- Holding a `MutexGuard` across `.await` deadlocks tasks scheduled onto the same worker; clippy's `await_holding_lock` catches some, not all.
- Forgetting `Send` bounds on spawned tasks: `Rc`, `RefCell`, raw pointers, non-`Send` futures break compile, but trait objects (`Box<dyn Future>`) often hide it.
- `async fn` in traits requires Rust 1.75+ and still has variance/`Send` quirks — the `async-trait` macro has a `Box<dyn>` cost.
- Cancellation drops the future at any `.await` point — partial state is the caller's problem (use `tokio::select!` cancel branches consciously).
- `block_on` inside an async context panics with cryptic "cannot block from within a runtime"; agents writing tests sometimes paper over this with nested runtimes.
- `tokio::spawn` returns a `JoinHandle` that must be awaited or aborted; orphaned handles silently leak memory and tasks.

## Agentic workflow
Have the agent generate the typed service skeleton (`pub struct UserService<'a>`, methods returning `Result<_, AppError>`), then a second pass to add `try_join!` / `JoinSet` for fan-out. A reviewer agent runs `cargo clippy -- -W clippy::pedantic -W clippy::await_holding_lock -W clippy::unused_async` and reports back. `cargo nextest` for fast test feedback; `tokio-console` to verify no task is stuck. For any concurrent code path, require a `loom`-tested invariant if shared mutable state is involved.

### Recommended subagents
- `faion-sdd-executor-agent` — sequential service-method-by-service-method implementation with quality gates.
- `simplify` skill — reduce over-spawned tasks; agents tend to `tokio::spawn` everything.
- A custom `rust-clippy-reviewer` agent that runs `cargo clippy --all-targets -- -D warnings` and proposes fixes.

### Prompt pattern
```
Implement <method> on <Service>.
Constraints:
- async fn signature, returns Result<T, AppError>.
- Run independent DB calls in tokio::try_join! when there are >=2.
- CPU-bound work (>1ms) in spawn_blocking.
- No MutexGuard held across .await — use parking_lot::Mutex only inside sync blocks.
- Add a unit test using #[tokio::test(flavor = "multi_thread")].
Output: code + test + a 1-line note on cancellation safety.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| cargo + rustup | Toolchain | rustup.rs |
| cargo-nextest | Faster, parallel test runner | `cargo install cargo-nextest` |
| cargo-watch | Re-run on file change | `cargo install cargo-watch` |
| cargo-expand | Expand `#[tokio::main]` and async-trait macros | `cargo install cargo-expand` |
| tokio-console | Live task / resource inspector (like `top` for tasks) | `cargo install tokio-console` + `console-subscriber` crate |
| clippy | Async-aware lints (`await_holding_lock`, `unused_async`) | `rustup component add clippy` |
| miri | UB detector for unsafe + concurrency | `rustup +nightly component add miri` |
| loom | Permutation testing for concurrent code | crate, used in `#[cfg(loom)] mod tests` |
| cargo-flamegraph | Profile async stacks | `cargo install flamegraph` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokio runtime | OSS | Yes | The runtime; pick `multi_thread` (default) or `current_thread` for single-core. |
| Axum / Actix / Tonic | OSS | Yes — typed builders | All built on Tokio; pick Axum for ergonomic typed extractors. |
| Sentry, Honeycomb, Grafana Tempo | SaaS | Yes — `tracing-opentelemetry` | Async traces propagate via `Span` if you instrument every `.await` boundary. |
| Tokio Console (server crate) | OSS | Yes | Embed `console-subscriber` in dev; agent can `tokio-console http://...` to inspect. |
| flamegraph.com / Pyroscope | SaaS | Yes | Continuous profiling for async stacks. |
| `loco-rs` | OSS | Yes | Rails-like Tokio framework; opinionated default project layout. |

## Templates & scripts
See `templates.md` and `examples.md` for full service layouts. Quick "is this future cancel-safe?" checklist used by the reviewer agent:

```rust
// scripts/cancel_safety.rs (notes, not runnable)
// 1. Does the future hold any external resource (lock, DB tx, file fd) across .await?
//    -> NOT cancel-safe; use a guard pattern that commits on Drop, or wrap in tokio::spawn + abort handle.
// 2. Does it write to disk midway through a multi-step write?
//    -> wrap in tokio::fs::OpenOptions + write to .tmp + rename on success.
// 3. Is it inside a tokio::select!?
//    -> only cancel-safe primitives (recv, sleep, AsyncRead) belong on a select branch.
```

## Best practices
- Default to `tokio::main(flavor = "multi_thread")`; switch to `current_thread` only for single-core embedded or to debug Send issues.
- Use `parking_lot::Mutex` for short critical sections, `tokio::sync::Mutex` only when you actually need to hold across `.await`.
- Channels: `mpsc` for work queues, `broadcast` for fan-out events, `watch` for "latest value" (e.g., config reload), `oneshot` for request/response.
- Always pair `tokio::spawn` with either `JoinHandle::await` or `tokio_util::task::AbortOnDropHandle` to avoid leaks.
- Wrap blocking syscalls (`std::fs`, `reqwest::blocking`, image processing) in `spawn_blocking`; never call them from a hot async path.
- Use `tracing` + `#[instrument]` on every public async fn; without it, async stack traces are useless.
- For graceful shutdown: signal via `tokio::sync::watch::channel(false)`, hand the receiver to every spawned task, await `JoinSet` on shutdown.

## AI-agent gotchas
- LLMs love `tokio::spawn` everywhere; the result is unstructured concurrency with no error propagation. Prefer `try_join!` / `JoinSet` and only `spawn` for true fire-and-forget background tasks.
- Agents will use `std::sync::Mutex` because that's what comes from training data; on the first `.await` while holding it, the task deadlocks itself. Force `parking_lot` or `tokio::sync::Mutex` in the prompt.
- "Add a timeout" usually becomes `tokio::time::timeout(Duration::from_secs(30), fut).await??;` which double-`?`s a `Result<Result<T, E>, Elapsed>` — agent must handle both layers.
- `async fn` in traits without `#[async_trait]` (or Rust ≥1.75 + `Send` bound) silently produces non-`Send` futures; spawn fails compile with a wall of trait-bound errors.
- `select!` branches that aren't cancel-safe (e.g., `db.transaction().begin()`) corrupt state on the unselected branch. Lock down which futures are allowed.
- LLM-written tests often use `#[tokio::test]` (single-thread) and then call `spawn_blocking` — passes, but doesn't reflect prod multi-thread runtime. Pin `flavor = "multi_thread"` in test attributes.
- Human-in-loop checkpoint: any change to runtime config (`flavor`, `worker_threads`, `block_on`) requires reviewer sign-off; perf and correctness traps live there.

## References
- Tokio Tutorial — https://tokio.rs/tokio/tutorial
- Tokio API — https://docs.rs/tokio
- Async Book — https://rust-lang.github.io/async-book/
- "What color is your function" (Tokio talk) — https://tokio.rs/blog/2020-04-preemption
- Cancellation safety — https://docs.rs/tokio/latest/tokio/macro.select.html#cancellation-safety
- tokio-console — https://github.com/tokio-rs/console
- loom — https://github.com/tokio-rs/loom
