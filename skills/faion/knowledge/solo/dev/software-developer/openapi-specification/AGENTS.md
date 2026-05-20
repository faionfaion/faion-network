---
slug: openapi-specification
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: OpenAPI 3.
content_id: "a1be3e382ce034bf"
tags: [openapi, rest-api, api-design, specification, documentation]
---
# OpenAPI Specification

## Summary

**One-sentence:** OpenAPI 3.

**One-paragraph:** OpenAPI 3.1 as the single source of truth for HTTP/JSON APIs: one canonical openapi.yaml at repo root, all schemas and error responses under components/ referenced via $ref, mandatory operationId on every operation, and CI gates (Spectral lint + oasdiff breaking-change check) that block merges introducing undocumented or breaking changes.

## Applies If (ALL must hold)

- Designing a new HTTP/JSON API where clients, servers, mocks, tests, and docs must stay in sync.
- Generating typed clients (TS, Python, Go) instead of hand-writing N SDKs.
- Contract-first work between FE and BE where one side is agent-built.
- Documenting an existing API before refactor.
- Public API surface where SDK generation and developer docs are expected.

## Skip If (ANY kills it)

- Pure internal RPCs between trusted services — use Protobuf/gRPC/tRPC; OpenAPI adds ceremony for no gain.
- GraphQL APIs — schema is the contract; OpenAPI is irrelevant.
- Event-driven / pub-sub — use AsyncAPI instead.
- Tiny one-endpoint webhook receivers — overhead exceeds value.
- Server-driven UI payloads over a stream, not REST.

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
