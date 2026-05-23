---
slug: go-error-handling
tier: pro
group: backend-systems
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a Go error-taxonomy spec: project-wide `AppError` struct (code, message, HTTP status, wrap chain), per-package sentinels, Gin/Echo middleware mapping `AppError` to RFC 7807 JSON."
content_id: "f93e8b614cc8d11d"
complexity: medium
produces: spec
est_tokens: 4300
tags: [go, error-handling, rfc-7807, gin, echo, middleware]
---

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

| Methodology | Why |
|-------------|-----|
| `[[error-handling]]` | RFC 7807 envelope |
| `[[go-backend]]` | service layout |

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
| `draft-apperror-struct` | haiku | Boilerplate AppError + helpers. |
| `write-middleware` | sonnet | Framework-specific render hook. |
| `audit-log-once` | sonnet | Detects log-spam + envelope leaks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-error-handling.json` | JSON Schema for the Go Error Handling (AppError + Centralised Mapper) output contract |
| `templates/go-error-handling.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-error-handling record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-error-handling.py` | Enforce the Go Error Handling (AppError + Centralised Mapper) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[error-handling]]
- [[go-error-handling-patterns]]
- [[go-http-handlers]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
