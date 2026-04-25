# Agent Integration — Go Project Structure

## When to use
- Bootstrapping a new Go service, CLI, or library and you need a layout that scales
- Refactoring a flat single-package Go program once it crosses ~3 entry points or ~5 domain concepts
- Standardizing across multiple Go services in a monorepo or org so agents can navigate predictably
- Wiring DI manually with constructors in `cmd/<bin>/main.go` rather than reaching for a framework
- Producing repeatable Docker + Makefile + module hygiene that LLMs can replicate

## When NOT to use
- One-file scripts and learning exercises — flat layout beats premature `internal/cmd/pkg`
- Pure libraries: don't add `internal/` and `cmd/` if all you ship is exported packages
- Code generators that already define their own layout (`buf`, `kubebuilder`, `cobra-cli`) — follow theirs
- Multi-language monorepos where Go is one of N — use the org-wide layout, not Go-specific defaults
- When team consensus differs: enforcing `golang-standards/project-layout` against the team will lose

## Where it fails / limitations
- The popular `golang-standards/project-layout` is community-curated, not official; agents quote it as canon and overbuild
- `pkg/` is often misused as a dumping ground; without a clear "this is API for outsiders" rule, it loses meaning
- `internal/` boundary is enforced by the toolchain but agents still leak through interfaces with public types
- Cyclic-import errors hit late and confuse agents — they "fix" by exporting more symbols, worsening coupling
- DI by hand-wiring in `main.go` grows long; agents reach for `wire`/`fx` too early
- Default `cmd/<name>/main.go` layout creates ceremony for tiny CLIs that fit in one file

## Agentic workflow
For a new project, run a scaffolder agent that asks for module path, binary names, and DB driver, then emits the `cmd/`, `internal/`, `pkg/`, `Makefile`, `Dockerfile`, and a single test. For an existing project, an auditor agent maps imports, finds cycles and `internal/` violations, and proposes a single refactor PR. Treat `go vet`, `staticcheck`, and `golangci-lint` as the quality gate the agent must pass before commit.

### Recommended subagents
- `faion-sdd-executor-agent` — design + scaffold + verify with quality gates
- A custom `go-scaffolder` (haiku) — emits the canonical tree from a small JSON spec
- A custom `go-import-auditor` (sonnet) — runs `go list -deps`, detects cycles and `internal/` leaks, drafts a refactor plan

### Prompt pattern
```
Scaffold a Go service:
- module: github.com/<org>/<name>
- binaries: api, worker
- db: postgres (sqlx)
- logging: zap
Output: directory tree, go.mod, cmd/api/main.go, cmd/worker/main.go,
internal/{config,database,handler,repository,service,model}, Makefile, Dockerfile.
Use Go 1.22+, standard library net/http unless told otherwise.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go` (toolchain) | `go mod`, `go vet`, `go build`, `go test` | https://go.dev/dl |
| `golangci-lint` | Aggregator linter; canonical Go quality gate | https://golangci-lint.run |
| `staticcheck` | Deep static analysis (subset bundled in golangci-lint) | https://staticcheck.dev |
| `goimports` | Format + manage imports | `go install golang.org/x/tools/cmd/goimports@latest` |
| `gofumpt` | Stricter `gofmt` | https://github.com/mvdan/gofumpt |
| `go-mod-outdated` | Spot stale deps | `go install github.com/psampaz/go-mod-outdated@latest` |
| `air` / `reflex` | Live-reload during dev | https://github.com/air-verse/air |
| `mockery` | Generate mocks for interfaces | https://vektra.github.io/mockery |
| `ko` | Build OCI images for Go without Dockerfiles | https://ko.build |
| `goreleaser` | Cross-build + release artifacts | https://goreleaser.com |
| `wire` (optional) | Compile-time DI when hand-wiring grows | https://github.com/google/wire |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GoReleaser + GitHub Actions | OSS | Yes | YAML-driven, easy for agents to author |
| Renovate / Dependabot | SaaS | Yes | Keep `go.mod` honest |
| pkg.go.dev | SaaS | Yes | Doc surface for `pkg/` API |
| sigstore / cosign | OSS | Yes | Sign release binaries from CI |
| Datadog / New Relic / OpenTelemetry-Go | SaaS / OSS | Yes | Wire `internal/observability` once, reuse across `cmd/*` |
| Buf | SaaS+OSS | Yes | If proto/gRPC, integrates cleanly with `api/` directory |

## Templates & scripts
See `templates.md` for the full Makefile and Dockerfile. Inline minimal scaffolder snippet to materialize the standard tree:

```bash
#!/usr/bin/env bash
# scaffold-go.sh — usage: scaffold-go.sh github.com/org/name api worker
set -euo pipefail
mod="${1:?module path}"; shift
bins=("$@")
mkdir -p api deployments docs scripts pkg
for b in "${bins[@]}"; do mkdir -p "cmd/$b" && cat > "cmd/$b/main.go" <<EOF
package main
import "log"
func main() { log.Println("$b boot") }
EOF
done
for d in config database handler middleware model repository service; do
  mkdir -p "internal/$d"
  : > "internal/$d/.gitkeep"
done
go mod init "$mod"
gofmt -w .
echo "scaffold ready: $mod with binaries: ${bins[*]}"
```

## Best practices
- Keep `cmd/<bin>/main.go` thin: parse flags, load config, wire deps, call `Run(ctx)` from an internal package
- Put domain types in `internal/model`; keep them DB-tag-free if you also expose them via JSON — use separate DTOs in `internal/handler`
- Use `internal/` aggressively; reach for `pkg/` only when an external module imports it
- Define `Repository` and `Service` interfaces near consumers, not producers — keeps wiring testable and avoids leaky cross-package types
- One linter config: commit `.golangci.yml` and run identical rules locally and in CI
- Pin Go version in `go.mod` (`go 1.22`) and `Dockerfile` together; CI must match
- Always set `CGO_ENABLED=0` in container builds unless you need cgo; saves base image size and runtime headaches

## AI-agent gotchas
- Agents over-apply the `golang-standards/project-layout` to tiny projects; require a size threshold before adopting
- LLMs put everything in `pkg/` because tutorials show it; reviewers must enforce `internal/` default
- Cyclic imports are a frequent agent mistake — they "fix" by moving symbols up; instead, extract a third package owning the shared types
- Agents add `wire`/`fx` immediately; require a "manual wire grew past 100 lines" trigger before adding
- Agents forget `context.Context` plumbing through repository methods; lint with `contextcheck` linter
- Agents leave global `var DB *sql.DB`; require a constructor pattern (`NewUserRepository(db)`)
- Human-in-loop checkpoint: any DB schema change colocated under `internal/database/migrations/` needs a separate PR and review

## References
- https://go.dev/doc/effective_go
- https://go.dev/doc/modules/layout — official layout guidance (small)
- https://github.com/golang-standards/project-layout — community layout (verbose)
- https://github.com/uber-go/guide/blob/master/style.md
- https://google.github.io/styleguide/go/decisions
- https://golangci-lint.run
- https://github.com/google/wire — DI when needed
