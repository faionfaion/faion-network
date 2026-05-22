---
slug: api-error-handling
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Standardize REST API error responses using RFC 7807 Problem Details: a JSON object with `type` (URI), `title`, `status`, `detail`, `instance`, `traceId`, and optional `errors` array for field-level validation failures.
content_id: "69ecdae3ba96f738"
tags: [api-errors, problem-details, rfc-7807, error-handling, rest-api]
---
# API Error Handling

## Summary

**One-sentence:** Standardize REST API error responses using RFC 7807 Problem Details: a JSON object with `type` (URI), `title`, `status`, `detail`, `instance`, `traceId`, and optional `errors` array for field-level validation failures.

**One-paragraph:** Standardize REST API error responses using RFC 7807 Problem Details: a JSON object with `type` (URI), `title`, `status`, `detail`, `instance`, `traceId`, and optional `errors` array for field-level validation failures. Every error response must include a trace ID.

## Applies If (ALL must hold)

- Designing any new REST API endpoint that can fail.
- Unifying error responses across an existing API with inconsistent shapes.
- Implementing global exception handlers in FastAPI, Django, or Express.
- Adding field-level validation error details.

## Skip If (ANY kills it)

- Internal RPC calls where structured JSON adds overhead with no consumer benefit.
- Streaming endpoints where a full JSON error body disrupts the stream protocol.
- Simple CLI tools — plain stderr messages are sufficient.

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
