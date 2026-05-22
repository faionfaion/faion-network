---
slug: rust-testing
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a Rust test-strategy config (unit + integration + doctest layout, cargo-llvm-cov gate, proptest budget) that lints fast iteration without sacrificing coverage.
content_id: "a31f1c4e9b27f001"
complexity: medium
produces: config
est_tokens: 3800
tags: [rust, testing, cargo, proptest, llvm-cov]
---
# Rust Testing

## Summary

**One-sentence:** Configures Rust's three test layers (inline `#[cfg(test)]` unit, `tests/*.rs` integration, `///` doctests) plus cargo-llvm-cov coverage gate and a proptest budget.

**One-paragraph:** Rust testing has three orthogonal layers and most projects use only one. Unit tests inside `#[cfg(test)] mod tests` cover private functions cheaply. Integration tests in `tests/` exercise the public API like a downstream consumer. Doctests verify documented examples still compile and pass. This methodology forces all three to be present (gated by `cargo test --doc` + `cargo test --tests` in CI), wires `cargo-llvm-cov` for branch coverage with diff-cover on PR (target ≥85% on changed lines), reserves `proptest` for invariants on data structures and parsers, and forbids `.unwrap()` outside `#[cfg(test)]` (paired with [[rust-error-handling]]).

**Ефективно для:**

- Нова Rust бібліотека: doctests документуються та валідуються одночасно.
- Парсери, кодеки, structures: proptest з shrinking ловить edge cases unit-tests пропускають.
- Refactor публічного API: integration tests у `tests/` ловлять breaking change.
- Switching mock framework: built-in `#[cfg(test)]` модуль + `mockall` крихітніший за external test harnesses.

## Applies If (ALL must hold)

- Rust crate with `Cargo.toml`.
- Public API or invariant-rich data structures present (anything beyond hello-world).
- CI runs on every PR and can execute `cargo test --all-targets`.

## Skip If (ANY kills it)

- Build scripts and procedural macros — different testing harness; out of scope.
- `#![no_std]` with limited test infrastructure (use `defmt-test` or `embedded-test` instead).
- Spike code or experiment branches where coverage gate slows iteration.
- Pure binary crate with no library extract — integration tests less applicable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `Cargo.toml` | TOML | crate root |
| CI workflow | YAML | `.github/workflows/` |
| Critical-path manifest | path list | `Cargo.toml [package.metadata.faion]` or AGENTS.md |
| Coverage tool | binary | `cargo install cargo-llvm-cov` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rust-error-handling]] | Tests are allowed to `.unwrap()`; non-test code is not — clippy gate config shared. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: three-layers-mandatory, llvm-cov-gate, doctest-not-rustdoc-only, proptest-on-parsers, no-test-in-pub-namespace, integration-tests-folder | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for test-strategy config + coverage gate | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: only-unit-tests, doctest-without-runs, proptest-no-shrink, shared-mutable-state-tests | 700 |
| `content/04-procedure.xml` | essential | 5-step setup: detect crate type → install llvm-cov → wire CI → add doctests → set proptest budget | 700 |
| `content/06-decision-tree.xml` | essential | Routing: feature type → unit/integration/doctest/proptest mix | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_crate_layout` | haiku | `cargo metadata` parse. |
| `propose_test_layer` | sonnet | Decide which layer per feature. |
| `write_doctest` | sonnet | Tied to documentation prose. |
| `proptest_strategy_design` | opus | Invariant identification is cross-cutting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rust-coverage-gate.sh` | CI script running `cargo llvm-cov` + diff-cover against base branch |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-testing.py` | Validate test-strategy config JSON against schema | After config generation |

## Related

- [[rust-error-handling]] — test code escapes the `.unwrap()` gate via `#[cfg(test)]`.
- [[code-coverage]] — language-agnostic coverage discipline; this methodology specialises to Rust.

## Decision tree

See `content/06-decision-tree.xml`. Branches on test scope: private invariant → unit; public API behavior → integration; documentation example → doctest; data-structure / parser invariant → proptest. All leaves reference rules from `01-core-rules.xml`.
