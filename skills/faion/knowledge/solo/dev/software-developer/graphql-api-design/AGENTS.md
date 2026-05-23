---
slug: graphql-api-design
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Design GraphQL schemas (SDL first) where every mutation returns a typed MutationNamePayload with userErrors and authorization lives in directives.
content_id: "816f194f0d103dae"
complexity: medium
produces: spec
est_tokens: 4200
tags: [graphql, schema-design, api-design, dataloader, authorization]
---
# GraphQL API Design

## Summary

**One-sentence:** Design GraphQL schemas (SDL first) where every mutation returns a typed MutationNamePayload with userErrors and authorization lives in directives.

**One-paragraph:** Schema-first GraphQL design where the SDL is the source of truth, codegen drives client and server types, and every mutation returns a typed `MutationNamePayload { data, userErrors }`. Authorization is declared as schema directives (e.g. @auth(scope: ADMIN)); resolvers do not embed authorization checks ad-hoc. Naming conventions are nailed down (Connection/Edge for paginated lists, Input for mutation arguments, Result-shape unions for errors). Output is the schema spec + auth model + naming guide.

**Ефективно для:**

- Authoring or refactoring GraphQL schemas where shape consistency matters.
- Aligning multiple teams on naming and mutation patterns.
- Designing authorization that survives schema growth.
- Documenting decisions before implementation lands.

## Applies If (ALL must hold)

- GraphQL is the chosen protocol (see graphql-api).
- Schema spans multiple aggregates (>=5 types with relations).
- Mutations are non-trivial (validation, partial-success cases).
- Authorization beyond 'logged in' is needed (per-resource scopes).

## Skip If (ANY kills it)

- Schema is a thin facade over one resource — design overhead exceeds value.
- Authorization is one global flag (logged in / not) — directives are over-engineering.
- Protocol is REST or gRPC — this methodology does not apply.
- Schema is consumer-defined (federation subgraph generated from clients).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain model: aggregates + relations + lifecycle states | doc or ERD | tech-lead |
| Mutation list: create/update/delete per aggregate + custom verbs | table | tech-lead |
| Authorization model: scopes, roles, ownership rules | policy | security |
| Naming policy: Connection/Edge, Input, Payload, error union shape | ADR | tech-lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[graphql-api]] | Implementation conventions for resolvers + DataLoader. |
| [[api-versioning]] | Schema diff gates align with this design. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (mutation payload type, userErrors array, auth via directives, naming conventions, no scalar primitives for IDs) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for GraphQL design spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: aggregates → types → mutations → auth model → naming check | 800 |
| `content/05-examples.xml` | essential | Worked example: Payment mutation with userErrors + @auth | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `type_modeling` | opus | Aggregate-to-type mapping needs deep synthesis. |
| `mutation_payload_design` | sonnet | Mechanical payload type emission with userErrors. |
| `auth_directive_set` | opus | Authorization model encoded as directives. |
| `naming_audit` | sonnet | Walk types, enforce naming convention. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.graphql` | Reference SDL with Payload + userErrors + @auth directives |
| `templates/dataloader.py` | DataLoader factory for Python servers (Ariadne/Strawberry) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graphql-api-design.py` | Validate GraphQL design spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[graphql-api]]
- [[api-versioning]]
- [[rest-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps schema complexity, authorization needs, and mutation shape to a rule from `01-core-rules.xml`, telling the agent whether to apply the design rules or skip when the schema is too small for the conventions. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
