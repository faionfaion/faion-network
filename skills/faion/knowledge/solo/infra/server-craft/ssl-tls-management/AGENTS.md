---
slug: ssl-tls-management
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Configure HTTPS on a Linux VPS with one of three certificate strategies: Let's Encrypt (direct exposure, 90-day auto-renew via certbot), Cloudflare origin cert (15-year cert behind Cloudflare proxy, no renewal), or hybrid.
content_id: "76cded83e5d4fc87"
tags: [ssl, tls, nginx, cloudflare, letsencrypt]
---
# SSL/TLS Management

## Summary

**One-sentence:** Configure HTTPS on a Linux VPS with one of three certificate strategies: Let's Encrypt (direct exposure, 90-day auto-renew via certbot), Cloudflare origin cert (15-year cert behind Cloudflare proxy, no renewal), or hybrid.

**One-paragraph:** Configure HTTPS on a Linux VPS with one of three certificate strategies: Let's Encrypt (direct exposure, 90-day auto-renew via certbot), Cloudflare origin cert (15-year cert behind Cloudflare proxy, no renewal), or hybrid. Always use Cloudflare Full(Strict) mode — never Flexible. nginx SSL hardening: TLS 1.2/1.3 only, strong ciphers, OCSP stapling (Let's Encrypt only), HSTS.

## Applies If (ALL must hold)

- New domain needing HTTPS on any nginx virtual host
- Migrating from Let's Encrypt to a Cloudflare origin cert (eliminating renewal ops)
- Auditing TLS configuration for SSL Labs A+ score
- Adding HSTS or OCSP stapling to an existing nginx site
- Configuring SSL for a domain behind Cloudflare proxy

## Skip If (ANY kills it)

- Cloudflare Flexible mode — causes redirect loops when nginx redirects HTTP to HTTPS
- OCSP stapling with Cloudflare origin certs — they have no OCSP responder; only enable with Let's Encrypt or commercial certs
- Self-signed certs for production — use origin certs instead (trusted by Cloudflare edge)
- Adding preload to HSTS before confirming all subdomains support HTTPS — removal takes months

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

- parent skill: `solo/infra/server-craft/`
