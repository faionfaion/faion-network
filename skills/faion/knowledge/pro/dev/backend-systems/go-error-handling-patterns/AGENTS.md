---
slug: go-error-handling-patterns
tier: pro
group: backend-systems
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a Go error-handling tactics spec: wrap with `%w` once per layer, translate storage sentinels at repository boundary, single `apperror` package with sentinel vars + AppError struct, log exactly once per request."
content_id: "5995c6d54b5c83eb"
complexity: medium
produces: spec
est_tokens: 4300
tags: [go, errors, wrap, sentinels, log-once]
---

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

| Methodology | Why |
|-------------|-----|
| `[[go-error-handling]]` | AppError taxonomy |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
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
| `templates/go-error-handling-patterns.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-error-handling-patterns record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-error-handling-patterns.py` | Enforce the Go Error Handling Patterns (Wrap, Translate, Sentinel, Log-Once) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[go-error-handling]]
- [[go-backend]]
- [[go-http-handlers]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
