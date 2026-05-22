---
slug: api-graphql
tier: solo
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GraphQL lets clients fetch nested, multi-resource data in a single request against a typed schema.
content_id: "703437193c68f507"
tags: [graphql, dataloader, schema-first, federation, relay-pagination]
---
# GraphQL Patterns

## Summary

**One-sentence:** GraphQL lets clients fetch nested, multi-resource data in a single request against a typed schema.

**One-paragraph:** GraphQL lets clients fetch nested, multi-resource data in a single request against a typed schema. The schema (SDL) is the contract; code is derived from it. Every relation field must use DataLoader to prevent N+1 queries. Public endpoints must enforce depth and complexity limits.

## Applies If (ALL must hold)

- Client needs to fetch nested data (user → orders → items) in a single round-trip with field selection.
- Multiple consumers (web, mobile, partner) want different shapes off the same backend without bespoke REST endpoints.
- You want a typed schema as the contract between BE and FE generators (codegen, Apollo, urql, Relay).
- Real-time fan-out via subscriptions belongs alongside the same query/mutation graph.
- Federating multiple services into one supergraph (Apollo Federation, Hot Chocolate, Mercurius).

## Skip If (ANY kills it)

- Simple CRUD on a single resource — REST is shorter, cacheable, and well-tooled.
- File upload heavy / streaming binary — multipart REST or gRPC stream is better.
- Public, cache-on-CDN read APIs — GET + URL semantics outperform POST /graphql.
- Hard p99 latency budgets where resolver fan-out is unpredictable.
- Tiny team without bandwidth to operate persisted queries, depth limits, complexity scoring.

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
