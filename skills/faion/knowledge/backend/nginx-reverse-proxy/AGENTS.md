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
| `templates/nginx-reverse-proxy.md.j2` | Human-readable audit trail for the vhost change. |
| `templates/nginx-reverse-proxy.md` | Human-readable audit trail for the vhost change. Generated from `templates/nginx-reverse-proxy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/site-fullstack.conf` | Reference vhost — API prefix-strip, WebSocket, SPA, ratelimit. |
| `templates/proxy-params.conf` | Forwarded headers snippet — Host, X-Real-IP, X-Forwarded-Proto. |
| `templates/websocket.conf` | Upgrade headers snippet — requires `$connection_upgrade` map. |
| `templates/security-headers.conf` | HSTS + X-Content-Type-Options + Referrer-Policy. |
| `templates/rate-limiting.conf` | Per-zone limit_req declarations. |
| `templates/cloudflare-realip.conf` | Restore client IP from CF-Connecting-IP. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/nginx-reverse-proxy.json`

```json
{
  "artefact_id": "<vhost-slug>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "domain": "<example.com>",
  "backend_upstream": "127.0.0.1:<port>",
  "tls_mode": "cloudflare-origin",
  "websocket": false,
  "rate_limit_zone": "api_general",
  "security_headers": [
    "HSTS",
    "X-Content-Type-Options"
  ],
  "owner": "<@handle>"
}
```

### `templates/site-fullstack.conf`

```conf
# /etc/nginx/sites-available/DOMAIN.conf
# Full-stack app template: API prefix-strip, WebSocket, X-Accel-Redirect, SPA
# Replace: DOMAIN, BACKEND_API_PORT, FRONTEND_PORT, ATTACHMENT_DIR

server {
    listen 80;
    listen 443 ssl;
    server_name DOMAIN;

    # SSL (Cloudflare origin cert or Let's Encrypt)
    ssl_certificate     /etc/nginx/ssl/cloudflare-origin.pem;
    ssl_certificate_key /etc/nginx/ssl/cloudflare-origin-key.pem;
    include             snippets/ssl-params.conf;

    include snippets/security-headers.conf;
    client_max_body_size 10M;

    # API — strip /api prefix, proxy to backend
    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:BACKEND_API_PORT;
        limit_req zone=api_general burst=20 nodelay;
    }

    # Health check — no auth, no rate limit
    location /health {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:BACKEND_API_PORT;
    }

    # WebSocket
    location /ws {
        include snippets/proxy-params.conf;
        include snippets/websocket.conf;
        proxy_pass http://127.0.0.1:BACKEND_API_PORT;
    }

    # Internal file serving (X-Accel-Redirect from backend)
    location /internal-files/ {
        internal;
        alias ATTACHMENT_DIR;
    }

    # Frontend SPA
    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:FRONTEND_PORT;
    }
}
```

### `templates/proxy-params.conf`

```conf
# /etc/nginx/snippets/proxy-params.conf
# Reusable proxy headers for all reverse proxy locations
# Include with: include snippets/proxy-params.conf;

proxy_set_header Host              $host;
proxy_set_header X-Real-IP         $remote_addr;
proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto https;
proxy_set_header X-Forwarded-Host  $host;
proxy_set_header X-Forwarded-Port  $server_port;

proxy_connect_timeout 60s;
proxy_send_timeout    60s;
proxy_read_timeout    60s;

proxy_buffering         off;
proxy_request_buffering off;
```

### `templates/websocket.conf`

```conf
# /etc/nginx/snippets/websocket.conf
# WebSocket upgrade headers — include in WebSocket location blocks
# Requires the map block in http context (nginx.conf or conf.d/):
#   map $http_upgrade $connection_upgrade {
#       default upgrade;
#       ''      close;
#   }

proxy_http_version 1.1;
proxy_set_header Upgrade   $http_upgrade;
proxy_set_header Connection $connection_upgrade;

# Long timeout for persistent WebSocket connections (24 hours)
proxy_read_timeout 86400;
proxy_send_timeout 86400;
```

### `templates/security-headers.conf`

```conf
# /etc/nginx/snippets/security-headers.conf
# Security response headers — include in every server block
# Note: Set Content-Security-Policy per-site (app-specific sources)

add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
add_header X-Content-Type-Options    "nosniff"                             always;
add_header X-Frame-Options           "SAMEORIGIN"                          always;
add_header Referrer-Policy           "strict-origin-when-cross-origin"     always;
add_header Permissions-Policy        "camera=(), microphone=(), geolocation=()" always;
```

### `templates/rate-limiting.conf`

```conf
# /etc/nginx/conf.d/rate-limiting.conf
# Rate limiting zones — defined in http context
# Reference in server/location blocks: limit_req zone=api_general burst=20 nodelay;

# General API: 10 requests/second per IP
limit_req_zone $binary_remote_addr zone=api_general:10m rate=10r/s;

# Auth endpoints: 3 requests/minute per IP (anti-brute-force)
limit_req_zone $binary_remote_addr zone=api_auth:10m    rate=3r/m;

# File uploads: 5 requests/minute per IP
limit_req_zone $binary_remote_addr zone=api_upload:10m  rate=5r/m;

# Concurrent connection limit per IP
limit_conn_zone $binary_remote_addr zone=conn_per_ip:10m;

# Return 429 Too Many Requests
limit_req_status  429;
limit_conn_status 429;
```

### `templates/cloudflare-realip.conf`

```conf
# /etc/nginx/snippets/cloudflare-realip.conf
# Restore real client IP when behind Cloudflare proxy
# Include in http context or each server block
# Update Cloudflare IP ranges: https://www.cloudflare.com/ips/

# Cloudflare IPv4
set_real_ip_from 103.21.244.0/22;
set_real_ip_from 103.22.200.0/22;
set_real_ip_from 103.31.4.0/22;
set_real_ip_from 104.16.0.0/13;
set_real_ip_from 104.24.0.0/14;
set_real_ip_from 108.162.192.0/18;
set_real_ip_from 131.0.72.0/22;
set_real_ip_from 141.101.64.0/18;
set_real_ip_from 162.158.0.0/15;
set_real_ip_from 172.64.0.0/13;
set_real_ip_from 173.245.48.0/20;
set_real_ip_from 188.114.96.0/20;
set_real_ip_from 190.93.240.0/20;
set_real_ip_from 197.234.240.0/22;
set_real_ip_from 198.41.128.0/17;

# Cloudflare IPv6
set_real_ip_from 2400:cb00::/32;
set_real_ip_from 2606:4700::/32;
set_real_ip_from 2803:f800::/32;
set_real_ip_from 2405:b500::/32;
set_real_ip_from 2405:8100::/32;
set_real_ip_from 2a06:98c0::/29;
set_real_ip_from 2c0f:f248::/32;

# Use CF-Connecting-IP header (set by Cloudflare) for real client IP
real_ip_header CF-Connecting-IP;
```
