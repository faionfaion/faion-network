---
slug: error-handling
tier: pro
group: backend-systems
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a per-service error-envelope spec: RFC 7807 / 9457 Problem Details (`type`, `title`, `status`, `detail`, `instance`, `traceId`), single exception mapper, and validation error array."
content_id: "d0f4f042894eb8b8"
complexity: medium
produces: spec
est_tokens: 4300
tags: [error-handling, rfc-7807, api, http, problem-details]
---

# Error Handling (RFC 7807 Problem Details)

## Summary

**One-sentence:** Produces a per-service error-envelope spec: RFC 7807 / 9457 Problem Details (`type`, `title`, `status`, `detail`, `instance`, `traceId`), single exception mapper, and validation error array.

**Ефективно для:**

- REST / GraphQL APIs with multiple consumer types.
- Multi-service backends sharing a tracing system.
- Public APIs needing self-documenting errors (`type` URI).
- Validation-heavy endpoints with field-level errors.

**One-paragraph:** Standardized HTTP API error envelope following RFC 7807 / RFC 9457: every 4xx and 5xx response carries `type` (URI), `title`, `status`, `detail`, `instance`, and `traceId` fields, with an optional `errors[]` array for field-level validation failures. A single exception handler per framework maps all error types to this shape so client code parses one envelope rather than five.

## Applies If (ALL must hold)

- Service exposes HTTP / JSON responses (REST, OpenAPI, GraphQL HTTP).
- Observability stack carries a `trace_id` per request.
- Framework has a global exception handler hook.
- Consumers can rely on a stable error envelope.

## Skip If (ANY kills it)

- Wire protocol is not HTTP / JSON (gRPC, MQTT, raw TCP).
- Internal-only RPC with bespoke error envelope contracted.
- Public spec already locked to non-7807 shape (don't break clients).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Framework with global exception handler | code | team |
| Tracing system + `trace_id` propagation | infra doc | SRE |
| Error type catalogue (URIs) | doc site | team |
| Localisation strategy (single locale vs multi) | product decision | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[api-developer]]` | endpoint contracts |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-envelope` | haiku | RFC 7807 fields from spec. |
| `write-mapper` | sonnet | Framework-specific global handler. |
| `audit-error-leaks` | sonnet | Detects stack-trace leaks + multi-shape drift. |

## Templates

| File | Purpose |
|------|---------|
| `templates/error-handling.json` | JSON Schema for the Error Handling (RFC 7807 Problem Details) output contract |
| `templates/error-handling.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a error-handling record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-error-handling.py` | Enforce the Error Handling (RFC 7807 Problem Details) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[go-error-handling]]
- [[go-error-handling-patterns]]
- [[database-design]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
