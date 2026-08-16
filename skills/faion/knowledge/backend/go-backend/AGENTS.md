# Go Backend Development Patterns

## Summary

**One-sentence:** Produces a Go service scaffold spec: cmd/ + internal/ + pkg/ layout, handler→service→repository layering, request DTOs, context propagation, typed errors, graceful shutdown, framework choice (Gin/Echo/Chi/stdlib).

**Ефективно для:**

- New Go services with REST / gRPC endpoints.
- Migrating prototype Go code to production discipline.
- Multi-binary monorepos under one `cmd/` parent.
- LLM-agent-driven scaffolding of repetitive resources.

**One-paragraph:** Production-grade Go backend patterns with Gin / Echo / Chi / stdlib: project structure (`cmd/` + `internal/` + `pkg/`), layered architecture (handler → service → repository), HTTP routers, request binding, worker pools, fan-out/fan-in concurrency, centralized error handling, interfaces defined at the consumer side for testability, context propagation, typed errors with HTTP status codes, graceful shutdown with `WaitGroup`, goroutine leak prevention, and middleware ordering pitfalls agents face.

## Applies If (ALL must hold)

- Service in Go ≥1.22 (stdlib router available).
- Layered architecture (handler/service/repository) acceptable.
- Single framework choice locked per service.
- Production deploy uses graceful shutdown semantics.

## Skip If (ANY kills it)

- Single-file scripts / one-shot CLIs — overkill.
- Pure library packages (`pkg/`) without runtime services.
- Team standardised on a different framework split mid-codebase.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Layout decision | ADR | tech lead |
| Framework choice (Gin/Echo/Chi/stdlib) | ADR | tech lead |
| Logging + tracing pipeline | infra doc | SRE |
| Error taxonomy | ADR | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[go-layout-directory-structure]]` | directory skeleton |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 14 testable rules with rationale + source | ~1500 |
| `content/02-output-contract.xml` | essential | artefact JSON Schema + repo-shape contract + valid / invalid examples | ~1200 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns with symptom / root-cause / fix | ~1400 |
| `content/04-procedure.xml` | essential | 5-step artefact procedure + 6-step scaffold sub-procedure | ~1500 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-layout` | haiku | Mechanical directory + boilerplate. |
| `generate-resource` | sonnet | Per-resource handler/service/repo set. |
| `review-layering` | sonnet | Audits handler→service→repo direction. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-backend.json` | JSON Schema for the Go Backend Development Patterns output contract |
| `templates/go-backend.md.j2` | Markdown skeleton with the required fields |
| `templates/go-backend.md` | Markdown skeleton with the required fields Generated from `templates/go-backend.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a go-backend record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-backend record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/app-error.go` | AppError struct, sentinel errors and constructors the ErrorHandler middleware maps from |
| `templates/check-layout.sh` | CI script verifying `internal/` dirs exist and `internal/` is not imported externally |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-backend.py` | Enforce the Go Backend Development Patterns output contract | After subagent returns, before downstream consumer reads |
| `scripts/check-go-layout.py` | Scan a real Go repo for layout invariants: cmd/api/main.go, internal/ subdirs, thin main, interfaces out of `repository/`, forbidden `BindJSON` / `c.JSON(4xx)` / gin.Context-in-goroutine | Pre-commit gate; CI before `go build` |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[go-http-handlers]]
- [[go-error-handling]]
- [[go-concurrency-patterns]]
- [[go-goroutines]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/go-backend.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/go-backend.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^gobe\\-[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!team$|we$|us$|engineering$)"
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 60
    },
    "inputs_used": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "source": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "deprecated"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "notes": {
      "type": "string"
    }
  }
}
```
