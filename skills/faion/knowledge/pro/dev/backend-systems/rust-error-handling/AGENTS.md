---
slug: rust-error-handling
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use thiserror for library/crate-level typed error enums and anyhow at application binary boundaries.
content_id: "e2d0ade4aa96a99e"
tags: [rust, error-handling, result-type, async]
---
# Rust Error Handling

## Summary

**One-sentence:** Use thiserror for library/crate-level typed error enums and anyhow at application binary boundaries.

**One-paragraph:** Use thiserror for library/crate-level typed error enums and anyhow at application binary boundaries. Never use Box<dyn Error> in public function signatures. Wrap errors with ? propagation; add .context() at layer boundaries, not on every ?. Map domain errors to HTTP responses via impl IntoResponse for AppError at the handler layer only.

## Applies If (ALL must hold)

- New Rust crate or service exposing typed, programmatic errors.
- Refactoring unwrap()/expect() heavy paths into Result<T, E> with ? propagation.
- Designing an error enum a library crate callers will match on.
- Mapping domain errors to HTTP responses in Axum/Actix handlers.
- Wiring tracing + anyhow::Context for production observability.

## Skip If (ANY kills it)

- Throwaway scripts, build.rs, or tests where unwrap() carries clear intent.
- Invariant-violation paths where panic! is correct (programmer bugs).
- FFI boundaries returning C error codes — convert at the boundary, not via anyhow::Error.
- Single-binary CLI with fn main() -> anyhow::Result<()> — no custom enum needed.

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

- parent skill: `pro/dev/backend-systems/`
