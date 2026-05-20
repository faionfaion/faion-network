---
slug: api-rest-design
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design REST APIs by mapping resources (plural nouns, lowercase, hyphenated) to HTTP methods (GET/POST/PUT/PATCH/DELETE), returning correct status codes for each outcome, using query parameters for filtering and sorting, and nesting sub-resources for ownership relationships.
content_id: "05a4786b800a229d"
tags: [api, rest, http, design]
---
# REST API Design

## Summary

**One-sentence:** Design REST APIs by mapping resources (plural nouns, lowercase, hyphenated) to HTTP methods (GET/POST/PUT/PATCH/DELETE), returning correct status codes for each outcome, using query parameters for filtering and sorting, and nesting sub-resources for ownership relationships.

**One-paragraph:** Design REST APIs by mapping resources (plural nouns, lowercase, hyphenated) to HTTP methods (GET/POST/PUT/PATCH/DELETE), returning correct status codes for each outcome, using query parameters for filtering and sorting, and nesting sub-resources for ownership relationships.

## Applies If (ALL must hold)

- Designing any new HTTP API surface from scratch (greenfield service, internal microservice, public SaaS).
- Adding endpoints to an existing API where naming, status codes, and pagination must stay consistent across teams.
- Auditing an inconsistent API to refactor toward Richardson Level 2/3 maturity before publishing SDKs.
- Generating server stubs and SDKs from a spec (pairs with api-contract-first and api-openapi-spec).
- LLM agents drafting endpoint sets from a domain model — gives a fixed grammar so output is deterministic and reviewable.

## Skip If (ANY kills it)

- Real-time bidirectional communication — use WebSockets or SSE instead.
- Bulk or batch operations with complex transactions — consider GraphQL or RPC.
- Internal service-to-service calls where gRPC is already the standard.
- Asynchronous, event-driven flows where Webhook + Pub/Sub is a better fit (use AsyncAPI, not REST).
- Streaming, large bidirectional payloads, ultra-low latency — gRPC, WebSocket, or SSE are better.
- Complex graph traversal queries with N+1 fan-out — GraphQL beats REST for client-driven shape selection.

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
