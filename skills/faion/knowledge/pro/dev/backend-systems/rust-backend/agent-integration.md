# Agent Integration — Rust Backend (Axum/Actix)

## When to use
- Greenfield Rust HTTP service that needs project layout + handler + service + DB + tests in one shot.
- Migrating a Python/Node service to Rust for tail-latency or memory reasons; need a faithful 1:1 port skeleton.
- Standardizing several Rust services on one shape: same `AppError`, same handler/service/db split, same test scaffolding.
- Onboarding new contributors who must produce a working CRUD slice without learning Tokio/Axum trivia first.
- Pair-programming with an LLM that needs a complete, opinionated stack to avoid wandering.

## When NOT to use
- Library crates (no HTTP) — only the project-structure portion applies.
- Cross-runtime libraries — drop Tokio specifics.
- Embedded/no_std — pick `embassy` and discard this entirely.
- Lambda/Cloud-Functions style — `lambda_runtime` plus a minimal handler is leaner than the layout shown.
- gRPC-only services — use `tonic`, the handler shape differs, although service/db split still applies.

## Where it fails / limitations
- The bundled methodology covers Axum primarily; Actix-web equivalents exist but aren't shown side-by-side and confuse mixed teams.
- `UserService<'a>` borrowing a `&Database` works in tests with mocks but fights `tokio::spawn`'s `'static` requirement once you add background jobs.
- Mocking via `mockall` for the `Database` struct breaks when `sqlx::query!` macros are used — those need a real connection at compile time.
- `IntoResponse` for `AppError` must enumerate every variant; missing one returns a default 500 with empty body.
- Validator-derived errors don't auto-convert to RFC 7807; the integration is left to the user.
- Integration test scaffolding (`tests/api_tests.rs`) needs a per-test database — the `setup_app().await` is `todo!()`; agents tend to leave it stubbed.

## Agentic workflow
The agent should drive a vertical slice: pick the entity, generate `models/<x>.rs`, `db/<x>.rs`, `services/<x>.rs`, `handlers/<x>.rs`, `routes/<x>.rs`, and integration tests in one PR. Always start by reading `Cargo.toml`, `error.rs`, and `AppState` to keep types consistent. After implementation, run `cargo fmt`, `cargo clippy --all-targets -- -D warnings`, `cargo nextest run`, and a smoke-test `curl` against the new endpoint via `cargo run` in a sandbox. For a brand-new repo, the agent should bootstrap the layout (see `rust-project-structure/agent-integration.md`) before generating the first slice. Schema/DB changes ride along but should land as a separate commit when reasonable.

### Recommended subagents
- `faion-sdd-executor-agent` — wraps the slice as an SDD task; gates: clippy, nextest, integration test pass, `sqlx prepare` if used.
- An architect (Opus) for `AppError` extension, `AppState` shape, and trait-vs-struct decision on `UserService`.
- An implementer (Sonnet) for boilerplate per file.
- `password-scrubber-agent` — review responses for leaked DB error strings.

### Prompt pattern
```
Add a CRUD vertical slice for <entity> across models/db/services/handlers/routes,
matching the patterns in skills/faion/knowledge/pro/dev/backend-systems/rust-backend/README.md.
Use existing AppState, AppError, Database. Validate input with `validator`. Map errors to
RFC 7807 in IntoResponse for AppError. Add unit tests (mockall) and integration tests
(tests/<entity>_tests.rs). Stop when `cargo nextest run` is green.
```

```
Audit this rust-backend slice for: missing IntoResponse arms, password handling not on
spawn_blocking, bind error swallowed, unbounded JOIN in db query, missing context propagation
for tracing, and absence of timeout on outbound HTTP. Output file:line.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo` | Build/test/run | https://doc.rust-lang.org/cargo/ |
| `cargo nextest` | Faster, parallel test runner | https://nexte.st |
| `cargo watch` | Recompile on change | `cargo install cargo-watch` |
| `cargo clippy` | Lint | rustup component |
| `cargo fmt` | Format | rustup component |
| `cargo audit` | RustSec advisories | https://github.com/rustsec/rustsec |
| `sqlx-cli` | Migrations + query check | https://github.com/launchbadge/sqlx |
| `cargo expand` | See macro expansions when debugging derives | https://github.com/dtolnay/cargo-expand |
| `tokio-console` | Live runtime view | https://github.com/tokio-rs/console |
| `bunyan` / `bat` | Pretty-print structured logs from `tracing-bunyan-formatter` | https://github.com/LukeMathWalker/bunyan |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Shuttle | SaaS PaaS | Yes (CLI) | Deploys Axum/Actix with minimal config; ideal for agent-driven prototypes. |
| Fly.io | SaaS PaaS | Yes (`flyctl`) | Distroless container builds nicely from this layout. |
| Railway | SaaS | Yes (CLI) | Detects Rust automatically. |
| Supabase / Neon | SaaS PG | Yes | Pairs with `sqlx` + `DATABASE_URL`. |
| Sentry | SaaS | Yes | `sentry`/`sentry-tower` plug into the layout. |
| Honeycomb / Datadog | SaaS | Yes | `tracing-opentelemetry` exporter. |
| crates.io | OSS | Yes | Resolve deps; pin to compatible Axum version. |

## Templates & scripts
See `templates.md` for full Axum + sqlx templates. Inline `AppError` skeleton agents can extend:

```rust
use axum::{http::StatusCode, response::{IntoResponse, Response}, Json};
use serde::Serialize;

#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("not found: {0}")]    NotFound(String),
    #[error("conflict: {0}")]     Conflict(String),
    #[error("validation: {0}")]   Validation(String),
    #[error("unauthorized")]      Unauthorized,
    #[error(transparent)]         Db(#[from] sqlx::Error),
    #[error(transparent)]         Join(#[from] tokio::task::JoinError),
}

#[derive(Serialize)]
struct Problem<'a> { #[serde(rename="type")] ty: &'a str, title: &'a str, status: u16, detail: String }

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, ty, title) = match &self {
            AppError::NotFound(_)     => (StatusCode::NOT_FOUND,           "/errors/not-found",     "Not Found"),
            AppError::Conflict(_)     => (StatusCode::CONFLICT,            "/errors/conflict",      "Conflict"),
            AppError::Validation(_)   => (StatusCode::BAD_REQUEST,         "/errors/validation",    "Validation Error"),
            AppError::Unauthorized    => (StatusCode::UNAUTHORIZED,        "/errors/unauthorized",  "Unauthorized"),
            AppError::Db(_) | AppError::Join(_) =>
                                         (StatusCode::INTERNAL_SERVER_ERROR,"/errors/internal",     "Internal Error"),
        };
        tracing::error!(error = %self, "request failed");
        (status, Json(Problem { ty, title, status: status.as_u16(), detail: self.to_string() })).into_response()
    }
}
```

## Best practices
- One `AppError` enum per service; never use `anyhow::Error` at API boundaries.
- `#[tokio::main]` only in `main.rs`; library code stays runtime-agnostic where possible.
- Keep `AppState` cheap to clone (wrap heavy fields in `Arc`); Axum clones it per request.
- Pass `&AppState` extractors, not individual sub-fields, to avoid signature churn.
- Use `tracing::instrument` on every handler and service method with `skip(state, password)`.
- Run integration tests with a real PG via `testcontainers` or a transactional rollback wrapper to avoid pollution.
- `sqlx prepare` and check in `.sqlx/` so CI builds without `DATABASE_URL`.
- Pin minor versions of Axum/sqlx/tokio in `Cargo.toml`; commit `Cargo.lock` for binaries.
- Layer middleware in this order, outer→inner: `TraceLayer`, request-id, CORS, auth, rate-limit, app router.

## AI-agent gotchas
- Axum 0.6 vs 0.7: handler signatures and state extraction changed (`Router::with_state`); LLMs blend the two. Read `Cargo.toml` first.
- Agents copy lifetime annotations (`UserService<'a>`) blindly; this fails as soon as you `tokio::spawn` the service. Prefer `Arc<Database>` ownership.
- `mockall` cannot mock structs whose methods use `sqlx::query!`-macro return types — the macros embed file paths. Use a trait abstraction the agent must derive.
- LLMs forget to add `IntoResponse` for new `AppError` variants; the build still passes (default impl unreachable) but runtime panics. Require a `match` on every variant.
- Password hashing (Argon2/bcrypt) must run via `spawn_blocking`; agents inline it in async fns and starve the runtime.
- Validator integration leaks the entire `ValidationErrors` debug string in responses; require explicit per-field mapping to `errors[]`.
- Tests with `oneshot(...).await` consume the router; agents try to send a second request to the same instance and get cryptic errors. Use `tower::ServiceExt::clone()` or a fresh app per case.
- Human-in-loop checkpoint: review `IntoResponse` mapping changes; an accidentally-changed status code is a silent contract break.
- `sqlx::Pool` cloning is cheap but spawning per-request `Pool::connect` is catastrophic; agents do this when "fixing" Send issues.
- Generated integration tests use `setup_app().await` as `todo!()` — must be filled with a real test container or migration runner.

## References
- Axum: https://docs.rs/axum
- Actix-web: https://actix.rs/docs/
- sqlx: https://github.com/launchbadge/sqlx
- tokio: https://tokio.rs/tokio/tutorial
- tracing: https://docs.rs/tracing
- Zero To Production In Rust: https://www.zero2prod.com/
- Axum examples: https://github.com/tokio-rs/axum/tree/main/examples
- testcontainers-rs: https://github.com/testcontainers/testcontainers-rs
