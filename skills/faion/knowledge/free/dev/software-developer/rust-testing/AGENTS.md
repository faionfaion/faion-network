---
slug: rust-testing
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Testing patterns for Rust services: unit tests with `mockall` in `#[cfg(test)] mod tests` co-located with the SUT, async tests via `#[tokio::test]`, integration tests against real `axum::Router` via `tower::ServiceExt`, and property tests with `proptest`.
content_id: "001fc58fae66182c"
tags: [rust, testing, mockall, tokio, proptest]
---
# Rust Testing

## Summary

**One-sentence:** Testing patterns for Rust services: unit tests with `mockall` in `#[cfg(test)] mod tests` co-located with the SUT, async tests via `#[tokio::test]`, integration tests against real `axum::Router` via `tower::ServiceExt`, and property tests with `proptest`.

**One-paragraph:** Testing patterns for Rust services: unit tests with `mockall` in `#[cfg(test)] mod tests` co-located with the SUT, async tests via `#[tokio::test]`, integration tests against real `axum::Router` via `tower::ServiceExt`, and property tests with `proptest`. Key rule: prefer fakes over mocks for trait-heavy code; always `await` joined async task handles; run `cargo nextest` in CI.

## Applies If (ALL must hold)

- Rust services where correctness is non-negotiable (auth, billing, infra control planes) — `cargo test` + `mockall` + `proptest` give compile-time + property-level guarantees beyond what dynamic-language tests reach.
- Async services on `tokio` — `#[tokio::test]` is the de-facto runner; agents writing axum/tonic services need consistent test shape.
- Library crates publishing to crates.io — doctest discipline (`/// # Examples`) prevents silent doc rot.
- Refactor work where the borrow checker shifts function signatures — typed tests fail closed; LLM regressions surface immediately.
- Codebases enforcing `cargo deny` + coverage threshold via `cargo llvm-cov` in CI.

## Skip If (ANY kills it)

- Hot iteration prototypes — Rust's slow incremental compile + test startup punishes small loops; write the impl first.
- Pure FFI shims to C libs — testing requires the linked C side; integration tests pay double cost. Prefer a thin Rust wrapper + tests on the wrapper.
- Code where mocks dominate the test (`mockall` everywhere) — that's a sign the design is over-coupled. Refactor toward trait-based seams or use real implementations behind `#[cfg(test)]`.
- Macro-heavy crates where the test of value is `trybuild` (compile-fail tests), not runtime assertions.
- Embedded `no_std` targets — `cargo test` needs std; use `defmt-test` / on-target runners instead.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `free/dev/software-developer/`
