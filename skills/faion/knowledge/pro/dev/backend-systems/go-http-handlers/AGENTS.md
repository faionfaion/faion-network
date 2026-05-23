---
slug: go-http-handlers
tier: pro
group: backend-systems
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a Go HTTP-handler spec: handler methods on dependency-injecting struct, request DTOs with binding/validate tags, typed response structs, RFC 7807 mapping, httptest-driven table tests."
content_id: "66f63532bb241ce8"
complexity: medium
produces: spec
est_tokens: 4300
tags: [go, http, handlers, gin, echo, chi]
---

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
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
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
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-http-handlers record |

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
