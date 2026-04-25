# Agent Integration — Rust Backend

## When to use
- New service where p99 latency, memory footprint, or CPU efficiency dominate (proxies, edge functions, real-time pipelines).
- Replacing a hot service in another language because GC pauses, FFI overhead, or per-instance cost is unacceptable.
- Long-running daemons / agents where memory safety + zero-runtime is desirable (no JVM, no Node).
- Embedding into existing Rust ecosystem (sqlx, tower, hyper, tonic) and benefiting from the type system end-to-end.
- Building a binary that must ship as a single file with no runtime dependencies (CLI tools, sidecars).

## When NOT to use
- CRUD service with low traffic where Django/Rails/FastAPI ships in 1/3 the time at 99% the perf.
- Heavily relational app with frequent schema churn — `sqlx::query!` macro requires a live DB at compile time, slows iteration.
- Team without Rust experience and a hard deadline — borrow checker + async traits + lifetimes is months of ramp-up.
- Frontend-heavy backend-for-frontend where Node + tRPC + Prisma is the productive default.
- Plugin systems with dynamic loading — Rust's strict ABI makes this awkward (use WASM/extism or accept the constraint).

## Where it fails / limitations
- Compile times kill iteration loops on cold caches (10–60s incremental, 2–5min cold). `cargo-chef`, `sccache`, and split crates are mandatory.
- `sqlx` offline mode + macros require careful CI cache (`.sqlx/` files) or builds break on every schema change.
- Adding a single feature flag often touches `Cargo.toml`, `lib.rs`, multiple `mod.rs`, and the type signature it changes.
- Error types: `thiserror` + `anyhow` mix often goes wrong; either fully model errors or fully erase, not both halfway.
- Axum vs Actix vs Rocket vs Poem: framework churn is real; pick Axum for ecosystem fit unless there's a specific reason.
- Test fixtures (DB setup/teardown) less ergonomic than Django/Rails; use `sqlx::test` or `testcontainers` and accept slower runs.

## Agentic workflow
Project skeleton first: agent generates the `Cargo.toml` workspace, `src/{config,error,db,services,handlers,routes,middleware}/mod.rs`, and a baseline Axum router with `AppState`. Each feature added via `faion-sdd-executor-agent` in expand-contract style: define DB query (sqlx) → service method → handler → route → integration test. Reviewer agent runs `cargo fmt`, `cargo clippy --all-targets -- -D warnings`, `cargo nextest run`, and `cargo audit`. For DB migrations, separate agent runs `sqlx migrate add` and ensures both up + down scripts. Prefer thin handlers that delegate into services so handlers stay testable without HTTP.

### Recommended subagents
- `faion-sdd-executor-agent` — drives task list per feature with quality gates.
- A custom `rust-clippy-reviewer` (you create) — gating `clippy -D warnings`, `cargo audit`, `cargo machete` (unused deps).
- `simplify` skill — collapse over-abstracted traits and over-spawned tasks (LLMs love generics).

### Prompt pattern
```
Add endpoint <METHOD> <PATH> for <feature>.
Constraints:
- Axum handler: extract via typed extractors (Path, Query, Json, State).
- Delegate all logic to services::<module>::<fn>; handler stays HTTP-only.
- DB via sqlx::query!/query_as! macros; never string-format SQL.
- Return Result<Json<T>, AppError>; AppError implements IntoResponse.
- Add integration test using axum::test or hyper::Client against a tower::Service stack.
- No unwrap()/expect() outside main.rs and tests.
Output: code + test + 1 line on idempotency.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| cargo + rustup | Toolchain | rustup.rs |
| cargo-nextest | Faster test runner | `cargo install cargo-nextest` |
| cargo-watch | Re-run on change | `cargo install cargo-watch` |
| cargo-audit | RustSec advisory check | `cargo install cargo-audit` |
| cargo-deny | Licence + dup + advisory policy | `cargo install cargo-deny` |
| cargo-machete | Detect unused deps | `cargo install cargo-machete` |
| cargo-chef | Cached docker builds | `cargo install cargo-chef` |
| sccache / mold | Build cache + faster linker | `cargo install sccache`; mold via package manager |
| sqlx-cli | Migrations + offline metadata | `cargo install sqlx-cli` |
| diesel_cli / sea-orm-cli | Alternative ORM CLIs | `cargo install` |
| cargo-flamegraph | Profile binaries | `cargo install flamegraph` |
| cargo-llvm-cov | Coverage | `cargo install cargo-llvm-cov` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Axum + tower + hyper | OSS | Yes | Modern default; typed extractors and middleware compose cleanly. |
| Actix-web | OSS | Yes | Mature, very fast, actor-flavoured; less ergonomic typed state. |
| Rocket | OSS | Partial | Macros heavy; ergonomic but slower-evolving. |
| Poem / Loco / Pavex | OSS | Yes | Newer frameworks; Loco is "Rails for Rust". |
| Tonic | OSS | Yes | gRPC over Tokio; protobuf-driven, friendly to codegen agents. |
| sqlx / SeaORM / Diesel | OSS | Yes | Pick sqlx for raw SQL + compile-time check, SeaORM for active-record style, Diesel for full ORM. |
| Shuttle.rs | SaaS | Yes — `cargo shuttle` | Rust-native deploy with infra-from-code; nice for solo. |
| Fly.io / Railway / Render / Lambda | SaaS | Yes | All accept a Docker image; pair with `cargo-chef` for fast CI. |
| Sentry / Honeycomb / Grafana Tempo | SaaS | Yes — `tracing-opentelemetry` | Wire OTel exporters via tracing layer. |
| pganalyze / Datadog | SaaS | Yes | Pairs with sqlx logging. |

## Templates & scripts
See `templates.md` for full Axum/Actix scaffolds. Minimal `AppError` that converts to a clean HTTP response:

```rust
// src/error.rs
use axum::{http::StatusCode, response::{IntoResponse, Response}, Json};
use serde_json::json;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("not found: {0}")]
    NotFound(String),
    #[error("conflict: {0}")]
    Conflict(String),
    #[error("unauthorized")]
    Unauthorized,
    #[error("validation: {0}")]
    Validation(String),
    #[error(transparent)]
    Db(#[from] sqlx::Error),
    #[error(transparent)]
    Other(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, msg) = match &self {
            Self::NotFound(_)    => (StatusCode::NOT_FOUND,        self.to_string()),
            Self::Conflict(_)    => (StatusCode::CONFLICT,         self.to_string()),
            Self::Unauthorized   => (StatusCode::UNAUTHORIZED,     self.to_string()),
            Self::Validation(_)  => (StatusCode::BAD_REQUEST,      self.to_string()),
            _                    => (StatusCode::INTERNAL_SERVER_ERROR, "internal error".into()),
        };
        if status.is_server_error() { tracing::error!(error = ?self, "server error"); }
        (status, Json(json!({"error": msg}))).into_response()
    }
}
```

## Best practices
- One workspace, multiple crates: `app-core`, `app-db`, `app-http`, `app-bin`. Faster compiles, clearer ownership.
- `AppState` is `Clone` (cheap; usually `Arc<...>` inside) — clone freely into handlers.
- Use `sqlx::query!` / `query_as!` macros for compile-time SQL verification; commit `.sqlx/` cache for offline CI.
- Errors: one `AppError` enum with `IntoResponse`; map sqlx + anyhow + domain errors into it. No `unwrap` outside `main.rs`/tests.
- Tracing on every public async fn (`#[instrument]`); structured logs via `tracing-subscriber` JSON formatter in prod.
- Configuration via `figment` or `config-rs` from env + file; never `dotenv` in prod binaries (only dev).
- Migrations only forward; reverts via new "fix-up" migrations, not destructive `down`.
- Use `tower` middleware (`TraceLayer`, `TimeoutLayer`, `CorsLayer`, `RateLimitLayer`); compose, don't reinvent.
- Multi-stage Docker (cargo-chef builder + slim runtime); strip symbols (`strip = "debuginfo"` in profile).

## AI-agent gotchas
- LLMs reach for `unwrap()`/`expect()` everywhere; will turn a 404 into a 500 panic. Force "no unwrap outside `main.rs`/`tests/`" in the prompt and lint with `clippy::unwrap_used`.
- Agents string-concat SQL because `query!` macro errors confuse them; this re-introduces SQL injection. Force `sqlx::query!` macros and reject any string formatting in SQL.
- `async fn` returning a non-`Send` future (e.g., uses `Rc`, holds `RefCell`) — fails to spawn into Tokio. The error trail is long; agents often "fix" by adding `Box::pin` instead of removing the offending non-`Send` value.
- Agents add `tokio::spawn` inside handlers and forget to await; the response returns 200 while the work fails silently. Either inline the work or use a typed background-job system.
- LLMs love generics: `fn handler<T, U, V>(...)` for what should be three concrete types. Hits compile-time blowups; force concrete types unless trait abstraction is justified.
- `From<X> for AppError` is omitted for new error sources, agent then writes `.map_err(|e| AppError::Other(anyhow!(e)))` everywhere. Force adding `#[from]` variants.
- Migrations: agents write data migrations inside the SQL file using `INSERT INTO ... SELECT FROM`; on big tables, this locks the schema. Prefer batched online migration in code.
- Clippy autofix occasionally rewrites `if let Some(x) = ... { ... } else { return ... }` into `?`, changing semantics for non-`Option` types — review clippy diffs.
- Human-in-loop checkpoint: any change to runtime config (`flavor`, `worker_threads`), `unsafe { ... }` blocks, or migration `down` files must require human approval.

## References
- The Rust Book — https://doc.rust-lang.org/book/
- Tokio docs + tutorial — https://tokio.rs/tokio/tutorial
- Axum docs — https://docs.rs/axum
- sqlx README — https://github.com/launchbadge/sqlx
- "Zero to Production in Rust" — Luca Palmieri (Actix-web; principles transfer to Axum).
- tracing — https://docs.rs/tracing
- RustSec Advisory DB — https://rustsec.org/
- cargo-chef — https://github.com/LukeMathWalker/cargo-chef
