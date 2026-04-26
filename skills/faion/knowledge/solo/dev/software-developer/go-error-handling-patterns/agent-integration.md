# Agent Integration — Go Error Handling Patterns

## When to use
- Designing error contracts for new Go services (HTTP, gRPC, CLI)
- Refactoring legacy Go code that returns bare `errors.New("failed")` without context
- Auditing for double-wrapping, swallowed errors, or missing `errors.Is`/`errors.As` checks
- Mapping domain sentinel errors to HTTP status codes / gRPC `codes.*`
- Building structured error logging with `slog` + error attributes

## When NOT to use
- Languages with exception-based control flow (Python, Java, JS) — patterns differ
- Quick scripts where `log.Fatal` is acceptable
- One-shot migration scripts; investing in error taxonomy is overkill

## Where it fails / limitations
- `fmt.Errorf("%w", err)` only wraps a single error; for multi-error aggregation use `errors.Join` (Go 1.20+) — agents miss this and concat strings
- Sentinel errors leak across package boundaries: `errors.Is(err, sql.ErrNoRows)` requires importing `database/sql` everywhere — better wrap at repository layer with domain `ErrNotFound`
- `pkg/errors` (deprecated) coexists with stdlib `errors`; mixing them breaks `Unwrap` chain — agents grep both styles and confuse them
- `panic`/`recover` boundaries: a wrapped error from a goroutine never reaches `errors.Is` in the parent unless explicitly forwarded via channel
- Stack traces: stdlib `errors` does not capture them; need `cockroachdb/errors` or `pkg/errors` for traces
- Comparing wrapped errors with `==` instead of `errors.Is` is a silent bug LLMs reproduce from older training data

## Agentic workflow
Agents should treat errors as an audited interface: define sentinel errors and custom types in a single `apperror`/`domain/errors.go` file, then use `staticcheck` and `errcheck` to enforce no unhandled returns. A review subagent diffs handler-layer changes and asserts every error path either returns a wrapped error with context (`fmt.Errorf("op X: %w", err)`) or maps to a typed response. Use `golangci-lint` config in CI as the contract.

### Recommended subagents
- General-purpose subagent — implementation of error taxonomy + wrapping
- `faion-sdd-execution` — gate that runs `errcheck`, `staticcheck`, `golangci-lint` and forbids `_ = err`
- Code-review subagent — diff scan for `errors.New`+verb patterns, missing `%w`, `==` comparison on errors
- Test-writing subagent — generates `errors.Is`/`errors.As` table tests for each sentinel

### Prompt pattern
```
Refactor pkg/<name> error handling:
1. List all `return ... err` sites; for each ensure %w wrapping with the operation name.
2. Replace string-equality error checks with errors.Is/As.
3. Move ad-hoc errors.New into pkg/apperror as named sentinels.
4. Run `errcheck ./... && staticcheck ./...`; fix until clean.
Output a unified diff plus a table mapping old → new sentinels.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `errcheck` | Detect unchecked errors | `go install github.com/kisielk/errcheck@latest` |
| `staticcheck` | Lint incl. error patterns (SA1014, SA9003) | `go install honnef.co/go/tools/cmd/staticcheck@latest` |
| `golangci-lint` | Aggregator (errcheck, errorlint, wrapcheck) | https://golangci-lint.run |
| `errorlint` | Detects non-`%w` formatting + `==` comparisons | enabled inside golangci-lint |
| `wrapcheck` | Forces wrapping at layer boundaries | enabled inside golangci-lint |
| `nilerr` | Returns nil after non-nil err | enabled inside golangci-lint |
| `go vet` | Stdlib error verb mismatches | shipped with go |
| `cockroachdb/errors` | Stack-trace + Sentry hints | `go get github.com/cockroachdb/errors` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS | Yes (Go SDK) | Auto-extracts wrapped errors; benefits from `cockroachdb/errors` traces |
| Datadog APM / error tracking | SaaS | Yes | Tag spans with sentinel error names for grouping |
| Honeycomb | SaaS | Yes | Use error attribute on spans, not free-text |
| `slog` (stdlib) | OSS | Yes | Pair with `slog.Any("err", err)` and a custom `LogValuer` to expand wrapped chain |
| `zap` / `zerolog` | OSS | Yes | `.With(zap.Error(err))` flattens chain; ensure attribute names are stable |

## Templates & scripts
See `templates.md` for sentinel + custom-type packages and HTTP mapping middleware. Inline lint config to drop into a repo:

```yaml
# .golangci.yml — error-focused subset
linters:
  enable:
    - errcheck
    - errorlint
    - wrapcheck
    - nilerr
    - staticcheck
    - govet
linters-settings:
  errorlint:
    errorf: true
    asserts: true
    comparison: true
  wrapcheck:
    ignoreSigs:
      - .Errorf(
      - errors.New(
      - errors.Unwrap(
      - errors.Join(
      - .Wrap(
      - .Wrapf(
issues:
  exclude-rules:
    - path: _test\.go
      linters: [wrapcheck]
```

## Best practices
- One `apperror` package per service; sentinels live there, not scattered. Every other package imports.
- Wrap with the operation, not a generic phrase: `fmt.Errorf("user_create: %w", err)` beats `fmt.Errorf("error: %w", err)`
- Custom error types implement `Error() string`, `Unwrap() error`, and (where relevant) `Is(target error) bool` so `errors.Is` works through value-typed wrappers
- HTTP/gRPC mapping lives at the edge handler, never inside business logic — that keeps domain errors transport-agnostic
- Use `errors.Join` for "n things failed" (validation, batch) instead of returning the first error
- Log the error chain once at the boundary; do not log + return — that creates duplicate Sentry events
- Distinguish **expected** failures (`ErrNotFound`, `ErrConflict`) from **unexpected** (panics, infra) — only the latter goes to alerts
- For 3rd-party SDK errors, wrap immediately at the integration boundary; do not let `*googleapi.Error` leak deeper

## AI-agent gotchas
- LLM training data is mixed pre/post Go 1.13 — agents emit `errors.Wrap(err, "x")` (pkg/errors) when project uses stdlib only. Lock the lint config and let it correct the agent.
- `%v` vs `%w` looks identical; `%v` formats but does not wrap. errorlint rule catches this; ensure it's enabled before agent edits.
- Agents over-define sentinel hierarchies (`ErrUserNotFound`, `ErrOrderNotFound`...). Prefer a single `ErrNotFound` plus context in the wrapped message.
- `if err != nil { return err }` without wrapping is a wrapcheck violation; agents add `return err` from muscle memory
- `errors.As` requires a pointer to a pointer for interface targets; agents commonly pass a value, the call silently returns false
- Agents conflate panic (programmer error) with error return (expected). Hard rule: panics never cross package boundaries except in `init`
- Human-in-loop required when introducing new transport-level mappings (HTTP status, gRPC codes) — wrong codes break clients silently

## References
- Go blog "Working with Errors in Go 1.13": https://go.dev/blog/go1.13-errors
- Dave Cheney "Don't just check errors, handle them gracefully": https://dave.cheney.net/2016/04/27/dont-just-check-errors-handle-them-gracefully
- `errors` package docs: https://pkg.go.dev/errors
- `errorlint`: https://github.com/polyfloyd/go-errorlint
- `wrapcheck`: https://github.com/tomarrell/wrapcheck
- Cockroach error library: https://github.com/cockroachdb/errors
- Uber Go style guide (Errors section): https://github.com/uber-go/guide/blob/master/style.md#errors
