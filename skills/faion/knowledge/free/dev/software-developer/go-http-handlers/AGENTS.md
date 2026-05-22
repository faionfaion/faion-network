---
slug: go-http-handlers
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces thin Go HTTP handlers (Gin/Echo/net-http) with explicit Recovery>Logger>RequestID>Auth middleware order, ShouldBindJSON request structs, c.Request.Context() propagation, and a graceful-shutdown wrapper.
content_id: "go-http-handlers-fb07"
complexity: medium
produces: code
est_tokens: 4100
tags: [go, gin, echo, net-http, middleware, graceful-shutdown]
---
# Go HTTP Handlers

## Summary

**One-sentence:** Produces thin Go HTTP handlers (Gin/Echo/net-http) with explicit Recovery>Logger>RequestID>Auth middleware order, ShouldBindJSON request structs, c.Request.Context() propagation, and a graceful-shutdown wrapper.

**One-paragraph:** Build production HTTP services in Go with explicit middleware composition (use `gin.New()` not `gin.Default()`), single-purpose middlewares (Recovery first, Logger, RequestID, then auth and domain), thin handlers that only bind → validate → call one service method → translate to HTTP, validation via struct binding tags (`binding:"required,email"`), `c.Request.Context()` plumbed to every service/repo call, and explicit `ReadHeaderTimeout` + `ReadTimeout` + `WriteTimeout` + `IdleTimeout` on `http.Server`. Wrap the server in a SIGINT/SIGTERM handler that calls `srv.Shutdown(ctx)` with a 10-15s drain.

**Ефективно для:** new Go HTTP services, refactors where handlers contain business logic or capture gin.Context in goroutines, services missing graceful shutdown or timeouts, agent-generated scaffolds that default to `gin.Default()`.

## Applies If (ALL must hold)

- Building/refactoring a Go HTTP service (Gin, Echo, or net/http).
- Service has clear handler / service / repository layers (or will adopt them via `[[go-backend]]`).
- Team agrees to explicit middleware composition (no `gin.Default()`).
- Service must drain in-flight requests on shutdown.

## Skip If (ANY kills it)

- gRPC service — different middleware model.
- Lambda / serverless function handlers — no long-lived http.Server.
- Pure library code without an HTTP layer.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Framework choice | gin / echo / net-http | tech stack ADR |
| Timeout budget | seconds (read/write/idle) | infra/SRE ADR |
| Auth scheme | JWT/cookie/none | security ADR |
| Logger | slog/zap/zerolog | observability ADR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-backend]]` | Provides the layered layout and ErrorHandler middleware. |
| `[[go-error-handling]]` | AppError translation lives in a middleware that this layer registers. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: explicit middleware order, gin.New, ctx propagation, no Background in handler, no goroutine capturing c, thin handlers, binding-tag validation, server timeouts | ~800 |
| `content/02-output-contract.xml` | essential | Required server.go shape (middleware order, timeouts, shutdown) + handler shape | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: gin.Default, ctx.Background, handler-spawned goroutine on c.Request.Context, business logic in handler, default timeouts | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure to build server.go + first handler | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "Is this an HTTP service that owns its lifecycle?" | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold server.go (Wire + Run) | sonnet | Pattern-driven. |
| Generate one handler from spec | sonnet | bind+validate+service+translate. |
| Audit handler thinness | sonnet | Line-count + branching check. |
| Diagnose goroutine ctx-leak | opus | Concurrency reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/server.go` | Wire(cfg) -> *http.Server with timeouts; Run(ctx) with graceful shutdown. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-http-handlers.py` | Grep for `gin.Default`, `ctx.Background()`, missing timeouts, business logic in handler files. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[go-backend]]` — overall layout
- `[[go-error-handling]]` — middleware translation
- `[[go-concurrency]]` — never capture c in goroutines

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: HTTP service yes/no, owns lifecycle yes/no, explicit middleware composition allowed yes/no.
