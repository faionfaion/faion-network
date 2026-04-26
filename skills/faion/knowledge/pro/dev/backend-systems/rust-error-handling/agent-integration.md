# Agent Integration — Rust Error Handling

## When to use
- New Rust crate or service that must expose typed, programmatic errors instead of stringly-typed messages.
- Refactor of `unwrap()` / `expect()` heavy code path into `Result<T, E>` with `?` propagation.
- Designing an error enum for a library that other crates will match on (`#[non_exhaustive]`, `#[from]` conversions).
- Wiring `tracing` + error context (`anyhow::Context`) for production observability.
- Mapping domain errors to HTTP responses in Axum/Actix handlers (`IntoResponse` for the error type).

## When NOT to use
- Throwaway scripts, build-time `build.rs`, or tests where `unwrap()` carries clear intent.
- Cases where `panic!` is correct (invariant violations, programmer-bug paths) — wrapping them in `Result` only hides bugs.
- FFI boundaries returning C error codes — handle conversion at the boundary, not by leaking `anyhow::Error` outward.
- Single-binary CLI with `fn main() -> anyhow::Result<()>` — no need for a custom enum.

## Where it fails / limitations
- `anyhow::Error` is a great application-layer type but a poor library-layer type — callers cannot match on variants.
- `thiserror` `#[from]` makes invisible conversions; chains across many layers obscure root cause if `#[source]` is omitted.
- LLMs frequently emit `Box<dyn Error>` for libraries when `thiserror` is the right tool — review every PR for this.
- `?` in `async fn` requires the future's error type to convert; agents often forget to add the `From` impl and try to `.map_err` everywhere.
- Backtraces require nightly or `RUST_BACKTRACE=1` plus `anyhow::Error::backtrace()` — production builds often miss this.
- Agents over-add `.context()` on every `?`, producing noisy chains; one context per layer boundary is enough.

## Agentic workflow
Treat error-type design as a one-shot architecture pass, then drive implementation with a coding subagent. The reviewer agent must check that the error enum has stable variants, no `Box<dyn Error>` leakage in public signatures, and that conversions use `#[from]` rather than manual `match`. For application code, prefer `anyhow` at the binary boundary and `thiserror` enums per crate; the agent should never mix `anyhow::Result` and a typed error in the same public function.

### Recommended subagents
- `faion-sdd-executor-agent` — apply `thiserror` + `anyhow` template, regenerate variants, run `cargo check` per task.
- General code-review subagent (reviewer pass) — flag `unwrap`, `expect`, `Box<dyn Error>`, panicking `From` impls.
- `password-scrubber-agent` — when error messages may embed secrets (DB URLs, tokens) before they hit logs.

### Prompt pattern
Plan: "Define a `thiserror` enum `<Crate>Error` covering `Db`, `Validation`, `NotFound`, `Conflict`, `Unauthorized`, `Internal(#[from] anyhow::Error)`. Add `IntoResponse` mapping to HTTP. Replace all `unwrap()` in `src/` with `?` and bubble up. Show diff before applying."

Review: "Audit `src/**/*.rs` for `unwrap()`, `expect(`, `Box<dyn Error>` in public signatures, and `panic!` outside `#[cfg(test)]`. Return a list with file:line and proposed fix."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo clippy -- -D clippy::unwrap_used -D clippy::expect_used` | Lint to ban panicking calls | rustup component add clippy |
| `cargo machete` | Detect unused error-handling deps (`anyhow`, `thiserror`) | cargo install cargo-machete |
| `cargo expand` | Inspect generated code from `#[derive(Error)]` | cargo install cargo-expand |
| `cargo audit` | Surface CVEs in `anyhow`/`thiserror`/`eyre` chain | cargo install cargo-audit |
| `cargo nextest run` | Faster test runs while iterating on error mapping | cargo install cargo-nextest |
| `eyre` / `color-eyre` | Drop-in for `anyhow` with prettier reports | crates.io/crates/color-eyre |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Sentry | SaaS | Yes | `sentry-anyhow` integration captures error chains; agents can add via one Cargo dep |
| Honeycomb / OpenTelemetry | SaaS/OSS | Yes | `tracing` + `tracing-error` attaches spans to errors; OTLP exporter is mechanical |
| Loki + Grafana | OSS | Yes | Structured `tracing_subscriber::fmt().json()` ships error-chain JSON straight to Loki |
| BetterStack / Logtail | SaaS | Yes | HTTP log drain; agent only needs API token |
| Crash reporters (`minidumper`, `breakpad`) | OSS | Partial | Out-of-process crash capture; setup is non-trivial, keep human in loop |

## Templates & scripts
See `templates.md` for the canonical `thiserror` enum and `From` impl set. Quick lint-as-CI step:

```bash
#!/usr/bin/env bash
# scripts/check-errors.sh — fail PR if forbidden patterns appear
set -euo pipefail
cargo clippy --all-targets --all-features -- \
  -D clippy::unwrap_used \
  -D clippy::expect_used \
  -D clippy::panic \
  -D clippy::todo \
  -D clippy::unimplemented \
  -W clippy::missing_errors_doc
# Forbid Box<dyn Error> in public signatures
if rg -nP '^\s*pub\s+fn\b.*Box<dyn\s+(std::)?error::Error' src/; then
  echo "Box<dyn Error> in public API — use a typed error enum"
  exit 1
fi
```

## Best practices
- One error enum per crate; library crates expose the enum, binary crates may convert to `anyhow::Error` at `main`.
- Always `#[non_exhaustive]` on public error enums so adding a variant is not a breaking change.
- Use `#[source]` (not just `#[from]`) when the variant carries semantic context beyond the wrapped error.
- Map domain errors to HTTP at the handler layer via `impl IntoResponse for Error`, never inside services.
- Keep `Display` messages human-readable but free of PII or secrets — log structured fields separately via `tracing`.
- Add `#[track_caller]` on small helpers that wrap `?` patterns so backtraces point at the caller.

## AI-agent gotchas
- Models love adding `.unwrap()` "to keep it short" inside `async fn`. Reject every PR that does this.
- LLMs often invent `From<&str>` or `From<String>` impls — these silently swallow context. Force `#[from]` on real error types only.
- `anyhow!("...")` macros with format args concatenated by the model can leak environment values; route secrets through a scrubber (`password-scrubber-agent`) before logging.
- Agents may "fix" a borrow-checker error by switching the function to return `Result<T, String>`; reviewer must catch this.
- When generating `IntoResponse` mappings, agents commonly return `500` for everything; require a per-variant status mapping table in the prompt.
- Beware: an agent that adds `#[from] anyhow::Error` to a `thiserror` enum collapses the type system back to stringly-typed errors — disallow in libraries.

## References
- The Rust Book, ch. 9 — https://doc.rust-lang.org/book/ch09-00-error-handling.html
- `thiserror` docs — https://docs.rs/thiserror
- `anyhow` docs — https://docs.rs/anyhow
- "Error Handling in Rust" (BurntSushi) — https://blog.burntsushi.net/rust-error-handling/
- `eyre` / `color-eyre` — https://docs.rs/color-eyre
- Axum error handling — https://docs.rs/axum/latest/axum/error_handling/
