---
slug: api-gateway-security
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: API gateway security layers: TLS termination at the edge, authentication (API keys, JWT, OAuth 2.
content_id: "8785d4549ee82500"
tags: [api-gateway, security, authentication, authorization, tls]
---
# API Gateway Security: Authentication, Authorization, TLS, WAF, and Headers

## Summary

**One-sentence:** API gateway security layers: TLS termination at the edge, authentication (API keys, JWT, OAuth 2.

**One-paragraph:** API gateway security layers: TLS termination at the edge, authentication (API keys, JWT, OAuth 2.0, mTLS), authorization (RBAC, scopes), WAF for threat detection, request validation for size and schema, CORS policy enforcement, header sanitization (stripping internal headers before forwarding), and audit logging. Each layer is mandatory — missing one creates an exploitable gap.

## Applies If (ALL must hold)

- Configuring authentication mechanisms for public or partner APIs (JWT, OAuth 2.0, API keys).
- Implementing mTLS for service-to-service or high-security partner integrations.
- Setting up WAF rules, IP whitelisting, bot detection, or DDoS protection.
- Enforcing CORS policies and security headers (HSTS, X-Content-Type-Options, CSP).
- Adding request size limits, schema validation, and input sanitization.
- Configuring audit logging for compliance (GDPR, HIPAA, PCI-DSS).
- Stripping internal headers (X-Internal-*, JWTs after validation) before forwarding to backends.

## Skip If (ANY kills it)

- Gateway-level authorization for fine-grained business rules — those belong in the service (e.g., "can this user edit this specific document?"). Gateway handles coarse-grained access (authenticated? has scope?), services handle fine-grained (owns the resource?).
- Applying WAF rules to internal-only, service-mesh-only APIs — WAF overhead is justified only at the external edge.
- Performing complex token introspection on every request at high RPS without caching — always cache authorizer results (AWS: 300s TTL; Kong: JWT plugin caches JWKS).

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

- parent skill: `solo/dev/software-architect/`
