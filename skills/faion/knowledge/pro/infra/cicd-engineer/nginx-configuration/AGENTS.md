---
slug: nginx-configuration
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nginx is a high-performance HTTP server, reverse proxy, and load balancer.
content_id: "87e35f3c469ab0ff"
tags: [nginx, reverse-proxy, ssl-tls, web-server, security]
---
# Nginx Configuration

## Summary

**One-sentence:** Nginx is a high-performance HTTP server, reverse proxy, and load balancer.

**One-paragraph:** Nginx is a high-performance HTTP server, reverse proxy, and load balancer. This methodology covers configuration patterns for reverse proxy setups, SSL/TLS termination, caching, and security hardening based on 2025-2026 best practices.

## Applies If (ALL must hold)

- Setting up web servers for static or dynamic content
- Configuring reverse proxy for backend services
- Implementing SSL/TLS termination with TLS 1.2/1.3
- Setting up load balancing
- Optimizing web application performance with caching
- Implementing security headers (HSTS, CSP, X-Frame-Options)
- WebSocket proxy configuration

## Skip If (ANY kills it)

- Service-mesh internal traffic (mTLS, sidecar routing) — use Envoy or Istio instead
- Dynamic routing with frequent topology changes — Traefik or Caddy handle this more cleanly with auto-discovery
- Pure API gateway with auth, quotas, and transformations — Kong or AWS API Gateway provide purpose-built features

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

- parent skill: `pro/infra/cicd-engineer/`
