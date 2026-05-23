# Go Error Handling (typed AppError + middleware)

## Summary

**One-sentence:** Produces a Go error-handling pipeline (typed AppError, fmt.Errorf %w wrapping, repository boundary mapping, middleware translation, golangci-lint errorlint/wrapcheck) that yields consistent HTTP responses across the service.

**One-paragraph:** Define `AppError{Code, Message, HTTPStatus, Err}` implementing `Error()` and `Unwrap()` so `errors.Is/As` work through wrapping. Always wrap with `fmt.Errorf("context: %w", err)`, never `%v`. Map driver errors (pgx.ErrNoRows, sql.ErrNoRows) to AppError at the repository layer — never let driver errors reach handlers. Handlers return error; an HTTP middleware logs and translates AppError to JSON via `errors.As`. Panic recovery middleware runs BEFORE the error mapper. `golangci-lint` runs with errorlint, wrapcheck, errcheck, nilnil enabled.

**Ефективно для:** new Go services, refactors merging ad-hoc error shapes into one typed envelope, repos where driver errors leak to handlers or status codes get demoted on rewrap, services adopting structured logging tied to AppError fields.

## Applies If (ALL must hold)

- Service returns errors across layers (handler → service → repository).
- Team accepts one typed AppError and one translation middleware.
- golangci-lint can be added to CI with custom linters enabled.
- Errors must map to HTTP status codes deterministically.

## Skip If (ANY kills it)

- Pure library code that never reaches an HTTP boundary (use errors.Is/As only).
- Pre-1.13 Go codebase that cannot use `%w` wrapping (upgrade first).
- Generated code where errors are owned by a different layer (protoc-gen-* envelopes).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Layer list (handler/service/repository) | Markdown | `[[go-backend]]` layout |
| Driver list (pgx, sqlx, http clients) | Markdown | infra ADR |
| HTTP framework | string (gin/echo/net-http) | tech stack ADR |
| Logger | string (slog/zap/zerolog) | observability ADR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-backend]]` | Provides apperror/ package location and middleware wiring. |
| `[[go-http-handlers]]` | Handlers return error and use the translation middleware. |
| `[[error-handling]]` | Cross-language RFC 7807 envelope this maps onto. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: AppError shape, %w wrapping, repo boundary mapping, Handler+Wrap, panic-then-map order, lint config, constructors not mutable vars | ~800 |
| `content/02-output-contract.xml` | essential | Required apperror package shape + middleware order + lint config | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: %v wrapping, type assertion at HTTP boundary, driver errors leaking, mutable package vars, status demotion on rewrap | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure: scaffold pkg/apperror → wrap rules → repo mapping → middleware → lint gate | ~800 |
| `content/06-decision-tree.xml` | essential | Root question on Go service + HTTP layer | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold pkg/apperror | sonnet | Template-driven. |
| Boundary mapping for new driver | sonnet | Lookup table generation. |
| errors.Is/As migration from type assertions | opus | AST-level reasoning over wrap chains. |
| Lint config | haiku | Boilerplate YAML. |

## Templates

| File | Purpose |
|------|---------|
| `templates/apperror.go` | Drop-in pkg/apperror package: AppError type, constructors, Wrap helper. |
| `templates/error-middleware.go` | HTTP middleware translating AppError to JSON via errors.As. |
| `templates/prompt-error-scaffold.txt` | Prompt for sub-agent generating the apperror package + middleware. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-error-handling.py` | Verifies %w usage, no type assertions at HTTP boundaries, apperror.go shape. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[go-backend]]` — middleware order
- `[[go-http-handlers]]` — handler signatures
- `[[error-handling]]` — RFC 7807 cross-mapping

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: Go service with HTTP layer, %w available (Go 1.13+), team can install one translation middleware. Any "no" -> skip.
