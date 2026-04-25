# Agent Integration — Go Error Handling

Methodology defines a custom `AppError` type with code, message, HTTP status, wrapped error, plus middleware to translate to JSON responses. Use this file to drive the pattern from a Claude subagent without re-deriving conventions.

## When to use
- New Go HTTP service (chi/gin/echo/stdlib `net/http`) needing consistent JSON error responses.
- Refactor of a service that returns bare `errors.New(...)` everywhere — wrap into `AppError` with codes.
- Adding correlation IDs / trace IDs to error responses for production debugging.
- Standardizing error logging format (structured: `slog`, `zerolog`, `zap`) — `AppError.Error()` becomes the message field.
- Library code that wants typed errors callable via `errors.Is` / `errors.As` from consumers.

## When NOT to use
- gRPC services — use `google.golang.org/grpc/status` + `codes.Code`; `AppError.HTTPStatus` is meaningless there.
- CLIs — error responses aren't JSON; print to stderr and exit non-zero. Overhead not justified.
- Library packages exposed publicly — defining a custom error type forces consumers to depend on your package; prefer sentinel errors + `errors.Is`.
- Code with deep error paths where `fmt.Errorf("%w", err)` chains already do the job — adding `AppError` adds noise.
- Languages other than Go (this is Go-specific). For Python/TS, see `error-handling/` (RFC 7807).

## Where it fails / limitations
- **README is incomplete**: only shows the error type definition. Missing the middleware, how routes return `AppError`, how to use `errors.As(&AppError)` at boundaries.
- `AppError.HTTPStatus` is a mutable field on package-level vars (`ErrNotFound`, `ErrUnauthorized`). Returning the var directly + reassigning Status is a footgun (`*AppError` is shared).
- No stack traces — pure Go errors lose the call site. Pair with `github.com/cockroachdb/errors` or `golang.org/x/exp/errors` for stack capture.
- `Wrap` always sets `HTTPStatus: 500` — wrapping a 4xx becomes 5xx silently.
- `Code: "INTERNAL_ERROR"` hardcoded in `Wrap` overrides whatever was on the inner error. Lossy.
- No JSON marshaling of inner `Err` (`json:"-"`) — fine for security, but agents will wonder why the wrapped message is missing in responses.
- No mapping from `pgx`/`gorm` errors (`ErrNoRows`) to `AppError` — left as exercise; agents skip it.

## Agentic workflow
Drive Go error work as: (1) introduce `pkg/apperror` package with the README's `AppError`, (2) replace package-level mutable vars with constructor functions, (3) write a `pkg/httpx/middleware.go` recovery + error handler that calls `errors.As(err, &appErr)`, (4) update each handler to return `error` and use `apperror.New*` helpers, (5) add a `pkg/apperror/apperror_test.go` testing wrapping, code propagation, HTTP status mapping. Run `go vet ./...` + `staticcheck ./...` + `golangci-lint run --enable errorlint`.

### Recommended subagents
- `faion-code-agent` — Default for type/middleware scaffolding.
- `faion-backend-developer` (sibling skill) — Owns Go-specific idioms (panic vs error, sentinel errors, `errors.Is/As`).
- `faion-test-agent` — Writes table-driven error tests (`got = errors.As(err, &target)`).
- `faion-software-architect` — Decides package layout (`pkg/apperror` vs `internal/errors`).
- `faion-api-developer` — Aligns error responses with API contract (RFC 7807 vs custom shape).

### Prompt pattern
Introduce the package:

```
Create pkg/apperror with AppError type per
free/dev/software-developer/go-error-handling/README.md.
Fix three smells in README:
  1) Replace package-level mutable vars with constructor functions
     (NewNotFound, NewUnauthorized, NewValidation).
  2) `Wrap` must preserve the inner *AppError's HTTPStatus and Code if present.
  3) Add `WrapWithStatus(err, msg, status)` for explicit override.
Add table-driven tests covering errors.As, errors.Is, Unwrap chain depth.
Run: go test ./pkg/apperror/... -race -v.
```

Middleware:

```
Add pkg/httpx/error_middleware.go: chi middleware that
recovers panics, calls errors.As(err, &appErr), writes JSON:
{code, message, trace_id} with appErr.HTTPStatus.
Default to 500 + ErrInternal when no match. Log via slog with attrs
(code, status, trace_id, error). Return diff + go test output.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go vet` | Stdlib static analysis | bundled |
| `staticcheck` | Deeper static analysis (incl. SA9003 incorrect error wrapping) | https://staticcheck.io |
| `golangci-lint` | Aggregator (errcheck, errorlint, wrapcheck, ireturn) | https://golangci-lint.run |
| `errorlint` (in golangci-lint) | Catches `err == ErrX` instead of `errors.Is` | https://github.com/polyfloyd/go-errorlint |
| `wrapcheck` (in golangci-lint) | Forces wrapping of returned external errors | https://github.com/tomarrell/wrapcheck |
| `go test -race` | Race detector | bundled |
| `go test -run -count=1` | Disable test cache for error path tests | bundled |
| `gotestsum` | Friendlier test output, JUnit XML | https://github.com/gotestyourself/gotestsum |
| `delve` (`dlv`) | Debugger; inspect error chain at runtime | https://github.com/go-delve/delve |
| `errcheck` | Find unchecked errors | https://github.com/kisielk/errcheck |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Sentry Go SDK | SaaS APM | Yes — `sentry.CaptureException(err)` | Plays well with `errors.As` chains |
| Datadog APM | SaaS | Yes — `tracer.WithError` | Captures HTTPStatus tags from middleware |
| OpenTelemetry Go | OSS / SaaS-agnostic | Yes — `span.RecordError(err)` | Emit error code as span attribute |
| Honeycomb | SaaS | Yes — OTel-native | Best for high-cardinality `error.code` field |
| Rollbar | SaaS | Yes — Go SDK | Older but stable |
| GitHub Actions | CI | Yes — run `golangci-lint` on PR | Cache `~/.cache/go-build` |

## Templates & scripts
README covers the type. Add this missing middleware (≤45 lines):

```go
package httpx

import (
    "encoding/json"
    "errors"
    "log/slog"
    "net/http"

    "yourmod/pkg/apperror"
)

type errBody struct {
    Code    string `json:"code"`
    Message string `json:"message"`
    TraceID string `json:"trace_id,omitempty"`
}

type Handler func(http.ResponseWriter, *http.Request) error

func Wrap(h Handler) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        err := h(w, r)
        if err == nil {
            return
        }
        var appErr *apperror.AppError
        if !errors.As(err, &appErr) {
            appErr = apperror.Wrap(err, "internal error")
        }
        slog.ErrorContext(r.Context(), "http error",
            "code", appErr.Code,
            "status", appErr.HTTPStatus,
            "err", err,
        )
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(appErr.HTTPStatus)
        _ = json.NewEncoder(w).Encode(errBody{
            Code: appErr.Code, Message: appErr.Message,
            TraceID: TraceIDFromCtx(r.Context()),
        })
    }
}
```

## Best practices
- **Sentinel + custom-type hybrid.** Use sentinel `var ErrUserExists = errors.New("user exists")` for matching, wrap into `*AppError` at the HTTP boundary. Don't expose `*AppError` from domain packages.
- **Always wrap with `%w`**: `fmt.Errorf("create user: %w", err)`. Lets `errors.Is`/`errors.As` work across layers.
- **Don't return README's mutable package vars directly.** Replace `return ErrNotFound` with `return apperror.NewNotFound("user")` — avoids accidental Status mutation across requests.
- **Map driver errors at the repo layer.** `pgx.ErrNoRows` → `apperror.NewNotFound(...)`; never let `pgx.*` leak to handlers.
- **Add stack traces on `Wrap`.** Use `runtime.Caller` or `cockroachdb/errors.WithStack`. Without it, prod logs are useless.
- **Code field is API-stable contract.** Treat changes as breaking. Document codes in `docs/api/errors.md`.
- **Distinguish 4xx and 5xx logging levels**: 4xx → `slog.Info`/`Warn`, 5xx → `slog.Error` + Sentry capture. Don't page on 404s.
- **`errors.As(err, &target)` not `err.(*AppError)`** — the type assertion ignores wrapping.
- **One error package per service.** Don't import another service's error types — copy or share via a shared kernel module.
- **Test the unhappy paths** with table-driven tests covering each `apperror.New*` constructor + `Wrap` chain.

## AI-agent gotchas
- **README's package-level vars are bombs.** `apperror.ErrNotFound.Message = "X"` mutates the global. An LLM will eventually do this; gate via constructors.
- **`Wrap` clobbers status to 500.** Wrapping `ErrUnauthorized` (401) becomes 500 — silent regression. Make `Wrap` preserve inner `*AppError` fields when present.
- **`%w` vs `%v`** — `%v` formats but doesn't wrap. `errors.Is` / `errors.As` returns false; agents debug for hours. errorlint catches it.
- **JSON marshaling silently drops `Err`** (`json:"-"`). When debugging, log the chain via `fmt.Sprintf("%+v", err)` instead.
- **Panic recovery middleware order.** Recovery must run BEFORE error-mapping; otherwise panics return blank 500s with no body.
- **`errors.New` + sentinel + `Is`** works, but adding fields to a sentinel makes it impossible to have multiple distinct instances. Use a typed error if you need both matching and data.
- **Concurrent error handling**: `errors.Join` (Go 1.20+) preserves all errors; aggregators that just `fmt.Errorf("%w; %w", ...)` (pre-1.20) only preserve one.
- **Generic error stringification** (`err.Error()`) often leaks internal paths / stack info into 500 responses. Always sanitize messages on the way out.
- **`errcheck` is essential.** Without it, `_ = json.NewEncoder(w).Encode(body)` looks fine; the actual write error gets dropped, debugging in prod is hell.
- **golangci-lint defaults are minimal.** Enable `errorlint`, `wrapcheck`, `errname`, `nilnil` explicitly for this pattern to be enforced.
- **`Sentinel == Sentinel` works for unwrapped errors only.** Wrapping breaks `==`; replace with `errors.Is`. Pre-Go 1.13 code never updated.
- **HTTP status from `AppError` may conflict with framework defaults** (chi sets 200 if you call `WriteHeader` after writing body). Always set status BEFORE encoding body.

## References
- README: `./README.md`
- Sibling Go skills: `../go-backend/`, `../go-concurrency/`, `../go-http-handlers/`
- Cross-skill (general): `../error-handling/` (RFC 7807 — language-agnostic)
- Go errors blog: https://go.dev/blog/error-handling-and-go
- Working with Errors in Go 1.13+: https://go.dev/blog/go1.13-errors
- `errors.Is/As/Unwrap`: https://pkg.go.dev/errors
- cockroachdb/errors (stack traces): https://github.com/cockroachdb/errors
- errorlint: https://github.com/polyfloyd/go-errorlint
- wrapcheck: https://github.com/tomarrell/wrapcheck
- Slog (structured logging): https://pkg.go.dev/log/slog
