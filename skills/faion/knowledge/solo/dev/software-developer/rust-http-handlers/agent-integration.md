# Agent Integration — Rust HTTP Handlers

## When to use
- Building a Rust web service on `axum` (or `actix-web` / `rocket` / `poem`) and you need a consistent handler shape.
- Migrating a single hot endpoint from a slower stack (Python/Node) into Rust for latency or memory wins.
- Greenfield CLI/edge service where Rust's correctness pays off (auth gateway, image proxy, websocket fan-out).
- Systems where you already use `sqlx` / `sea-orm` / `diesel` and want type-safe handlers wired to the DB.
- Wasm-edge handlers (Cloudflare Workers via `worker` crate, Fastly Compute, Spin) — same handler discipline applies.

## When NOT to use
- Prototype CRUD where iteration speed > latency — Python/TS will ship 5x faster.
- Heavy ORM-y workloads with rapidly evolving schemas — `sqlx` `query!` macros require migrations to compile.
- Plugins / scripting hooks where dynamic dispatch is the requirement.
- Polyglot services where the team has zero Rust experience — operational cost dominates.

## Where it fails / limitations
- Compile times balloon as the handler tree + extractors grow; cold builds in CI hit minutes without `sccache`/`mold`.
- `axum` extractor errors are confusing for beginners ("trait `Handler<...>` not implemented") — agents often guess wrongly at the missing bound.
- `State<T>` requires `T: Clone + Send + Sync + 'static`; sharing a non-`Clone` resource (e.g. raw `tokio::sync::Mutex<DB>`) fights the type system.
- Validator errors (`validator` crate) don't auto-convert to your `AppError`; you need a `From` impl.
- Error type design churn: `thiserror` vs `anyhow` vs custom `AppError` causes endless refactors.
- Async cancellation: dropping a future mid-await can leave DB transactions hanging — agents don't think about this.
- File uploads with `multipart`: streaming, size limits, and timeouts are easy to misconfigure.
- WebSockets / SSE require very different patterns; the README only covers JSON.

## Agentic workflow
A planner subagent reads an OpenAPI spec or feature doc and lists the handlers to add (path, method, extractors, response, errors). An implementer subagent writes the handler + DTOs (`*Request` / `*Response`) + a `From<Model> for Response` impl + the route registration. A test subagent generates `tower::ServiceExt::oneshot` integration tests against an in-memory app + test DB. A reviewer subagent runs `cargo clippy --all-targets -- -D warnings`, `cargo machete` (unused deps), and `cargo audit`.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → handler → tests → review.
- A user-defined `clippy-fixer` (model: haiku) — runs `cargo clippy --fix --allow-dirty` and reports remaining warnings.
- A user-defined `axum-extractor-doctor` (model: sonnet) — when a `Handler` trait error appears, identifies which extractor is misconfigured.
- `password-scrubber-agent` — sweep test fixtures for tokens.

### Prompt pattern
- "Read `rust-http-handlers/README.md`. Implement `POST /v1/orders` on axum 0.7. Inputs: `CreateOrderRequest` (validated). Outputs: `201 Created` with `OrderResponse`. Errors map to `AppError`. Use `State<AppState>` for DB. Add a `tower::ServiceExt::oneshot` test that asserts both the happy path and a 422 on a validation failure. Output unified diff."
- "Audit `src/handlers/` against `rust-http-handlers/README.md`. Flag handlers that: take `&AppState` instead of `State(state)`; return `Result<_, anyhow::Error>` instead of `AppError`; mutate state without `Arc<Mutex<_>>` or a transactional boundary; lack OpenAPI annotations (`utoipa`)."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo-watch` | Reload on save | `cargo install cargo-watch` |
| `cargo-nextest` | Faster, friendlier test runner | `cargo install cargo-nextest` |
| `cargo-machete` | Find unused deps | `cargo install cargo-machete` |
| `cargo-deny` | License + advisory + duplicate dep policy | `cargo install cargo-deny` |
| `cargo-audit` | Known CVEs in deps | `cargo install cargo-audit` |
| `sccache` / `mold` | Speed up cold builds | `cargo install sccache`, `apt install mold` |
| `bacon` | Background continuous build/check | `cargo install bacon` |
| `httpie` / `xh` | Manual handler probes | `pipx install httpie`, `cargo install xh` |
| `wrk` / `oha` / `bombardier` | Load tests | `cargo install oha` |
| `cargo-llvm-cov` | Coverage | `cargo install cargo-llvm-cov` |
| `cargo-mutants` | Mutation testing | `cargo install cargo-mutants` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| `axum` (tokio) | OSS | Yes | The pragmatic default; the README targets it. |
| `actix-web` | OSS | Yes | Higher raw perf; ergonomics differ. |
| `rocket` | OSS | Partial | Macros-heavy; LLMs wobble. |
| `poem` / `loco` | OSS | Yes | `loco` mimics Rails — good for solo CRUD. |
| `utoipa` / `aide` | OSS | Yes | Generate OpenAPI from handler signatures (pair with `openapi-specification`). |
| Cloudflare Workers (`worker` crate) | SaaS | Yes | Rust → Wasm; some axum patterns don't apply. |
| Fastly Compute | SaaS | Yes | Similar Wasm constraints. |
| Shuttle.dev | SaaS | Yes | Push-to-deploy Rust services; great for solo. |
| Fly.io / Railway / Render | SaaS | Yes | Standard container deploy targets. |

## Templates & scripts
See `templates.md`. Minimal `axum` + integration-test skeleton an agent should reach for:

```rust
// tests/users_handler.rs
use axum::body::Body;
use axum::http::{Request, StatusCode};
use http_body_util::BodyExt;
use serde_json::json;
use tower::ServiceExt;
use myapp::app;            // pub fn app(state: AppState) -> axum::Router
use myapp::test_state;     // helper -> AppState backed by sqlx test pool

#[tokio::test]
async fn create_user_201() {
    let state = test_state().await;
    let resp = app(state).oneshot(
        Request::builder()
            .method("POST")
            .uri("/v1/users")
            .header("content-type", "application/json")
            .body(Body::from(json!({
                "name": "Ada",
                "email": "ada@example.com",
                "password": "averyl0ngpassword"
            }).to_string()))
            .unwrap()
    ).await.unwrap();

    assert_eq!(resp.status(), StatusCode::CREATED);
    let bytes = resp.into_body().collect().await.unwrap().to_bytes();
    let v: serde_json::Value = serde_json::from_slice(&bytes).unwrap();
    assert_eq!(v["email"], "ada@example.com");
}
```

## Best practices
- Define one `AppError` enum with `thiserror`; impl `IntoResponse` once; never let handlers return `anyhow::Error` to clients.
- Keep handlers thin — call into a `Service` struct (`UserService::new(&state.db).create(...)`); handlers only translate IO ↔ domain.
- Validate input in DTOs with `validator` (or `garde`); call `.validate()?` first thing; map errors via `From<ValidationErrors> for AppError`.
- Use `Arc<sqlx::PgPool>` (it's cheap to clone) inside `AppState`; don't wrap in extra `Mutex`.
- For long-running handlers, set a `tower::timeout::TimeoutLayer` and a global concurrency limit; don't rely on the runtime to bound work.
- Always log with `tracing` + `tracing-subscriber`; instrument handlers with `#[tracing::instrument]`; carry `request_id` extractor.
- Use `axum::extract::State` (typed) — never grab globals from `lazy_static!` in handlers.
- For OpenAPI, prefer `aide` or `utoipa` to keep spec + handler in sync; commit the generated spec.
- Bound JSON body size with `Json::<T>::from_request` + `RequestBodyLimitLayer`; otherwise OOM is one curl away.
- `Result<(StatusCode, Json<T>), AppError>` is a clearer return type than naked `Json<T>` when the success status varies (201 vs 200).
- For DB transactions, write `Service` methods that take `&mut sqlx::Transaction<'_, Postgres>`; the handler `.commit()` after success.
- Run `cargo clippy --all-targets --all-features -- -D warnings -W clippy::pedantic` in CI; fail builds.

## AI-agent gotchas
- LLMs frequently confuse axum 0.6 vs 0.7 APIs (`Router::with_state` arrived in 0.7; `axum::Server::bind` is gone in 0.7+). Pin the major version in the prompt.
- Extractors must be in the right order: `State` → path/query → `Json` body. LLMs scramble the order, leading to opaque trait errors.
- `Handler` trait errors look like "the trait bound … is not satisfied" — agents often respond by adding random `where` clauses; the real fix is usually a missing extractor `Send`/`Sync` or a non-`Clone` `State`.
- Agents emit `unwrap()` / `expect()` in handler bodies — every one is a 500. Force `?` + `AppError`.
- LLMs forget `tower::ServiceBuilder` middleware ordering — outer-most layer runs first; misordered tracing/timeout/auth = wrong logs and missed timeouts.
- `validator` errors don't go to JSON automatically. Without a `From<ValidationErrors>` impl, agents commit code that returns 500 instead of 422.
- For `sqlx` macros (`query!`, `query_as!`), agents forget to set `DATABASE_URL` or `SQLX_OFFLINE=true` + `cargo sqlx prepare` — CI breaks.
- Async-cancellation safety: an agent will write `let row = sqlx::query!(…).execute(&mut tx).await?; do_io().await?;` — if the client disconnects mid-`do_io`, the transaction is dropped without commit. Mention cancellation explicitly.
- Compile-times: agents add monomorphization-heavy crates (`serde_with` everywhere, generic-soup) without warning. Watch incremental compile time and call them out.
- Human-in-loop checkpoint: changes to `AppError`, middleware order, or `Router::with_state` boundaries should be reviewed manually — small mistakes here ripple to every handler.
- Wasm targets (Workers/Compute): `tokio` doesn't apply; agents copy axum patterns that don't compile to Wasm. Tell the agent the target up-front.

## References
- axum docs — https://docs.rs/axum/latest/axum/
- The Rust async book — https://rust-lang.github.io/async-book/
- `tracing` — https://docs.rs/tracing/latest/tracing/
- `validator` — https://docs.rs/validator/latest/validator/
- `sqlx` — https://docs.rs/sqlx/latest/sqlx/
- `utoipa` — https://github.com/juhaku/utoipa
- `aide` — https://github.com/tamasfe/aide
- Tokio cancellation — https://tokio.rs/tokio/topics/shutdown
- `tower-http` middleware — https://docs.rs/tower-http/latest/tower_http/
