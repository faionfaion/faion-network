# API Rate Limiting

## Summary

**One-sentence:** Designs a per-key rate-limit policy with sliding-window or token-bucket algorithm, 429 envelope (RFC 7807 + Retry-After), and per-tier quotas keyed off the auth scheme.

**One-paragraph:** Rate limiting that fires too late causes outages; firing too early kills legitimate clients. This methodology designs a rate-limit policy keyed off the AUTH-* artefact (token / user / api-key), picks algorithm (sliding-window for fairness, token-bucket for burst tolerance), sets per-tier quotas, and wires a 429 response with RFC 7807 envelope + Retry-After. Output: rate-limit policy + per-tier table + k6 verification script.

**Ефективно для:**

- Solo dev who got a $400 surprise bill from a runaway client.
- Public API where free / paid / partner tiers need different quotas.
- Adding burst tolerance for a billing endpoint hit at hour boundaries.
- Wiring Retry-After header so well-behaved clients back off automatically.

## Applies If (ALL must hold)

- API has identifiable callers (per AUTH-* key).
- Storage available for the limiter (Redis / Valkey / in-memory at small scale).
- Author has authority to set quota policy.

## Skip If (ANY kills it)

- Internal-only RPC behind a service mesh (mesh handles rate-limiting).
- Public read-only endpoint where CDN absorbs traffic.
- Bot-detection layer (separate methodology).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Auth artefact | AUTH-* spec_id | api-authentication |
| Caller-tier inventory | free / paid / partner / internal | PM |
| Redis or Valkey | connection string | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-authentication]] | Source of the limiter key (token / user / api-key). |
| [[api-error-handling]] | 429 envelope reuses the RFC 7807 shape. |

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
| `api_rate_limiting_draft` | sonnet | Bounded synthesis. |
| `api_rate_limiting_validate` | haiku | Mechanical schema check. |
| `api_rate_limiting_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sliding_window.py` | Stdlib sliding-window limiter keyed on auth identity |
| `templates/k6-rate-limit-check.js` | k6 load script that verifies 429 + Retry-After at burst boundary |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-rate-limiting artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-rate-limiting artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-rate-limiting.py` | Validate api-rate-limiting artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[caching-strategy]]
- [[api-authentication]]
- [[api-error-handling]]
- [[api-rest-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
