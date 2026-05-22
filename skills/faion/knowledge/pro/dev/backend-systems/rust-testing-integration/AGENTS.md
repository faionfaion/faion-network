---
slug: rust-testing-integration
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Integration tests for Rust HTTP services drive the real Axum (or Actix) router via tower::ServiceExt::oneshot without binding a port.
content_id: "6eb428381b73f9d3"
tags: [rust, integration-test, axum, testcontainers, tower]
---
# Rust Integration Testing — Axum/Tower and Testcontainers

## Summary

**One-sentence:** Integration tests for Rust HTTP services drive the real Axum (or Actix) router via tower::ServiceExt::oneshot without binding a port.

**One-paragraph:** Integration tests for Rust HTTP services drive the real Axum (or Actix) router via tower::ServiceExt::oneshot without binding a port. Database tests use testcontainers-rs to spin up a per-test Postgres container — or a shared container with per-test schema isolation — ensuring tests never depend on a shared dev DB and never leave state that breaks parallel runs.

## Applies If (ALL must hold)

- Rust services using Axum/Actix/Tonic where you need confidence that the real router, extractors, middleware, and DB round-trip work end-to-end.
- Any handler that reads or writes a database and where a mock would just assert the mock setup.
- Pagination, filtering, and ordering logic that requires real SQL execution to be meaningful.
- Scenarios where multiple components interact and the unit-level boundaries are wrong.

## Skip If (ANY kills it)

- Business logic that has no I/O — a unit test with mockall is cheaper and faster.
- Hot-path benchmarks — cargo test is not cargo bench; use criterion for perf-sensitive code.
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
