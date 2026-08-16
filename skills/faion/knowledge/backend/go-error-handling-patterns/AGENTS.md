# Go Error Handling Patterns (Wrap, Translate, Sentinel, Log-Once)

## Summary

**One-sentence:** Produces a Go error-handling tactics spec: wrap with `%w` once per layer, translate storage sentinels at repository boundary, single `apperror` package with sentinel vars + AppError struct, log exactly once per request.

**Ефективно для:**

- Services with 3+ layers between storage and handler.
- Teams that previously had log-spam or lost error chains.
- Codebases with multiple storage backends (SQL + NoSQL + cache).
- Migrations from string-comparing errors to typed chains.

**One-paragraph:** Wrap errors once per layer with `fmt.Errorf("verb context: %w", err)` to preserve the `errors.Is`/`errors.As` chain. Translate storage-layer sentinels (`sql.ErrNoRows`) into domain sentinels (`ErrNotFound`) at the repository boundary. Define ONE `apperror` package with sentinel vars and a typed `AppError` struct; never scatter `errors.New("not found")` per call site. Log errors at exactly one place per request — the outermost handler.

## Applies If (ALL must hold)

- Go ≥1.13 (error wrapping).
- Multi-layer architecture (handler → service → repository).
- Lint rules accept `errorlint` / `wrapcheck`.
- Logging is structured (zap / zerolog / slog).

## Skip If (ANY kills it)

- Single-layer scripts — `fmt.Errorf("%s", err)` is enough.
- Library packages — return wrapped errors, no logging.
- gRPC services that already use `status` codes end-to-end.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| apperror package committed | code | team |
| Per-package sentinel catalogue | doc page | team |
| Lint config with errorlint + wrapcheck | CI config | SRE |
| Structured logger | ADR | tech lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[go-error-handling]]` | AppError taxonomy |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 testable rules with rationale + source | ~1300 |
| `content/02-output-contract.xml` | essential | artefact JSON Schema + error-module code-shape contract + forbidden code shapes | ~1400 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with symptom / root-cause / fix | ~1200 |
| `content/04-procedure.xml` | essential | 5-step artefact procedure + 5-step implementation sub-procedure | ~1400 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-existing-errors` | sonnet | Finds double-wraps + string equality. |
| `draft-translation-table` | haiku | Storage sentinel → domain sentinel map. |
| `write-lint-rules` | haiku | errorlint / wrapcheck config. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-error-handling-patterns.json` | JSON Schema for the Go Error Handling Patterns (Wrap, Translate, Sentinel, Log-Once) output contract |
| `templates/go-error-handling-patterns.md.j2` | Markdown skeleton with the required fields |
| `templates/go-error-handling-patterns.md` | Markdown skeleton with the required fields Generated from `templates/go-error-handling-patterns.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a go-error-handling-patterns record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-error-handling-patterns record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/check-errors.sh` | Grep gate for string-equality error checks, `%v` wraps and unhandled returns |
| `templates/apperror.go` | Canonical sentinel set + AppError with Unwrap + constructors + `AsAppError` extractor |
| `templates/golangci.yml` | golangci-lint config: errorlint (errorf/asserts/comparison), wrapcheck, errcheck, nilerr |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-error-handling-patterns.py` | Enforce the Go Error Handling Patterns (Wrap, Translate, Sentinel, Log-Once) output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[go-error-handling]]
- [[go-backend]]
- [[go-http-handlers]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/go-error-handling-patterns.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/go-error-handling-patterns.json",
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
      "pattern": "^goep\\-[a-z0-9-]+$"
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
