# GraphQL API Design

## Summary

Design GraphQL APIs schema-first: the SDL is the contract that humans review before code is written. Every list field uses Relay-style cursor pagination; every relation field has a DataLoader scoped per-request in context; every mutation returns a typed payload with union error types; every public endpoint has depth (8–10) and complexity (100–500) limits.

## Why

Schema-first aligns frontend/backend teams on a stable contract before implementation begins. DataLoader is not optional: N+1 queries are the default failure mode for any nested list resolver, and they pass unit tests while destroying prod performance. Relay pagination survives concurrent writes; offset pagination produces duplicates and gaps.

## When To Use

- New service designed schema-first with SDL as the human-reviewed contract
- Multiple distinct clients (web, mobile, partner) each needing different shapes
- Federation/microservices planned for later — start with supergraph mindset
- Heavy use of nested reads with field-level auth (SaaS dashboard with org/role permissions)
- Real-time + query unification: subscriptions next to queries on the same schema

## When NOT To Use

- Public cacheable read API — REST + CDN wins
- Hard latency budgets where unbounded resolver fan-out is unacceptable
- File upload / streaming-binary heavy workloads
- Single-client, single-team CRUD — DataLoader + codegen overhead is not paid back
- Org without bandwidth to operate persisted queries, schema registry, breaking-change checks

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema-design.xml` | Type system, interfaces, enums, input types, payload + error union pattern |
| `content/02-resolvers-security.xml` | DataLoader, permission classes, depth/complexity limits, error handling |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.graphql` | SDL skeleton: Node/Timestamped interfaces, Connection/Edge/PageInfo, Payload with error union |
| `templates/dataloader.py` | Strawberry DataLoader: batch_load_fn with key-order preservation |

## Scripts

none
