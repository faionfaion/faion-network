---
slug: api-authentication
tier: solo
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Custom auth middleware is the highest-risk code in the repo: subtle bugs like omitting aud/iss checks, accepting alg:none, or returning 200 on JWTError bypass all access control silently.
content_id: "e94c4166fb5f3ef3"
tags: [authentication, api-security, jwt, oauth, api-keys]
---
# API Authentication

## Summary

**One-sentence:** Custom auth middleware is the highest-risk code in the repo: subtle bugs like omitting aud/iss checks, accepting alg:none, or returning 200 on JWTError bypass all access control silently.

**One-paragraph:** Custom auth middleware is the highest-risk code in the repo: subtle bugs like omitting aud/iss checks, accepting alg:none, or returning 200 on JWTError bypass all access control silently. Protect API endpoints with the minimum auth mechanism that fits the trust boundary: API keys (hashed, prefixed) for server-to-server, short-lived JWT (RS256, 5–15 min) plus rotating refresh tokens for user sessions, OAuth 2.0 Authorization Code + PKCE for third-party delegation. Never roll custom crypto or validation logic—use authlib, jose, or a vendor SDK. Every auth change requires negative tests (expired, wrong audience, missing scope).

## Applies If (ALL must hold)

- Any API exposing user data, billing, or write operations across an authentication boundary
- Server-to-server integrations (API keys with rotation or OAuth client credentials)
- Third-party access on behalf of users (OAuth 2.0 auth code + PKCE)
- First-party SPA + mobile sessions: short-lived access JWT + rotating refresh token, ideally cookie-bound
- Machine-to-machine in zero-trust networks (mTLS or signed JWTs with audience claims)
- Scoped delegation instead of admin-or-nothing permissions

## Skip If (ANY kills it)

- Internal services on a private network where mTLS or service mesh identity already authenticates the caller—adding JWT layers is theatre
- Public read-only endpoints (status, public data)—auth adds friction without security gain
- Embedding HS256 secrets into mobile/SPA bundles—they will leak; use OAuth + PKCE or server proxy
- One-off scripts reading a single resource—a per-script API key is sufficient

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

- parent skill: `solo/dev/api-developer/`
