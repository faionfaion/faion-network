# Agent Integration — Go Project Structure

## When to use
- Bootstrapping a new Go service or CLI and choosing a layout that matches community norms (`cmd/`, `internal/`, `pkg/`).
- Splitting a single-package main into `internal/{handler,service,repository,model}` once it crosses ~1k LoC.
- Adding a second binary (background worker, admin CLI) to an existing service — second `cmd/<name>/main.go`.
- Standardizing layout across many Go services so on-call engineers find files in the same place.
- Generating skeletons for vertical slices (resource → handler/service/repository/model) repeatably.

## When NOT to use
- Tiny single-file scripts or quick experiments — `main.go` next to `go.mod` is enough.
- Library-only repos — `cmd/`, `internal/`, `deployments/` are noise; structure by feature subpackages.
- Go modules being published — heavy `internal/` use prevents downstream consumers from importing helpers.
- Monorepos with many services — prefer one Go module per service and avoid a giant root with `cmd/<a>` `cmd/<b>` … cross-importing.
- "Clean Architecture" purists — this layout is utility-first, not domain-aggregate-first; force-fitting DDD here gets ugly.

## Where it fails / limitations
- The `golang-standards/project-layout` is not officially endorsed by the Go team; following it religiously can be a smell.
- `pkg/` is widely misused — it should hold code intended to be importable by other repos; most services don't need it.
- `internal/` is enforced by the compiler; once code is there, an external consumer cannot import even with permission.
- `cmd/<name>/main.go` plus `internal/` makes test files spread across packages; `go test ./...` is the right invocation but coverage gathering is fiddly.
- Hand-rolled `getEnv` config trips up on bool/int parsing edge cases; libraries (`envconfig`, `viper`, `koanf`) are usually better.
- Graceful shutdown shown in README only handles HTTP server, not workers/DB pools/queue consumers.
- Mixing `internal/handler` (HTTP-coupled) with non-HTTP entry points (CLI, cron) leads to handler imports outside HTTP context.

## Agentic workflow
The agent should (1) inspect the repo: is this a single binary, multi-binary, library? (2) propose layout: flat for small, `cmd+internal` for services, `cmd+internal+pkg` only when external import is needed; (3) generate the directory tree with empty `.gitkeep` placeholders + a working `cmd/<name>/main.go` + `internal/config/config.go` + a Makefile + Dockerfile; (4) wire CI (`golangci-lint`, `go test -race ./...`); (5) generate one vertical slice through handler→service→repository so the layout is exercised end-to-end. Do not let the agent introduce `pkg/` unless it can name an external consumer.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the bootstrap as an SDD task; gates: `go vet`, `golangci-lint run`, `go test -race ./...`, `go build ./...`.
- An architect (Opus) for the single-binary vs workspace decision, package boundaries, and config strategy.
- A boilerplate implementer (Sonnet) for slice/layout generation.

### Prompt pattern
```
Bootstrap a Go 1.22 HTTP service. Use the layout from go-project-structure/README.md.
Stack: Gin v1.10, sqlx + lib/pq, zap. Generate cmd/api/main.go with graceful shutdown,
internal/config (env-driven), internal/handler, internal/service, internal/repository,
internal/model. Implement /healthz and CRUD for `Item` end-to-end. Add Makefile,
Dockerfile (multi-stage, distroless), .golangci.yml. Stop when `make test` is green.
```

```
Audit this repo against go-project-structure: misuse of pkg/, cyclic imports,
package-level globals, missing graceful shutdown for workers, config parsing without
type safety. Output findings with file:line.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go mod` | Module mgmt | stdlib |
| `golangci-lint` | Aggregator linter | https://golangci-lint.run |
| `staticcheck` | Deeper static analysis | https://staticcheck.dev |
| `govulncheck` | CVE scan for deps | https://go.dev/blog/vuln |
| `gotestsum` | Pretty test runner | https://github.com/gotestyourself/gotestsum |
| `air` | Live reload during dev | https://github.com/cosmtrek/air |
| `mockery` / `gomock` | Generate mocks for repository interfaces | https://vektra.github.io/mockery/ · https://github.com/uber-go/mock |
| `wire` | Compile-time DI when manual wiring grows | https://github.com/google/wire |
| `go-licenses` | License compliance check | https://github.com/google/go-licenses |
| `koanf` / `viper` / `envconfig` | Typed config loaders | https://github.com/knadh/koanf |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes | `actions/setup-go`, matrix on Go versions; standard CI. |
| Goreleaser | OSS | Yes | Builds + releases binaries; reads `cmd/` automatically. |
| Docker Hub / ghcr | SaaS | Yes | Multi-stage Dockerfile in README is the canonical pattern. |
| Fly.io | SaaS PaaS | Yes (`flyctl`) | Detects Go via `go.mod`. |
| Railway / Render | SaaS PaaS | Yes | Same. |
| pkg.go.dev | OSS | Yes (HTML) | Public docs; only hits if module is published. |
| Sentry / Datadog | SaaS | Yes | `sentry-go`, `dd-trace-go` slot into the layout. |

## Templates & scripts
See `templates.md` for full templates. Inline scaffolder for a vertical slice across all internal packages:

```bash
#!/usr/bin/env bash
# scripts/new_resource.sh users
set -euo pipefail
N="$1"
T="$(echo "${N}" | sed 's/.*/\u&/' | sed 's/s$//')"   # users -> User
mkdir -p internal/{model,repository,service,handler}
cat > "internal/model/${N}.go" <<EOF
package model
type ${T} struct{ ID, Name string }
EOF
cat > "internal/repository/${N}.go" <<EOF
package repository
import ("context"; "github.com/jmoiron/sqlx"; m "yourmod/internal/model")
type ${T}Repo interface{ Create(context.Context, *m.${T}) error }
type ${N}Repo struct{ db *sqlx.DB }
func New${T}Repo(db *sqlx.DB) ${T}Repo { return &${N}Repo{db} }
func (r *${N}Repo) Create(ctx context.Context, x *m.${T}) error { return nil /* TODO */ }
EOF
cat > "internal/service/${N}.go" <<EOF
package service
import ("context"; r "yourmod/internal/repository"; m "yourmod/internal/model")
type ${T}Service struct{ repo r.${T}Repo }
func New${T}Service(repo r.${T}Repo) *${T}Service { return &${T}Service{repo} }
func (s *${T}Service) Create(ctx context.Context, x *m.${T}) error { return s.repo.Create(ctx, x) }
EOF
echo "scaffolded $N across model/repository/service. Add handler manually."
```

## Best practices
- Default to one binary, one module. Add a second `cmd/<name>` only when a real second entrypoint exists.
- Keep `internal/` rich and `pkg/` empty until proven otherwise; renaming `pkg/foo` → `internal/foo` later is painful.
- Inject dependencies through constructors (`NewXService(deps...)`); never package-level globals.
- Define interfaces at the consumer (the service) not the producer (the repository) — Go style.
- Set explicit `http.Server` timeouts (`ReadHeaderTimeout`, `WriteTimeout`, `IdleTimeout`) in `cmd/api/main.go`.
- Graceful shutdown must close DB pools, drain queues, cancel contexts — not just `srv.Shutdown`.
- Use a typed config loader (`envconfig`/`koanf`); roll-your-own `getEnv` invites silent type bugs.
- CI matrix on the two latest Go minor versions; `go vet`, `staticcheck`, `go test -race -shuffle=on` are the minimum gates.
- Pin tools used by the build via `tools.go` and `go mod tidy` for reproducible local toolchains, or use `go run -mod=mod tool@version`.

## AI-agent gotchas
- LLMs reflexively create a `pkg/` directory and put helpers there; this leaks internals once anyone imports the module. Reject `pkg/` without a named external consumer.
- Generated `cmd/api/main.go` often skips `defer srv.Shutdown(ctx)` or shuts down the DB pool before draining requests; require an audit checklist.
- Agents drop graceful shutdown for worker binaries entirely. Require a `select { case <-quit: case <-ctx.Done(): }` pattern in every long-running goroutine.
- LLMs use `package-level var DB *sql.DB`; this works for tutorials and breaks for tests. Insist on constructor injection.
- Agents propose cyclic imports (handler → service → handler) when extracting interfaces; require a `graph` of imports before commit.
- Generated `getEnvInt` and similar helpers silently return defaults on parse error; require an explicit error-on-malformed mode.
- An agent migrating from flat layout often rewrites import paths globally and breaks vendored or replaced modules; require a `go build ./...` proof and a check for `replace` directives in `go.mod`.
- Human-in-loop checkpoint: any move into `internal/` from a previously exported path is a public-API break; agents underestimate this.
- Agents emit `Dockerfile` without `USER nobody` and without distroless base; review for prod-readiness.

## References
- Standard Go Project Layout: https://github.com/golang-standards/project-layout
- Effective Go: https://go.dev/doc/effective_go
- Go Modules Reference: https://go.dev/ref/mod
- Uber Go Style Guide: https://github.com/uber-go/guide/blob/master/style.md
- Practical Go (Dave Cheney): https://dave.cheney.net/practical-go/presentations/qcon-china.html
- Go Style at Google: https://google.github.io/styleguide/go/
- "I'll take pkg/ for $200" (rejecting pkg-by-default): https://travisjeffery.com/b/2019/11/i-ll-take-pkg-over-internal/
