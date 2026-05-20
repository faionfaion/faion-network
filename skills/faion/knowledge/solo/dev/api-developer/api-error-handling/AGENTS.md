---
slug: api-error-handling
tier: solo
group: dev
domain: api-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Inconsistent error shapes force clients to write per-endpoint error parsing.
content_id: "69ecdae3ba96f738"
tags: [api, error-handling, rfc-7807, rest, problem-details]
---
# API Error Handling

## Summary

**One-sentence:** Inconsistent error shapes force clients to write per-endpoint error parsing.

**One-paragraph:** Inconsistent error shapes force clients to write per-endpoint error parsing. RFC 7807 is an IETF standard that gives clients a predictable envelope to inspect without reading docs. The traceId field correlates client-reported errors to server logs, cutting debugging time dramatically. Never exposing raw exception messages prevents information leakage.

## Applies If (ALL must hold)

- Designing a new REST or HTTP API from scratch
- Standardising error responses across an existing API with inconsistent formats
- Adding structured field-level validation errors for form-backing endpoints
- When debugging requires correlating client errors to server-side log traces

## Skip If (ANY kills it)

- GraphQL APIs — use the errors array in the GraphQL envelope instead
- Internal service-to-service APIs where both sides are controlled and a simpler format is agreed — RFC 7807 overhead is not always justified
- WebSocket or streaming APIs where error framing is protocol-specific

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

- parent skill: `solo/dev/api-developer/`
