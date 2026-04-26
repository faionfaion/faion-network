# API Error Handling

## Summary

Standardize REST API error responses using RFC 7807 Problem Details: a JSON object with `type` (URI), `title`, `status`, `detail`, `instance`, `traceId`, and optional `errors` array for field-level validation failures. Every error response must include a trace ID.

## Why

RFC 7807 gives API consumers a machine-readable error type URI, a human-readable title, and a correlation handle (traceId) — all in one predictable envelope. Consistent structure means clients need one error-handling code path instead of one per endpoint. Never exposing internal errors prevents information leakage that aids attackers.

## When To Use

- Designing any new REST API endpoint that can fail
- Unifying error responses across an existing API with inconsistent shapes
- Implementing global exception handlers in FastAPI, Django, or Express
- Adding field-level validation error details

## When NOT To Use

- Internal RPC calls where structured JSON adds overhead with no consumer benefit
- Streaming endpoints where a full JSON error body disrupts the stream protocol
- Simple CLI tools — plain stderr messages are sufficient

## Content

| File | What's inside |
|------|---------------|
| `content/01-problem-detail.xml` | RFC 7807 schema rules, required vs optional fields, traceId requirement |
| `content/02-implementation.xml` | FastAPI exception handlers for ValidationError and generic Exception; error code constants |

## Templates

| File | Purpose |
|------|---------|
| `templates/problem-detail.json` | RFC 7807 response envelope with all fields annotated |
| `templates/error-handler.py` | FastAPI global exception handler wiring ProblemDetail model |
