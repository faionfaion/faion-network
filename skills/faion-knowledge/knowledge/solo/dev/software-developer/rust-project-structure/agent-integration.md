# Agent Integration — Rust Project Structure (Axum/Actix)

## When to use
- Bootstrapping a new Rust HTTP service (Axum, Actix-web, Poem, Salvo) where you want a layered structure: routes → handlers → services → db.
- Migrating a single-file `main.rs` prototype into a module-organized service before it grows past ~1k LOC.
- Multi-crate workspaces where shared domain types live in a library crate and the binary crate wires HTTP.
- Building services that need explicit `AppState` injection for testability (handlers receive `State<AppState>` cleanly).

## When NOT to use
- One-off CLI tools or scripts — `clap` + a flat `src/main.rs` is enough; layered structure is overhead.
- Async libraries (no HTTP server) — drop `routes/`, `handlers/`, keep just `lib.rs` + module tree.
- gRPC-only services — tonic generates server stubs in a different shape; don't force the HTTP-handler layout.
- Rocket / very opinionated frameworks that prescribe their own layout (use the framework's idiom).

## Where it fails / limitations
- `AppState: Clone` requirement — agents add non-Clone fields (e.g., `tokio::sync::Mutex` directly, or a `Box<dyn Trait>`) and break compile.
- Module visibility creep: agents make everything `pub` to ease tests, exposing internals.
- Handler ↔ service contracts blur — agents put DB queries in handlers when in a hurry; refactoring later is painful.
- Error-type proliferation: each module defines its own `Error`, conversions explode. Centralize in `error.rs`.
- `mod.rs` vs `module.rs` mixing — both styles in one project trigger reviewer confusion (Rust 2018+ allows either).
- Async lifetime issues in `Router::with_state` cause cryptic compiler errors agents struggle to debug without `cargo expand`.

## Agentic workflow
Drive a Rust subagent in a tight compile-test loop: (1) generate the module skeleton with `cargo new` + `cargo add`, (2) implement handler/service pairs from a feature spec, (3) compile + clippy + test on every change. Use `bacon` or `cargo watch -x check` so the agent gets sub-second feedback. Always require the agent to run `cargo clippy -- -D warnings` and `cargo fmt --check` before declaring done — Rust's compiler is the best LLM critic available.

### Recommended subagents
- `rust-scaffolder` (Sonnet) — runs `cargo init`, edits `Cargo.toml`, creates `src/{routes,handlers,services,db,models,middleware}/mod.rs`.
- `rust-implementer` (Sonnet) — writes handlers + services from a spec; iterates on compile errors.
- `rust-reviewer` (Sonnet) — checks clippy lints, error-type unification, lifetime correctness, `Clone` on state.
- `rust-test-writer` (Haiku) — writes integration tests with `axum::Router::oneshot` or `tower::ServiceExt`.

### Prompt pattern
```
Task: Add POST /api/v1/users to the existing Axum project.
Wire into: src/routes/users.rs (already has GET).
Layers: handler -> services::users::create -> db::users::insert.
Validation: Pydantic-equivalent via `validator` crate on CreateUserInput.
Error: must convert through crate::error::AppError (impl IntoResponse).
Done = `cargo clippy -- -D warnings && cargo test` passes.
```

```
Refactor: extract DB pool + config into AppState (currently lazy_static).
AppState must derive Clone (Arc internally where needed).
Update Router::with_state and all handler signatures.
Run cargo expand if state-injection compile errors are unclear.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo` | Build/test/run | Ships with Rust toolchain |
| `cargo clippy` | Linter, must-have | `rustup component add clippy` |
| `cargo fmt` | Formatter | `rustup component add rustfmt` |
| `cargo watch` / `bacon` | File-watch loop for agents | `cargo install cargo-watch bacon` |
| `cargo expand` | Macro expansion (debug `#[derive]`) | `cargo install cargo-expand` |
| `cargo nextest` | Faster, structured test runner | `cargo install cargo-nextest` |
| `cargo machete` | Find unused deps | `cargo install cargo-machete` |
| `cargo audit` | CVE scanner | `cargo install cargo-audit` |
| `cargo deny` | License + ban list policy | `cargo install cargo-deny` |
| `sqlx-cli` | Migrations + query check | `cargo install sqlx-cli` |
| `sea-orm-cli` | SeaORM entity generation | `cargo install sea-orm-cli` |
| `tokio-console` | Live tokio task inspector | `cargo install tokio-console` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| crates.io | OSS registry | Yes | Use sparse index for fast `cargo update` in CI |
| docs.rs | OSS | Yes | Agents fetch crate docs by version; primary truth source |
| Shuttle.dev | SaaS | Yes via CLI | Deploys Axum/Actix without infra; `shuttle deploy` |
| Fly.io | SaaS | Yes via CLI | `fly launch` with Rust buildpack |
| GitHub Actions `dtolnay/rust-toolchain` | CI | Yes | Stable matrix CI in <50 lines of YAML |
| `rust-analyzer` LSP | OSS | Yes via MCP | Better than cargo for symbol lookup; agents query via LSP MCP |
| Sentry, Honeycomb | SaaS | Yes via crates | `tracing` + OTLP export hooks in nicely |

## Templates & scripts
See `templates.md`. Bootstrap script for the canonical layout:

```bash
#!/usr/bin/env bash
# Usage: ./new-axum-svc.sh my-service
set -euo pipefail
NAME=$1
cargo new --bin "$NAME"
cd "$NAME"
cargo add axum tokio --features tokio/full
cargo add tower-http --features tower-http/trace
cargo add tracing tracing-subscriber serde --features serde/derive
cargo add anyhow thiserror
mkdir -p src/{routes,handlers,services,db,models,middleware}
for d in routes handlers services db models middleware; do
  echo "// $d module root" > "src/$d/mod.rs"
done
cat > src/error.rs <<'EOF'
use axum::http::StatusCode;
use axum::response::{IntoResponse, Response};
#[derive(thiserror::Error, Debug)]
pub enum AppError {
    #[error("not found")] NotFound,
    #[error(transparent)] Anyhow(#[from] anyhow::Error),
}
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let code = match self { Self::NotFound => StatusCode::NOT_FOUND, _ => StatusCode::INTERNAL_SERVER_ERROR };
        (code, self.to_string()).into_response()
    }
}
EOF
echo "Scaffolded $NAME"
```

## Best practices
- Make `AppState` a small `Clone` struct of `Arc<T>` fields — never `Arc<AppState>` wrapping the whole thing (Axum extracts `State<AppState>` directly).
- Centralize errors in `crate::error::AppError` and `impl IntoResponse` once — every handler returns `Result<Json<T>, AppError>`.
- Prefer `?` with `From` impls (via `thiserror`) over manual error mapping.
- Keep handlers thin: parse → call service → map result. No DB or business logic in handlers.
- Use `sqlx::query_as!` (macro) for compile-time-checked queries; commit `.sqlx/` cache for offline builds.
- Layer middleware via `tower_http`: `TraceLayer`, `CompressionLayer`, `CorsLayer`, `RequestBodyLimitLayer`.
- Split workspace into binary + library crate when LOC > ~3k or when integration tests need to import internals.
- Use `tracing` with `#[instrument]` on services; avoid `println!` and `dbg!` in committed code.

## AI-agent gotchas
- Compile errors with `Send + Sync + 'static` bounds on `State` are the #1 LLM stumbling block — agents add `Rc` or `RefCell` from instinct; require `Arc` + `tokio::sync` primitives instead.
- Trait-object soup: agents reach for `Box<dyn Service>` without thinking — prefer generics + concrete types unless polymorphism is genuinely needed.
- Borrow-checker tantrums: agents will clone aggressively to silence the compiler; review for unnecessary `.clone()` calls.
- Async-in-trait pitfalls: agents try `async fn` in traits without `async-trait`; require either the macro or `impl Future` return types.
- Forgetting `#[tokio::main]` features (default vs `full`) — runtime config errors at startup.
- `unwrap()` and `expect("TODO")` leaks — require clippy `-W clippy::unwrap_used -W clippy::expect_used` for non-test code.
- Module-tree mistakes: agents create `routes/users.rs` but forget `pub mod users;` in `routes/mod.rs`. Always run `cargo check` after file creation.
- Human-in-loop checkpoint: schema migrations (`sqlx migrate add ...`) must be reviewed — agents producing reversible-looking irreversible migrations is common.

## References
- https://docs.rs/axum
- https://actix.rs
- https://docs.rs/sqlx
- https://github.com/launchbadge/realworld-axum-sqlx (canonical example)
- https://rust-lang.github.io/api-guidelines/
- https://github.com/hyperium/tonic (gRPC alternative layout)
- https://corrode.dev/blog/idiomatic-rust-resources/
- https://docs.shuttle.dev
