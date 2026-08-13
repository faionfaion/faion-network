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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/nginx.conf`

```conf
user www-data;
worker_processes auto;
worker_rlimit_nofile 65535;
pid /run/nginx.pid;

events {
    worker_connections 8192;
    multi_accept       on;
    use                epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout 65;
    server_tokens   off;

    # rate-limit zones (shared across workers)
    limit_req_zone  $binary_remote_addr zone=req_per_ip:10m  rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=conn_per_ip:10m;

    # TLS defaults
    ssl_protocols           TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers             ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_session_cache       shared:SSL:10m;
    ssl_session_timeout     10m;
    ssl_stapling            on;
    ssl_stapling_verify     on;

    log_format main_ext '$remote_addr - $remote_user [$time_local] '
                        '"$request" $status $body_bytes_sent '
                        '"$http_referer" "$http_user_agent" '
                        'rt=$request_time uct=$upstream_connect_time urt=$upstream_response_time';
    access_log  /var/log/nginx/access.log  main_ext;
    error_log   /var/log/nginx/error.log warn;

    upstream app_backend {
        zone app_backend 64k;
        least_conn;
        server 10.0.1.1:8080 max_fails=3 fail_timeout=30s;
        server 10.0.1.2:8080 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }

    server {
        listen 80;
        server_name app.example.com;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name app.example.com;

        ssl_certificate     /etc/nginx/certs/app.example.com.crt;
        ssl_certificate_key /etc/nginx/certs/app.example.com.key;

        # security headers (apply on errors too)
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
        add_header X-Frame-Options DENY always;
        add_header X-Content-Type-Options nosniff always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

        limit_req  zone=req_per_ip  burst=20 nodelay;
        limit_conn conn_per_ip 30;

        location / {
            proxy_pass http://app_backend;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_connect_timeout 5s;
            proxy_read_timeout    60s;
            proxy_next_upstream   error timeout http_502 http_503 http_504;
        }
    }
}
```
