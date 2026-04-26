# Rust Backend (Axum)

## Summary

Opinionated layout and patterns for Rust HTTP services using Axum: one `AppError` enum per service with `IntoResponse` mapping to RFC 7807, layered modules (`routes/`, `handlers/`, `services/`, `models/`, `db/`), `AppState` shared via `Arc`, CPU-bound work on `spawn_blocking`, and a vertical-slice delivery model (models → db → services → handlers → routes + tests in one PR).

## Why

Rust's type system eliminates entire categories of bugs, but the Axum API surface changed significantly between 0.6 and 0.7 and LLMs blend the two. A single canonical shape for `AppState`, `AppError`, handler signatures, and test scaffolding prevents silent contract breaks and keeps agent-generated PRs coherent across services.

## When To Use

- Greenfield Rust HTTP service needing full project layout + handlers + services + DB + tests.
- Migrating a Python/Node service to Rust for tail-latency or memory reasons.
- Standardizing several Rust services on one shape (same `AppError`, handler/service/db split, test scaffolding).
- Onboarding new contributors who need a working CRUD slice without learning Tokio/Axum trivia first.

## When NOT To Use

- Library crates (no HTTP) — only the project-structure portion applies.
- gRPC-only services — use `tonic`; handler shape differs.
- Lambda/Cloud-Functions — `lambda_runtime` plus a minimal handler is leaner.
- Embedded/no_std — use `embassy` instead.
- Cross-runtime libraries — drop Tokio specifics.

## Content

| File | What's inside |
|------|---------------|
| `content/01-project-layout.xml` | Directory layout, module wiring, Axum router setup, `AppState` shape. |
| `content/02-handlers-and-services.xml` | Type-safe handler pattern, `tokio::try_join!` for parallel queries, `spawn_blocking` for CPU work. |
| `content/03-testing.xml` | Unit tests with `mockall`, integration tests with `tower::ServiceExt::oneshot`. |
| `content/04-gotchas.xml` | Agent gotchas: Axum 0.6 vs 0.7, lifetime borrowing vs `Arc`, mockall limits, `IntoResponse` coverage. |

## Templates

| File | Purpose |
|------|---------|
| `templates/app-error.rs` | `AppError` enum with `IntoResponse` mapping to RFC 7807 `ProblemDetail`. |
