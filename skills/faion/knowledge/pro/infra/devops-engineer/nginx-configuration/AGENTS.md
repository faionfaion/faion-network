---
slug: nginx-configuration
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nginx as high-performance HTTP server, reverse proxy, and load balancer.
content_id: "87e35f3c469ab0ff"
tags: [nginx, reverse-proxy, load-balancing, tls, web-server]
---
# Nginx Configuration

## Summary

**One-sentence:** Nginx as high-performance HTTP server, reverse proxy, and load balancer.

**One-paragraph:** Nginx as high-performance HTTP server, reverse proxy, and load balancer. Key production requirements: TLS 1.2/1.3 only, server_tokens off, all security headers (HSTS, X-Frame-Options, X-Content-Type-Options), rate limiting, and gzip compression. Always test with nginx -t before reload.

## Applies If (ALL must hold)

- Serving static sites or SPA frontends with aggressive cache headers
- Reverse proxying backend services with proper X-Forwarded-* headers
- SSL/TLS termination with Let's Encrypt certificates
- Load balancing across multiple upstream backends
- Rate limiting login/API endpoints to prevent brute-force

## Skip If (ANY kills it)

- Dynamic application logic — Nginx is a proxy, not an app server
- Complex routing rules that require request body inspection — use Envoy or Traefik
- Kubernetes ingress at scale — use a dedicated ingress controller (nginx-ingress, Traefik)
- Service mesh traffic management — that's Istio/Linkerd territory

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

- parent skill: `pro/infra/devops-engineer/`
