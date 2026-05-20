---
slug: api-authentication
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Authentication methodology covering API Keys, JWT, OAuth 2.
content_id: "e94c4166fb5f3ef3"
tags: [api-authentication, security, jwt, oauth, api-keys]
---
# API Authentication

## Summary

**One-sentence:** Authentication methodology covering API Keys, JWT, OAuth 2.

**One-paragraph:** Authentication methodology covering API Keys, JWT, OAuth 2.0, and mTLS — each suited to a distinct traffic shape. Choose the method per use-case: API keys for server-to-server, JWTs for user sessions (RS256/EdDSA, ≤15 min TTL), OAuth 2.0 + PKCE for third-party delegation, mTLS for high-trust B2B. Never hand-roll OAuth flows; always use a library or IdP.

## Applies If (ALL must hold)

- Adding auth to a new service: S2S → API key, user sessions → JWT, third-party → OAuth 2.0.
- Migrating from session cookies to JWT/OIDC for multi-client (mobile + SPA + partner).
- Implementing key rotation, scope tightening, or per-tenant key model.
- Hardening: short access TTL + refresh token rotation + revocation list.
- Federating identity through an IdP (Auth0, Keycloak, Cognito, Clerk, WorkOS).

## Skip If (ANY kills it)

- Hand-rolling OAuth/OIDC — use a library (`authlib`, `oauthlib`, `node-openid-client`).
- Long-lived JWTs (>1 h) to avoid refresh complexity — revocation becomes impossible.
- API keys for end-user auth — they end up in the browser (a public secret).
- mTLS for public consumer apps — cert distribution kills UX; reserve for B2B / agent-to-agent.
- Implicit flow or password grant — both are deprecated in OAuth 2.1.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/software-developer/`
