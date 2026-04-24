# Agent Integration — Rust Project Structure (Axum/Actix)

## When to use
- Bootstrapping a new Rust web service with Axum or Actix-web and need a production layout from day one.
- Splitting a single-file `main.rs` into modules once it crosses ~500 lines.
- Creating a Cargo workspace for a service that will gain crates (proto, common, cli) over time.
- Adding a new feature area (background workers, admin API) and choosing whether it's a binary, lib, or workspace member.
- Standardizing layout across a fleet of Rust services so on-call engineers find files in the same place.

## When NOT to use
- One-off scripts or proc-macros — keep them flat in `src/main.rs` or a single library crate.
- Embedded/`no_std` projects — directory recipe assumes async/Tokio and dynamic allocation.
- WASM-only crates — you'll want `wasm-bindgen`, `web-sys`, different feature gating.
- Pure FFI shims — layout is dominated by `build.rs` and bindgen, not handlers/services.

## Where it fails / limitations
- Layout maps cleanly to CRUD HTTP services; heavily event-driven systems (CQRS, sagas) need additional `events/`, `commands/`, `projections/` modules not shown here.
- `AppState` cloning grows expensive once it holds many `Arc`s — at scale, prefer `tower::Layer` extension or `axum::Extension` with sharded state.
- The flat `routes/handlers/services/db` split hides domain boundaries; in a DDD codebase prefer `domain/<bounded-context>/{api,app,infra}` instead.
- Compile times explode if every module is in the same crate; split into a workspace once `cargo check` exceeds ~30s.
- Cyclic `mod.rs` imports between `services/` and `db/` are easy to introduce; the compiler messages are confusing for new Rustaceans.

## Agentic workflow
Hand the agent the empty repo plus the chosen framework (Axum vs Actix), DB driver (sqlx/sea-orm/diesel), and async runtime; the agent (1) runs `cargo new`, (2) seeds `Cargo.toml` with pinned versions, (3) generates the directory tree, (4) writes a working health-check route end-to-end, (5) writes one CRUD vertical slice (`routes/handlers/services/db`) for a sample entity. Stop after the slice runs `cargo test` green — humans pick the next entity. For migrations to a workspace, the agent should do it as a separate task: move `src/` to `crates/api/src/`, add `Cargo.toml` workspace table, fix imports.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the bootstrap as an SDD task; quality gates: `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`, `cargo audit`.
- A general implementer (Sonnet) for vertical-slice generation; an architect (Opus) for the workspace-vs-single-crate decision and `AppState` shape.

### Prompt pattern
```
Bootstrap a new Axum 0.7 service with sqlx-postgres, tracing, tower-http.
Use the layout in rust-project-structure/README.md. Implement /health and /api/v1/users CRUD
end-to-end (routes/handlers/services/db/models). Pin versions in Cargo.toml. Stop when
`cargo test` is green and `curl localhost:3000/health` returns OK.
```

```
Convert this single-crate service into a Cargo workspace with crates: api (binary),
domain (lib), infra (lib). Move files, update imports, prove with `cargo build --workspace`.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo` | Build, test, run, workspace mgmt | https://doc.rust-lang.org/cargo/ |
| `cargo-edit` | `cargo add/rm/upgrade` | `cargo install cargo-edit` |
| `cargo-watch` | Recompile on file change during dev | `cargo install cargo-watch` |
| `cargo-nextest` | Faster test runner with better output | https://nexte.st |
| `cargo-audit` | RustSec advisory check | `cargo install cargo-audit` |
| `cargo-deny` | License + duplicate-dep policing | https://embarkstudios.github.io/cargo-deny/ |
| `clippy` | Lint, ships with rustup | `rustup component add clippy` |
| `rustfmt` | Format | `rustup component add rustfmt` |
| `sqlx-cli` | DB migrations + offline query check | `cargo install sqlx-cli` |
| `cargo-generate` | Bootstrap from template repos | https://cargo-generate.github.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| crates.io | OSS registry | Yes (REST + index) | Resolve dep versions, check yanked. |
| docs.rs | OSS | Yes (HTML) | Agent can fetch crate docs by URL pattern. |
| GitHub | SaaS | Yes (`gh`, REST, MCP) | Template repos, `cargo-generate` sources. |
| Shuttle | SaaS PaaS | Yes (CLI) | `shuttle init` wraps Axum/Actix layout. |
| Fly.io | SaaS PaaS | Yes (`flyctl`) | Pairs with the same project layout. |
| Sentry | SaaS | Yes | `sentry` crate slots into `main.rs` setup. |
| GitHub Actions | SaaS | Yes | `actions-rs/toolchain` standard for CI. |

## Templates & scripts
See `templates.md` for a full Axum starter. Inline scaffolder for a new domain module:

```bash
#!/usr/bin/env bash
# scripts/new_module.sh <name>  e.g. ./scripts/new_module.sh products
set -euo pipefail
N="$1"
for dir in routes handlers services db models; do
  f="src/$dir/${N}.rs"
  [ -e "$f" ] && { echo "$f exists"; exit 1; }
  printf "// %s/%s.rs\n\n// TODO: implement\n" "$dir" "$N" > "$f"
  grep -q "pub mod $N;" "src/$dir/mod.rs" || echo "pub mod $N;" >> "src/$dir/mod.rs"
done
echo "created $N module across routes/handlers/services/db/models"
```

## Best practices
- Pin all deps to exact minor versions in `Cargo.toml` and commit `Cargo.lock` for binaries (not for libraries).
- Keep `main.rs` under ~80 lines: just config load, state build, router compose, serve.
- Use `tower-http::trace::TraceLayer` from day one; retrofitting tracing is painful.
- Put DB queries behind a `Database` struct, not free functions, so tests can pass a mock or a `sqlx::PgPool` clone trivially.
- Promote to a Cargo workspace as soon as you need a second binary (worker, admin CLI) or shared types crate.
- `error.rs` should expose one `AppError` enum with `IntoResponse`; map all upstream errors via `From` impls.
- Feature-gate dev-only deps (`#[cfg(feature = "test-utils")]`); CI builds with `--all-features`.
- Use `cargo nextest run --all-features` and `cargo clippy --all-targets -- -D warnings` as merge gates.

## AI-agent gotchas
- Agents pick stale crate versions (Axum 0.6 vs 0.7 has breaking router-state changes); always require the agent to read `Cargo.toml` and use the version present.
- LLMs will mix `actix-web` and `axum` syntax mid-file when context overflows — pin the framework choice in the system prompt and reject the file if the wrong import appears.
- Generated `mod.rs` chains often miss a `pub mod foo;` line, leading to "unresolved module" errors; require the agent to grep `mod.rs` after creating each file.
- Lifetimes in `UserService<'a>` patterns trip LLMs — they emit `'static` to silence the compiler; insist on owned `Database` or `Arc<Database>` instead.
- An agent migrating to a workspace will forget to update `default-members` and CI paths; require a `cargo build --workspace` proof before commit.
- Human-in-loop checkpoint: the `AppState` shape is sticky — once many handlers depend on it, refactoring is expensive. Review the agent's first draft.
- `sqlx::query!` macros require `DATABASE_URL` at compile time; the agent will not realize this and CI will break. Use `sqlx prepare` or `SQLX_OFFLINE=true` and check in `.sqlx/`.

## References
- Axum docs: https://docs.rs/axum
- Actix-web docs: https://actix.rs/docs/
- The Rust Book (workspaces): https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html
- Cargo Book: https://doc.rust-lang.org/cargo/
- Zero To Production In Rust (LucaPalmieri): https://www.zero2prod.com/
- tower-http: https://docs.rs/tower-http
