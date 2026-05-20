---
slug: go-http-handlers
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: HTTP handler pattern for Go: handlers as methods on a dependency-injecting struct, request DTOs with binding/validate tags, typed response structs, RFC 7807 error mapping, and httptest-based table-driven tests.
content_id: "f153f4f0a4100705"
tags: [go, http, handlers, gin, echo]
---
# Go HTTP Handlers (Gin/Echo/Chi/stdlib)

## Summary

**One-sentence:** HTTP handler pattern for Go: handlers as methods on a dependency-injecting struct, request DTOs with binding/validate tags, typed response structs, RFC 7807 error mapping, and httptest-based table-driven tests.

**One-paragraph:** HTTP handler pattern for Go: handlers as methods on a dependency-injecting struct, request DTOs with binding/validate tags, typed response structs, RFC 7807 error mapping, and httptest-based table-driven tests. Framework choice (Gin, Echo, Chi, stdlib 1.22 muxer) is locked per project and never mixed mid-file.

## Applies If (ALL must hold)

- Building a JSON REST API with Gin, Echo, Chi, or stdlib net/http 1.22+.
- Migrating between routers with a consistent handler shape.
- Wiring middleware (auth, request ID, recovery, CORS, rate limit, tracing) idiomatically.
- Generating CRUD handlers from a schema (OpenAPI, sqlc) where shape is repetitive.

## Skip If (ANY kills it)

- gRPC services — use grpc-go and interceptors.
- WebSocket-first apps — gorilla/websocket or nhooyr.io/websocket.
- Static asset serving — http.FileServer or a CDN.
- Streaming/SSE-heavy endpoints — drop to http.ResponseWriter directly for Gin.
- Stdlib-only constraints on new services (1.22 muxer preferred without a framework dep).

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
