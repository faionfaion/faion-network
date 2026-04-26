# Error Handling (RFC 7807 Problem Details)

## Summary

Standardized HTTP API error envelope following RFC 7807 / RFC 9457: every 4xx and 5xx response carries `type` (URI), `title`, `status`, `detail`, `instance`, and `traceId` fields, with an optional `errors[]` array for field-level validation failures. A single exception handler per framework maps all error types to this shape.

## Why

Inconsistent error shapes break API clients, make debugging impossible without log access, and prevent automated SDK generation. RFC 7807 gives clients a machine-readable `type` URI to branch on, a stable `traceId` to correlate with backend traces, and a `status` field that matches the HTTP status — three properties that ad-hoc `{"error": "..."}` payloads never reliably provide.

## When To Use

- Designing or refactoring HTTP API error responses so every endpoint emits the same envelope.
- Mapping framework exceptions to HTTP responses (FastAPI, Express, Spring, ASP.NET, Axum).
- Wiring `traceId` into responses and logs for Sentry/Datadog/Tempo correlation.
- Generating OpenAPI/Problem schema components for SDK code-gen.
- Migrating ad-hoc `{"error": "..."}` payloads to a documented error contract.

## When NOT To Use

- Internal RPC/gRPC paths — use `google.rpc.Status` instead.
- WebSocket frames or SSE event streams — design a separate envelope.
- Hot paths where every byte matters (mobile-bandwidth APIs) — strip to `code`/`message`.
- Public unauthenticated endpoints where `instance` and `traceId` leak request topology.

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema.xml` | ProblemDetail + FieldError JSON schema, OpenAPI component definition. |
| `content/02-implementation.xml` | FastAPI exception handlers, error codes enum, traceId propagation. |
| `content/03-rules.xml` | Antipatterns (info leakage, missing 5xx, stale type URIs) and best practices. |

## Templates

| File | Purpose |
|------|---------|
| `templates/problem_detail.py` | Pydantic ProblemDetail model + FastAPI exception handlers. |
| `templates/openapi_problem.yaml` | OpenAPI components/schemas for ProblemDetail and FieldError. |
| `templates/check_problem_refs.py` | Script verifying every 4xx/5xx op refs ProblemDetail in OpenAPI spec. |
