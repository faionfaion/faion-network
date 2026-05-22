---
slug: rust-http-handlers
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Handler pattern for Axum (and Actix-web): typed request/response DTOs with validator derives, shared AppState behind Arc, AppError enum implementing IntoResponse, and #[tracing::instrument] on every handler.
content_id: "69913b3750141766"
tags: [rust, axum, http-handlers, web]
---
# Rust HTTP Handlers (Axum)

## Summary

**One-sentence:** Handler pattern for Axum (and Actix-web): typed request/response DTOs with validator derives, shared AppState behind Arc, AppError enum implementing IntoResponse, and #[tracing::instrument] on every handler.

**One-paragraph:** Handler pattern for Axum (and Actix-web): typed request/response DTOs with validator derives, shared AppState behind Arc, AppError enum implementing IntoResponse, and #[tracing::instrument] on every handler. Handlers return Result<Json<Resp>, AppError>; extractors are ordered body-last.

## Applies If (ALL must hold)

- Building JSON REST APIs with Axum or Actix-web.
- Refactoring loosely-typed handlers into the request-DTO / service-call / response-DTO layered pattern.
- Adding validator-based request validation and typed error responses.
- Implementing streaming responses (SSE, WebSocket) with Tokio.
- Wiring middleware: tracing, CORS, auth, rate limiting via tower-http.

## Skip If (ANY kills it)

- High-throughput RPC where Tonic (gRPC) is a better fit.
- Async-light scripts and CLIs — reqwest + tokio without a server framework.
- Teams with more comfort in Go/Python where perf gain doesn't justify Rust compile times.
- Frontends serving lots of HTML — consider leptos/dioxus ecosystems.

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
