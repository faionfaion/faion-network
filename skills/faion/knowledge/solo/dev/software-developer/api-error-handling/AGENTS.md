---
slug: api-error-handling
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-net]
summary: Builds an RFC 7807 Problem Details error envelope + a typed error catalogue with stable type URIs, traceId on every error, and 4xx/5xx split policy.
content_id: "2af34dc675078749"
complexity: medium
produces: spec
est_tokens: 4200
tags: [api, error-handling, rfc-7807, problem-details, tracing]
---
# API Error Handling

## Summary

**One-sentence:** Builds an RFC 7807 Problem Details error envelope + a typed error catalogue with stable type URIs, traceId on every error, and 4xx/5xx split policy.

**One-paragraph:** Inconsistent error envelopes are the largest source of partner-integration friction. This methodology emits an error-catalogue: one envelope shape (RFC 7807), a stable `type` URI per error class (not per occurrence), a mandatory `traceId` for log correlation, and a strict 4xx/5xx split (4xx = caller fixable, 5xx = our fault). Output: catalogue + envelope schema + per-language handler templates.

**Ефективно для:**

- Solo dev shipping an API where every endpoint returns a different error shape.
- Adding `traceId` so support can correlate a customer complaint with logs.
- Replacing hard-coded 500s with categorised 4xx where the user can fix it.
- Wiring a partner integration where the partner needs stable type URIs to handle errors programmatically.

## Applies If (ALL must hold)

- API has &gt;= 2 distinct error classes already in production.
- Logging infrastructure produces a traceId (OTel / Datadog / Sentry).
- Author has authority to break clients on a documented version bump (or roll out behind a header).

## Skip If (ANY kills it)

- API has zero error classes (e.g. pure proxy) — defer.
- Legacy SOAP stack — out of scope.
- Internal RPC with proto errors — separate methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing error inventory | list of {endpoint, status, body shape} | code or runtime sampling |
| Tracer | OTel-compatible tracer | platform |
| Auth scheme | AUTH-* artefact | api-authentication |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-documentation]] | Error catalogue links from the Error Codes section. |
| [[api-rate-limiting]] | 429 envelope shape is shared. |

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
| `api_error_handling_draft` | sonnet | Bounded synthesis. |
| `api_error_handling_validate` | haiku | Mechanical schema check. |
| `api_error_handling_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/error-handler.py` | FastAPI middleware that wraps every error into RFC 7807 envelope with traceId |
| `templates/problem-detail.json` | RFC 7807 Problem Details example body |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-error-handling artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-error-handling artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-error-handling.py` | Validate api-error-handling artefact against schema | Pre-commit; CI on each artefact change |

## Related



## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
