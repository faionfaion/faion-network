# Agent Integration — Go Error Handling

## When to use
- Establishing a project-wide error policy (typed `apperror.AppError`, codes, HTTP status mapping) on a new Go service.
- Refactoring legacy `fmt.Errorf` strings into wrapped, typed, classifiable errors that the HTTP layer can render consistently.
- Adding a centralized error-handler middleware that maps domain errors to JSON responses + structured logs + traces.
- Building error sentinels and `errors.Is` / `errors.As` predicates for cross-package error checks.

## When NOT to use
- Library code intended for external consumers — exposing your `AppError` type leaks internals; library errors should be small, plain, and use `errors.Is/As`-friendly sentinels.
- Tiny CLIs / one-shot scripts — `fmt.Errorf("%w", err)` plus an exit code is enough; full error taxonomy is overkill.
- Anywhere the team has standardized on another error library (`pkg/errors`, `cockroachdb/errors`, `joeshaw/multierror`); don't fork.
- Greenfield where Go 1.20+ `errors.Join` + `%w` already covers the wrapping needs without a custom struct.

## Where it fails / limitations
- The README's `AppError.Error()` includes the wrapped error text; if you log `err.Error()` AND log `err` with structured logger, you double-log and may leak PII.
- Sentinel pattern (`var ErrNotFound = &AppError{...}`) is mutable — anyone with a pointer can change the message at runtime. Prefer value sentinels or factory functions only.
- `Wrap(err, msg)` always returns 500 — agents call it on user errors and lose the right HTTP status (validation 400, not-found 404).
- `errors.Is` against pointer sentinels works only because of pointer identity; if a goroutine reconstructs the same struct via JSON or copy, identity breaks.
- The middleware reads `c.Errors.Last()` only — if a handler appended multiple errors, earlier ones are dropped silently.
- Error message localization isn't covered; agents shipping multilingual APIs will hardcode English in `apperror.Message`.

## Agentic workflow
Treat errors as a typed subsystem on par with handlers and repositories. One agent designs the error catalog (codes, HTTP statuses, log severity) as a single Markdown table; another wires the middleware and adapter functions; a reviewer agent (Opus) walks every `return err` in handlers and verifies the error is typed, wrapped, and logged exactly once. Force `errcheck` and `errorlint` in CI to make missing wrappings fail at compile time.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the SDD task; quality gates should add `errcheck` + `golangci-lint --enable=errorlint,wrapcheck`.
- A custom `error-policy-reviewer` (Opus, read-only) — given the diff, list every `return err`. For each, verify typed wrapper, code, HTTP status, log severity. Reject any "untyped" rows.
- `password-scrubber-agent` — error messages frequently embed connection strings or tokens.

### Prompt pattern
```
Add error type <ErrCheckoutClosed> to apperror.
Deliverables: (1) constructor `NewCheckoutClosed(orderID string) *AppError` with code, message, HTTPStatus, (2) sentinel `ErrCheckoutClosed` predicate via errors.Is, (3) test that `errors.Is(wrapped, ErrCheckoutClosed)` is true after fmt.Errorf("%w", ...).
Then update the order service to return this error and add a middleware test asserting the JSON body and status code.
```

```
Audit handlers/. For each `return err`: classify as typed/untyped, identify code and HTTP status, list all log statements that mention it. Output JSON. Reject rows where untyped=true OR log_count != 1.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `errcheck` | Forbid ignored returns | https://github.com/kisielk/errcheck |
| `errorlint` | Enforce `%w` / `errors.Is/As` style | https://github.com/polyfloyd/go-errorlint |
| `wrapcheck` | Require errors crossing package boundaries to be wrapped | https://github.com/tomarrell/wrapcheck |
| `nilerr` | Catch `if err != nil { return nil }` mistakes | https://github.com/gostaticanalysis/nilerr |
| `staticcheck` (SA4006, SA1019) | Misc error misuse | https://staticcheck.dev/ |
| `golangci-lint` | Aggregator with all of the above | https://golangci-lint.run/ |
| Sentry CLI | Upload sourcemaps / releases | https://docs.sentry.io/cli/ |
| `delve` | Inspect error chains in panics | https://github.com/go-delve/delve |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS | Yes | `sentry-go` integrates with `apperror.Unwrap`; agents auto-tag `code` + `http_status`. |
| Rollbar | SaaS | Yes | Similar to Sentry; weaker Go SDK ergonomics. |
| Datadog Error Tracking | SaaS | Yes | Reads OTel error spans; pair with `otelhttp` instrumentation. |
| Honeycomb | SaaS | Yes | Trace-first; errors as span events with `error.type` + `error.message`. |
| OpenTelemetry SDK | OSS | Yes | Vendor-neutral; agent should `span.RecordError(err)` + set status. |
| `cockroachdb/errors` | OSS | Yes | Richer than stdlib (stack traces, telemetry codes); good when stdlib feels thin. |
| `pkg/errors` | OSS | Partial | Pre-Go-1.13; agents will reach for it out of habit — prefer stdlib + `cockroachdb/errors`. |

## Templates & scripts
See `templates.md` for the full `apperror` package + middleware. Recommended additions to the README skeleton:

```go
// internal/apperror/predicate.go
package apperror

import "errors"

// Predicate helpers so callers can use errors.Is on category, not pointer identity.
type Code string

const (
    CodeNotFound     Code = "NOT_FOUND"
    CodeUnauthorized Code = "UNAUTHORIZED"
    CodeValidation   Code = "VALIDATION_ERROR"
    CodeConflict     Code = "CONFLICT"
)

func IsCode(err error, code Code) bool {
    var ae *AppError
    if !errors.As(err, &ae) {
        return false
    }
    return Code(ae.Code) == code
}

// Use: if apperror.IsCode(err, apperror.CodeNotFound) { ... }
```

## Best practices
- One error catalog per service, committed as Markdown next to the `apperror` package — agents read it before adding new codes.
- Wrap at every layer boundary with `fmt.Errorf("user lookup: %w", err)`. The wrapping prefix tells the SRE who's calling whom in the chain.
- Log errors exactly once, at the boundary that decides the HTTP/RPC response. Earlier logs duplicate noise.
- Never embed secrets or full SQL into error messages — those bubble to clients via the middleware. Use `apperror.Internal(err)` to swap the message and keep the chain.
- Use `errors.Is` with a `Code` predicate, not pointer identity, so deserialized errors still match.
- Distinguish *expected* domain errors (404, 409, 422) from *unexpected* errors (5xx). Only the latter should page on-call.
- Integrate with tracing: every error crossing the handler boundary should `span.RecordError(err)` and `span.SetStatus(codes.Error, ...)`.

## AI-agent gotchas
- LLMs return raw `err.Error()` to clients ("pq: duplicate key value violates unique constraint ..."). Always intercept in middleware.
- Agents conflate `errors.Is` (sentinel) and `errors.As` (type assertion). Force code review to check the right one is used.
- `Wrap(err, msg)` is overused as a generic wrapper; agents apply it to *every* error and lose the original HTTP status. Provide typed wrappers (`AsValidation`, `AsConflict`, `AsInternal`).
- Agents `panic` on unexpected errors instead of returning them. Block any `panic(` in handlers.
- `errors.Join` (Go 1.20+) — agents trained on older corpora reach for `multierror` deps; default to `errors.Join`.
- Stack traces: stdlib errors don't carry stacks. Decide once whether to use `cockroachdb/errors` for stacks; either way, document the choice — agents will mix libraries otherwise.
- Human-in-loop checkpoint: any new error code that surfaces to clients (especially with PII or status code change) needs reviewer sign-off — these are part of the API contract.

## References
- Go blog: error wrapping — https://go.dev/blog/go1.13-errors
- Effective Go: errors — https://go.dev/doc/effective_go#errors
- "Failure is your domain" (Cockroach Labs) — https://www.cockroachlabs.com/blog/error-handling-and-go-1-13/
- Uber error guidelines — https://github.com/uber-go/guide/blob/master/style.md#errors
- errorlint rules — https://github.com/polyfloyd/go-errorlint
- OpenTelemetry semantic conventions for errors — https://opentelemetry.io/docs/specs/semconv/exceptions/
