---
slug: graphql-api
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for building GraphQL APIs: schema-first SDL development with codegen, per-request DataLoader for every 1:N relation, depth limit (5-8) and query complexity cap before resolvers run, cursor-based (Relay) pagination for any list, and graphql-inspector diff in CI to block breaking schema changes.
content_id: "5f79024fb231c446"
tags: [graphql, api, dataloader, pagination, security]
---
# GraphQL API

## Summary

**One-sentence:** A methodology for building GraphQL APIs: schema-first SDL development with codegen, per-request DataLoader for every 1:N relation, depth limit (5-8) and query complexity cap before resolvers run, cursor-based (Relay) pagination for any list, and graphql-inspector diff in CI to block breaking schema changes.

**One-paragraph:** A methodology for building GraphQL APIs: schema-first SDL development with codegen, per-request DataLoader for every 1:N relation, depth limit (5-8) and query complexity cap before resolvers run, cursor-based (Relay) pagination for any list, and graphql-inspector diff in CI to block breaking schema changes. Mutations return the modified entity, never Boolean. Authorization checks live per-resolver, not just at the gateway.

## Applies If (ALL must hold)

- Mobile + web clients with divergent data shapes against the same backend
- Aggregating 3+ microservices into one client-facing API (federation/stitching)
- Internal tooling where consumers need fast schema iteration without REST versioning
- Real-time UIs needing subscriptions over WebSocket / SSE
- Backend-for-frontend (BFF) layers where type-safe client codegen is needed

## Skip If (ANY kills it)

- File-upload-heavy APIs — use multipart REST or presigned URLs instead
- Public APIs where CDN URL-level caching is critical — REST wins
- Simple CRUD with one consumer — REST ships faster
- Teams without query-cost / depth limiting infrastructure — DoS risk is real

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
