---
slug: graphql-api-design
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Schema-first GraphQL design where the SDL is the source of truth, codegen drives client and server types, and every mutation returns a typed MutationNamePayload with a userErrors array.
content_id: "816f194f0d103dae"
tags: [graphql, schema-design, api-design, dataloader, authorization]
---
# GraphQL API Design

## Summary

**One-sentence:** Schema-first GraphQL design where the SDL is the source of truth, codegen drives client and server types, and every mutation returns a typed MutationNamePayload with a userErrors array.

**One-paragraph:** Schema-first GraphQL design where the SDL is the source of truth, codegen drives client and server types, and every mutation returns a typed MutationNamePayload with a userErrors array. Core rule: every list-returning resolver must use a DataLoader instantiated per-request; every field with sensitive data must have explicit field-level authorization.

## Applies If (ALL must hold)

- Multiple clients (web + iOS + Android + partner) with divergent field needs over the same domain
- Highly relational data where REST would force N+1 round-trips or sprawling ?expand= params
- Schema-first development where the contract is the source of truth and codegen drives types
- Subscriptions for live dashboards, chat, or collaborative editing
- Federated services (Apollo Federation, GraphQL Hive) with one supergraph over many teams

## Skip If (ANY kills it)

- Public cache-heavy CDN-fronted APIs — REST + HTTP cache headers wins
- File upload or streaming binary payloads — multipart REST or signed URLs are simpler
- Tiny CRUD app with a single client — schema overhead and N+1 traps are not worth it
- Latency-sensitive RPC inside a cluster — gRPC is faster and stricter
- When your team has zero GraphQL experience and the deadline is tight; learning curve hits hard at the resolver-and-dataloader stage

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
