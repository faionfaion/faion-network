---
slug: rust-error-handling
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a Rust error-design spec choosing `thiserror` for libraries, `anyhow` for apps, with `Result<T, E>` everywhere, `?` propagation, and a clippy gate forbidding `.unwrap()` in non-test code.
content_id: "e2d0ade4aa96a99e"
complexity: medium
produces: spec
est_tokens: 3800
tags: [rust, error-handling, result, thiserror, anyhow]
---
# Rust Error Handling

## Summary

**One-sentence:** Decides between `thiserror` (libraries) and `anyhow` (apps), requires `Result<T, E>` for all fallible operations, mandates `?` over manual match, and gates `.unwrap()`/`.expect()` out of production via clippy.

**One-paragraph:** Rust has two viable error stories — opaque dynamic (`anyhow::Error`, great for apps because callers only log) and typed enums (`thiserror`, great for libraries because callers branch on variants). Mixing them is the canonical mess: applications grow library-shaped error enums that nobody downstream uses, and libraries propagate `anyhow::Error` which downstream code cannot match. This methodology picks one per crate based on whether the crate is a binary or a published library, gates `.unwrap()` / `.expect()` in non-test code via clippy, and requires every error variant to carry context (`#[from]` for source chains, `#[error("...")]` for display) so the eventual log line names what failed.

**Ефективно для:**

- Нова Rust бібліотека (crate в публікації): чіткий enum помилок, downstream може match.
- Бінарний застосунок (CLI, web service): anyhow + ? — менше boilerplate, кращі повідомлення.
- Міграція прототипу з `.unwrap()` всюди → production-ready: пошарово замінити на `?` + context.
- FFI / WASM межі: типізовані помилки на кордоні, dynamic усередині.

## Applies If (ALL must hold)

- Rust crate (binary or library) with fallible operations (I/O, network, parsing, FFI, DB).
- Crate has a `Cargo.toml` and clippy is wired (default for `cargo new`).
- Stable Rust ≥1.81 (for `core::error::Error` if `#![no_std]`).

## Skip If (ANY kills it)

- Truly unrecoverable invariants — use `panic!` / `assert!`; turning them into `Result` muddies intent.
- `build.rs` and one-off tooling — `Box<dyn Error>` is fine.
- `#![no_std]` embedded code where ecosystem support for `core::error::Error` is partial.
- Procedural macro internals — `syn::Result` is the convention; rolling a custom error there fights the ecosystem.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `Cargo.toml` | TOML | crate root |
| Crate type | `[lib]` / `[[bin]]` | `Cargo.toml` |
| Public-API surface | path list | `lib.rs` re-exports |
| Clippy config | `clippy.toml` (optional) | crate root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rust-ownership]] | Error types carry data; ownership shapes (`String` vs `&'static str`) matter. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: thiserror-for-lib, anyhow-for-app, no-unwrap-non-test, question-mark-over-match, source-chains-required, context-on-conversion | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for error-design spec + clippy lint config | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: anyhow-in-library, untyped-string-error, swallowing-source, unwrap-in-production | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure: classify crate → pick crate → write enum/anyhow → swap unwraps → gate clippy | 700 |
| `content/05-examples.xml` | optional | Worked example: library Error enum with `#[from]` chains | 600 |
| `content/06-decision-tree.xml` | essential | Routing: crate type → error library → variant strategy | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_crate` | haiku | `Cargo.toml` parse; deterministic. |
| `enumerate_failures` | sonnet | Read fallible call sites; build variant list. |
| `write_error_enum` | sonnet | Per-crate boilerplate generation. |
| `swap_unwraps` | haiku | Mechanical `?` substitution with context. |

## Templates

| File | Purpose |
|------|---------|
| `templates/error.rs.thiserror.tmpl` | `thiserror`-based Error enum scaffold for libraries |
| `templates/clippy.toml` | Clippy lint block forbidding `unwrap_used`, `expect_used` outside tests |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-error-handling.py` | Validate error-design spec JSON against schema | After spec generation |

## Related

- [[rust-ownership]] — error variants own their data; lifetime decisions matter.
- [[rust-testing]] — `.unwrap()` is allowed in tests; clippy config relaxes there.

## Decision tree

See `content/06-decision-tree.xml`. Tree first asks crate type (library / binary / build-script) → picks `thiserror` (lib), `anyhow` (bin), or `Box<dyn Error>` (build). Then asks whether downstream needs variant matching → yes ⇒ enum with `#[from]` source chains; no ⇒ opaque error with `.context()`. All leaves reference rules from `01-core-rules.xml`.
