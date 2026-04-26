# Go Error Handling Patterns

## Summary

Go error handling convention for services: define all sentinel errors and custom types in one `apperror` package; wrap every error with operation context using `fmt.Errorf("op: %w", err)`; check errors with `errors.Is`/`errors.As`, never `==`; map domain errors to HTTP/gRPC codes only at the transport edge; log once at the boundary, never log-and-return. Enforce with `errcheck`, `errorlint`, and `wrapcheck` in CI.

## Why

Bare `errors.New("failed")` without context makes stack traces useless in production. `%v` formats without wrapping — `errors.Is` cannot traverse the chain. Logging + returning creates duplicate Sentry events. Centralizing sentinels in one `apperror` package makes the domain error contract explicit and prevents `sql.ErrNoRows` from leaking into business logic. Linters catch the 80% of violations LLMs reproduce from pre-1.13 training data.

## When To Use

- Designing error contracts for new Go services (HTTP, gRPC, CLI)
- Refactoring legacy Go code that returns bare errors without context
- Auditing for double-wrapping, swallowed errors, or missing `errors.Is`/`errors.As`
- Mapping domain sentinel errors to HTTP status codes or gRPC codes
- Building structured error logging with `slog` + error attributes

## When NOT To Use

- Quick scripts where `log.Fatal` is acceptable
- One-shot migration scripts where error taxonomy investment is overkill

## Content

| File | What's inside |
|------|---------------|
| `content/01-error-rules.xml` | Wrapping rule, sentinel definition, errors.Is/As usage, log-once boundary rule |
| `content/02-examples-and-antipatterns.xml` | Good/bad examples for wrapping, HTTP mapping, multi-error aggregation, panic boundaries |

## Templates

| File | Purpose |
|------|---------|
| `templates/apperror.go` | Sentinel errors + AppError custom type + constructor functions + AsAppError helper |
| `templates/golangci.yml` | golangci-lint config enabling errcheck, errorlint, wrapcheck, nilerr, staticcheck |
