# Rust HTTP Handlers (Axum)

## Summary

Handler pattern for Axum (and Actix-web): typed request/response DTOs with `validator` derives, shared `AppState` behind `Arc`, `AppError` enum implementing `IntoResponse`, and `#[tracing::instrument]` on every handler. Handlers return `Result<Json<Resp>, AppError>`; extractors are ordered body-last.

## Why

Axum's type system encodes the request contract at compile time, eliminating an entire class of runtime panics. Without the structured AppError + extractor-order discipline, agents routinely produce handlers that panic on parse failure, expose database errors to clients, and fight the borrow checker on `&str` parameters. The pattern also enables one-shot `Router::oneshot` unit tests with no network.

## When To Use

- Building JSON REST APIs with Axum or Actix-web.
- Refactoring loosely-typed handlers into the request-DTO / service-call / response-DTO layered pattern.
- Adding `validator`-based request validation and typed error responses.
- Implementing streaming responses (SSE, WebSocket) with Tokio.
- Wiring middleware: tracing, CORS, auth, rate limiting via `tower-http`.

## When NOT To Use

- High-throughput RPC where Tonic (gRPC) is a better fit.
- Async-light scripts and CLIs — `reqwest` + `tokio` without a server framework.
- Teams with more comfort in Go/Python where perf gain doesn't justify Rust compile times.
- Frontends serving lots of HTML — consider `leptos`/`dioxus` ecosystems.

## Content

| File | What's inside |
|------|---------------|
| `content/01-handler-pattern.xml` | Extractor ordering, request/response DTO shape, validator derives. |
| `content/02-app-error.xml` | AppError enum with thiserror, IntoResponse impl, public message scrubbing. |
| `content/03-rules.xml` | Rules and antipatterns: no &str params, no unwrap, cargo check loop. |

## Templates

| File | Purpose |
|------|---------|
| `templates/app_error.rs` | Full AppError enum with IntoResponse (thiserror + axum). |
| `templates/handler_example.rs` | CRUD handler set: list, get, create, update, delete. |
