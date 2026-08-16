# Go Error Handling (AppError + Centralised Mapper)

## Summary

**One-sentence:** Produces a Go error-taxonomy spec: project-wide `AppError` struct (code, message, HTTP status, wrap chain), per-package sentinels, Gin/Echo middleware mapping `AppError` to RFC 7807 JSON.

**Ефективно для:**

- Services with 5+ error categories surfaced to clients.
- Microservice meshes needing consistent envelope across services.
- Telemetry pipelines that group by `error.code`.
- Public APIs needing self-documenting error catalogue.

**One-paragraph:** Typed error taxonomy for Go services: a project-wide `AppError` struct with code, message, HTTP status, and wrapping chain, plus a central Gin / Echo middleware that converts domain errors to structured JSON. Every error crossing a layer boundary MUST be wrapped, typed, and logged exactly once at the handler boundary.

## Applies If (ALL must hold)

- Go service exposes HTTP / gRPC.
- Middleware framework supports a single error handler hook.
- Tracing system tags errors with code/category.
- Team agreed on a single AppError struct shape.

## Skip If (ANY kills it)

- Internal CLIs without exposed errors — `fmt.Errorf` is enough.
- Library packages — return wrapped errors, leave envelope to caller.
- gRPC-only services — use `status.Error` codes instead of HTTP status.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Error catalogue | doc page | team |
| Framework error-hook (Gin/Echo) | code | team |
| Tracing tagger | infra doc | SRE |
| Logging format (structured JSON) | ADR | tech lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[error-handling]]` | RFC 7807 envelope |
| `[[go-backend]]` | service layout |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 13 testable rules with rationale + source | ~1600 |
| `content/02-output-contract.xml` | essential | artefact JSON Schema + apperror/middleware/lint code-shape contract + valid / invalid examples | ~1500 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns with symptom / root-cause / fix | ~1300 |
| `content/04-procedure.xml` | essential | 5-step artefact procedure + 5-step implementation sub-procedure | ~1500 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-apperror-struct` | haiku | Boilerplate AppError + helpers. |
| `write-middleware` | sonnet | Framework-specific render hook. |
| `audit-log-once` | sonnet | Detects log-spam + envelope leaks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-error-handling.json` | JSON Schema for the Go Error Handling (AppError + Centralised Mapper) output contract |
| `templates/go-error-handling.md.j2` | Markdown skeleton with the required fields |
| `templates/go-error-handling.md` | Markdown skeleton with the required fields Generated from `templates/go-error-handling.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a go-error-handling record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-error-handling record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/apperror.go` | AppError type, immutable sentinels, fresh-instance constructors, status-preserving `Wrap`, `IsCode` |
| `templates/error_middleware.go` | Gin ErrorHandler middleware rendering AppError to the JSON envelope |
| `templates/error-middleware-stdlib.go` | net/http variant: `Handler func(w,r) error` + `Wrap` adapter, 4xx→slog.Info / 5xx→slog.Error |
| `templates/prompt-error-scaffold.txt` | Sub-agent prompt generating the apperror package + middleware + table-driven tests |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-error-handling.py` | Enforce the Go Error Handling (AppError + Centralised Mapper) output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[error-handling]]
- [[go-error-handling-patterns]]
- [[go-http-handlers]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/go-error-handling.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/go-error-handling.json",
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
      "pattern": "^goeh\\-[a-z0-9-]+$"
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
