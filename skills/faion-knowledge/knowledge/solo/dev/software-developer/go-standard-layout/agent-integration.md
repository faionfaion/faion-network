# Agent Integration — Go Standard Layout

## When to use
- Bootstrapping a new Go service or CLI: agent scaffolds `cmd/` + `internal/` + `pkg/` plus go.mod, Makefile, Dockerfile, and CI.
- Refactoring a flat single-package Go project that has outgrown a single directory.
- Multi-binary repos (API + worker + CLI sharing a domain) — the layout cleanly separates entry points.
- Onboarding new contributors to a Go codebase: layout matches what `golang.org/doc/modules/layout`-aware engineers expect.
- Enforcing import boundaries in a modular monolith written in Go (`internal/` + per-feature subpackages).
- Pre-commit / CI agent enforcing that nothing under `pkg/` imports from `internal/`.

## When NOT to use
- Tiny utility CLI / library with <5 files — keep it flat; methodology rightly avoids ceremony in trivial repos.
- Strict adherence to the unofficial `golang-standards/project-layout` repo, which the Go team itself does not endorse — use this methodology's pragmatic subset instead.
- Polyglot monorepos where a Go package is one of many — adapt the layout to the monorepo conventions (e.g., Bazel, Nx).
- One-shot Lambdas / small Cloud Functions where `main.go` next to the manifest beats deep folders.
- Plugin systems requiring pure `pkg/` exports — `internal/` would block third-party integrators by design.

## Where it fails / limitations
- **`pkg/` overuse:** teams dump everything under `pkg/` to "make it reusable"; methodology warns flatness but pattern persists. Result: stable surface that nobody actually consumes outside the repo.
- **Interface placement drift:** the README says "interfaces at consumer side"; agents and humans default to declaring them next to the implementation, leading to import cycles.
- **`internal/` package balloon:** without sub-package discipline, `internal/` becomes a 200-file dump where nothing is encapsulated.
- **Service vs handler boundary:** the example shows `handler` calling `service` directly via concrete type — fine for small apps, breaks for testability when the team adds DI later.
- **Migrations in `migrations/`:** layout shows it but doesn't say which tool (golang-migrate, goose, atlas); ambiguity = inconsistent adoption.
- **Multi-module repos:** unclear how to split if you need separate `go.mod` per service — methodology doesn't address it.
- **Versioned API folders absent:** REST/gRPC versioning (`internal/handler/v1`, `v2`) is not in the template.

## Agentic workflow
Drive Go layout as a three-pass agent flow: (1) **scaffolder agent** generates the standard tree from the methodology + a one-page brief (service name, deps, deploy target); (2) **layout-linter agent** runs in CI and rejects PRs that put new code under `pkg/` without justification, or import `internal/` from outside the module, or declare interfaces at the producer side; (3) **boundary refactorer agent** flags handler ⇄ service ⇄ repository violations (e.g., handler importing repository directly) and proposes the smallest patch. Pair with `architecture-decision-records/` so any deviation from the layout is recorded in an ADR.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts layout-refactor work into SDD `todo/` tasks (one task per package boundary).
- A **Go-scaffolder agent** (purpose-built, worth creating): given service name + dependencies, emits the full tree + Makefile + Dockerfile + GitHub Actions workflow + golangci-lint config in one pass.
- A **layout-linter agent** (purpose-built): wraps `go-cleanarch`, `golangci-lint`, custom `depguard` rules; explains every violation in plain English.
- A **migration-tool ADR agent**: forces an ADR on the choice of `golang-migrate` vs `goose` vs `atlas` so the `migrations/` folder doesn't drift across services.

### Prompt pattern
Scaffold:
```
You are a senior Go engineer. Generate the project tree for a new
service named <name>. Stack: Gin (HTTP), pgx (Postgres),
golang-migrate (migrations), zerolog (logs). Follow exactly the layout
in solo/dev/software-developer/go-standard-layout/README.md:
- cmd/<name>/main.go
- internal/{handler,service,repository,model,middleware,config}/
- pkg/  (empty until justified)
- migrations/
- Makefile (build/test/lint/migrate)
- Dockerfile (multi-stage)
- .github/workflows/ci.yml (gofmt, vet, golangci-lint, go test, build)
- golangci.yml with depguard rules forbidding pkg/ -> internal/.
Output as a list of files with full content.
```

Layout review:
```
Read <PR diff>. Flag any of:
1. New file under pkg/ that is only consumed by this repo.
2. Interface declared next to its implementation in internal/service.
3. Cross-package import from cmd/ into internal/ via wildcard.
4. handler/ importing repository/ directly (must go via service/).
For each, output: file, violation, 1-line fix. No code changes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go` toolchain | Module init, build, test, vet | https://go.dev/dl/ |
| `gofmt` / `goimports` | Format + sort imports | included with Go |
| `golangci-lint` | Aggregator linter (errcheck, govet, gosec, depguard, revive, staticcheck) | https://golangci-lint.run |
| `go-cleanarch` | Detects Clean-Architecture / layered-monolith violations | https://github.com/roblaszczak/go-cleanarch |
| `depguard` (in golangci-lint) | Forbid imports across boundary (e.g., `pkg/` → `internal/`) | https://github.com/OpenPeeDeeP/depguard |
| `wire` (Google) | Compile-time DI when interface placement bites | https://github.com/google/wire |
| `golang-migrate` | Migrations CLI matching `migrations/` folder | https://github.com/golang-migrate/migrate |
| `goose` | Alternative migrations CLI | https://github.com/pressly/goose |
| `atlas` | Schema-as-code migrations | https://atlasgo.io |
| `mockgen` (uber-go/mock) | Generate mocks for consumer-side interfaces | https://github.com/uber-go/mock |
| `go-arch-lint` | Custom architecture rules in YAML | https://github.com/fe3dback/go-arch-lint |
| `goreleaser` | Multi-platform release with the layout's `cmd/` binaries | https://goreleaser.com |
| `mage` | Go-native task runner replacing Makefile | https://magefile.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS CI | yes | Default Go CI; agents can scaffold from official `setup-go` action. |
| GitLab CI | SaaS / self-host | yes | Same niche; YAML-driven, agent-friendly. |
| Drone CI / Buildkite | SaaS / self-host | yes | Solid Go ecosystems; less common. |
| sqlc | OSS code-gen | yes | Generates type-safe Go from SQL — fits well in `internal/repository/`. |
| ent (Facebook) | OSS ORM/code-gen | yes | Fits `internal/model/`; agents can codegen from schema. |
| protocol-buffers + buf | OSS | yes | gRPC contract-first; outputs map cleanly to `internal/handler/grpc/`. |
| Cobra + Viper | OSS CLI/config | yes | Fits `cmd/<name>/main.go` with Viper config in `internal/config/`. |
| go.dev pkg.go.dev | docs | n/a | Public-API expectations for `pkg/`; reference for whether something belongs there. |
| OpenTelemetry Go SDK | OSS | yes | Lives in `internal/middleware/` for HTTP / interceptor for gRPC. |
| Pinned `golang-standards/project-layout` | community | n/a | The widely-shared but unofficial layout — use this methodology's pragmatic version, not the repo's heavy version. |

## Templates & scripts

`templates.md` ships handler/service/repository templates. The gap is a `golangci-lint` config that mechanically enforces the layout boundaries. Inline drop-in (≤50 lines):

```yaml
# .golangci.yml — enforce go-standard-layout boundaries.
run:
  go: "1.22"
  timeout: 5m
linters:
  enable:
    - depguard
    - revive
    - errcheck
    - govet
    - gosec
    - staticcheck
    - unused
linters-settings:
  depguard:
    rules:
      no-internal-from-pkg:
        list-mode: lax
        files: ["**/pkg/**"]
        deny:
          - pkg: "**/internal/**"
            desc: "pkg/ must not import internal/"
      handler-must-not-touch-repository:
        list-mode: lax
        files: ["**/internal/handler/**"]
        deny:
          - pkg: "**/internal/repository"
            desc: "handler/ must call service/, not repository/"
  revive:
    rules:
      - name: package-comments
      - name: var-naming
      - name: exported
issues:
  exclude-dirs: [migrations, vendor, bin]
```
Run `golangci-lint run` in pre-commit and CI. The layout-linter agent reads its JSON output to write human-readable PR comments.

## Best practices
- Treat `pkg/` as guilty-until-proven-innocent: every new package needs an ADR justifying public API.
- Default interfaces to consumer side (`internal/service` declares the `UserRepo` interface it needs; `internal/repository` implements it). Catches via `go-cleanarch`.
- One binary = one `cmd/<name>/main.go` containing only wiring; business logic stays in `internal/`.
- Pin a single migration tool repo-wide; record in ADR-0001.
- Multi-stage Docker build with `scratch` or `distroless`; `cmd/<name>` becomes the only `COPY`.
- `Makefile` (or `mage`) is the source of truth for `lint`, `test`, `build`, `migrate`, `run` — scaffold both forms once.
- Add `go vet ./...` and `golangci-lint run` to a `make ci` target and to pre-commit.
- Versioned API folders (`internal/handler/v1`) when you go past one external consumer.

## AI-agent gotchas
- LLMs love copying the unofficial `golang-standards/project-layout` (with its many extra folders). Force the prompt to use *this* methodology's smaller subset.
- Generated code often declares interfaces in the producer package, causing import cycles when humans add tests. Add a lint rule plus an explicit prompt instruction.
- `pkg/` bloat: agents auto-export everything as "best practice." Block via `depguard` and require ADR.
- Migrations get scattered across `db/`, `migrations/`, `internal/db/migrations/` if you don't pin in the prompt.
- Generated Dockerfiles tend to use `golang:latest` (rebuilds break) and skip `CGO_ENABLED=0` (binary won't run on `scratch`). Pin Go version + CGO flags in the prompt.
- Long Go modules blow context; feed agents one package + go.mod + golangci.yml at a time.
- Human-in-loop checkpoints: (1) any new top-level folder, (2) any `pkg/` addition, (3) module split (introducing a second `go.mod`) — these are hard to reverse cleanly.

## References
- Go Modules layout (official) — https://go.dev/doc/modules/layout
- Russ Cox / Go team commentary on `golang-standards/project-layout` — https://github.com/golang-standards/project-layout/issues/117
- Effective Go — https://go.dev/doc/effective_go
- Practical Go: Real World Advice — Dave Cheney — https://dave.cheney.net/practical-go/presentations/qcon-china.html
- Standard Go Project Layout (community, opinionated) — https://github.com/golang-standards/project-layout
- go-cleanarch — https://github.com/roblaszczak/go-cleanarch
- golangci-lint — https://golangci-lint.run
- depguard — https://github.com/OpenPeeDeeP/depguard
- Local methodology: `go-standard-layout/README.md`, `templates.md`, `examples.md`, `checklist.md`
