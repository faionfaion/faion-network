# Go HTTP Handlers (Gin / Echo / Chi / stdlib)

## Summary

**One-sentence:** Produces a Go HTTP-handler spec: handler methods on dependency-injecting struct, request DTOs with binding/validate tags, typed response structs, RFC 7807 mapping, httptest-driven table tests.

**Ефективно для:**

- Adding new HTTP endpoints to a Go service.
- Migrating handlers from one framework to another.
- LLM agents generating CRUD endpoints from OpenAPI.
- Refactoring fat handlers into thin shells delegating to services.

**One-paragraph:** HTTP handler pattern for Go: handlers as methods on a dependency-injecting struct, request DTOs with `binding` / `validate` tags, typed response structs, RFC 7807 error mapping, and httptest-based table-driven tests. Framework choice (Gin, Echo, Chi, stdlib 1.22 muxer) is locked per project and never mixed mid-file.

## Applies If (ALL must hold)

- Project locked on one HTTP framework.
- Service layer + request DTO layer exist.
- Tests run under httptest with the actual router wired in.
- Error mapping middleware exists.

## Skip If (ANY kills it)

- Pure gRPC service — different handler shape.
- Static-only / proxy-only routes — no business logic.
- Server-sent events / WebSocket endpoints — different lifecycle.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Framework choice (Gin/Echo/Chi/stdlib) | ADR | tech lead |
| Service interface | code | team |
| Request DTO conventions (binding tags) | ADR | tech lead |
| Error middleware | code | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-backend]]` | service skeleton |
| `[[go-error-handling]]` | AppError + middleware |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 11 testable rules with rationale + source | ~1500 |
| `content/02-output-contract.xml` | essential | artefact JSON Schema + server/handler shape contract + valid / invalid examples | ~1600 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns with symptom / root-cause / fix | ~1300 |
| `content/04-procedure.xml` | essential | 5-step artefact procedure + 5-step scaffold sub-procedure | ~1500 |
| `content/01-router-setup.xml` | recommended | Middleware order + stdlib 1.22 muxer as the zero-dependency default | ~500 |
| `content/02-handler-pattern.xml` | recommended | Handler struct DI, ShouldBindJSON, context propagation | ~600 |
| `content/03-rules.xml` | recommended | Framework consistency, server timeouts, httptest discipline, agent gotchas | ~600 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-handler` | haiku | Boilerplate per resource. |
| `write-dto-validation` | sonnet | Picks tags + validator funcs. |
| `table-test` | haiku | Mechanical httptest expansion. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-http-handlers.json` | JSON Schema for the Go HTTP Handlers (Gin / Echo / Chi / stdlib) output contract |
| `templates/go-http-handlers.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a go-http-handlers record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-http-handlers record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/gin_router.go` | Gin router with the documented middleware order and route groups |
| `templates/stdlib_handler.go` | stdlib 1.22 App struct with `routes()`, `writeJSON`, `writeProblem` |
| `templates/server.go` | `Wire(cfg) *http.Server` with all four timeouts + `Run()` graceful shutdown on SIGINT/SIGTERM |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-http-handlers.py` | Enforce the Go HTTP Handlers (Gin / Echo / Chi / stdlib) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[go-backend]]
- [[go-error-handling]]
- [[error-handling]]
- [[go-error-handling-patterns]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/go-http-handlers.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/go-http-handlers.json",
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
      "pattern": "^gohh\\-[a-z0-9-]+$"
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
