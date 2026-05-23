---
slug: api-contract-first
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-net]
summary: Generates an OpenAPI spec + CI contract-test wiring so both server and clients are generated from the same source — never the other way round.
content_id: "3b66652d93b80901"
complexity: medium
produces: spec
est_tokens: 4200
tags: [api, contract-first, openapi, codegen, ci]
---
# API Contract-First Development

## Summary

**One-sentence:** Generates an OpenAPI spec + CI contract-test wiring so both server and clients are generated from the same source — never the other way round.

**One-paragraph:** Code-first APIs drift between server and client; contract-first locks both to one source. This methodology emits an OpenAPI 3.1 spec (or AsyncAPI for events), the CI job that breaks on schema-drift, and the codegen wiring for server stubs + client SDKs. Output: contract-pack with `openapi.yaml`, `contract-ci.yaml`, and a checklist that every PR touching the API also updates the spec.

**Ефективно для:**

- Solo dev shipping a new public API where mobile + web + partners all need a client.
- Migrating a code-first Flask/Express API to contract-first to stop schema drift.
- Adding a CI gate that prevents PRs from landing without an updated spec.
- Generating SDKs in 3 languages instead of hand-writing each.

## Applies If (ALL must hold)

- API has &gt;= 1 consumer that is not the same team as the producer.
- OpenAPI 3.1 tooling is available (or AsyncAPI for event-based).
- Repo CI can run a contract-diff step (openapi-diff / oasdiff).
- Author has authority to enforce the gate on the PR.

## Skip If (ANY kills it)

- Single-team, single-consumer prototype where drift cost is zero.
- GraphQL API (schema serves the contract — use api-graphql).
- Legacy SOAP — out of scope.
- Internal-only RPC where protobuf already enforces contract.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| API surface inventory | list of endpoints | code or PM |
| OpenAPI baseline | openapi.yaml or empty stub | templates/openapi-base.yaml |
| CI runner | GitHub Actions / GitLab CI | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-openapi-spec]] | Spec authoring conventions. |
| [[api-versioning]] | Breaking-change rules for the spec. |

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
| `api_contract_first_draft` | sonnet | Bounded synthesis. |
| `api_contract_first_validate` | haiku | Mechanical schema check. |
| `api_contract_first_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/contract-ci.yaml` | GitHub Actions workflow that runs oasdiff against base branch |
| `templates/openapi-base.yaml` | OpenAPI 3.1 skeleton with version-policy stub + additionalProperties=false defaults |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-contract-first artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-contract-first artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-contract-first.py` | Validate api-contract-first artefact against schema | Pre-commit; CI on each artefact change |

## Related



## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
