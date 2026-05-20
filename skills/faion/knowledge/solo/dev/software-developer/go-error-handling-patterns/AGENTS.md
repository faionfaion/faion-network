---
slug: go-error-handling-patterns
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Go error handling convention for services: define sentinel errors in one apperror package; wrap with fmt.
content_id: "62abd60a22cf38be"
tags: [go, error-handling, best-practices, testing]
---
# Go Error Handling Patterns

## Summary

**One-sentence:** Go error handling convention for services: define sentinel errors in one apperror package; wrap with fmt.

**One-paragraph:** Go error handling convention for services: define sentinel errors in one apperror package; wrap with fmt.Errorf("op: %w", err); check errors with errors.Is/As, never ==; map domain errors to HTTP/gRPC codes only at transport edge; log once at boundary, never log-and-return.

## Applies If (ALL must hold)

- Designing error contracts for a new Go service or library
- Refactoring legacy Go code with bare errors.New or stringly-typed errors
- Auditing for double-wrapping, missing errors.Is checks, or log-and-return chains
- Mapping domain errors to HTTP status codes or gRPC status
- Preparing for SLO/observability rollout where one failure must yield exactly one alert

## Skip If (ANY kills it)

- Quick scripts where log.Fatal on first error is acceptable
- One-shot migration scripts where building a sentinel taxonomy is overkill
- main.go bootstrap where panic is the documented failure mode

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

- parent skill: `solo/dev/software-developer/`
