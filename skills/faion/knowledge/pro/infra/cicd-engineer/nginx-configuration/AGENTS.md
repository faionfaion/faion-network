---
slug: nginx-configuration
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an nginx config (server block + snippets) for reverse-proxy + TLS 1.2/1.3 + security headers + caching, with rate-limit zones and explicit upstream definition.
content_id: "285a394fa7ff2179"
complexity: medium
produces: config
est_tokens: 4500
tags: [nginx, reverse-proxy, ssl-tls, web-server, security]
---

# Nginx Configuration

## Summary

**One-sentence:** Produces an nginx config (server block + snippets) for reverse-proxy + TLS 1.2/1.3 + security headers + caching, with rate-limit zones and explicit upstream definition.

**One-paragraph:** Nginx sits at the edge of every web stack — terminating TLS, balancing load, serving statics, proxying APIs. The defaults are unsafe: missing HSTS, no security headers, no rate-limit zones, gzip off, single worker. This methodology produces a hardened nginx config (main + snippets + per-site server block) covering TLS 1.2/1.3 only, Mozilla intermediate cipher suite, HSTS / CSP / X-Frame-Options / X-Content-Type-Options, gzip + brotli, rate-limit zones, OCSP stapling, and reverse-proxy params with WebSocket upgrade. Validator confirms presence of all required directives + absence of TLS 1.0/1.1.

**Ефективно для:**

- Reverse proxy перед Django/Node/FastAPI backend з HTTPS-терминацією.
- Static-site serving з агресивним кешуванням (1y immutable для assets).
- WebSocket upgrade (chat, live updates) — потрібні Connection/Upgrade headers.
- Rate-limit-зоны: захист auth endpoints від credential stuffing.
- Hardened TLS config: 1.2/1.3 only, HSTS preload, OCSP stapling.

## Applies If (ALL must hold)

- Service is served via nginx (or migrating from Apache / Caddy / Traefik).
- TLS termination happens at nginx (not at upstream LB).
- Backend is an HTTP service that can be proxied (Django, Node, FastAPI, static SPA).

## Skip If (ANY kills it)

- Service-mesh internal mTLS — use Envoy / Istio sidecar, not nginx.
- Highly dynamic routing with auto-discovery — Traefik or Caddy handle this more cleanly.
- Pure API gateway needs (auth, quotas, transformations) — Kong / AWS API Gateway purpose-built for it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| TLS certificate | PEM (fullchain + key) — Let's Encrypt or commercial | certbot / cert-manager / vault |
| Backend upstream | host:port or socket path | deployment manifest |
| Domain list | FQDN + optional ALT names | DNS / Cloudflare |
| Security baseline | list of required headers (HSTS, CSP, etc.) + cipher policy | security team / Mozilla SSL Config Generator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[load-balancing-concepts]] | Algorithm + health-check choices feed the upstream block |
| [[ssl-tls-setup]] | Cipher suite + OCSP stapling details belong there |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: tls-12-13-only, security-headers-required, http-2-or-3, rate-limit-on-auth, gzip-not-on-precompressed, skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for config artefact + valid/invalid + forbidden directives | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: tls-10-still-enabled, no-hsts, single-worker, proxy-pass-without-headers | 800 |
| `content/04-procedure.xml` | essential | 6 steps: TLS material → main.conf → snippets → server block → test → reload | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on workload shape → directive set | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-workload` | haiku | Bucket: static / reverse-proxy / websocket / mixed. |
| `compose-server-block` | sonnet | Assemble snippets + server-block matching the workload. |
| `explain-rationale` | sonnet | Tie each directive to the rule it satisfies. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nginx.conf` | Main nginx.conf skeleton with worker / events / http blocks + global TLS + gzip + rate-limit zones |
| `templates/security-headers.conf` | Reusable snippet of security response headers (HSTS / CSP / X-Frame / etc.) |
| `templates/site-reverse-proxy.conf` | Per-site server block: HTTP→HTTPS redirect + HTTPS server + reverse-proxy with WebSocket upgrade |
| `templates/_smoke-test.json` | Minimum filled artefact used by validate-nginx-configuration.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nginx-configuration.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[load-balancing-concepts]]
- [[ssl-tls-setup]]
- [[security-policy-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it whenever you have to defend the directive set for a new server block in a security review.
