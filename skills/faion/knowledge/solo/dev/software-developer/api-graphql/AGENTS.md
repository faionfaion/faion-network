---
slug: api-graphql
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GraphQL allows clients to specify exactly what data they need, reducing over-fetching and under-fetching versus REST.
content_id: "703437193c68f507"
tags: [graphql, dataloader, api, n-plus-one, schema-design]
---
# GraphQL API Patterns

## Summary

**One-sentence:** GraphQL allows clients to specify exactly what data they need, reducing over-fetching and under-fetching versus REST.

**One-paragraph:** GraphQL allows clients to specify exactly what data they need, reducing over-fetching and under-fetching versus REST. Core rule: every resolver returning a list of related entities must use a DataLoader instantiated per-request — without it, a list of 100 parents generates 101 database queries (N+1).

## Applies If (ALL must hold)

- Frontends composing data from many backend resources per screen (one round-trip)
- Multiple consumer types (web, iOS, Android, partner API) with different field requirements
- Federated services where independent teams own subgraphs stitched at a gateway
- Real-time features (subscriptions over WebSocket/SSE) for live dashboards, chat, presence
- BFF layer composing REST microservices into one typed graph

## Skip If (ANY kills it)

- File uploads or streaming binary — multipart REST or signed URLs are simpler
- Public cache-heavy read APIs — REST + HTTP cache headers + CDN is faster and simpler
- Single-app, single-consumer CRUD — schema overhead and N+1 traps are not worth it
- Hard real-time latency budgets — every query parses and plans, adding overhead vs REST

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
