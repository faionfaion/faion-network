---
slug: ssl-tls-management
tier: solo
group: infra
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a per-domain TLS plan — Cloudflare-origin OR Let's Encrypt — with cert paths, renewal cron, and ssl_params snippet — gated by an expiry-monitor cron.
content_id: "f327008169151603"
complexity: medium
produces: config
est_tokens: 4500
tags: ["tls", "ssl", "letsencrypt", "cloudflare", "certbot"]
---
# SSL/TLS Management

## Summary

**One-sentence:** Generates a per-domain TLS plan — Cloudflare-origin OR Let's Encrypt — with cert paths, renewal cron, and ssl_params snippet — gated by an expiry-monitor cron.

**One-paragraph:** TLS on a solo VPS is two flavours: Cloudflare full(strict) with origin certs (15-year, no renewal) or Let's Encrypt with certbot (90-day, auto-renew). This methodology pins the choice per domain, declares the cert paths, the ssl_params snippet (Mozilla 'Intermediate'), the renewal cron (LE) or expiry-monitor (CF), and an OCSP stapling toggle. Output: a TlsPlan + cron entries.

**Ефективно для:**

- Multi-domain VPS behind Cloudflare full(strict).
- Apex domains where Let's Encrypt is the only option.
- Auditing existing TLS posture against Mozilla recommendations.
- Setting up expiry monitoring before the first cert lapses.

## Applies If (ALL must hold)

- Serving HTTPS on a custom domain from a VPS.
- Switching between Cloudflare-origin and Let's Encrypt.
- Auditing current TLS posture for forbidden algorithms (TLS 1.0/1.1).
- Setting up renewal automation for the first time.

## Skip If (ANY kills it)

- Managed platform that handles TLS termination (Heroku/Vercel/Netlify).
- Internal-only services behind WireGuard/Tailscale with no public TLS.
- Existing working renewal + monitoring — don't re-introduce churn.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain list + chosen TLS mode | YAML/CSV | operator inventory |
| Cloudflare API token (origin certs) OR ACME account (LE) | secret in 1Password | operator credentials |
| Allowed ciphers + protocols | Mozilla preset name | Mozilla SSL Config Generator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| nginx-reverse-proxy | TLS config is consumed by nginx vhosts produced upstream. |
| cloudflare-domain-dns | Cloudflare-origin mode requires the domain proxied through Cloudflare. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-strict-mode-only, r2-monitored-expiry, r3-modern-ciphers, r4-named-renewal-owner, r5-ocsp-stapling-when-le | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the SSL/TLS Management artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: flexible-mode-shipped, no-expiry-monitor, weak-ciphers-default, certbot-renew-no-deploy-hook | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-tls-plan` | sonnet | Per-domain decision with stakes. |
| `render-ssl-params` | haiku | Template fill from Mozilla preset. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ssl-tls-management.json` | TlsPlan JSON skeleton (domains + mode + renewal). |
| `templates/ssl-tls-management.md` | Human-readable audit trail. |
| `templates/ssl-params.conf` | Mozilla 'Intermediate' ciphers + protocols snippet. |
| `templates/site-cloudflare.conf` | Reference vhost using Cloudflare origin cert. |
| `templates/site-letsencrypt.conf` | Reference vhost using Let's Encrypt cert + ACME challenge. |
| `templates/setup-cloudflare-origin-cert.sh` | Generates origin cert via Cloudflare API + installs to /etc/nginx/ssl. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ssl-tls-management.py` | Validate TlsPlan JSON against the schema. | Pre-deploy + post-renewal. |
| `scripts/check-cert-expiry.sh` | Expiry monitor — exit 1 if any cert < 14d to expiry. | Daily cron. |
| `scripts/test-tls-config.sh` | Runs testssl.sh / sslyze against the live config. | Post-config-change + monthly. |

## Related

- [[nginx-reverse-proxy]]
- [[cloudflare-domain-dns]]
- [[monitoring-logging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
