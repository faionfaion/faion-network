# Agent Integration — Go Standard Layout

## When to use
- Greenfield Go services where the team wants a single, agreed-upon directory convention to cut bikeshedding ("where does this go?").
- Mid-size services with multiple binaries (`cmd/api`, `cmd/worker`, `cmd/migrate`) sharing a domain core under `internal/`.
- Monorepos that need to publish reusable libraries via `pkg/` while keeping app code private under `internal/`.
- Onboarding-heavy teams where a navigable layout matters more than micro-optimisations to package shape.
- Refactoring a "single-package" Go app that grew past ~3k LOC and now wants explicit handler/service/repository seams.

## When NOT to use
- Tiny CLIs (≤500 LOC, one binary). `main.go` + a couple of files is sufficient; the layout is a tax.
- Library-only modules. The `golang-standards/project-layout` doc explicitly says it's not for libraries.
- When the team has already converged on a different convention (Domain-driven `internal/<context>/...` package-by-feature). Switching mid-flight churns the diff for no win.
- Hyper-optimised single-package code (compiler-friendly, low ceremony) where every package boundary is a `string`-allocating call.
- Educational/demo repos where the layout obscures the lesson — keep flat.

## Where it fails / limitations
- **`pkg/` cargo-cult.** Teams add `pkg/` from the layout without anything to publish; it just becomes a second random bin. Skip until you have a real external API.
- **Layered packages don't enforce dependency direction.** `internal/handler` can `import "internal/repository"` directly, bypassing service. Without `depguard` or import linting, the layout is decorative.
- **Interfaces in the wrong package.** README says "interfaces defined at consumer side" — agents put them in `internal/repository` (producer) instead of `internal/service` (consumer), creating import cycles.
- **`internal/` tree gets too deep.** `internal/service/order/v2/usecases/...` defeats the navigability the layout was supposed to bring.
- **Test pollution.** `_test.go` files placed in the same package access unexported symbols freely; readability suffers when the package is large. Black-box tests in `package handler_test` are saner.
- **Config sprawl.** `internal/config` becomes a god struct that depends on every package's options; agents grow it.
- **Migrations + binary coupling.** `migrations/` lives at the root but the binary that applies them lives in `cmd/migrate`; without a Makefile the dance is undiscoverable.
- **`gin-gonic` lock-in.** The README's handler example uses `gin`; the layout works with `chi`/`echo`/`net/http` too, but mixing routers across handler files is a smell.

## Agentic workflow
Drive Go service scaffolding as a four-stage pipeline: (1) a layout agent generates the `cmd/` + `internal/` skeleton from the spec (entity inventory + endpoint inventory); (2) a code-gen agent emits handler + service + repository + model per resource; (3) a wiring agent assembles `cmd/api/main.go` (config → DB → repos → services → handlers → router → server); (4) a review agent runs the import-rule checklist (handler imports service; service imports repository interface; repository implementation imports model + DB driver; no cycles). Persist the layout decision (chi vs gin vs echo, sqlc vs gorm vs database/sql, slog vs zerolog) in `.aidocs/product_docs/go-stack.md` so agents stop re-deciding per PR. Pair with sibling methodologies `pro/dev/backend-systems/go-project-structure/`, `pro/dev/backend-systems/go-error-handling-patterns/`, `pro/dev/backend-systems/go-concurrency-patterns/`.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task = one resource (model + repo iface + repo impl + service + handler + tests + wiring). Sonnet is sufficient; opus only for module boundaries.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — `internal/config` and `cmd/*/main.go` often pull DSNs/JWT secrets from the env; scrub fixtures and sample configs before commit.
- A purpose-built **go-layout-review-agent** (worth adding under `agents/`): linter that flags handler→repository imports (skipping service), exported types in `internal/` that aren't necessary, `pkg/` directories with no external consumers, and interface declarations colocated with implementations.

### Prompt pattern
Layout pass:
```
You are a Go architect. Given the spec in <spec>, produce:
(a) cmd/ binaries: name, purpose (api/worker/migrate/seed),
    main responsibilities (≤5 bullets each).
(b) internal/ packages: handler, service, repository, model,
    middleware, config — each with file list + types + interfaces.
    Interfaces live in the consumer package (service for repo iface).
(c) pkg/ packages: only if they have a documented external consumer,
    otherwise leave empty.
Reject any handler that imports a repository directly. Reject any
exported type in internal/ that isn't used in cmd/.
```

Anti-pattern review:
```
Review a Go layout PR. Flag:
(1) handler package importing a repository package,
(2) interface defined in the producer package (e.g., repo iface in
    internal/repository instead of internal/service),
(3) cmd/<name> doing business logic instead of wiring,
(4) pkg/ entry with no external import,
(5) circular imports across internal/ subpackages,
(6) global state in any package other than cmd/<name>/main.go,
(7) _test.go in same package when black-box test would be cleaner.
Cite file:line. No fixes — only flags.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go` | Build, test, fmt, vet, mod | https://go.dev |
| `golangci-lint` | Aggregator linter (errcheck, govet, staticcheck, revive) | https://golangci-lint.run |
| `depguard` (golangci) | Forbid imports across package boundaries | https://github.com/OpenPeeDeeP/depguard |
| `gomod-outdated` / `go-mod-upgrade` | Track stale deps | https://github.com/psampaz/go-mod-outdated |
| `gosec` | Security linter (hardcoded creds, weak crypto) | https://github.com/securego/gosec |
| `goimports` / `gofumpt` | Imports + stricter format | https://github.com/mvdan/gofumpt |
| `mockgen` (uber-go/mock) | Generate mocks against interfaces | https://github.com/uber-go/mock |
| `sqlc` / `gorm gen` / `ent` | Generate typed DB access from SQL/schema | https://sqlc.dev |
| `air` / `wgo` | Live-reload during dev | https://github.com/cosmtrek/air |
| `delve` (`dlv`) | Debugger | https://github.com/go-delve/delve |
| `pprof` | Profiling (CPU, alloc, goroutine, mutex) | bundled |
| `goreleaser` | Cross-compile + release artifacts | https://goreleaser.com |
| `cobra` / `urfave/cli` | CLI scaffolding for `cmd/*` binaries | https://cobra.dev |
| `koanf` / `viper` | Config loading from file/env/flag | https://github.com/knadh/koanf |
| `migrate` / `goose` / `atlas` | Schema migrations driven by `cmd/migrate` | https://github.com/golang-migrate/migrate |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions w/ `setup-go` | SaaS | yes | Standard CI for `go test ./... && golangci-lint run`. |
| SonarCloud / DeepSource / Codacy | SaaS | yes | Architecture rules + smell detection per PR. |
| Renovate / Dependabot | SaaS | yes | Auto-PR Go module bumps; agents triage. |
| Sentry / Honeycomb / Datadog APM | SaaS | yes | Native Go SDKs; instrument `internal/middleware`. |
| OpenTelemetry Go SDK | OSS | yes | One init in `cmd/api/main.go`, instrumentation across `internal/*`. |
| Air / Tilt / Skaffold | OSS | yes | Inner dev loop with hot reload. |
| testcontainers-go | OSS | yes | Real Postgres/Redis in tests; first-class for repository implementations. |

## Templates & scripts
README ships the canonical layout. Add a `.golangci.yml` enforcing layer rules:

```yaml
linters:
  enable: [depguard, errcheck, govet, staticcheck, revive, gocyclo, gosec]
linters-settings:
  depguard:
    rules:
      handler:
        files: ["internal/handler/**"]
        deny:
          - pkg: "project/internal/repository"
            desc: "handler must call service, not repository"
      service:
        files: ["internal/service/**"]
        deny:
          - pkg: "github.com/gin-gonic/gin"
            desc: "service must not depend on web framework"
      domain:
        files: ["internal/model/**"]
        deny:
          - pkg: "database/sql"
            desc: "model must not depend on DB driver"
```

Inline layout-lint:

```bash
#!/usr/bin/env bash
# go-layout-lint.sh — quick layout sanity checks
set -euo pipefail
root="${1:-.}"
fail=0
echo "## handler importing repository directly"
grep -rEn '"[^"]+/internal/repository"' "$root/internal/handler" 2>/dev/null && fail=1 || true
echo "## interface in producer (repo) package"
for f in "$root"/internal/repository/*.go; do
  grep -Eq '^type [A-Z][a-zA-Z]+ interface' "$f" && { echo "iface in producer: $f"; fail=1; }
done
echo "## pkg/ with no consumer outside repo"
[[ -d "$root/pkg" ]] && for d in "$root"/pkg/*/; do
  name=$(basename "$d")
  grep -rEq "\"[^\"]+/pkg/$name\"" "$root" --exclude-dir="pkg" || { echo "unused pkg/$name"; fail=1; }
done
exit "$fail"
```

## Best practices
- **`cmd/<name>` is wiring only.** Read config, build dependencies, start the server. No business logic, no goroutines spawning workers (compose them in services).
- **`internal/` is the default home.** Code goes there until proven externally consumed. Then promote to `pkg/`.
- **Interfaces at the consumer.** `service.UserRepository` lives in `internal/service`; `internal/repository` implements it. Inverted dependencies, no import cycle.
- **Small, focused packages.** Aim for one responsibility per package (handlers, services, repos). Long file is fine; long package is not.
- **Don't export what you don't have to.** Lowercase types in `internal/` keep the package surface small.
- **One linter config per repo.** `.golangci.yml` is committed; CI runs `golangci-lint run --timeout=3m` on every PR. Don't rely on per-developer setup.
- **Context-first signatures.** Every service/repo method takes `ctx context.Context` as the first parameter. README example follows this; agents sometimes drop it.
- **Errors wrapped with `%w`.** `fmt.Errorf("get user %s: %w", id, err)`. Aligns with `errors.Is` / `errors.As`.
- **Repository returns domain models, not ORM rows.** The translation happens in the repo impl. `service` and above don't know about SQL.
- **Tests next to code.** `*_test.go` co-located. For black-box style use `package handler_test` to avoid touching unexported internals.
- **Migrations versioned.** Each migration in `migrations/NNNN_description.up.sql` + `.down.sql`. Apply via `cmd/migrate` or `golang-migrate`.
- **`Makefile`/`Taskfile.yml`** documents canonical commands (`make test`, `make lint`, `make migrate-up`).

## AI-agent gotchas
- **`pkg/` reflex.** Agents add `pkg/utils`, `pkg/helpers` from muscle memory. Lint these out; force `internal/` first.
- **Interface in producer package.** Agents declare `repository.UserRepository` interface in `internal/repository`; consumer imports producer. Force consumer-side declaration in the prompt.
- **`gin-gonic` leakage into service.** Agents pass `*gin.Context` past the handler. Force `ctx context.Context` and pull values up explicitly.
- **Global DB handle.** Agents create `var DB *sql.DB` at package scope. Force constructor injection from `cmd/<name>/main.go`.
- **Skipped error wrapping.** Agents `return err` from repos; service has no idea where it came from. Force `%w`-wrap on every error crossing a layer.
- **`init()` side effects.** Agents add `init()` to register handlers/migrations; brittle. Use explicit constructors called from `main`.
- **Context not propagated.** Agents start a goroutine in a service without a derived context; cancellation lost. Force `errgroup.WithContext` or named worker pools.
- **Test on the wrong layer.** Agents test handlers via the real router with a real DB. Force handler tests with mocked services + repository tests with `testcontainers-go`.
- **Hallucinated stdlib APIs.** Agents invent `sql.QueryRowContext` signatures. Pin to the Go version in `go.mod`.
- **Human-in-loop on layout changes.** Renaming a top-level directory or moving a package is a churn event. Don't auto-merge.

## References
- "Go Standards Project Layout" (community). https://github.com/golang-standards/project-layout
- Effective Go. https://go.dev/doc/effective_go
- Go Code Review Comments. https://github.com/golang/go/wiki/CodeReviewComments
- Go Modules Reference. https://go.dev/ref/mod
- Russ Cox — "Go Project Structure" notes (mailing list, talks).
- "Practical Go" — Dave Cheney. https://dave.cheney.net/practical-go
- Ardanlabs Service repo (alt convention worth knowing). https://github.com/ardanlabs/service
- `golangci-lint` linters list. https://golangci-lint.run/usage/linters/
- Sibling methodologies in this repo: `pro/dev/backend-systems/go-project-structure/`, `pro/dev/backend-systems/go-backend/`, `pro/dev/backend-systems/go-http-handlers/`, `pro/dev/backend-systems/go-error-handling-patterns/`.
