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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[load-balancing-concepts]]
- [[ssl-tls-setup]]
- [[security-policy-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it whenever you have to defend the directive set for a new server block in a security review.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/nginx.conf`

```conf
user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 4096;
    multi_accept on;
    use epoll;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript image/svg+xml;

    # Rate limit zones
    limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/s;
    limit_req_zone $binary_remote_addr zone=api:10m rate=20r/s;

    # Global TLS settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### `templates/security-headers.conf`

```conf
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'" always;
```

### `templates/site-reverse-proxy.conf`

```conf
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    include /etc/nginx/snippets/security-headers.conf;

    # Auth rate-limit
    location /api/auth/ {
        limit_req zone=auth burst=10 nodelay;
        proxy_pass http://backend;
        include /etc/nginx/snippets/proxy-params.conf;
    }

    location / {
        proxy_pass http://backend;
        include /etc/nginx/snippets/proxy-params.conf;

        # WebSocket upgrade
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### `templates/_smoke-test.json`

```json
{
  "domain": "example.com",
  "upstream": "backend:8000",
  "tls": {
    "protocols": [
      "TLSv1.2",
      "TLSv1.3"
    ],
    "hsts_max_age": 63072000,
    "ocsp_stapling": true
  },
  "headers": [
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Content-Security-Policy"
  ],
  "rate_limit_zones": [
    "auth=5r/s",
    "api=20r/s"
  ],
  "http2": true,
  "websocket_upgrade": true
}
```
