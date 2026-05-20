---
slug: api-openapi-spec
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Machine-readable HTTP API contract using OpenAPI 3.
content_id: "4ba61c07b889d549"
tags: [openapi, api-design, contract-first, codegen, api-spec]
---
# OpenAPI Specification

## Summary

**One-sentence:** Machine-readable HTTP API contract using OpenAPI 3.

**One-paragraph:** Machine-readable HTTP API contract using OpenAPI 3.1. Every path operation requires operationId, tags, request/response schemas via $ref, and realistic examples. The spec is authored before server code; generated code (stubs, SDKs) flows from the spec, never the reverse. Breaking changes are detected with oasdiff in CI and require human approval.

## Applies If (ALL must hold)

- Designing or evolving any HTTP/JSON API with more than one consumer.
- Documentation must stay in sync with implementation (regen docs on every spec PR).
- Generating typed SDK clients for frontend, mobile, or partners.
- Mocking endpoints for frontend while backend is in flight.
- Contract testing with Schemathesis or Dredd against staging.
- Replacing handwritten Postman collections with a single source of truth.

## Skip If (ANY kills it)

- GraphQL APIs — use SDL/GraphQL schema; OpenAPI for GraphQL is awkward.
- gRPC / protobuf services — .proto is the contract.
- Trivial internal endpoints with one consumer (same team).
- Server-rendered HTML apps (Django templates, Rails views).
- Streaming APIs (SSE, WebSockets with rich semantics) — AsyncAPI is the right spec.
- Tightly coupled libraries (Python imports), where a function signature is the contract.

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
