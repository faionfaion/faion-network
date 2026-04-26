# Rust HTTP Handlers

## Summary

Type-safe HTTP handler pattern for Axum (and Actix-web/Poem) using extractors, typed `AppState`, validated request DTOs, and a single `AppError` that implements `IntoResponse`. Handlers stay thin — they parse, delegate to a `Service`, and map results.

## Why

Rust's type system eliminates entire categories of runtime errors, but only if the handler boundary is correctly typed. Without a unified `AppError`, validation errors and DB errors leak as 500s. Without `State<AppState>`, sharing DB pools requires unsafe globals. Thin handlers that delegate to `Service` keep business logic testable without an HTTP runtime.

## When To Use

- Building a new Axum/Actix-web/Poem HTTP service
- Migrating a hot endpoint from Python/Node into Rust for latency or memory wins
- Greenfield auth gateway, image proxy, websocket fan-out, or Wasm-edge handler
- Any project using `sqlx`/`sea-orm`/`diesel` that needs type-safe handler-to-DB wiring

## When NOT To Use

- Rapid-prototype CRUD where iteration speed beats latency — Python/TS ships 5x faster
- Heavy ORM workloads with rapidly evolving schemas (`sqlx query!` macros require migrations to compile)
- Plugins or scripting hooks where dynamic dispatch is the requirement
- Polyglot services with zero Rust experience on the team — operational cost dominates

## Content

| File | What's inside |
|------|---------------|
| `content/01-handler-rules.xml` | Core rules: thin handlers, unified AppError, extractor ordering, validator integration |
| `content/02-examples.xml` | Worked CRUD handler set (list/get/create/update/delete) with AppState injection |

## Templates

| File | Purpose |
|------|---------|
| `templates/handler-test.rs` | `tower::ServiceExt::oneshot` integration test skeleton |
