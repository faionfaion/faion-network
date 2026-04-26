# API Authentication

## Summary

Authentication methodology covering API Keys, JWT, OAuth 2.0, and mTLS — each suited to
a distinct traffic shape. Choose the method per use-case: API keys for S2S, JWTs for user
sessions (RS256/EdDSA, ≤15 min TTL), OAuth 2.0 + PKCE for third-party delegation, mTLS for
high-trust B2B. Never hand-roll OAuth flows; always use a library or IdP.

## Why

Authentication is the #1 source of CVEs when implemented from scratch. Using the right method
per traffic shape eliminates whole attack classes: asymmetric JWTs prevent token-forgery by
any service holding a shared secret; short TTL + refresh rotation makes stolen tokens
short-lived; PKCE removes code-interception from public OAuth clients.

## When To Use

- Adding auth to a new service: S2S → API key, user sessions → JWT, third-party → OAuth 2.0
- Migrating from session cookies to JWT/OIDC for multi-client (mobile + SPA + partner)
- Implementing key rotation, scope tightening, or per-tenant key model
- Hardening: short access TTL + refresh token rotation + revocation list
- Federating identity through an IdP (Auth0, Keycloak, Cognito, Clerk, WorkOS)

## When NOT To Use

- Hand-rolling OAuth/OIDC — use a library (`authlib`, `oauthlib`, `node-openid-client`)
- Long-lived JWTs (>1 h) to avoid refresh complexity — revocation becomes impossible
- API keys for end-user auth — they end up in the browser (a public secret)
- mTLS for public consumer apps — cert distribution kills UX; reserve for B2B / agent-to-agent
- Implicit flow or password grant — both are deprecated in OAuth 2.1

## Content

| File | What's inside |
|------|---------------|
| `content/01-auth-methods.xml` | Method comparison table, decision rules, key practices per method |
| `content/02-jwt-patterns.xml` | JWT claims, RS256/EdDSA, short TTL, refresh rotation, denylist |
| `content/03-oauth-flows.xml` | Authorization code + PKCE, client credentials, scope management |

## Templates

| File | Purpose |
|------|---------|
| `templates/fastapi-jwt-verifier.py` | FastAPI dependency for RS256 JWT verification |
| `templates/api-key-check.py` | Constant-time SHA-256 API key verification |
