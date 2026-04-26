# Agent Integration — Go Backend

## When to use
- Greenfield Go service with `cmd/` + `internal/` layout where the agent scaffolds packages, handlers, services, and repositories.
- Adding a new endpoint to an existing Gin/Echo project where the structure is already enforced.
- Migrating a Flask/Express prototype to a Go binary while keeping the same REST contract.
- Generating worker-pool / fan-out-fan-in glue code around a well-typed `Job` interface.
- Producing typed `AppError` taxonomies and matching middleware for an existing service.

## When NOT to use
- The project uses a non-standard layout (Hex / Clean / monorepo-with-multi-module). The README assumes Go standard layout — agent will produce the wrong import paths.
- Performance-critical hot paths where allocation and goroutine count matter more than structure (LLM rarely reasons about escape analysis or `sync.Pool` correctly).
- Cgo / unsafe / kernel-bypass code — out of scope and high blast radius.
- Generics-heavy domain libraries — patterns here are pre-generics style.

## Where it fails / limitations
- README mixes Gin and Echo idioms; an agent left to choose will sometimes blend them in one file (Echo `c.Bind` with Gin `gin.H`). Pin one router in the prompt.
- `interface defined at consumer side` rule is easy to violate — agents tend to add interfaces in the package that defines the impl. Needs review.
- Error wrapping example uses sentinel singletons (`ErrNotFound`) AND a constructor (`NewNotFound`); agent often picks the wrong one for the case.
- No context-cancellation propagation example for the worker pool's `Submit` path — agents may drop ctx silently.
- Validator tags shown only for Gin (`binding:"..."`); Echo path needs a separate validator wiring agent must add.

## Agentic workflow
Drive Go backend work as scaffold → fill → verify. Use a single subagent to scaffold the full directory tree from the README, then per-domain subagents to implement handler/service/repository triples. Always run `go vet ./...`, `staticcheck ./...`, and `go test ./...` between steps so the LLM gets a fast feedback signal. For concurrency code (worker pool, fan-out), require the agent to write a race-detector test (`go test -race`) before claiming done.

### Recommended subagents
- `faion-sdd-executor-agent` — for SDD task lists; pairs well with the `internal/{handler,service,repository}` triple per feature.
- General-purpose Claude subagent with explicit "Gin only" or "Echo only" instruction — prevents mixing.
- `password-scrubber-agent` — before commit, scan generated `config/` for embedded credentials.

### Prompt pattern
```
You are scaffolding a Go service following internal/handler + internal/service + internal/repository.
Router: Gin only. Validator: go-playground/validator via gin binding tags.
Errors: use apperror.AppError; map to HTTP via ErrorHandler middleware.
For each new endpoint: handler test (httptest.NewRecorder), service test (mock repo), no DB integration test in this pass.
After writing: run `go vet ./...` and `go test ./...`. Stop on first failure.
```

```
Implement a worker pool for <task>. Reuse internal/worker/Pool.
Constraints: ctx-aware Submit (return ctx.Err() if cancelled); race-test required.
Do not introduce new deps. No global state.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go` | Build, test, vet, mod | https://go.dev/dl/ |
| `staticcheck` | Lint beyond `go vet` | `go install honnef.co/go/tools/cmd/staticcheck@latest` |
| `golangci-lint` | Aggregator (govet, errcheck, gosec, ineffassign, ...) | https://golangci-lint.run/ |
| `gofumpt` | Stricter `gofmt` | `go install mvdan.cc/gofumpt@latest` |
| `goimports` | Auto-manage imports | `go install golang.org/x/tools/cmd/goimports@latest` |
| `mockgen` | Generate interface mocks | `go install go.uber.org/mock/mockgen@latest` |
| `air` | Live-reload during dev | `go install github.com/cosmtrek/air@latest` |
| `migrate` | DB migrations matching `migrations/` dir | `go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest` |
| `gosec` | Security scanner | `go install github.com/securego/gosec/v2/cmd/gosec@latest` |
| `govulncheck` | Known-vuln scanner (official) | `go install golang.org/x/vuln/cmd/govulncheck@latest` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Gin | OSS framework | Yes | Best documented for LLMs; default choice. |
| Echo | OSS framework | Yes | Built-in JWT/Recover middleware; cleaner middleware API. |
| Chi | OSS framework | Yes | Stdlib-style; minimal magic, easy for agents. |
| Fiber | OSS framework | Caution | Fasthttp under the hood — incompatible with `net/http` middleware ecosystem. |
| Buf / connect-go | OSS RPC | Yes | gRPC + Connect; great when contract-first. |
| OpenAPI Generator (`oapi-codegen`) | OSS | Yes | Generate handlers from OpenAPI; pairs with this layout. |
| Sentry / Honeycomb / Datadog | SaaS | Yes | All have Go SDK + middleware; trivial to inject in `SetupRouter`. |

## Templates & scripts
See `templates.md` and `examples.md` for handler/service/repo skeletons. Useful agent-side script to enforce layout before commit:

```bash
#!/usr/bin/env bash
# scripts/check-layout.sh — fail commit if Go layout drifts.
set -euo pipefail
required=("cmd" "internal/handler" "internal/service" "internal/repository" "internal/model")
for d in "${required[@]}"; do
  [[ -d "$d" ]] || { echo "missing: $d"; exit 1; }
done
# No imports of internal/ from outside this module.
mod=$(go list -m)
if grep -RIn "\"$mod/internal/" --include="*.go" -- . | grep -v "^$mod" >/dev/null; then
  echo "internal/ imported from outside module"; exit 1
fi
go vet ./...
staticcheck ./...
echo "layout ok"
```

## Best practices
- Define interfaces in the **consumer** package (e.g. `service` defines `UserRepository`, `repository` provides the impl). Agent prompts must restate this, otherwise it gets reversed.
- Pass `context.Context` as the first arg of every exported function that does I/O. The README's `service.GetByID(c.Request.Context(), id)` is the model — enforce this.
- Use `errors.Is` / `errors.As` with the sentinel `AppError` values, not string comparison; the README's `Unwrap` enables this.
- Build small, single-purpose middlewares (`RequestID`, `Logger`, `Recovery`, `Auth`) — easier for agents to compose than one mega-middleware.
- Keep `cmd/api/main.go` thin: only wiring (config → deps → router → server). Agents bloat `main.go` if not constrained.
- For request DTOs, use a separate `*Request` struct from the domain model — never bind directly into `model.User`.

## AI-agent gotchas
- LLMs love adding generics where the README uses interface{}/any-style code; pin Go version in the prompt to keep outputs consistent.
- `gin.Context` is request-scoped — agents sometimes capture it inside a goroutine. Always derive `ctx := c.Request.Context()` before spawning.
- `c.Errors` aggregation in error middleware works only when handlers call `c.Error(err)` and `return`; agents often `c.JSON(...)` directly, bypassing the middleware. Add a lint or review checkpoint.
- The `Pool.Submit` path blocks if the buffer is full — agent-generated callers may deadlock under cancellation. Require a `select { case p.jobs <- job: case <-ctx.Done(): }` variant.
- Running `go mod tidy` after every agent step is safer than batched: catches stray imports early.
- Human-in-loop checkpoint: review generated `Auth()` middleware — agents commonly produce token-validation code with subtle bypasses (e.g. accepting empty `Authorization`).

## References
- https://go.dev/doc/effective_go
- https://github.com/golang-standards/project-layout
- https://gin-gonic.com/docs/
- https://echo.labstack.com/docs
- https://github.com/uber-go/guide/blob/master/style.md
- https://dave.cheney.net/practical-go/presentations/qcon-china.html
