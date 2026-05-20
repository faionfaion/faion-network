---
slug: error-handling
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Standardized HTTP API error envelope following RFC 7807 / RFC 9457: every 4xx and 5xx response carries type (URI), title, status, detail, instance, and traceId fields, with an optional errors[] array for field-level validation failures.
content_id: "2122f774409c6e33"
tags: [error-handling, rfc-7807, api, http, problem-details]
---
# Error Handling (RFC 7807 Problem Details)

## Summary

**One-sentence:** Standardized HTTP API error envelope following RFC 7807 / RFC 9457: every 4xx and 5xx response carries type (URI), title, status, detail, instance, and traceId fields, with an optional errors[] array for field-level validation failures.

**One-paragraph:** Standardized HTTP API error envelope following RFC 7807 / RFC 9457: every 4xx and 5xx response carries type (URI), title, status, detail, instance, and traceId fields, with an optional errors[] array for field-level validation failures. A single exception handler per framework maps all error types to this shape.

## Applies If (ALL must hold)

- Designing or refactoring HTTP API error responses so every endpoint emits the same envelope.
- Mapping framework exceptions to HTTP responses (FastAPI, Express, Spring, ASP.NET, Axum).
- Wiring traceId into responses and logs for Sentry/Datadog/Tempo correlation.
- Generating OpenAPI/Problem schema components for SDK code-gen.
- Migrating ad-hoc {"error": "..."} payloads to a documented error contract.

## Skip If (ANY kills it)

- Internal RPC/gRPC paths — use google.rpc.Status instead.
- WebSocket frames or SSE event streams — design a separate envelope.
- Hot paths where every byte matters (mobile-bandwidth APIs) — strip to code/message.
- Public unauthenticated endpoints where instance and traceId leak request topology.

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
