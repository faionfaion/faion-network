---
slug: rest-api-design
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Resource-oriented HTTP API design conventions: plural noun paths, correct HTTP method semantics, standard status codes, and consistent filter/pagination parameters.
content_id: "f884a7a52d12de33"
tags: [rest, api, http, openapi, spectral]
---
# REST API Design

## Summary

**One-sentence:** Resource-oriented HTTP API design conventions: plural noun paths, correct HTTP method semantics, standard status codes, and consistent filter/pagination parameters.

**One-paragraph:** Resource-oriented HTTP API design conventions: plural noun paths, correct HTTP method semantics, standard status codes, and consistent filter/pagination parameters. Core rule: paths use plural nouns in kebab-case with no verbs (/users, not /getUsers); POST returns 201 + Location header; DELETE returns 204; errors use RFC 7807 application/problem+json.

## Applies If (ALL must hold)

- Designing a new HTTP API for a web/mobile client or third-party consumer
- Refactoring RPC-shaped endpoints (/getUsers, /doThing) into resource-oriented routes
- Reviewing PR diffs for status-code, method-semantic, or naming drift
- Generating client SDKs or OpenAPI specs that depend on consistent route shapes
- Onboarding LLM agents that will call the API — predictable verbs/nouns reduce tool-use errors

## Skip If (ANY kills it)

- Internal RPC between trusted services with strict latency budgets — gRPC fits better
- Highly relational graph queries with many shapes per page — GraphQL avoids round-trips
- Server-streamed events (logs, ticks, model output) — SSE/WebSockets/HTTP streaming
- Pure file transfer pipelines — S3-style presigned URLs beat REST envelopes
- One-off webhook receivers where shape is dictated by the sender

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
