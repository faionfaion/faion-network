---
slug: nginx-reverse-proxy
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Configure nginx as a multi-domain reverse proxy on a single VPS: proxy_pass to backend services, WebSocket upgrades, security headers, rate limiting, and the snippets pattern for DRY configuration.
content_id: "a932e6be0f8a0424"
tags: [nginx, reverse-proxy, websocket, rate-limiting, security-headers]
---
# nginx Reverse Proxy

## Summary

**One-sentence:** Configure nginx as a multi-domain reverse proxy on a single VPS: proxy_pass to backend services, WebSocket upgrades, security headers, rate limiting, and the snippets pattern for DRY configuration.

**One-paragraph:** Configure nginx as a multi-domain reverse proxy on a single VPS: proxy_pass to backend services, WebSocket upgrades, security headers, rate limiting, and the snippets pattern for DRY configuration. Architecture: Internet → Cloudflare → nginx (80/443) → local services on 127.0.0.1:PORT.

## Applies If (ALL must hold)

- Deploying any web application on a VPS that needs HTTP/HTTPS routing
- Exposing multiple domains or subdomains from a single server
- Adding WebSocket support to an existing proxy setup
- Applying security headers (HSTS, CSP, X-Content-Type-Options) across all sites
- Rate limiting API endpoints against brute-force or abuse

## Skip If (ANY kills it)

- When using a managed platform (Heroku, Railway, Render) — proxy is handled for you
- Kubernetes environments — use an Ingress controller instead
- When Caddy or Traefik is already in use — don't mix reverse proxies on the same server
- For TLS termination when Cloudflare Full(Strict) mode is configured — Cloudflare already handles the browser-facing TLS, nginx still needs a cert for origin

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
