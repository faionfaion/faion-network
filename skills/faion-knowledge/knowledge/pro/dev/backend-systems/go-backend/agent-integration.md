# Agent Integration — Go Backend

## When to use
- Bootstrapping a new Go service (Gin/Echo/Chi) with the `cmd/` + `internal/` + `pkg/` layout.
- Adding HTTP handlers, middleware, request validation, or worker pools to an existing Go backend.
- Refactoring ad-hoc Go code into the layered handler → service → repository structure.
- Adding `apperror`-style typed errors and centralized error middleware.

## When NOT to use
- Greenfield where the team has more Python/TS experience and operational constraints don't justify Go's runtime profile.
- Pure CLI tools — different layout (`cmd/<tool>/main.go` + flat libs); see `go-project-structure`.
- Async-heavy event processing where a message bus + lightweight consumer in any language fits better than a long-lived HTTP service.
- Prototypes where dependency injection wiring would slow down iteration; prefer a single-file spike first.

## Where it fails / limitations
- Gin's middleware error chain (`c.Errors`) is easy to misuse — agents often forget `c.Next()` ordering and the error handler never fires.
- `internal/` boundary protections are weakened if the agent puts shared types in `pkg/` prematurely; once exposed, you can't pull them back without breaking external consumers.
- The provided `Pool` example has no result channel and silently swallows job errors — fine for fire-and-forget, dangerous as a default.
- `c.ShouldBindJSON` returns Go validator errors that are user-unfriendly; the snippet ships them raw to the client (info-leak + bad UX).
- Standard layout debate: agents will cargo-cult `pkg/` even when nothing public exists — leading to empty dirs and confused imports.

## Agentic workflow
Drive Go backend work through SDD: spec the endpoint contract first, generate handler+service+repository skeletons in one pass (Sonnet), then have a reviewer pass enforce the layered boundaries and error-typing rules. Pair coding agents with `go vet`, `staticcheck`, and `golangci-lint` runs after every edit — they catch most LLM-induced concurrency / nil-pointer mistakes cheaply. For new services, start by committing the directory tree + `go.mod` + a no-op `main.go` so subsequent agents have a stable target.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the SDD task lifecycle (spec → design → impl → review) for a Go feature; quality gates already enforce build + vet.
- A custom `go-reviewer` (Opus, read-only) — verifies layered architecture (no handler imports repo, no repo imports handler), context propagation, and `apperror` typing.
- `password-scrubber-agent` — sanitize hardcoded JWT secrets / DSNs the LLM tends to inline in `SetupRouter`.

### Prompt pattern
```
Add endpoint <METHOD /path> to module <name>.
Write three files: internal/handler/<name>.go, internal/service/<name>.go, internal/repository/<name>.go.
Handler depends on service interface; service depends on repository interface; repository is the only package that imports the DB driver.
Use apperror.AppError for all returned errors. Bind input with `binding:"required"` tags. Propagate ctx from c.Request.Context().
After writing, run: gofmt -w, go vet ./..., golangci-lint run.
```

```
Review the diff for: (1) layered boundaries, (2) ctx propagation in every I/O call, (3) error wrapping with apperror, (4) goroutine leaks (any `go func` without ctx exit).
Return JSON: {violations: [{file, line, rule, fix}]}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go` | Build, test, vet, mod | https://go.dev/doc/ |
| `golangci-lint` | Aggregated linter (govet, staticcheck, errcheck, ineffassign, gosec) | https://golangci-lint.run/ |
| `staticcheck` | Deep analysis (unused, error checks) | https://staticcheck.dev/ |
| `gofumpt` | Stricter `gofmt` | https://github.com/mvdan/gofumpt |
| `air` | Live reload during dev | https://github.com/cosmtrek/air |
| `mockgen` | Interface mocks for repo/service | https://github.com/uber-go/mock |
| `swag` | Generate OpenAPI from Gin annotations | https://github.com/swaggo/swag |
| `goose` / `migrate` | DB migrations | https://github.com/pressly/goose · https://github.com/golang-migrate/migrate |
| `pprof` | CPU/heap/goroutine profiles | https://pkg.go.dev/net/http/pprof |
| `delve` | Debugger | https://github.com/go-delve/delve |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Gin | OSS framework | Yes | Largest LLM training corpus; agents produce idiomatic code. |
| Echo | OSS framework | Yes | Cleaner middleware model; good when agent must compose typed handlers. |
| Chi | OSS framework | Yes | Stdlib-style; preferred when agent should not import a "framework". |
| Fiber | OSS framework | Partial | Fasthttp under the hood — incompatible with `net/http` middleware ecosystem; warn the agent. |
| Sentry / Rollbar | SaaS | Yes | Drop-in middleware; agent can wire `sentrygin.New` automatically. |
| Datadog APM | SaaS | Yes | `dd-trace-go` middleware; agents add it via env var + import. |
| OpenTelemetry collector | OSS | Yes | `otelhttp` + `otelgin` packages; preferred over vendor SDKs for portability. |
| Prometheus | OSS | Yes | `promhttp.Handler()` on `/metrics`; agent should add a histogram per route. |

## Templates & scripts
See `templates.md` for handler/service/repository scaffolds and `examples.md` for end-to-end CRUD. Useful agent-driven scaffold (≤50 lines):

```bash
#!/usr/bin/env bash
# scripts/new-go-service.sh <module-path> <service-name>
set -euo pipefail
MOD=$1; SVC=$2
mkdir -p "$SVC"/{cmd/api,internal/{handler,service,repository,model,middleware,config},migrations,pkg}
cd "$SVC"
go mod init "$MOD"
cat > cmd/api/main.go <<EOF
package main

import (
    "log"
    "net/http"
    "$MOD/internal/handler"
)

func main() {
    h := handler.New()
    log.Fatal(http.ListenAndServe(":8080", h.Router()))
}
EOF
cat > internal/handler/handler.go <<'EOF'
package handler

import "net/http"

type Handler struct{}

func New() *Handler { return &Handler{} }

func (h *Handler) Router() http.Handler {
    mux := http.NewServeMux()
    mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    })
    return mux
}
EOF
go mod tidy
go vet ./...
echo "ok: $SVC"
```

## Best practices
- Define interfaces at the consumer (handler defines `service.UserService`, not the service package) — this keeps `internal/service` swappable in tests.
- Always pass `ctx := c.Request.Context()` into the service layer; never call DB drivers without a context.
- Centralize the error handler middleware and forbid `c.JSON(http.StatusXXX, err.Error())` directly in handlers — it leaks internal errors.
- Run `golangci-lint run --new-from-rev=HEAD~1` in CI so agents only have to fix what they touched.
- Keep `go.mod` clean: agents that add a dep must justify it in the commit body. Prefer stdlib + Gin/Echo + sqlx/pgx + zap.
- Use `errgroup.WithContext` over hand-rolled WaitGroup+errCh whenever there's an error to bubble up; it composes with cancellation.

## AI-agent gotchas
- LLMs love to spawn goroutines without `ctx` — every `go func()` you accept must include either a context check or a clear lifetime contract; otherwise the worker leaks forever.
- `gin.Default()` already includes Logger+Recovery; agents often add them again, double-logging every request. Pin the middleware list explicitly.
- Agents export types from `internal/` by mistake by referencing them in `pkg/` — Go won't compile, but the agent's first fix is usually to move the type to `pkg/`. Force them to fix the import direction instead.
- The provided `Wrap(err, msg)` returns 500 even for known categories — agents call it on user errors and lose the right HTTP status. Require typed wrappers (`apperror.AsValidation`, `apperror.AsNotFound`).
- Human-in-loop checkpoint: any new dependency in `go.mod` and any addition to `pkg/` (public surface) needs explicit reviewer approval — these are easy to add and hard to remove.

## References
- Effective Go — https://go.dev/doc/effective_go
- Gin docs — https://gin-gonic.com/docs/
- Echo docs — https://echo.labstack.com/docs
- Chi router — https://github.com/go-chi/chi
- Standard project layout (note: opinionated, not official) — https://github.com/golang-standards/project-layout
- Uber Go style guide — https://github.com/uber-go/guide/blob/master/style.md
