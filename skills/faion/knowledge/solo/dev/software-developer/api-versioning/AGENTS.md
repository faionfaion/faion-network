---
slug: api-versioning
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-net]
summary: Picks a versioning scheme (url-path / accept-header / header-key), classifies a proposed change as breaking or additive, and emits a version-bump plan with deprecation window + sunset header.
content_id: "59471a20c5eef7b2"
complexity: medium
produces: decision-record
est_tokens: 4200
tags: [api, versioning, semver, deprecation, sunset]
---
# API Versioning

## Summary

**One-sentence:** Picks a versioning scheme (url-path / accept-header / header-key), classifies a proposed change as breaking or additive, and emits a version-bump plan with deprecation window + sunset header.

**One-paragraph:** API versioning fails most when the team cannot tell whether a change is breaking. This methodology picks one scheme (url-path / accept-header / header-key), runs a breaking-change classifier against the diff (new required field = breaking; new optional field = additive; rename = breaking; etc.), emits the version-bump plan (major if breaking, minor if additive, patch if doc-only), and adds a Sunset header with concrete dates for any deprecation.

**Ефективно для:**

- Solo dev shipping v2 of the public API and unsure which changes are breaking.
- Adding a Sunset header so partners know when to migrate.
- Choosing between /v1/orders vs Accept: application/vnd.example.v1+json — and sticking with the choice.
- Wiring a Spectral rule that fails breaking changes without a major bump.

## Applies If (ALL must hold)

- API has external consumers.
- OpenAPI spec is available (api-openapi-spec).
- Author can ship a version bump + maintain &gt;= 1 prior version during deprecation window.

## Skip If (ANY kills it)

- Pre-public-launch API where breaking changes are free.
- Internal-only API with same-team consumer (synchronised deploys).
- Version pinning per-feature (separate methodology).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OpenAPI spec (proposed + base) | openapi.yaml + diff | api-openapi-spec |
| Existing versioning policy | info.x-versioning block | current spec |
| Deprecation window | days | platform / partner contract |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-openapi-spec]] | Spec carries the x-versioning policy. |
| [[api-contract-first]] | CI diff gate detects breaking changes. |

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
| `api_versioning_draft` | sonnet | Bounded synthesis. |
| `api_versioning_validate` | haiku | Mechanical schema check. |
| `api_versioning_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/versioning.py` | Stdlib breaking-change classifier on a spec diff |
| `templates/spectral-rules.yaml` | Spectral ruleset enforcing one-scheme + breaking-change requires major bump |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-versioning artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-versioning artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-versioning.py` | Validate api-versioning artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[api-rest-design]]
- [[api-contract-first]]
- [[api-documentation]]
- [[api-openapi-spec]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
