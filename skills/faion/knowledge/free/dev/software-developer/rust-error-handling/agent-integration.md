# Agent Integration — Rust Error Handling

## When to use
- Writing or refactoring any Rust code where functions can fail (file I/O, network, parsing, FFI, DB).
- Designing the public API of a Rust library — choice between `thiserror` (libraries) and `anyhow` (apps) is fundamental.
- Migrating from `unwrap()`/`expect()` panics in prototype code to `Result<T, E>` for production.
- Adding error reporting / observability so failures carry context, source chains, and (optionally) backtraces.

## When NOT to use
- Truly unrecoverable invariants (out-of-bounds array access in safety-critical code) — use `panic!` or `assert!`; turning them into `Result` muddies intent.
- Build scripts (`build.rs`) and one-off tooling — `?` + `Box<dyn Error>` is fine, no custom error type needed.
- `#![no_std]` embedded code where `std::error::Error` doesn't exist (use `core::error::Error` from 1.81 stable, but ecosystem support is partial).
- Procedural macro internals — `syn::Result` is the convention; rolling a custom error there fights the ecosystem.

## When NOT to bother with custom error types
- Binaries / CLIs: just use `anyhow::Result<()>` everywhere; you don't need a typed enum.
- Libraries used by exactly one consumer (your own app): one shared `AppError` enum is fine; don't overengineer per-module error types.

## Where it fails / limitations
- `Box<dyn Error>` discards type information and prevents callers from matching specific failures — fine in mains, terrible in libraries.
- `?` operator + `From` conversions can blow up compile times in deeply nested chains; explicit `.map_err(...)` is sometimes faster to compile.
- `thiserror` won't generate `#[from]` impls for generic types easily; agents writing generic libraries will hit confusing trait-bound errors.
- `anyhow::Error` erases types: you can't downcast cleanly across `async` boundaries when the type implements `!Send`.
- Backtrace capture (`RUST_BACKTRACE=1`) costs runtime; agents writing performance-sensitive code must scope it (e.g., debug-only).
- Errors thrown across FFI boundaries lose Rust panics — agents writing C ABIs must catch panics with `std::panic::catch_unwind`.

## Agentic workflow
A code-writing agent picks the strategy based on artifact type: library → `thiserror` enum + `#[from]`; binary → `anyhow::Result` + `.context("…")` everywhere. A code-review agent runs `clippy::unwrap_used` and `clippy::expect_used` denial lints, plus a custom AST walker that flags `.unwrap()` outside `#[cfg(test)]`. A test agent verifies that error variants have stable `Display` strings (snapshot tests) and that `#[from]` conversions roundtrip.

### Recommended subagents
- `faion-sdd-executor-agent` — drives implementation; constitution.md should pin "thiserror for libs, anyhow for bins".
- A purpose-built `clippy-enforcer` subagent — runs `cargo clippy -- -D clippy::unwrap_used -D clippy::expect_used -D warnings`.
- A `error-doc-writer` subagent — for each `pub enum *Error` variant, generates a doc comment with cause + recovery hint.

### Prompt pattern
```
This crate is a library. Define a public Error enum with thiserror.
Variants: <list>. Use #[from] for IO/Parse/Db sources. No anyhow.
No Box<dyn Error>. Add #[non_exhaustive] to allow future variants.
```
```
Refactor `unwrap()` calls in <file>. Each must become either:
(a) `?` if the function returns Result, after declaring the right error type;
(b) `expect("…")` with a clear invariant message if truly unreachable;
(c) explicit match if recovery is possible.
Output a diff. Stop.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo` | Build + test runner | rustup default · https://doc.rust-lang.org/cargo/ |
| `cargo clippy` | Lints incl. unwrap_used/expect_used | `rustup component add clippy` |
| `cargo expand` | See generated thiserror impls | `cargo install cargo-expand` |
| `cargo deny` | Audit deps; ban unmaintained error crates | `cargo install cargo-deny` |
| `cargo nextest` | Faster test runner; better failure formatting | `cargo install cargo-nextest` |
| `cargo udeps` | Dead-dep check after error-crate consolidation | `cargo install cargo-udeps` |
| `cargo audit` | Security CVEs in error chain deps | `cargo install cargo-audit` |
| `mold` / `lld` | Faster linker; helps when `?` blows compile time | https://github.com/rui314/mold |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry (`sentry` crate) | SaaS | Yes | Captures errors with source chain via `Error::source()`. |
| Honeycomb / Datadog | SaaS | Yes | `tracing-error` integration carries error spans. |
| `tracing` + `tracing-error` | OSS | Yes | `SpanTrace` augments errors with span context; better than naive backtrace. |
| `eyre` / `color-eyre` | OSS | Yes | Drop-in replacement for `anyhow` with prettier reports. |
| GitHub Issues + cargo-make | SaaS/OSS | Yes | Auto-create issues on panic with stable error variant id. |

## Templates & scripts
See `templates.md` for full enum patterns. Inline minimal library error:

```rust
// lib.rs
use thiserror::Error;

#[derive(Debug, Error)]
#[non_exhaustive]
pub enum LibError {
    #[error("io error: {0}")]
    Io(#[from] std::io::Error),
    #[error("parse error at line {line}: {msg}")]
    Parse { line: usize, msg: String },
    #[error("not found: {0}")]
    NotFound(String),
}

pub type Result<T, E = LibError> = std::result::Result<T, E>;
```

```rust
// main.rs (binary)
use anyhow::{Context, Result};

fn main() -> Result<()> {
    let cfg = std::fs::read_to_string("config.toml")
        .context("reading config.toml")?;
    let parsed: toml::Value = toml::from_str(&cfg)
        .context("parsing config.toml")?;
    println!("{parsed:#?}");
    Ok(())
}
```

## Best practices
- Libraries: `thiserror` enums, `#[non_exhaustive]`, `#[from]` for source conversions, doc-comment per variant.
- Binaries: `anyhow::Result<()>` everywhere; chain `.context("doing X")` at every meaningful step. End-user output is via `Display`, not `Debug`.
- Always implement `Display` such that the message is human-readable WITHOUT trailing punctuation; the formatter chains causes with ": ".
- Use `?` not `.unwrap()` outside tests; `clippy::unwrap_used` + `clippy::expect_used` denied at workspace level.
- Don't `panic!` for input validation in libs — return `Err`. Reserve panics for "this can't happen" invariants.
- For async: `Send + Sync + 'static` bounds matter; `anyhow::Error` is `Send + Sync` by default, custom errors must implement them.
- Convert errors at boundaries: domain code returns domain errors; only the API/handler layer maps to HTTP status codes.
- `tracing-error::SpanTrace` is more useful than `Backtrace` in async code — it shows logical path, not stack frames.
- Don't `.to_string()` inner errors and lose source — that breaks `Error::source()` chains. Use `#[source]` or `#[from]`.

## AI-agent gotchas
- LLMs default to `unwrap()` in examples because it's shorter. Add `#![deny(clippy::unwrap_used)]` at crate root + system prompt instructing `?` + Result everywhere.
- LLMs frequently produce `Box<dyn std::error::Error>` returns in libraries. That's an anti-pattern; always specify the error type.
- `?` only works if the error implements `From<SourceError>` for the function's error type. LLMs forget the conversion impl — Clippy + cargo build fail loud, but agents that don't read errors carefully will keep iterating without fixing it.
- When mixing `anyhow` and `thiserror` in the same crate, agents lose track of which functions return which. Convention: every `pub fn` uses `crate::Result`; only `main` uses `anyhow`.
- LLMs often write `.map_err(|e| MyError::Other(e.to_string()))` — this drops the source error. Use `#[from]` and let the conversion be automatic.
- Agents skip `#[non_exhaustive]` on public enums, then break SemVer when adding a variant. Default policy: always add it on new pub enums.
- Async error reporting: agents wrap futures with `?` but forget `Send + 'static` bounds; spawning the future fails with cryptic trait-bound errors.
- Logging vs returning: agents log-and-swallow errors. Rule: log at the boundary that decides recovery (handler), return everywhere else.
- LLMs misuse `expect("invariant")` as a fancy unwrap. The expect message must explain WHY it can't fail; reviewers should reject "should never happen" as the message.

## References
- https://doc.rust-lang.org/book/ch09-00-error-handling.html — official chapter
- https://docs.rs/thiserror/ — thiserror reference
- https://docs.rs/anyhow/ — anyhow reference
- https://docs.rs/tracing-error/ — span-aware errors
- https://blog.burntsushi.net/rust-error-handling/ — Andrew Gallant's seminal post
- https://nrc.github.io/error-docs/ — Rust error-handling design overview
- https://sabrinajewson.org/blog/errors — Sabrina Jewson on layered errors
- https://docs.rs/snafu/ — snafu (alternative to thiserror with context-style API)
