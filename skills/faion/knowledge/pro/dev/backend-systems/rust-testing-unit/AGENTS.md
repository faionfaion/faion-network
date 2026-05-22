---
slug: rust-testing-unit
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Unit tests in Rust live inside a #[cfg(test)] mod tests block colocated with the production code.
content_id: "e96208b2ffda8e23"
tags: [rust, testing, mockall, unit-test, tokio]
---
# Rust Unit Testing with mockall and tokio::test

## Summary

**One-sentence:** Unit tests in Rust live inside a #[cfg(test)] mod tests block colocated with the production code.

**One-paragraph:** Unit tests in Rust live inside a #[cfg(test)] mod tests block colocated with the production code. Trait dependencies are mocked with mockall::mock!; async tests use #[tokio::test] with an explicit runtime flavor. Black-box tests go to the tests/ directory at crate root. Never mix the two.

## Applies If (ALL must hold)

- Rust services using Axum/Actix/Tonic where you need fast feedback with mockall mocks.
- Async-heavy code (tokio runtime) where the test harness must use #[tokio::test] with controlled time (tokio::time::pause) to avoid wall-clock dependence.
- Any service method that depends on a trait (database, HTTP client, clock) that can be mocked cheaply.
- Library crates where doc-tests, and cargo test --doc, should run on every PR.

## Skip If (ANY kills it)

- Trivial scripts where assert! inside main() is enough — the harness costs more than the test.
- Code where mocks dominate signal — if every dep is mocked, the test asserts the mock setup, not behavior. Prefer integration tests with real components.
- Pure serde round-trips where proptest is the right tool, not hand-written #[test]s.
- Cross-compile targets where running tests on the host does not reflect the target. Use cross + Docker, or skip and rely on CI.

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
