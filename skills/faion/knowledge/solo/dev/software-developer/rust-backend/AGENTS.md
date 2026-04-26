# Rust Backend

## Summary

Production-grade Axum (preferred) / Actix-web backend patterns covering project structure,
typed HTTP handlers, service layer with Tokio async, error handling via a single `AppError`
enum, sqlx for compile-time SQL verification, and unit/integration testing with mockall and
axum::test. Core rule: handlers stay HTTP-only, all logic delegates to services; no `unwrap()`
outside `main.rs` and tests.

## Why

Rust eliminates GC pauses, memory safety bugs, and per-instance cost for hot services. The
Axum + Tower + sqlx stack gives end-to-end type safety from route to DB query. Handlers thin
enough to test without HTTP, services independently testable with mocked repositories — this
combination yields low defect rates in production with minimal runtime overhead.

## When To Use

- New service where p99 latency, memory, or CPU efficiency dominates
- Replacing a hot service because GC pauses or per-instance cost is unacceptable
- Long-running daemons where memory safety + zero-runtime is required
- Building a binary that ships as a single file with no runtime dependencies

## When NOT To Use

- CRUD service with low traffic — Django/FastAPI ships in 1/3 the time at 99% the perf
- Heavily relational app with frequent schema churn — sqlx macros require live DB at compile time
- Team without Rust experience and a hard deadline — borrow checker ramp-up is months
- Frontend-heavy backend-for-frontend — Node + tRPC is the productive default
- Plugin systems with dynamic loading — strict ABI makes this awkward

## Content

| File | What's inside |
|------|---------------|
| `content/01-project-structure.xml` | Directory layout, Axum router setup, AppState wiring |
| `content/02-handlers-services.xml` | Typed extractors, handler pattern, service layer, concurrent processing |
| `content/03-error-testing.xml` | AppError enum with IntoResponse, unit tests with mockall, integration tests |

## Templates

| File | Purpose |
|------|---------|
| `templates/app-error.rs` | AppError enum with thiserror + Axum IntoResponse |
