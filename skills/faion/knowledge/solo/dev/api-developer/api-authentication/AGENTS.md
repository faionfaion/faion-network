# API Authentication

## Summary

Protect API endpoints with the minimum auth mechanism that fits the trust boundary: API keys (hashed, prefixed) for server-to-server, short-lived JWT (RS256, 5–15 min) + rotating refresh tokens for user sessions, OAuth 2.0 Authorization Code + PKCE for third-party delegation. Never roll custom crypto or validation logic — use `authlib`, `jose`, or a vendor SDK. Every auth change requires negative tests (expired, wrong audience, missing scope).

## Why

Custom auth middleware is the highest-risk code in the repo: subtle bugs — omitting `aud`/`iss` checks, accepting `alg:none`, catching `JWTError` and returning 200 — bypass all access control silently. Refresh token reuse under concurrent requests requires a per-family lock and reuse-detection (last-write-wins breaks). API keys stored unhashed are unrecoverable on breach.

## When To Use

- Any API exposing user data, billing, or write operations across an auth boundary
- Server-to-server integrations (API keys with rotation or OAuth client credentials)
- Third-party access on behalf of users (OAuth 2.0 auth code + PKCE)
- Machine-to-machine in zero-trust networks (mTLS or signed JWTs with audience claims)
- Scoped delegation instead of admin-or-nothing permissions

## When NOT To Use

- Internal services on a private network where service mesh identity authenticates the caller
- Public read-only endpoints (status, public data) — auth adds friction without security gain
- Embedding HS256 secrets into mobile/SPA bundles — they will leak; use OAuth + PKCE
- One-off scripts reading a single resource — a per-script API key is sufficient

## Content

| File | What's inside |
|------|---------------|
| `content/01-auth-methods.xml` | API keys, JWT (claims, implementation), OAuth 2.0 flows, scope management |
| `content/02-security-rules.xml` | Validation requirements, token binding, rotation rules, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/jwt_auth.py` | FastAPI JWT create/verify with exp, iss, aud, scope checks |
| `templates/jwt-misconfig-check.sh` | CI smoke test: fails if API accepts alg:none or wrong-aud tokens |

## Scripts

none
