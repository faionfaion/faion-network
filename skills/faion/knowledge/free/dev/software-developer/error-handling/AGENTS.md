# Error Handling (RFC 7807)

## Summary

A methodology for standardizing API error responses following RFC 7807 Problem Details: every error returns `type` (URI), `title`, `status`, `detail`, `instance`, `traceId`, and an optional `errors[]` array for field-level validation failures. All endpoints share one shape, one content-type (`application/problem+json`), and one error-handler entry point.

## Why

Inconsistent error shapes force every API client to handle each endpoint's unique format. RFC 7807 provides a machine-readable envelope that clients can parse generically, observability tools can index by `traceId`, and on-call engineers can trace across services. A single framework-level handler also prevents raw exception messages and stack traces from leaking to clients in production.

## When To Use

- New REST API where consistent client-side error handling matters.
- Refactoring mixed error shapes (`{error:"..."}`, `{detail:"..."}`, HTML) into one envelope.
- Public-facing APIs where error shape is part of the published contract.
- Multi-service architectures where clients must not memorize per-service formats.
- API gateway / BFF setups translating downstream errors.

## When NOT To Use

- gRPC — use `google.rpc.Status` + `google.rpc.error_details` instead.
- GraphQL — errors live in the response `errors[]` array per spec.
- Internal-only low-stability APIs where the envelope overhead outweighs benefit.
- Streaming endpoints (SSE, WebSocket) — error frames follow their own conventions.
- Static asset / file download endpoints — return raw HTTP status, no body.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | RFC 7807 field rules, content-type requirement, traceId propagation, 5xx masking |
| `content/02-examples.xml` | FastAPI handler, DRF handler, JSON schema, contract test helper |
| `content/03-antipatterns.xml` | Antipatterns: leaking PII/stack in detail, wrong content-type, status mismatch, missing traceId |

## Templates

| File | Purpose |
|------|---------|
| `templates/problem-details.schema.yaml` | JSON Schema 2020-12 for validating Problem Details responses in CI |
