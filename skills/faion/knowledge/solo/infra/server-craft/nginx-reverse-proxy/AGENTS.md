---
slug: nginx-reverse-proxy
tier: solo
group: infra
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an nginx vhost set + snippet pack for a multi-domain VPS — proxy_pass, WebSocket upgrade, security headers, rate limits — gated by a validated DeploymentPlan.
content_id: "b2938078be0789b4"
complexity: medium
produces: config
est_tokens: 4700
tags: ["nginx", "reverse-proxy", "websocket", "rate-limiting", "security-headers"]
---
# nginx Reverse Proxy

## Summary

**One-sentence:** Generates an nginx vhost set + snippet pack for a multi-domain VPS — proxy_pass, WebSocket upgrade, security headers, rate limits — gated by a validated DeploymentPlan.

**One-paragraph:** nginx terminates HTTPS, routes /api → backend on 127.0.0.1, upgrades WebSocket connections, applies HSTS/CSP headers, and rate-limits API endpoints. This methodology produces a vhost + snippet plan that survives copy-paste: proxy_pass without trailing-slash bugs, $connection_upgrade map declared in http context, X-Forwarded-Proto pinned to https for Cloudflare origins, and rate-limit zones declared in http context but applied per location.

**Ефективно для:**

- Solo VPS host running 3–10 domains on a single nginx with snippets/.
- Backend on 127.0.0.1:PORT behind Cloudflare full(strict) — origin still needs a cert.
- Apps with WebSocket endpoints (Socket.IO, FastAPI ws, n8n editor).
- API routes that must rate-limit unauthenticated POST traffic.

## Applies If (ALL must hold)

- Deploying a web application on a VPS that needs HTTP/HTTPS routing.
- Exposing multiple domains or subdomains from a single nginx.
- Adding WebSocket support to an existing proxy setup.
- Applying security headers (HSTS, CSP, X-Content-Type-Options) across sites.
- Rate-limiting API endpoints against brute-force or abuse.

## Skip If (ANY kills it)

- Managed platform (Heroku, Railway, Render) — proxy is handled for you.
- Kubernetes — use an Ingress controller instead.
- Caddy or Traefik already in use — don't mix reverse proxies on one host.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain list + backend port per app | YAML/CSV | operator inventory |
| Origin cert (Cloudflare or Let's Encrypt) | PEM + key | Cloudflare dashboard / certbot |
| Rate-limit budget per endpoint | req/s | load model |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| ssl-tls-management | Cert lifecycle owned upstream; this methodology consumes the cert paths. |
| firewall-management | UFW must allow 80/443 before nginx is reachable. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-proxy-pass-no-trailing-slash, r2-websocket-upgrade-map, r3-forwarded-proto-https, r4-csp-per-site, r5-ratelimit-in-http-context | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the nginx Reverse Proxy artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: trailing-slash-double, csp-in-global-snippet, ratelimit-not-declared, missing-x-forwarded-for, gzip-on-proxied-stream | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-vhost` | sonnet | Per-app template fill with branch points. |
| `audit-existing-config` | sonnet | Diff active vhost against rules. |
| `compose-snippet-pack` | haiku | Mechanical concat of validated snippets. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nginx-reverse-proxy.json` | Per-vhost DeploymentPlan JSON skeleton (domain, backend, runtime, headers). |
| `templates/nginx-reverse-proxy.md` | Human-readable audit trail for the vhost change. |
| `templates/site-fullstack.conf` | Reference vhost — API prefix-strip, WebSocket, SPA, ratelimit. |
| `templates/proxy-params.conf` | Forwarded headers snippet — Host, X-Real-IP, X-Forwarded-Proto. |
| `templates/websocket.conf` | Upgrade headers snippet — requires `$connection_upgrade` map. |
| `templates/security-headers.conf` | HSTS + X-Content-Type-Options + Referrer-Policy. |
| `templates/rate-limiting.conf` | Per-zone limit_req declarations. |
| `templates/cloudflare-realip.conf` | Restore client IP from CF-Connecting-IP. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nginx-reverse-proxy.py` | Validate DeploymentPlan against the output-contract schema. | Pre-deploy, before `nginx -t`. |
| `scripts/nginx-audit.sh` | Lint live nginx config against the rule-set. | Weekly cron + post-change. |

## Related

- [[ssl-tls-management]]
- [[firewall-management]]
- [[cloudflare-domain-dns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
