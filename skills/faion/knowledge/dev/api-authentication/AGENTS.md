# API Authentication

## Summary

**One-sentence:** Picks an API authentication scheme (JWT, OAuth2 client-creds, API-key, mTLS, opaque-session) and emits a scheme-spec with token lifetime, rotation, and revocation paths.

**One-paragraph:** Authentication is mismatched to use-case more often than it is broken cryptographically. This methodology selects from five canonical schemes — JWT, OAuth2 client-credentials, API-key, mTLS, opaque-session — based on caller type, audience, and revocation requirement, and emits a scheme-spec: token shape, lifetime, rotation interval, revocation path, and the failure mode the choice prevents (e.g. JWT for cross-service, never for B2C session).

**Ефективно для:**

- Solo dev choosing between JWT and opaque session for a new SaaS.
- Adding a B2B partner integration that needs OAuth2 client-credentials.
- Auditing an existing API where revocation is broken because tokens are long-lived.
- Standardising on one auth scheme per audience instead of three by accident.

## Applies If (ALL must hold)

- API has &gt;= 1 authenticated endpoint.
- Caller type is identifiable (browser / mobile / server / IoT).
- Audience boundary is defined (own users vs partners vs public).
- Revocation requirement is known (instant vs eventual).

## Skip If (ANY kills it)

- Public read-only endpoints (no auth needed).
- Internal-only RPC inside a VPC with mTLS at the mesh — separate methodology.
- Legacy SOAP / WS-Security stack — out of scope.
- Ephemeral preview environments where auth is bypassed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Caller types | list | PM / architect |
| Revocation SLA | duration (seconds) | security / ops |
| Identity provider | OIDC / SAML / homegrown | platform |
| Existing token shapes | JWT / opaque / API-key string | running API |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-rate-limiting]] | Auth scheme drives the rate-limit key (token / user / API-key). |
| [[api-error-handling]] | 401/403 envelope must match the API's Problem Details format. |

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
| `api_authentication_draft` | sonnet | Bounded synthesis. |
| `api_authentication_validate` | haiku | Mechanical schema check. |
| `api_authentication_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/api-key-check.py` | Stdlib API-key validator with rotation overlap |
| `templates/fastapi-jwt-verifier.py` | FastAPI dependency that verifies JWT against JWKS + denylist |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-authentication artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-authentication artefact for validator round-trip |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-authentication.py` | Validate api-authentication artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[api-rate-limiting]]
- [[api-error-handling]]
- [[api-rest-design]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.
