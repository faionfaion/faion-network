# Go Error Handling Patterns

## Summary

Wrap errors once per layer with `fmt.Errorf("verb context: %w", err)` to preserve the `errors.Is`/`errors.As` chain. Translate storage-layer sentinels (`sql.ErrNoRows`) into domain sentinels (`ErrNotFound`) at the repository boundary. Define one `apperror` package with sentinel vars and a typed `AppError` struct; never scatter `errors.New("not found")` per call site. Log errors at exactly one place per request — the outermost handler.

## Why

`fmt.Errorf("...: %v", err)` silently drops `errors.Is` chain. Per-call `errors.New` allocates a new pointer, breaking sentinel comparison. Logging-then-returning the same error at every layer produces duplicate log lines per request. These are the three most frequent LLM failure modes in Go error handling; they can be caught mechanically with `errorlint`, `wrapcheck`, and `errcheck` in CI.

## When To Use

- New Go service or package where error contracts must be stable for callers.
- Refactoring a codebase using `errors.New(fmt.Sprintf(...))` instead of `fmt.Errorf("...: %w", err)`.
- Wiring `errors.Is`/`errors.As` checks at HTTP/gRPC boundaries to map domain errors to status codes.
- Adding retry-with-backoff and panic-recovery middleware for production handlers.
- Aggregating validation errors via `errors.Join` (Go 1.20+) or a `MultiError` type.

## When NOT To Use

- Quick scripts or `main` packages where `log.Fatalf` on first error is acceptable.
- Test helpers — `t.Fatal(err)` is preferred over wrapping.
- Code that interacts only with the standard library and never returns an error to a caller.
- Legacy packages with stable public sentinel errors — changing them is a breaking change.

## Content

| File | What's inside |
|------|---------------|
| `content/01-wrapping-and-sentinels.xml` | `fmt.Errorf` with `%w`, sentinel vars, repository-boundary translation. |
| `content/02-custom-error-types.xml` | `AppError` struct with `Code/Message/Status/Details/Err`, constructor functions, `errors.As`. |
| `content/03-http-handlers.xml` | Handler error mapping, panic-recovery middleware, `MultiError` for validation. |
| `content/04-retry-and-antipatterns.xml` | Retry with exponential backoff, `Retryable` interface, antipatterns: ignored errors, log+return. |

## Templates

| File | Purpose |
|------|---------|
| `templates/check-errors.sh` | Pre-commit gate: `go vet`, `errcheck`, `golangci-lint` with `errorlint`/`wrapcheck`/`nilerr`. |
