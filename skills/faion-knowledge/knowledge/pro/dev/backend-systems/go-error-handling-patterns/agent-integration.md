# Agent Integration — Go Error Handling Patterns

## When to use
- New Go service or package where error contracts must be stable for callers (sentinel errors, custom error types).
- Refactoring a codebase that uses `errors.New(fmt.Sprintf(...))` instead of `fmt.Errorf("...: %w", err)` for wrapping.
- Wiring `errors.Is` / `errors.As` checks at HTTP/gRPC boundaries to map domain errors to status codes.
- Adding retry-with-backoff and panic-recovery middleware for production handlers.
- Aggregating validation errors via `errors.Join` (Go 1.20+) or a `MultiError` type.

## When NOT to use
- Quick scripts, code generators, `main` packages where `log.Fatalf` is acceptable on first error.
- Test helpers — `t.Fatal(err)` is preferred over wrapping.
- Code that interacts only with the standard library and never returns an error to a caller (e.g., a closing `defer` with no caller to inspect).

## When NOT to use (continued)
- When upgrading a legacy package that has stable public sentinel errors — changing them is a breaking change.

## Where it fails / limitations
- `fmt.Errorf("...: %w", err)` only wraps one error; pre-1.20 there is no native multi-wrap. Agents often fake it via string concat, losing `errors.Is`.
- LLMs default to `errors.New("not found")` per call, breaking `errors.Is` matching — every site allocates a new error.
- `errors.As` requires a pointer to a pointer for typed errors; agents pass a value and the call silently fails to match.
- Panic recovery middleware can hide bugs if it swallows the stack trace; agents may strip `runtime/debug.Stack()` to "clean up logs".
- Wrapping the same error twice with the same context produces noisy chains; without discipline, logs become unreadable.
- Sentinel errors from third-party libs (e.g., `sql.ErrNoRows`, `pgx.ErrNoRows`, `mongo.ErrNoDocuments`) leak storage details upward; agents forget to translate at the repository boundary.

## Agentic workflow
The pattern is mechanical enough to drive with a coding subagent: define one `apperror` package with sentinel vars and a typed `AppError`, then sweep handlers/services to use `errors.Is`/`errors.As` at the right layer. Reviewer agent must confirm: errors are wrapped exactly once per layer with `%w`, no duplicate logging-then-returning, and storage-layer sentinels never escape the repository. Retry helpers should be generic `func[T any]` (Go 1.18+) with explicit `Retryable` interface.

### Recommended subagents
- `faion-sdd-executor-agent` — apply error-package template, sweep packages, run `go vet` + `errcheck`.
- General reviewer subagent — flag `_ = err`, `log.Printf(err); return err`, missing `%w`, and bare `errors.New` in hot paths.
- `password-scrubber-agent` — strip secrets from wrapped error messages before they reach logs.

### Prompt pattern
Plan: "Create `internal/apperror` with sentinels (`ErrNotFound`, `ErrUnauthorized`, `ErrValidation`, `ErrConflict`) and an `AppError` struct with `Code/Message/Status/Details/Err` and `Unwrap()`. Replace all bare `errors.New` in handlers with sentinel-or-AppError. Show diff."

Review: "Audit `**/*.go` for: (1) `fmt.Errorf` without `%w`, (2) returning unwrapped third-party storage errors, (3) `log.X(err); return err` duplication, (4) missing panic recovery on HTTP handlers. Output file:line + fix."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go vet` | Catches `Errorf` format mismatches | bundled with go |
| `errcheck` | Finds ignored error returns | go install github.com/kisielk/errcheck@latest |
| `staticcheck` | SA-rules covering wrap mistakes (SA4006, SA1019) | go install honnef.co/go/tools/cmd/staticcheck@latest |
| `golangci-lint` | Aggregates `errcheck`, `errorlint`, `wrapcheck`, `nilerr` | golangci-lint.run |
| `errorlint` | Specifically: missing `%w`, type-assertion vs `errors.As` | github.com/polyfloyd/go-errorlint |
| `wrapcheck` | Ensures external errors are wrapped at boundaries | github.com/tomarrell/wrapcheck |
| `gofmt` / `goimports` | Auto-format wrapped error chains | bundled / `golang.org/x/tools` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Sentry | SaaS | Yes | `sentry-go` captures wrapped chains; one init in `main` |
| Datadog APM | SaaS | Yes | `dd-trace-go` adds error tags to spans automatically |
| OpenTelemetry + Tempo/Jaeger | OSS | Yes | `otelhttp` middleware records error attribute on spans |
| Loki + Promtail | OSS | Yes | `slog` JSON handler ships error chain as structured field |
| BetterStack | SaaS | Yes | HTTP log drain, agent only needs token |

## Templates & scripts
See `templates.md` for `apperror` package, retry-with-backoff, and HTTP handler error mapper. Lint gate:

```bash
#!/usr/bin/env bash
# scripts/check-errors.sh — pre-commit error-handling gate
set -euo pipefail
go vet ./...
errcheck -ignoretests ./...
golangci-lint run --enable=errorlint,wrapcheck,nilerr,errcheck,gocritic ./...
# Forbid storage sentinels leaking to public packages
if rg -nP '(sql|pgx|mongo)\.Err(NoRows|NoDocuments)' --glob '!internal/repo/**' --glob '!internal/storage/**'; then
  echo "Storage sentinel leaked outside repository layer"
  exit 1
fi
```

## Best practices
- Wrap once per layer with `%w` and a verb describing what THIS layer was doing ("getting user %s: %w").
- Translate storage sentinels (`sql.ErrNoRows`) into your domain sentinels (`apperror.ErrNotFound`) at the repository boundary.
- Keep `AppError.Status` private to the HTTP edge — services should not know about HTTP codes.
- Use `errors.Join(errs...)` for validation aggregation in Go 1.20+ rather than a custom `MultiError`.
- Log at exactly one place per error (the top-level handler); intermediate layers wrap and return.
- Tag retryable errors via an interface (`type Retryable interface { Retryable() bool }`) so callers can check without sniffing strings.

## AI-agent gotchas
- Models default to `fmt.Errorf("err: %v", err)` — silently dropping `errors.Is` chain. Force `%w` in code review.
- Agents add `if err != nil { log.Printf(...); return err }` everywhere, producing duplicate log lines per request. Require log-then-return only at the outermost handler.
- LLMs love to invent new sentinel errors per file; require a single `apperror` package and reject duplicates.
- `errors.As(err, &someErr)` where `someErr` is a value type fails silently — agent should always pass a pointer to a pointer for struct errors.
- Panic recovery middleware generated by AI often forgets `debug.Stack()`, hiding the real cause.
- Retry loops generated by agents commonly retry non-retryable errors (4xx) — explicit `Retryable` interface prevents this.
- When wrapping context cancellation, agents may bury `context.Canceled`; preserve it via `errors.Is(err, context.Canceled)` checks at the top.

## References
- Go blog: Error handling — https://go.dev/blog/error-handling-and-go
- Go 1.13 errors — https://go.dev/blog/go1.13-errors
- Go 1.20 `errors.Join` — https://pkg.go.dev/errors#Join
- Dave Cheney: Don't just check errors — https://dave.cheney.net/2016/04/27/dont-just-check-errors-handle-them-gracefully
- Uber Go Style Guide (errors) — https://github.com/uber-go/guide/blob/master/style.md#errors
- `errorlint` — https://github.com/polyfloyd/go-errorlint
- `wrapcheck` — https://github.com/tomarrell/wrapcheck
