# Go Error Handling

## Summary

Typed error taxonomy for Go services: a project-wide `AppError` struct with code, message, HTTP status, and wrapping chain, plus a central Gin middleware that converts domain errors to structured JSON. Every error crossing a layer boundary must be wrapped, typed, and logged exactly once at the handler boundary.

## Why

Go's `error` interface carries no metadata. Without a typed wrapper, handlers make ad-hoc status decisions, logs miss correlation, and API responses are inconsistent. A single `AppError` struct + error catalog prevents the three most common drift patterns: untyped 500s, double-logging, and leaking internal messages to clients.

## When To Use

- Establishing a project-wide error policy on a new Go service.
- Refactoring legacy `fmt.Errorf` strings into typed, classifiable errors.
- Adding centralized error-handler middleware mapping domain errors to JSON + logs + traces.
- Building `errors.Is` / `errors.As` predicates for cross-package error checks.

## When NOT To Use

- Library code for external consumers — exposing `AppError` leaks internals; use small sentinels.
- Tiny CLIs / one-shot scripts — `fmt.Errorf("%w", err)` plus exit code is enough.
- Teams already standardized on `pkg/errors` or `cockroachdb/errors` — don't fork.
- Greenfield where Go 1.20+ `errors.Join` + `%w` already covers the wrapping needs.

## Content

| File | What's inside |
|------|---------------|
| `content/01-error-types.xml` | AppError struct, sentinel vars, factory constructors, Code predicate helper. |
| `content/02-middleware.xml` | Gin error-handler middleware pattern and multi-error pitfalls. |
| `content/03-rules.xml` | Wrapping, logging, and linting rules with antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/apperror.go` | Full `apperror` package: AppError, sentinels, Wrap, IsCode predicate. |
| `templates/error_middleware.go` | Gin ErrorHandler middleware mapping AppError to JSON. |
