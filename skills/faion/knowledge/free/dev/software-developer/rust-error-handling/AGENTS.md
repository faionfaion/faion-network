---
slug: rust-error-handling
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Result<T, E> for fallible operations, Option<T> for optional values, ? operator for ergonomic propagation.
content_id: "e2d0ade4aa96a99e"
tags: [rust, error-handling, result, exceptions]
---
# Rust Error Handling

## Summary

**One-sentence:** Result<T, E> for fallible operations, Option<T> for optional values, ? operator for ergonomic propagation.

**One-paragraph:** Result<T, E> for fallible operations, Option<T> for optional values, ? operator for ergonomic propagation. Use thiserror for libraries, anyhow for apps. Never .unwrap() in production.

## Applies If (ALL must hold)

- Writing or refactoring any Rust code where functions can fail (file I/O, network, parsing, FFI, DB).
- Designing the public API of a Rust library — choice between thiserror (libraries) and anyhow (apps) is fundamental.
- Migrating from unwrap()/expect() panics in prototype code to Result<T, E> for production.
- Adding error reporting / observability so failures carry context, source chains, and (optionally) backtraces.

## Skip If (ANY kills it)

- Truly unrecoverable invariants (out-of-bounds array access in safety-critical code) — use panic! or assert!; turning them into Result muddies intent.
- Build scripts (build.rs) and one-off tooling — ? + Box<dyn Error> is fine, no custom error type needed.
- #![no_std] embedded code where std::error::Error doesn't exist (use core::error::Error from 1.81 stable, but ecosystem support is partial).
- Procedural macro internals — syn::Result is the convention; rolling a custom error there fights the ecosystem.

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
