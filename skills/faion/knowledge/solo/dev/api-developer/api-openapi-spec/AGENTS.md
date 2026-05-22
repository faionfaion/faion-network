---
slug: api-openapi-spec
tier: solo
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Describe REST APIs as machine-readable YAML/JSON contracts (OpenAPI 3.
content_id: "4ba61c07b889d549"
tags: [openapi, contract-first, redocly, spectral, oasdiff]
---
# OpenAPI Specification

## Summary

**One-sentence:** Describe REST APIs as machine-readable YAML/JSON contracts (OpenAPI 3.

**One-paragraph:** Describe REST APIs as machine-readable YAML/JSON contracts (OpenAPI 3.1) that drive codegen, mocking, contract testing, and reference docs. Shard sources into `paths/`, `components/schemas/`, `components/responses/`, `components/parameters/` and bundle to a single `openapi.yaml` via `redocly bundle`. Every operation must have `operationId`, `summary`, `tags`, and examples; every reusable shape must live in `components/` as a `$ref`.

## Applies If (ALL must hold)

- HTTP / REST APIs that need a machine-readable contract for codegen, mocking, contract testing, and reference docs.
- Multi-language SDK distribution where TS / Python / Go / Java clients regenerate from a single source on each release.
- Public APIs where developer adoption depends on Swagger UI / Redoc / Mintlify-rendered reference docs.
- Internal API platforms standardizing on contract-first development with `oasdiff`-enforced compatibility.
- Agentic backend authoring — a strict OpenAPI spec is the most reliable scaffolding for LLMs to extend without hallucinating endpoints / fields.

## Skip If (ANY kills it)

- gRPC / Protobuf services — use `.proto` + `buf` instead; OpenAPI shoehorned around RPC fights tooling.
- AsyncAPI / event-driven systems — use AsyncAPI 2.x/3.x for Kafka, MQTT, WebSocket message envelopes.
- GraphQL — use the GraphQL SDL and tools like `graphql-codegen`; a partial OpenAPI overlay adds confusion.
- Highly volatile experimental endpoints — generating clients from each iteration is overhead; freeze the contract before publishing.

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
