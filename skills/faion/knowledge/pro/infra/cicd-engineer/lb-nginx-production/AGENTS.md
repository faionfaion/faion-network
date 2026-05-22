---
slug: lb-nginx-production
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production Nginx LB: worker_processes auto with worker_rlimit_nofile 65535, upstream zones for shared state, keepalive connections for HTTP/1.
content_id: "53a727095b6e5297"
tags: [nginx, load-balancing, tls, reverse-proxy, infrastructure]
---
# Nginx Production Load Balancer Configuration

## Summary

**One-sentence:** Production Nginx LB: worker_processes auto with worker_rlimit_nofile 65535, upstream zones for shared state, keepalive connections for HTTP/1.

**One-paragraph:** Production Nginx LB: worker_processes auto with worker_rlimit_nofile 65535, upstream zones for shared state, keepalive connections for HTTP/1.1 reuse, TLS 1.2+/1.3 with ssl_stapling, rate limiting zones (limit_req_zone + limit_conn_zone), security headers (HSTS, X-Frame-Options, X-Content-Type-Options), WebSocket upgrade support, and proxy_next_upstream for automatic retry on failure.

## Applies If (ALL must hold)

- Web server plus LB combo — serve static assets from Nginx while proxying dynamic traffic to backends.
- Static content caching — use proxy_cache to cache upstream responses at the LB layer.
- Path-based routing — separate /api, /ws, /admin traffic to different upstream pools.
- WebSocket proxying — native upgrade header support.
- Simpler configuration than HAProxy for HTTP-only workloads.

## Skip If (ANY kills it)

- TCP-heavy environments where 10-15% HAProxy performance advantage matters at scale.
- Advanced circuit breaking or fine-grained retry control — use HAProxy or Envoy.
- Active health checks without Nginx Plus — open source Nginx only supports passive (max_fails) health checking.

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
