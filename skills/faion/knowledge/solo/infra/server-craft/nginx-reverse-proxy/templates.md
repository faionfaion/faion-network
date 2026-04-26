# nginx Reverse Proxy Templates

Copy-paste ready nginx configurations for common reverse proxy patterns.

## Template 1: Full-Stack Web App (API + WebSocket + SPA)

File: `/etc/nginx/sites-available/myapp.example.com`

```nginx
# myapp.example.com — Full-stack app (Cloudflare proxied)

server {
    listen 80;
    listen 443 ssl;
    server_name myapp.example.com;

    # SSL (use your certificate paths)
    ssl_certificate /etc/letsencrypt/live/myapp.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.example.com/privkey.pem;

    # Security headers
    include snippets/security-headers.conf;

    # Max upload size
    client_max_body_size 10M;

    # API — strip /api prefix, proxy to backend
    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8100;
        limit_req zone=api_general burst=20 nodelay;
    }

    # Health check (no prefix stripping)
    location /health {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8100;
    }

    # WebSocket
    location /ws {
        include snippets/proxy-params.conf;
        include snippets/websocket.conf;
        proxy_pass http://127.0.0.1:8100;
    }

    # Protected file serving (X-Accel-Redirect)
    location /internal-attachments/ {
        internal;
        alias /srv/myapp/attachments/;
    }

    # Frontend SPA
    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8101;
    }
}
```

## Template 2: Static Site + API Backend

```nginx
# example.com — Static landing page + API

server {
    listen 80;
    server_name example.com www.example.com;

    include snippets/security-headers.conf;
    client_max_body_size 10M;

    # API proxy
    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8000;
        limit_req zone=api_general burst=20 nodelay;
    }

    # API docs
    location /docs {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8000;
    }

    location /openapi.json {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8000;
    }

    # Static files
    root /var/www/example;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2|woff|ttf)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

## Template 3: Multi-Subdomain Setup

```nginx
# app.example.com — Dashboard (SPA + API)
server {
    listen 80;
    server_name app.example.com;

    include snippets/security-headers.conf;
    client_max_body_size 10M;

    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8000;
    }

    location /ws {
        include snippets/proxy-params.conf;
        include snippets/websocket.conf;
        proxy_pass http://127.0.0.1:8000;
    }

    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:3000;
    }
}

# api.example.com — API direct access
server {
    listen 80;
    server_name api.example.com;

    include snippets/security-headers.conf;
    client_max_body_size 10M;

    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:8000;
        limit_req zone=api_general burst=20 nodelay;
    }
}
```

## Template 4: Proxy Params Snippet

File: `/etc/nginx/snippets/proxy-params.conf`

```nginx
# /etc/nginx/snippets/proxy-params.conf
# Common proxy headers for all reverse proxy locations

proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto https;
proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-Port $server_port;

# Timeouts
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;

# Buffering
proxy_buffering off;
proxy_request_buffering off;
```

## Template 5: WebSocket Snippet

File: `/etc/nginx/snippets/websocket.conf`

```nginx
# /etc/nginx/snippets/websocket.conf
# WebSocket upgrade headers

proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection $connection_upgrade;

# Long timeout for WebSocket connections (24 hours)
proxy_read_timeout 86400;
proxy_send_timeout 86400;
```

## Template 6: Security Headers Snippet

File: `/etc/nginx/snippets/security-headers.conf`

```nginx
# /etc/nginx/snippets/security-headers.conf
# Security headers for all sites

# Prevent MIME type sniffing
add_header X-Content-Type-Options "nosniff" always;

# Force HTTPS (2 years, include subdomains)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;

# Control referrer information
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Prevent clickjacking
add_header X-Frame-Options "SAMEORIGIN" always;

# Disable dangerous browser features
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

# Note: Content-Security-Policy should be set per-site
# as each site has different resource requirements
```

## Template 7: Rate Limiting Configuration

File: `/etc/nginx/conf.d/rate-limiting.conf`

```nginx
# /etc/nginx/conf.d/rate-limiting.conf
# Rate limiting zones (define in http context)

# General API: 10 requests/second per IP
limit_req_zone $binary_remote_addr zone=api_general:10m rate=10r/s;

# Auth endpoints: 3 requests/minute per IP (anti-brute-force)
limit_req_zone $binary_remote_addr zone=api_auth:10m rate=3r/m;

# File uploads: 5 requests/minute per IP
limit_req_zone $binary_remote_addr zone=api_upload:10m rate=5r/m;

# Connection limiting: 50 concurrent connections per IP
limit_conn_zone $binary_remote_addr zone=conn_per_ip:10m;

# Custom 429 response
limit_req_status 429;
limit_conn_status 429;
```

## Template 8: Cloudflare Real IP Snippet

File: `/etc/nginx/snippets/cloudflare-realip.conf`

```nginx
# /etc/nginx/snippets/cloudflare-realip.conf
# Restore real client IP when behind Cloudflare
# Update periodically: https://www.cloudflare.com/ips/

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

# Use CF-Connecting-IP header for real client IP
real_ip_header CF-Connecting-IP;
```

## Template 9: nginx Audit Script

```bash
#!/bin/bash
# nginx-audit.sh — Audit nginx configuration

echo "=============================="
echo "  nginx Configuration Audit"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

echo ""
echo "--- Version ---"
nginx -v 2>&1

echo ""
echo "--- Config Test ---"
sudo nginx -t 2>&1

echo ""
echo "--- Active Sites ---"
ls -la /etc/nginx/sites-enabled/ 2>/dev/null

echo ""
echo "--- Listening ---"
sudo ss -tlnp | grep nginx

echo ""
echo "--- Snippets ---"
ls /etc/nginx/snippets/ 2>/dev/null

echo ""
echo "--- Worker Processes ---"
sudo nginx -T 2>/dev/null | grep worker_processes

echo ""
echo "--- Rate Limit Zones ---"
sudo nginx -T 2>/dev/null | grep limit_req_zone

echo ""
echo "--- Upstream Blocks ---"
sudo nginx -T 2>/dev/null | grep -A2 "^[[:space:]]*upstream"

echo ""
echo "--- Security Headers Check ---"
for site in $(ls /etc/nginx/sites-enabled/ 2>/dev/null); do
    echo "  $site:"
    echo -n "    HSTS: "
    grep -q "Strict-Transport-Security" /etc/nginx/sites-enabled/$site && echo "YES" || echo "NO"
    echo -n "    X-Content-Type: "
    grep -q "X-Content-Type-Options" /etc/nginx/sites-enabled/$site && echo "YES" || echo "NO"
    echo -n "    CSP: "
    grep -q "Content-Security-Policy" /etc/nginx/sites-enabled/$site && echo "YES" || echo "NO"
done

echo ""
echo "--- Recent Errors ---"
sudo tail -5 /var/log/nginx/error.log 2>/dev/null
```
