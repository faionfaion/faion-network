# Rust Error Handling

## Summary

Use `thiserror` for library/crate-level typed error enums and `anyhow` at application binary boundaries. Never use `Box<dyn Error>` in public function signatures. Wrap errors with `?` propagation; add `.context()` at layer boundaries, not on every `?`. Map domain errors to HTTP responses via `impl IntoResponse for AppError` at the handler layer only.

## Why

`anyhow::Error` is great for application code but a poor library type — callers cannot match variants. `Box<dyn Error>` collapses the type system. `thiserror` derives `Display`, `Error`, and `From` impls with less boilerplate than hand-rolling, while keeping the public API typed and matchable. LLMs frequently emit `unwrap()` or `Box<dyn Error>` in public APIs; a typed enum with clippy gates catches these at CI.

## When To Use

- New Rust crate or service exposing typed, programmatic errors.
- Refactoring `unwrap()`/`expect()` heavy paths into `Result<T, E>` with `?` propagation.
- Designing an error enum a library crate callers will match on.
- Mapping domain errors to HTTP responses in Axum/Actix handlers.
- Wiring `tracing` + `anyhow::Context` for production observability.

## When NOT To Use

- Throwaway scripts, `build.rs`, or tests where `unwrap()` carries clear intent.
- Invariant-violation paths where `panic!` is correct (programmer bugs).
- FFI boundaries returning C error codes — convert at the boundary, not via `anyhow::Error`.
- Single-binary CLI with `fn main() -> anyhow::Result<()>` — no custom enum needed.

## Content

| File | What's inside |
|------|---------------|
| `content/01-error-types.xml` | `Result`/`Option` basics, `?` propagation, custom error enum with `thiserror`, `From` impls. |
| `content/02-anyhow.xml` | `anyhow` for application code: `context()`, `bail!`, `anyhow!`, downcasting. |
| `content/03-combinators.xml` | `map`, `map_err`, `and_then`, `or_else`, `unwrap_or`, Option combinators. |
| `content/04-async-and-antipatterns.xml` | Error handling in async code; antipatterns: `unwrap` in prod, ignored errors, stringly-typed errors. |

## Templates

| File | Purpose |
|------|---------|
| `templates/check-errors.sh` | CI script: clippy gates banning `unwrap_used`, `expect_used`, `Box<dyn Error>` in public APIs. |
