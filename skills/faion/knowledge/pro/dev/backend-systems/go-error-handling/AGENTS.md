---
slug: go-error-handling
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Typed error taxonomy for Go services: a project-wide AppError struct with code, message, HTTP status, and wrapping chain, plus a central Gin middleware that converts domain errors to structured JSON.
content_id: "e5fd377af7509efc"
tags: [go, errors, middleware, http, logging]
---
# Go Error Handling

## Summary

**One-sentence:** Typed error taxonomy for Go services: a project-wide AppError struct with code, message, HTTP status, and wrapping chain, plus a central Gin middleware that converts domain errors to structured JSON.

**One-paragraph:** Typed error taxonomy for Go services: a project-wide AppError struct with code, message, HTTP status, and wrapping chain, plus a central Gin middleware that converts domain errors to structured JSON. Every error crossing a layer boundary must be wrapped, typed, and logged exactly once at the handler boundary.

## Applies If (ALL must hold)

- Establishing a project-wide error policy on a new Go service.
- Refactoring legacy fmt.Errorf strings into typed, classifiable errors.
- Adding centralized error-handler middleware mapping domain errors to JSON + logs + traces.
- Building errors.Is / errors.As predicates for cross-package error checks.

## Skip If (ANY kills it)

- Library code for external consumers — exposing AppError leaks internals; use small sentinels.
- Tiny CLIs / one-shot scripts — fmt.Errorf("%w", err) plus exit code is enough.
- Teams already standardized on pkg/errors or cockroachdb/errors — don't fork.
- Greenfield where Go 1.20+ errors.Join + %w already covers the wrapping needs.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/dev/backend-systems/`
