# API Error Handling

## Summary

A methodology for structuring API error responses using RFC 7807 Problem Details format. Every error response carries `type` (URI), `title`, `status`, `detail`, `instance`, and `traceId`; field-level validation errors attach an `errors` array. All errors use a shared Pydantic model and centralised exception handlers.

## Why

Inconsistent error shapes force clients to write per-endpoint error parsing. RFC 7807 is an IETF standard that gives clients a predictable envelope to inspect without reading docs. The `traceId` field correlates client-reported errors to server logs, cutting debugging time dramatically. Never exposing raw exception messages prevents information leakage.

## When To Use

- Designing a new REST or HTTP API from scratch
- Standardising error responses across an existing API with inconsistent formats
- Adding structured field-level validation errors for form-backing endpoints
- When debugging requires correlating client errors to server-side log traces

## When NOT To Use

- GraphQL APIs — use the `errors` array in the GraphQL envelope instead
- Internal service-to-service APIs where both sides are controlled and a simpler format is agreed — RFC 7807 overhead is not always justified
- WebSocket or streaming APIs where error framing is protocol-specific

## Content

| File | What's inside |
|------|---------------|
| `content/01-problem-detail.xml` | RFC 7807 schema, field semantics, error code catalogue, message quality rules |
| `content/02-implementation.xml` | FastAPI exception handlers, ProblemDetail Pydantic model, validation error mapping |

## Templates

| File | Purpose |
|------|---------|
| `templates/problem_detail.py` | ProblemDetail Pydantic model + FastAPI exception handler wiring |
| `templates/error_codes.py` | ErrorCode constants for client and server error categories |
