---
slug: api-graphql
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-net]
summary: Designs a GraphQL schema with persisted queries, DataLoader N+1 protection, depth+complexity limits, and an error-extension envelope mirroring RFC 7807.
content_id: "9bae98bcbe71424a"
complexity: medium
produces: spec
est_tokens: 4200
tags: [api, graphql, dataloader, persisted-queries, complexity]
---
# GraphQL API Design

## Summary

**One-sentence:** Designs a GraphQL schema with persisted queries, DataLoader N+1 protection, depth+complexity limits, and an error-extension envelope mirroring RFC 7807.

**One-paragraph:** GraphQL gives clients a flexible query surface but trades that flexibility for new failure modes — N+1, runaway query depth, expensive resolvers. This methodology emits a schema-pack: SDL with persisted-query allowlist, DataLoader factory per N+1-prone relation, depth + complexity caps in the gateway, and an error-extension envelope mirroring RFC 7807 so clients see one error shape across REST + GraphQL. Output: schema.graphql + DataLoader factories + depth/complexity config.

**Ефективно для:**

- Solo dev adding GraphQL alongside REST for a more flexible mobile client.
- Existing GraphQL API where p95 latency exploded due to N+1 on a popular query.
- Closing GraphQL by switching to persisted queries (kills introspection surface in prod).
- Adding query-depth + complexity limits before launching to public.

## Applies If (ALL must hold)

- Schema has &gt;= 5 types with at least one N+1-prone relation (1:N navigation).
- Gateway can enforce depth + complexity (Apollo Router / Hasura / GraphQL Yoga).
- Client surface is &lt;= 5 known clients (so persisted queries are feasible).
- Author can ship a single deprecate-then-remove window.

## Skip If (ANY kills it)

- Pure REST API (use api-rest-design).
- Public open-introspection API where clients are unknown (persisted queries impossible).
- Sub-100-RPS internal GraphQL where N+1 cost is negligible.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain model | type sketches | PRD / architect |
| Existing N+1 hotspots | trace samples | APM |
| Gateway choice | Apollo Router / Yoga / Hasura | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-error-handling]] | Error-extension envelope mirrors RFC 7807. |
| [[api-rate-limiting]] | Persisted-query allowlist drives the rate-limit key. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `api_graphql_draft` | sonnet | Bounded synthesis. |
| `api_graphql_validate` | haiku | Mechanical schema check. |
| `api_graphql_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.graphql` | GraphQL SDL skeleton with persisted-query pragma + nullable defaults |
| `templates/dataloader-factory.ts` | TypeScript DataLoader factory for 1-to-N relations |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-graphql artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-graphql artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-graphql.py` | Validate api-graphql artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[graphql-api-design]]
- [[api-rest-design]]
- [[api-documentation]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
