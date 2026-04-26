# Go Backend

## Summary

Production-grade Go backend pattern using the standard `cmd/` + `internal/` project layout with Gin or Echo routers. Key conventions: interfaces defined at the consumer side, `context.Context` as first arg on all I/O functions, typed `AppError` mapped to HTTP via middleware, worker-pool concurrency via a `Pool` struct with channel-based job queue.

## Why

The `internal/` boundary prevents circular imports and keeps domain packages isolated. Consumer-side interfaces (service defines `UserRepository`, repository provides the impl) enable mockable unit tests without reflection-based mocking. Typed errors with `Unwrap()` let callers use `errors.Is` / `errors.As` for clean control flow. Worker pool decouples job submission from execution and supports graceful shutdown via `context.Context`.

## When To Use

- Greenfield Go service scaffolding with `cmd/` + `internal/handler/service/repository` layers.
- Adding endpoints to an existing Gin/Echo project following this layout.
- Generating typed `AppError` taxonomies and error-handler middleware.
- Building worker-pool / fan-out-fan-in glue code around a typed `Job` interface.

## When NOT To Use

- Non-standard layouts (Hex / Clean / monorepo multi-module) — import paths will be wrong.
- Performance-critical hot paths needing `sync.Pool` or escape-analysis awareness.
- Cgo / unsafe / kernel-bypass code — out of scope.
- Generics-heavy domain libraries — examples use pre-generics style.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Project layout, `cmd/` + `internal/` rules, interface-at-consumer rule, request DTO separation. |
| `content/02-http.xml` | Gin router setup, Echo router setup, request binding with validation tags, error handler middleware. |
| `content/03-concurrency.xml` | Worker pool implementation, fan-out/fan-in pattern, context propagation rules. |
| `content/04-errors.xml` | `AppError` struct with `Unwrap`, sentinel vars, constructors, HTTP mapping middleware. |

## Templates

| File | Purpose |
|------|---------|
| `templates/app-error.go` | `AppError` struct with sentinel errors and constructors. |
| `templates/check-layout.sh` | CI script: verify required `internal/` dirs exist and `internal/` is not imported from outside. |
