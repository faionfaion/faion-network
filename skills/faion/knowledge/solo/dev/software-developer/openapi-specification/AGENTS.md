---
slug: openapi-specification
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Authoring + CI gates for an OpenAPI 3.1 spec: one canonical bundle, $ref reuse, operationId everywhere, breaking-change gate via oasdiff, generator-spec drift detection.
content_id: "a7e898f963a6bebd"
complexity: medium
produces: spec
est_tokens: 5400
tags: [openapi, api-spec, contract-first, spectral, redocly]
---
# OpenAPI Specification

## Summary

**One-sentence:** Authoring + CI gates for an OpenAPI 3.1 spec: one canonical bundle, $ref reuse, operationId everywhere, breaking-change gate via oasdiff, generator-spec drift detection.

**One-paragraph:** OpenAPI documents rot the moment they diverge from server code, generators silently emit unsafe clients when required arrays are missing, and operationIds drift on path renames. This methodology fixes a contract-first authoring loop: one canonical openapi.yaml at repo root + redocly bundle for distribution; every operation carries operationId in kebab/camel; every reusable schema lives under components/* and is referenced via $ref; every response code carries named examples; Spectral + redocly lint on every PR; oasdiff blocks breaking changes; server-generated specs commit a snapshot and CI fails on drift.

**Ефективно для:**

- Перший API контракт - треба зафіксувати форму до імплементації.
- Server-generated spec (FastAPI / drf-spectacular / NestJS) дрейфує - потрібен gate.
- Клієнти ламаються на breaking change - треба oasdiff на PR.
- Кодген видає any замість union - перевірити discriminator.
- Команда забуває required array - типи стають Partial.

## Applies If (ALL must hold)

- Project ships an HTTP API consumed by external or internal clients.
- Spec will be the source of truth for generated clients and mock servers.
- CI infrastructure exists where linters and diff gates can run.
- A repository owner can sign off breaking-change overrides.

## Skip If (ANY kills it)

- Project is a throwaway prototype with no API consumers.
- API surface is GraphQL or gRPC only - use the appropriate schema language.
- Spec drift is intentional during a refactor (use a feature branch).
- Team prefers AsyncAPI for event-driven APIs - use that spec instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| API requirements | markdown user stories or specs | product |
| Auth model | OAuth2 / JWT / API key description | security |
| Error-shape decision | RFC 7807 problem+json yes/no | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-rest-design]] | consumer of the path/verb shape this spec freezes. |
| [[api-error-handling]] | consumer of the error schema this spec references. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: single bundle, operationId everywhere, $ref reuse, required array, oasdiff gate, named examples, server-spec drift check | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step contract-first authoring + CI wiring | ~900 |
| `content/05-examples.xml` | essential | Worked example contract-first vs server-generated | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-operations` | sonnet | Per-endpoint judgement; operationId + request/response shape. |
| `lift-components` | haiku | Mechanical $ref extraction once duplicates are flagged. |
| `configure-linters` | haiku | Boilerplate .redocly.yaml + .spectral.yaml. |
| `review-breaking-diff` | opus | Stakes high; one wrong call breaks every client. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-skeleton.yaml` | OpenAPI 3.1 skeleton with components reuse + security + named examples. |
| `templates/openapi-base.yaml` | Minimal OpenAPI 3.1 base for a brand-new service (info + servers + components shell). |
| `templates/openapi-ci.yml` | GitHub Actions workflow wiring Spectral + oasdiff gates on every PR. |
| `templates/spectral.yaml` | Spectral ruleset enforcing required arrays, named examples, security on operations. |
| `templates/_smoke-test.json` | Minimum viable artefact for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-openapi-specification.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[api-rest-design]]
- [[api-error-handling]]
- [[api-documentation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - source authority (hand vs generated), lint status, breaking-diff presence - onto a rule from `content/01-core-rules.xml`. Use it before touching the spec: it decides apply-vs-skip, picks the source-of-truth path, and routes BREAK diffs to human review.
