---
slug: api-gateway-graphql
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GraphQL federation via Apollo Router creates a unified supergraph from independently deployed domain subgraphs.
content_id: "aedf39a3d64074c7"
tags: [api-gateway, graphql, federation, apollo-router, subgraph]
---
# GraphQL Federation Gateway: Apollo Router, Subgraphs, and Query Security

## Summary

**One-sentence:** GraphQL federation via Apollo Router creates a unified supergraph from independently deployed domain subgraphs.

**One-paragraph:** GraphQL federation via Apollo Router creates a unified supergraph from independently deployed domain subgraphs. The router handles query planning, entity resolution across subgraphs, auth via JWT/JWKS, query depth and complexity limits, and persisted queries. Federation v2 uses @key, @shareable, @external, @requires directives. Never accept a supergraph without running rover supergraph compose to verify composition.

## Applies If (ALL must hold)

- Multiple teams maintaining independent GraphQL services that need a unified client API.
- Migrating from REST to GraphQL across multiple services without a big-bang rewrite.
- Building a composite data layer where entities (User, Product, Order) are owned by different services but cross-referenced in queries.
- Need GraphQL-specific query controls (depth limits, complexity limits, persisted queries) at a single gateway layer.
- Replacing schema stitching with the modern federation approach.

## Skip If (ANY kills it)

- Single-team GraphQL monolith — federation adds operational overhead (multiple services, rover tooling, supergraph composition CI) without benefit when one team owns the whole schema.
- REST-only backends where GraphQL is not used — use a REST gateway pattern instead.
- Simple BFF patterns where one gateway aggregates a few REST endpoints — REST aggregation in the gateway is simpler than standing up a federation stack.
- Teams without GraphQL expertise — federation v2 directives and composition rules have a significant learning curve; invest in training before adopting.

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

- parent skill: `solo/dev/software-architect/`
