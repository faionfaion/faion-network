---
slug: error-handling
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for standardizing API error responses following RFC 7807 Problem Details: every error returns `type` (URI), `title`, `status`, `detail`, `instance`, `traceId`, and an optional `errors[]` array for field-level validation failures.
content_id: "2122f774409c6e33"
tags: [rfc-7807, error-handling, api-design, problem-details, rest]
---
# Error Handling with RFC 7807 Problem Details

## Summary

**One-sentence:** A methodology for standardizing API error responses following RFC 7807 Problem Details: every error returns `type` (URI), `title`, `status`, `detail`, `instance`, `traceId`, and an optional `errors[]` array for field-level validation failures.

**One-paragraph:** A methodology for standardizing API error responses following RFC 7807 Problem Details: every error returns `type` (URI), `title`, `status`, `detail`, `instance`, `traceId`, and an optional `errors[]` array for field-level validation failures. All endpoints share one shape, one content-type (`application/problem+json`), and one error-handler entry point.

## Applies If (ALL must hold)

- New REST API where consistent client-side error handling matters.
- Refactoring mixed error shapes (`{error:"..."}`, `{detail:"..."}`, HTML) into one envelope.
- Public-facing APIs where error shape is part of the published contract.
- Multi-service architectures where clients must not memorize per-service formats.
- API gateway / BFF setups translating downstream errors.

## Skip If (ANY kills it)

- gRPC — use `google.rpc.Status` + `google.rpc.error_details` instead.
- GraphQL — errors live in the response `errors[]` array per spec.
- Internal-only low-stability APIs where the envelope overhead outweighs benefit.
- Streaming endpoints (SSE, WebSocket) — error frames follow their own conventions.
- Static asset / file download endpoints — return raw HTTP status, no body.

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
