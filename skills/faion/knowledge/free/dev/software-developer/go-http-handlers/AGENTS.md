# Go HTTP Handlers (Gin / Echo)

## Summary

A methodology for building Go HTTP services with Gin or Echo: explicit middleware stack (Recovery first, then Logger, then RequestID), thin handlers that only bind → call service → translate to HTTP, request structs with `binding:"required,..."` tags, `c.Request.Context()` propagated to all downstream calls, and a graceful shutdown wrapper on SIGINT/SIGTERM. Choose Gin for ecosystem breadth; Echo for first-party middleware and interface-driven handlers.

## Why

Both frameworks are safe defaults but have subtle traps: `gin.Default()` double-registers Logger/Recovery, middleware order changes auth/logging semantics silently, and attaching goroutines to `c.Request.Context()` causes panics after the response returns. These are not caught by the compiler. Explicit middleware registration, thin handlers, and context propagation rules prevent the class of bugs that only appear in production under concurrent load.

## When To Use

- Building a Go HTTP service with ergonomic routing and middleware composition.
- Gin: JSON-heavy endpoints, gin-binding tag validation, broad middleware ecosystem.
- Echo: first-party JWT/CORS/rate-limit, interface-driven handlers, HTTP/2.
- Greenfield microservice on Linux/k8s where memory footprint matters.
- Migrating a Python/Node API to Go for throughput or cost reasons.

## When NOT To Use

- Go 1.22+ shops where `net/http` ServeMux supports method+path routing and the team prefers stdlib-only.
- `fasthttp`-backed routers (Fiber) where stdlib middleware compatibility is required.
- gRPC-first services — drive HTTP via `grpc-gateway` instead.
- One-off CLIs or five-route admin tools.
- Teams already standardized on chi, Fiber, or huma — do not mix routers.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Middleware order, thin handler rule, context propagation, timeout rules, no background goroutines tied to request |
| `content/02-examples.xml` | Gin router setup, Echo router setup, request binding struct, graceful shutdown wrapper |
| `content/03-antipatterns.xml` | Antipatterns: gin.Default() double-middleware, context.Background() in handlers, goroutine leak, CORS wildcard |

## Templates

| File | Purpose |
|------|---------|
| `templates/server.go` | Graceful shutdown wrapper: signal.NotifyContext + http.Server.Shutdown with drain timeout |
