---
slug: graphql-api
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Build a GraphQL API with schema-first SDL, codegen, per-request DataLoader, depth + complexity limits, cursor pagination, and breaking-change CI gates.
content_id: "005abf9ce7795f81"
complexity: medium
produces: code
est_tokens: 4200
tags: [graphql, api, dataloader, pagination, security]
---
# GraphQL API

## Summary

**One-sentence:** Build a GraphQL API with schema-first SDL, codegen, per-request DataLoader, depth + complexity limits, cursor pagination, and breaking-change CI gates.

**One-paragraph:** Schema-first SDL development with codegen; every 1:N relation served by a per-request DataLoader to prevent N+1; depth limit (5-8) and query complexity cap enforced before resolvers run; cursor-based (Relay) pagination for any list; graphql-inspector or graphql-cli check diff in CI to block breaking schema changes. Mutations return typed `MutationNamePayload` types with explicit userErrors arrays. Output is schema.graphql + resolvers + dataloader wiring + CI gates.

**Ефективно для:**

- BFF-style GraphQL APIs serving multiple clients.
- Federated graphs where schema discipline is essential.
- Replacing REST endpoints whose payload composition is client-specific.
- AI-agent-generated services where the schema is the deterministic contract.

## Applies If (ALL must hold)

- GraphQL is the deliberate protocol (not retrofitted onto REST).
- Multiple consumers benefit from per-client payload shaping.
- Relations are graph-like (1:N, N:M) where DataLoader earns its place.
- Engineering owns schema discipline (codegen, depth/complexity, diff gates).

## Skip If (ANY kills it)

- Single consumer + simple resource shape — REST is simpler.
- Internal RPC where types matter more than payload shaping — use gRPC.
- Embedded systems or constrained environments where GraphQL overhead is prohibitive.
- Project relies on stack that doesn't support per-request DataLoader semantics.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Schema decisions: types, relations, paginated lists | SDL draft | tech-lead |
| Codegen target language + library (gqlgen, Apollo Server, Pothos) | config | platform |
| Depth + complexity caps decided + measured against worst-case queries | config | tech-lead |
| Schema diff tool wired (graphql-inspector or graphql-cli check) | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-versioning]] | Breaking-change policy aligns with schema diff gate. |
| [[logging-patterns]] | Resolver instrumentation logs operation_name + duration. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (schema-first, codegen, dataloader for 1:N, depth+complexity caps, cursor pagination, diff gate in CI) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for GraphQL API spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: SDL → codegen → resolvers → dataloaders → depth/complexity → diff gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schema_design` | opus | Type design + relations + pagination shape need deep synthesis. |
| `dataloader_wiring` | sonnet | Per-relation: declare, batch, register. |
| `depth_complexity_caps` | sonnet | Configure plugin; measure worst-case queries. |
| `diff_gate_setup` | sonnet | graphql-inspector CI job + baseline schema commit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/codegen.yml` | graphql-codegen config for TS/server + client types |
| `templates/dataloader-pattern.ts` | DataLoader factory pattern per request |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graphql-api.py` | Validate GraphQL API spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[graphql-api-design]]
- [[api-versioning]]
- [[logging-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps protocol choice, consumer shape, and DataLoader readiness to a rule from `01-core-rules.xml`, telling the agent whether to apply GraphQL conventions or skip for REST/gRPC. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
