# API Documentation

## Summary

**One-sentence:** Generates a six-section API reference (Overview, Auth, Quick Start, Endpoints, Error Codes, Changelog) with copy-paste curl examples and machine-readable OpenAPI alongside the prose.

**One-paragraph:** Developers evaluate APIs in under 5 minutes; missing any of six canonical sections causes abandonment. This methodology emits an API reference scaffold with the six required sections, copy-paste curl examples per endpoint, an error-codes table linked to the Problem Details schema (RFC 7807), and a Changelog tied to spec version bumps. Output: docs-bundle ready for static-site rendering + OpenAPI cross-link.

**Ефективно для:**

- Solo dev publishing the first public API docs on docs.example.com.
- Re-doing legacy docs that lost half their consumers due to missing Quick Start.
- Wiring the docs site to OpenAPI so examples stay in sync with the contract.
- Adding a Changelog so partners can plan around deprecations.

## Applies If (ALL must hold)

- API has external consumers (B2B / public).
- OpenAPI spec exists (api-contract-first or api-openapi-spec).
- Docs site is rendered (Docusaurus / Mintlify / Redoc / homegrown).
- Author has access to ship the docs site.

## Skip If (ANY kills it)

- Internal-only RPC documented in code comments.
- Single-team API where Slack channel is the docs.
- Generated SDK README only (no per-endpoint usage docs).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OpenAPI spec | openapi.yaml | api-contract-first output |
| Auth scheme | AUTH-* artefact | api-authentication output |
| Error catalogue | Problem Details JSON | api-error-handling output |
| Docs site stack | Docusaurus / Mintlify / Redoc | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-contract-first]] | Source of the spec the docs cross-link. |
| [[api-error-handling]] | Source of the error-codes table. |

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
| `api_documentation_draft` | sonnet | Bounded synthesis. |
| `api_documentation_validate` | haiku | Mechanical schema check. |
| `api_documentation_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/doc-structure.md` | Markdown skeleton enforcing the six-section structure |
| `templates/openapi-examples.yaml` | OpenAPI examples block patterns used by the docs site |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-documentation artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-documentation artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-documentation.py` | Validate api-documentation artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[api-openapi-spec]]
- [[api-rest-design]]
- [[api-contract-first]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
