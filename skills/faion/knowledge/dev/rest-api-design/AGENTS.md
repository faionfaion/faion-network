# REST API Design

## Summary

**One-sentence:** REST API design spec: resource-oriented URLs, verb semantics (GET/POST/PUT/PATCH/DELETE), correct status codes, cursor pagination, problem+json errors, versioning policy.

**One-paragraph:** REST APIs go bad when verbs leak into URLs (`/getUser`), when 200 OK ships error bodies, when pagination uses offset at scale, when errors are plain strings, and when versioning is implicit. This methodology produces a resource-design spec: noun-only URLs in plural form, verb semantics mapped to HTTP methods, status codes used per RFC 9110, cursor pagination for collections >1k, problem+json error shape, and a versioning policy (path /v1 with deprecation timeline).

**Ефективно для:**

- Перший публічний API - зафіксувати resource model + status codes.
- Legacy RPC-style API (`/getUser`, `/doThing`) переписується на REST.
- Pagination ламається на 10k+ rows - перейти на cursor.
- Error response - plain string; клієнти не можуть розрізнити причини.
- Breaking change на v1 - спланувати v2 + deprecation.

## Applies If (ALL must hold)

- Project exposes an HTTP API consumed by clients.
- Endpoints are resource-shaped (CRUD over nouns) more than command-shaped.
- Team can ship and own the API contract over time.
- OpenAPI spec is feasible (consumers want generated clients).

## Skip If (ANY kills it)

- GraphQL or gRPC is the chosen interface.
- API is event-driven (use AsyncAPI / webhooks methodology).
- Endpoints are pure RPC commands (no resource model fits).
- Internal-only one-off endpoint with no consumers.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource model | list of nouns + relationships | domain modelling |
| Auth model | OAuth2 / JWT / API key | security |
| Versioning policy | path / header / query | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[openapi-specification]] | spec format that captures this design as a machine-readable contract. |
| [[api-error-handling]] | downstream consumer of the error-shape decision in this spec. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: noun URLs, HTTP method semantics, truthful status codes, cursor pagination, problem+json, path versioning, query-param filters | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: resources, versioning, status codes, pagination, errors | ~900 |
| `content/05-examples.xml` | essential | Worked example for an e-commerce REST API | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-resources` | sonnet | Domain-modelling judgement. |
| `map-status-codes` | haiku | Mechanical mapping per outcome. |
| `draft-error-schema` | sonnet | Per-endpoint judgement on type URIs. |
| `plan-versioning` | opus | Stakes high; sunset timeline affects every consumer. |

## Templates

| File | Purpose |
|------|---------|
| `templates/resource-skeleton.yaml` | REST resource skeleton with cursor pagination + problem+json errors. |
| `templates/problem.json` | Problem+JSON example error body. |
| `templates/spectral-ruleset.yaml` | Spectral lint ruleset enforcing REST design rules on OpenAPI. |
| `templates/_smoke-test.json` | Minimum viable rest-design artefact for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rest-api-design.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[openapi-specification]]
- [[api-error-handling]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - URL shape, status truthfulness, pagination depth, error shape - onto a rule from `content/01-core-rules.xml`. Use it before merging endpoints: it catches verbs-in-URL, 200-on-error, and offset-pagination-at-scale upstream.
