# Agent Integration — Rust HTTP Handlers (Axum)

## When to use
- Building Axum (or Actix-web) HTTP services with strongly-typed extractors (`Path`, `Query`, `Json`, `State`).
- Refactoring loosely-typed handlers into the request-DTO + service-call + response-DTO layered pattern.
- Adding `validator`-based request validation, typed error responses via `AppError`, and OpenAPI generation.
- Implementing streaming responses (SSE, WebSocket, chunked) with Tokio + `axum::response::Sse`.
- Wiring middleware: tracing (`tower-http::trace`), CORS (`tower-http::cors`), auth, rate limiting.

## When NOT to use
- High-throughput RPC where Tonic (gRPC) is a better fit than HTTP/JSON.
- Async-light scripts and CLIs — `reqwest` + `tokio` without a server framework is simpler.
- Anywhere a smaller team has more comfort in Go/Python and the perf gain doesn't justify Rust's compile times.
- Frontends serving lots of HTML — Axum is fine, but consider `leptos`/`dioxus`/`maud` ecosystems if rendering dominates.

## Where it fails / limitations
- The README's `update` returns `(StatusCode, Json<UserResponse>)` while `get` returns `Json<UserResponse>` — inconsistent response shapes across handlers; agents copy and mix.
- `payload.validate()?` returns `validator::ValidationErrors` — agents must implement `From<ValidationErrors> for AppError` or compile fails.
- Axum's extractor order matters: body extractors (`Json<T>`) consume the request; placing `Json<T>` before `State` works but `Json<T>` before another body extractor doesn't compile with confusing errors.
- `State<AppState>` requires `AppState: Clone` (cheap clone, e.g. `Arc<Pool>` inside) — agents put non-clone types in state and fight the compiler.
- Lifetimes on `&str` parameters break async — handler params must be owned (`String`) or `'static`.
- Compile times: every extractor add-on bloats build; agents add deps casually and CI feedback loops grow to minutes.

## Agentic workflow
Rust HTTP work succeeds when the agent treats the type system as a contract. One agent designs the request/response DTOs and the `AppError` enum; the second wires extractors and routes; the compiler is the third reviewer (every borrow-checker error is feedback). Use `cargo check` after every edit (10x faster than `cargo build`); only compile + test before commit. Prefer `axum::extract::FromRequestParts` traits for cross-cutting state (auth user, request id) instead of repeating extractor boilerplate in every handler.

### Recommended subagents
- `faion-sdd-executor-agent` — quality gates: `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test --all-features`, optional `cargo deny check`.
- A custom `axum-handler-reviewer` (Opus, read-only) — verifies handlers don't take refs to non-`'static` data, Json-body extractor is last, AppError covers ValidationErrors + sqlx::Error + reqwest::Error, and routes are registered with consistent response shapes.
- `password-scrubber-agent` — JWT secrets / DB URLs in `AppState` initializers must not be hardcoded.

### Prompt pattern
```
Add endpoint <METHOD /path> to module <name>.
Inputs: request DTO with `validator` derives, response DTO.
Output: handler in src/handlers/<name>.rs, route registered in src/router.rs, AppError variants for new failure modes, integration test using axum::Router::oneshot.
Constraints: handler returns Result<Json<Resp>, AppError>; State<AppState> first; Json last; no &str params; no `.unwrap()` outside tests.
After writing, run `cargo fmt`, `cargo clippy --all-targets -- -D warnings`, `cargo test`.
```

```
Review handler diff. Confirm: (1) DTO validator derives present, (2) AppError covers all `?` propagations, (3) extractor order, (4) State is Clone (Arc-wrapped resources), (5) no panics on parse error, (6) consistent response shape (Json or (Status, Json)).
Output JSON of violations.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo` | Build, test, run | https://doc.rust-lang.org/cargo/ |
| `cargo check` | Fast type-check; primary feedback loop | https://doc.rust-lang.org/cargo/commands/cargo-check.html |
| `cargo clippy` | Lints; treat `-D warnings` as default | https://doc.rust-lang.org/clippy/ |
| `cargo fmt` | Format | https://github.com/rust-lang/rustfmt |
| `cargo nextest` | Faster test runner | https://nexte.st/ |
| `cargo deny` | License + advisory checks | https://github.com/EmbarkStudios/cargo-deny |
| `cargo audit` | RustSec vuln scan | https://github.com/rustsec/rustsec |
| `sqlx-cli` | Migrations + offline query check | https://github.com/launchbadge/sqlx |
| `bacon` | Live recompile / test runner | https://github.com/Canop/bacon |
| `tokio-console` | Inspect tokio tasks at runtime | https://github.com/tokio-rs/console |
| `wrk` / `vegeta` / `k6` | Load test | https://k6.io |
| `cargo-flamegraph` | Profile sync hot paths | https://github.com/flamegraph-rs/flamegraph |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Axum | OSS framework | Yes | Largest training corpus among Rust HTTP frameworks. |
| Actix-web | OSS framework | Partial | Different actor model; agents trained on Axum produce mistakes. |
| Tower / tower-http | OSS | Yes | Middleware ecosystem; agents should default to `tower-http` instead of bespoke middleware. |
| utoipa / aide | OSS | Yes | OpenAPI generation from typed handlers; reduces drift. |
| validator | OSS | Yes | Derive macros for input validation; pair with `From<ValidationErrors> for AppError`. |
| sentry-rust | SaaS | Yes | `sentry::capture_error` from `AppError::Internal`. |
| OpenTelemetry (`opentelemetry-otlp` + `tracing-opentelemetry`) | OSS | Yes | Tracing crate integration; `#[tracing::instrument]` on every handler. |
| `axum-extra` | OSS | Yes | Extra extractors (typed headers, cookies, multipart). |
| Datadog Rust APM | SaaS | Partial | Less mature than Go/Python SDKs; OTel is the safer default. |

## Templates & scripts
See `templates.md` and `examples.md` for full handlers + AppError + router scaffolds. Useful re-usable AppError baseline (≤45 lines) the agent should adopt:

```rust
// src/error.rs
use axum::{http::StatusCode, response::{IntoResponse, Response}, Json};
use serde_json::json;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("not found")]
    NotFound,
    #[error("unauthorized")]
    Unauthorized,
    #[error("validation: {0}")]
    Validation(#[from] validator::ValidationErrors),
    #[error("conflict: {0}")]
    Conflict(String),
    #[error("database: {0}")]
    Database(#[from] sqlx::Error),
    #[error("upstream: {0}")]
    Upstream(#[from] reqwest::Error),
    #[error("internal: {0}")]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code) = match &self {
            AppError::NotFound       => (StatusCode::NOT_FOUND,           "NOT_FOUND"),
            AppError::Unauthorized   => (StatusCode::UNAUTHORIZED,        "UNAUTHORIZED"),
            AppError::Validation(_)  => (StatusCode::UNPROCESSABLE_ENTITY,"VALIDATION_ERROR"),
            AppError::Conflict(_)    => (StatusCode::CONFLICT,            "CONFLICT"),
            AppError::Database(_)
            | AppError::Upstream(_)
            | AppError::Internal(_)  => (StatusCode::INTERNAL_SERVER_ERROR,"INTERNAL_ERROR"),
        };
        // Public message hides internal details.
        let msg = match &self {
            AppError::Database(_) | AppError::Upstream(_) | AppError::Internal(_) => "internal error".to_string(),
            other => other.to_string(),
        };
        tracing::error!(error = %self, "request failed");
        (status, Json(json!({ "error": { "code": code, "message": msg } }))).into_response()
    }
}
```

## Best practices
- Use `thiserror` for the error enum, `anyhow::Error` only for the catch-all variant; convert via `From` impls so `?` works everywhere.
- Wrap every handler in `#[tracing::instrument(skip(state), fields(user_id))]`; structured logs become free.
- Keep `AppState` cheaply cloneable: `Arc<DbPool>`, `Arc<HttpClient>`, `Arc<Config>`. Never put `&str` or non-`Send` types.
- Use `axum-extra::TypedHeader` for typed headers (`Authorization`, `Content-Type`) instead of parsing strings.
- Pin tokio + tower + axum in `Cargo.toml`; ecosystem is fast-moving and minor bumps break agent-generated code.
- Test handlers with `Router::oneshot(Request::builder()...)` — fast and hermetic, no network needed.
- Generate OpenAPI from types (utoipa / aide); ship `openapi.json` in CI to detect contract drift.

## AI-agent gotchas
- `unwrap()` and `expect()` look harmless to LLMs trained on examples — block them in prod paths via clippy `-D unwrap_used`.
- `&str` as a handler param doesn't compile (no `'static` lifetime); the agent's first fix is usually wrong (`'a` lifetime parameter that won't satisfy Axum's traits). Force `String`.
- Extractor order errors produce confusing trait-bound messages; if the agent loops on compile errors, hint that body extractors must come last.
- `sqlx::query!` requires DATABASE_URL at compile time or `.sqlx/` offline files. Agents writing CI configs miss the offline step.
- `tracing::info!` without `target =` overflows logs in hot paths; require sampling for high-QPS endpoints.
- Async + `Mutex`: agents reach for `std::sync::Mutex` in async code and create deadlocks. Use `tokio::sync::Mutex` (or `RwLock`) only when needed; prefer message-passing (`mpsc`) when contention is high.
- Human-in-loop checkpoint: any new dep in `Cargo.toml`, any unsafe block, any `tokio::spawn` with unbounded lifetime needs reviewer approval. Compile times and runtime correctness both regress quickly.

## References
- Axum docs — https://docs.rs/axum/latest/axum/
- Axum examples repo — https://github.com/tokio-rs/axum/tree/main/examples
- Tower / tower-http — https://docs.rs/tower-http/latest/tower_http/
- "Zero To Production In Rust" (Pirosanti) — chapters 3-7 cover an Axum-style stack.
- thiserror / anyhow — https://docs.rs/thiserror · https://docs.rs/anyhow
- utoipa OpenAPI — https://github.com/juhaku/utoipa
- aide — https://docs.rs/aide/latest/aide/
- tracing — https://docs.rs/tracing/latest/tracing/
