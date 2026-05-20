---
slug: api-rest-design
tier: solo
group: dev
domain: api-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Resource-oriented HTTP API design: noun-based URL structure, correct HTTP verb semantics and idempotency guarantees, canonical status code mapping, and optional HATEOAS links.
content_id: "05a4786b800a229d"
tags: [api-design, rest, http, openapi, conventions]
---
# REST API Design

## Summary

**One-sentence:** Resource-oriented HTTP API design: noun-based URL structure, correct HTTP verb semantics and idempotency guarantees, canonical status code mapping, and optional HATEOAS links.

**One-paragraph:** Resource-oriented HTTP API design: noun-based URL structure, correct HTTP verb semantics and idempotency guarantees, canonical status code mapping, and optional HATEOAS links. URLs use plural nouns, lowercase kebab-case, and query params for filtering/sorting — never verbs.

## Applies If (ALL must hold)

- New public or partner-facing HTTP APIs where stable resource semantics, browser caching, and HTTP-toolchain familiarity (curl, Postman, OpenAPI) outweigh raw RPC throughput.
- CRUD-shaped domains (users, orders, posts, tickets) that map cleanly to nouns + standard verbs and benefit from HTTP cache headers, conditional requests, and CDN edge caching.
- Public docs and SDK generation flows that consume an OpenAPI spec; REST + OpenAPI is the most common pairing for codegen tools.
- Multi-team platforms where consistency (one URL grammar, one pagination convention, one error envelope) matters more than raw flexibility.
- LLM-driven backend authoring — agents pattern-match RESTful conventions reliably, especially when paired with a contract-first OpenAPI spec.

## Skip If (ANY kills it)

- Real-time bidirectional flows (chat, presence, live cursors) — use WebSockets / SSE / WebTransport.
- Highly graph-shaped read patterns where clients fan-out to 10+ endpoints per screen — GraphQL or BFF reduces round-trips.
- Internal hot paths needing strict typing and 10x throughput — gRPC + Protobuf is faster.
- Streaming uploads/downloads with resumability — REST works but WebDAV / TUS / S3 multipart is purpose-built.
- Cases where every endpoint is "verb-shaped" (jobs, calculations, transformations) — RPC is more honest than `POST /actions/calculate`.

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
