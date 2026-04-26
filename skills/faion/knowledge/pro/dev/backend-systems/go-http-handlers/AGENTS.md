# Go HTTP Handlers (Gin/Echo/Chi/stdlib)

## Summary

HTTP handler pattern for Go: handlers as methods on a dependency-injecting struct, request DTOs with `binding`/`validate` tags, typed response structs, RFC 7807 error mapping, and `httptest`-based table-driven tests. Framework choice (Gin, Echo, Chi, stdlib 1.22 muxer) is locked per project and never mixed mid-file.

## Why

Go HTTP services accumulate three failure modes without this pattern: package-level globals for dependencies (not testable), raw `err.Error()` in JSON responses (leaks internals), and handler-level string-building (inconsistent API surface). Structuring handlers as methods on a struct makes dependency injection, testing, and code generation straightforward.

## When To Use

- Building a JSON REST API with Gin, Echo, Chi, or stdlib `net/http` 1.22+.
- Migrating between routers with a consistent handler shape.
- Wiring middleware (auth, request ID, recovery, CORS, rate limit, tracing) idiomatically.
- Generating CRUD handlers from a schema (OpenAPI, sqlc) where shape is repetitive.

## When NOT To Use

- gRPC services — use `grpc-go` and interceptors.
- WebSocket-first apps — `gorilla/websocket` or `nhooyr.io/websocket`.
- Static asset serving — `http.FileServer` or a CDN.
- Streaming/SSE-heavy endpoints — drop to `http.ResponseWriter` directly for Gin.
- Stdlib-only constraints on new services (1.22 muxer preferred without a framework dep).

## Content

| File | What's inside |
|------|---------------|
| `content/01-router-setup.xml` | Gin and Echo router setup, middleware order, group/subrouter patterns. |
| `content/02-handler-pattern.xml` | Handler struct, request DTO binding, RFC 7807 error mapping, response DTOs. |
| `content/03-rules.xml` | Middleware order rules, framework-mixing antipatterns, testing guidelines. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gin_router.go` | Gin router with middleware stack and user CRUD route group. |
| `templates/stdlib_handler.go` | stdlib 1.22 muxer pattern: App struct, routes(), writeJSON, writeProblem. |
