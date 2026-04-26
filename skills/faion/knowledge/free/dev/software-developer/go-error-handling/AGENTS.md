# Go Error Handling

## Summary

Custom `AppError` type with `Code`, `Message`, `HTTPStatus`, and wrapped `Err` fields, plus HTTP
middleware that translates `*AppError` into structured JSON responses. Wrap external errors into
`AppError` at repository boundaries; use `errors.As` (never type assertions) to unwrap at the
HTTP layer.

## Why

Go's built-in errors carry no HTTP status, machine-readable code, or structured context. Without a
shared error type, each handler invents its own response shape, status mapping, and logging format.
A single `AppError` + middleware pattern enforces consistency and lets `errors.Is` / `errors.As`
work across wrapping chains.

## When To Use

- New Go HTTP service (chi / gin / echo / stdlib `net/http`) needing consistent JSON error responses
- Refactoring a service that returns bare `errors.New(...)` — wrap with `apperror.New*` constructors
- Adding correlation / trace IDs to error responses for production debugging
- Standardizing structured error logging (`slog`, `zerolog`, `zap`)
- Library code needing typed errors callable via `errors.Is` / `errors.As`

## When NOT To Use

- gRPC services — use `google.golang.org/grpc/status` + `codes.Code`; `HTTPStatus` is meaningless
- CLI tools — errors go to stderr + exit code; JSON overhead not justified
- Public library packages — custom error type forces consumers to depend on your package; prefer sentinel errors
- Shallow code paths where `fmt.Errorf("%w", err)` chains already do the job

## Content

| File | What's inside |
|------|---------------|
| `content/01-apperror-type.xml` | `AppError` struct, constructors, `Unwrap`, sentinel vars, wrapping rules |
| `content/02-middleware.xml` | HTTP middleware using `errors.As`, slog logging, JSON response encoding |
| `content/03-antipatterns.xml` | Mutable package vars, `Wrap` clobbering status, `%v` vs `%w`, type assertion pitfalls |

## Templates

| File | Purpose |
|------|---------|
| `templates/apperror.go` | `pkg/apperror` package: `AppError` type + constructors + `Wrap` |
| `templates/error-middleware.go` | `pkg/httpx/error_middleware.go`: recovery + `errors.As` handler |
| `templates/prompt-error-scaffold.txt` | Prompt to scaffold `apperror` package + middleware + tests |
