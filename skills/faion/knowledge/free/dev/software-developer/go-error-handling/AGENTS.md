---
slug: go-error-handling
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Typed AppError with Code, Message, HTTPStatus, Err.
content_id: "e5fd377af7509efc"
tags: [go, error-handling, http, middleware, typed-errors]
---
# Go Error Handling

## Summary

**One-sentence:** Typed AppError with Code, Message, HTTPStatus, Err.

**One-paragraph:** Typed AppError with Code, Message, HTTPStatus, Err. HTTP middleware translates to JSON. Wrap at repo boundaries. Use errors.As, never type assertions.

## Applies If (ALL must hold)

- New Go HTTP service (chi / gin / echo / stdlib net/http) needing consistent JSON error responses
- Refactoring a service that returns bare errors.New(...) — wrap with apperror.New* constructors
- Adding correlation / trace IDs to error responses for production debugging
- Standardizing structured error logging (slog, zerolog, zap)
- Library code needing typed errors callable via errors.Is / errors.As

## Skip If (ANY kills it)

- gRPC services — use google.golang.org/grpc/status + codes.Code; HTTPStatus is meaningless
- CLI tools — errors go to stderr + exit code; JSON overhead not justified
- Public library packages — custom error type forces consumers to depend on your package; prefer sentinel errors
- Shallow code paths where fmt.Errorf("%w", err) chains already do the job

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

- parent skill: `free/dev/software-developer/`
