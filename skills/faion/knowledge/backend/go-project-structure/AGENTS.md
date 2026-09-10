# Go Project Structure

## Summary

**One-sentence:** Standard Go project layout using cmd/, internal/, and an optional pkg/ for code intended for external import.

**One-paragraph:** Standard Go project layout using cmd/, internal/, and an optional pkg/ for code intended for external import. Applications live under cmd/<name>/main.go, private logic under internal/{handler,service,repository,model,config}. Dependency injection via constructors; no package-level globals. Graceful shutdown covers the HTTP server, DB pools, queue consumers, and long-running goroutines. Output is the directory skeleton + config + Dockerfile + a working end-to-end vertical slice for at least one resource.

**Ефективно для:**

- Bootstrapping a new Go service or CLI that follows community norms.
- Standardising layout across many services so on-call engineers find files in the same place.
- Splitting a single-package main into internal/{handler,service,repository,model} once it crosses ~1k LoC.
- Adding a second binary (worker, admin CLI) as a second cmd/<name>/main.go.

## Applies If (ALL must hold)

- Bootstrapping a new Go service or CLI that follows community norms.
- Splitting a single-package main into internal/{handler,service,repository,model} once it crosses ~1k LoC.
- Adding a second binary (background worker, admin CLI) as a second cmd/<name>/main.go.
- Standardising layout across many services so on-call engineers find files in the same place.

## Skip If (ANY kills it)

- Tiny single-file scripts or quick experiments — main.go next to go.mod is enough.
- Library-only repos — cmd/, internal/, deployments/ are noise; structure by feature subpackages.
- Go modules being published publicly — heavy internal/ use prevents downstream consumers.
- Monorepos with many services sharing a root — prefer one Go module per service.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Go module path | string | team / repo convention |
| Resource list | yaml / md | team — the first vertical slice |
| Container target | OCI image | infra catalog |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 testable rules (layout, thin cmd, no cycles, Makefile orchestration, clean top level, shutdown, run + skip leaves) | ~1600 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns + allowed transformations | ~1100 |
| `content/03-failure-modes.xml` | essential | 11 antipatterns (symptom / root-cause / fix), incl. the agent-specific ones | ~1500 |
| `content/04-procedure.xml` | essential | 8-step procedure end-to-end incl. Makefile authoring + import-boundary enforcement | ~1200 |
| `content/06-decision-tree.xml` | essential | Root question + 11 blocking-gate branches → conclusion(ref=rule-id) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-layout` | sonnet | Layout decisions need light judgement; structure is mechanical. |
| `draft-vertical-slice` | sonnet | Writing handler/service/repo + tests benefits from sonnet. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Dockerfile` | Multi-stage distroless Dockerfile for Go services |
| `templates/.dockerignore` | **Ships with the Dockerfile or `COPY . .` bakes `.env` into the image.** |
| `templates/Makefile` | Build / run / test / lint / tidy targets |
| `templates/new-resource.sh` | Scaffold handler/service/repository/model for a new resource |
| `templates/scaffold-go.sh` | Bootstrap the whole tree: cmd/, internal/, pkg/, migrations/, go.mod |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-project-structure.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/dev/backend-systems/`
- [[rust-project-structure]]
- [[rust-backend]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
