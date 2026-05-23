# Nginx Production Load Balancer Configuration

## Summary

**One-sentence:** Generates a production Nginx LB config with worker tuning, upstream zone, keepalive, TLS 1.2+, security headers, rate-limit zones, and proxy_next_upstream retry.

**One-paragraph:** Production Nginx LB requires `worker_processes auto` with `worker_rlimit_nofile 65535`, `upstream` zones for shared state, `keepalive` connections for HTTP/1.1 reuse to upstreams, TLS 1.2+/1.3 with OCSP stapling, rate limiting zones (`limit_req_zone` + `limit_conn_zone`), security headers (HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy), WebSocket upgrade support, and `proxy_next_upstream` for automatic retry on failure.

**Ефективно для:**

- Web server + LB combo: serve static assets locally + proxy dynamic до upstream.
- HTTP-only LB замість HAProxy — простіша конфігурація + cache layer.
- Static content caching через `proxy_cache` + `proxy_cache_valid`.
- WebSocket / SSE proxying — `Upgrade` + `Connection` headers без розривів.
- Path-based routing: /api → app pool, /ws → websocket pool, /static → assets.

## Applies If (ALL must hold)

- Web server + LB combo — serve static assets from Nginx + proxy dynamic to backends.
- Static-content caching — use `proxy_cache` to cache upstream responses at the LB layer.
- Path-based routing — separate `/api`, `/ws`, `/admin` to different upstream pools.
- WebSocket proxying — native upgrade-header support.
- Simpler config than HAProxy for HTTP-only workloads.

## Skip If (ANY kills it)

- TCP-heavy environments where HAProxy's 10–15% advantage matters at scale.
- Advanced circuit breaking / fine-grained retry control — use HAProxy or Envoy.
- Active health checks without Nginx Plus — OSS Nginx only does passive (`max_fails`).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Upstream pool | IP:port list | service inventory |
| TLS cert + key | PEM | cert manager |
| Static-asset path | filesystem | deploy pipeline |
| Rate-limit policy | req/sec per IP | product / abuse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[nginx-configuration]] | Base directives (events, http, server) extended here for LB. |
| [[lb-health-checks]] | Per-backend probe path required by `max_fails` config. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: worker-auto, upstream-zone, keepalive-upstream, tls-1-2-min, limit-req-zone, security-headers | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tune-workers` | sonnet | CPU + RAM sizing arithmetic. |
| `write-server-block` | sonnet | Path routing + TLS + headers. |
| `lint-config` | haiku | Mechanical `nginx -t` + nginx-config-formatter. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nginx.conf` | Production nginx.conf with worker tuning + upstream + TLS + rate limit + headers |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-nginx-production.py` | Validate the Nginx artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[nginx-configuration]]
- [[lb-haproxy-production]]
- [[lb-monitoring]]
- [[lb-health-checks]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (workload kind, static vs dynamic split, TLS need, rate-limit need) to a concrete config shape, each leaf referencing a rule from `01-core-rules.xml`.
