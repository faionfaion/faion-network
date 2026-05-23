---
slug: go-backend
tier: pro
group: backend-systems
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a Go service scaffold spec: cmd/ + internal/ + pkg/ layout, handler→service→repository layering, request DTOs, context propagation, typed errors, graceful shutdown, framework choice (Gin/Echo/Chi/stdlib)."
content_id: "58fefb2147034dd6"
complexity: deep
produces: spec
est_tokens: 4300
tags: [go, backend, gin, echo, rest, production]
---

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

| Methodology | Why |
|-------------|-----|
| `[[go-layout-directory-structure]]` | directory skeleton |

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
| `scaffold-layout` | haiku | Mechanical directory + boilerplate. |
| `generate-resource` | sonnet | Per-resource handler/service/repo set. |
| `review-layering` | sonnet | Audits handler→service→repo direction. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-backend.json` | JSON Schema for the Go Backend Development Patterns output contract |
| `templates/go-backend.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-backend record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-backend.py` | Enforce the Go Backend Development Patterns output contract | After subagent returns, before downstream consumer reads |

## Related

- [[go-http-handlers]]
- [[go-error-handling]]
- [[go-concurrency-patterns]]
- [[go-goroutines]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
