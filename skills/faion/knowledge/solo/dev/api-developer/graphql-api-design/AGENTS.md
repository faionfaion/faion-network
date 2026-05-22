---
slug: graphql-api-design
tier: solo
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design GraphQL APIs schema-first: the SDL is the contract that humans review before code is written.
content_id: "816f194f0d103dae"
tags: [graphql, schema-first, dataloader, relay-pagination, federation]
---
# GraphQL API Design

## Summary

**One-sentence:** Design GraphQL APIs schema-first: the SDL is the contract that humans review before code is written.

**One-paragraph:** Design GraphQL APIs schema-first: the SDL is the contract that humans review before code is written. Every list field uses Relay-style cursor pagination; every relation field has a DataLoader scoped per-request in context; every mutation returns a typed payload with union error types; every public endpoint has depth (8–10) and complexity (100–500) limits.

## Applies If (ALL must hold)

- New service designed schema-first, where SDL is the contract reviewed by humans + consumed by codegen.
- Multiple distinct clients (web, mobile, partner) each need a different shape of the same domain.
- You expect federation/microservices later — start with the supergraph mindset.
- Heavy use of nested reads with field-level auth (e.g. SaaS dashboard with org/role permissions).
- Real-time + query unification: subscriptions next to queries on the same schema.

## Skip If (ANY kills it)

- Public, cacheable read API → REST + CDN wins.
- Hard latency budgets where unbounded resolver fan-out is unacceptable.
- File upload / streaming-binary heavy workloads.
- Single-client, single-team CRUD — overhead of schema, codegen, DataLoaders, depth/complexity is not paid back.
- Org without bandwidth to operate persisted queries, schema registry, breaking-change checks.

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
