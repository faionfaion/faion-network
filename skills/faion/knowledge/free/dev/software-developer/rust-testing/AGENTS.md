# Rust Testing

## Summary

Testing patterns for Rust services: unit tests with `mockall` in `#[cfg(test)] mod tests` co-located with the SUT, async tests via `#[tokio::test]`, integration tests against real `axum::Router` via `tower::ServiceExt`, and property tests with `proptest`. Key rule: prefer fakes over mocks for trait-heavy code; always `await` joined async task handles; run `cargo nextest` in CI.

## Why

Rust's type system eliminates whole classes of bugs at compile time but cannot catch logic errors, missed edge cases, or async task panics. Typed tests fail closed — refactors that shift function signatures break tests immediately, before CI. `cargo nextest` parallelizes at the process level (not thread level), making suites 10-60% faster and isolating test-global-state leaks.

## When To Use

- Rust services where correctness is non-negotiable (auth, billing, infra control planes).
- Async services on tokio — `#[tokio::test]` is the de-facto runner for axum/tonic.
- Library crates publishing to crates.io — doctest discipline prevents silent doc rot.
- Refactor work where the borrow checker shifts signatures — typed tests surface regressions immediately.
- Codebases enforcing `cargo llvm-cov` coverage threshold in CI.

## When NOT To Use

- Hot iteration prototypes — slow incremental compile + test startup punishes small loops; write the impl first.
- Pure FFI shims where testing requires the linked C side — prefer a thin wrapper + test the wrapper.
- Macro-heavy crates where the test of value is `trybuild` (compile-fail), not runtime assertions.
- Embedded `no_std` targets — `cargo test` needs std; use `defmt-test` / on-target runners instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-unit-tests.xml` | `#[cfg(test)] mod tests`, `mockall` setup, async test patterns, assert_matches. |
| `content/02-integration-tests.xml` | `tests/*.rs` against `axum::Router` via `tower::ServiceExt`, `testcontainers`. |
| `content/03-property-tests.xml` | `proptest!` macros, strategy constraints, run count configuration. |
| `content/04-antipatterns.xml` | `unwrap()` in SUT, mock ordering bugs, async drop issues, snapshot without review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rust-coverage-gate.sh` | CI script enforcing line + branch coverage thresholds via `cargo llvm-cov`. |
