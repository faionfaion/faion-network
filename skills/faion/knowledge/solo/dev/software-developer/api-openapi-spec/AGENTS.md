---
slug: api-openapi-spec
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-net]
summary: Produces a Spectral-clean OpenAPI 3.1 spec with strict schemas, examples per operation, x-versioning policy, and security scheme block linked to the auth methodology.
content_id: "4ca6123ccbfa9e54"
complexity: medium
produces: spec
est_tokens: 4200
tags: [api, openapi, spectral, spec, versioning]
---
# OpenAPI Spec Authoring

## Summary

**One-sentence:** Produces a Spectral-clean OpenAPI 3.1 spec with strict schemas, examples per operation, x-versioning policy, and security scheme block linked to the auth methodology.

**One-paragraph:** OpenAPI specs that lint clean still ship surprises. This methodology emits a Spectral-validated OpenAPI 3.1 spec with strict response schemas (additionalProperties=false), one example per request/response, an x-versioning policy declared in info, a security scheme block aligned with the AUTH-* artefact, and components.schemas reused (never inlined twice). Output: openapi.yaml + spectral.yaml + a validate-openapi.sh runner.

**Ефективно для:**

- Solo dev authoring the canonical spec for a new public API.
- Adding Spectral CI to an existing spec that nobody lints.
- Cleaning up an API where 30 endpoints inline the same User schema.
- Wiring x-versioning so downstream tools (codegen, docs) honor deprecations.

## Applies If (ALL must hold)

- Spec lives in OpenAPI 3.1 (or 3.0 in transition).
- Spectral CLI is available for linting.
- Author has authority to refactor schemas into components.

## Skip If (ANY kills it)

- GraphQL schema (use api-graphql).
- AsyncAPI / event-driven spec (out of scope).
- Legacy code-first API where spec is read-only output.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing spec | openapi.yaml | repo or empty stub |
| Auth artefact | AUTH-* spec_id | api-authentication |
| Spectral CLI | binary | @stoplight/spectral-cli |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-contract-first]] | Codegen + CI assumes a clean spec from this methodology. |
| [[api-versioning]] | x-versioning policy is declared here, enforced in versioning. |

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
| `api_openapi_spec_draft` | sonnet | Bounded synthesis. |
| `api_openapi_spec_validate` | haiku | Mechanical schema check. |
| `api_openapi_spec_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-user-api.yaml` | Reference user-api OpenAPI 3.1 spec with strict schemas + x-versioning |
| `templates/spectral.yaml` | Spectral ruleset enforcing the rules in 01-core-rules.xml |
| `templates/validate-openapi.sh` | Shell runner that lints spec with Spectral and counts duplicate schemas |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-openapi-spec artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-openapi-spec artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-openapi-spec.py` | Validate api-openapi-spec artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[api-contract-first]]
- [[api-documentation]]
- [[api-rest-design]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
