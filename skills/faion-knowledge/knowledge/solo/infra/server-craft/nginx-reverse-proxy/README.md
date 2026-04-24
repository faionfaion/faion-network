# nginx Reverse Proxy

Comprehensive nginx reverse proxy configuration methodology for multi-domain VPS servers. Covers proxy_pass, WebSocket upgrades, security headers, rate limiting, caching, upstream blocks, and the snippets pattern for reusable configuration.

## Scope

- Reverse proxy basics (proxy_pass, upstream)
- WebSocket upgrade handling
- Proxy headers (X-Real-IP, X-Forwarded-For, X-Forwarded-Proto)
- Upstream blocks and load balancing
- Security headers (CSP, HSTS, X-Content-Type-Options)
- Rate limiting (limit_req, limit_conn)
- Static file serving and caching
- Snippets pattern for DRY configuration
- Multi-domain setup on single server
- Cloudflare integration (real IP restoration)

## Why This Matters

nginx as a reverse proxy is the standard architecture for deploying web applications:

- **Single entry point** for all domains on the server
- **SSL termination** at the edge (or via Cloudflare)
- **WebSocket support** for real-time applications
- **Security headers** applied consistently across all sites
- **Rate limiting** to protect backend services
- **Static file serving** without hitting the application server

## Architecture

```
Internet -> Cloudflare (SSL, DDoS) -> nginx (port 80/443)
  -> /api/*   -> proxy_pass 127.0.0.1:8100 (FastAPI)
  -> /ws      -> proxy_pass 127.0.0.1:8100 (WebSocket)
  -> /        -> proxy_pass 127.0.0.1:8101 (React SPA)
```

### Configuration Structure

```
/etc/nginx/
  nginx.conf                    # Main config (worker_processes, events, http)
  mime.types                    # MIME type mappings
  conf.d/                      # Global config drops
  snippets/                    # Reusable config snippets
    proxy-params.conf          # Common proxy headers
    websocket.conf             # WebSocket upgrade headers
    security-headers.conf      # Security headers
    rate-limiting.conf         # Rate limiting zones
    cloudflare-realip.conf     # Cloudflare IP restoration
  sites-available/             # Site configs (all sites)
    nero.faion.net
    meetingtax.io
    eulaguard.com
  sites-enabled/               # Symlinks to active sites
    nero.faion.net -> ../sites-available/nero.faion.net
    meetingtax.io -> ../sites-available/meetingtax.io
    eulaguard.com -> ../sites-available/eulaguard.com
```

## Key Concepts

### 1. proxy_pass

The core directive for reverse proxying:

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8100/;  # Trailing / strips /api prefix
}
```

With trailing `/`: `/api/users` -> `http://127.0.0.1:8100/users`
Without trailing `/`: `/api/users` -> `http://127.0.0.1:8100/api/users`

### 2. WebSocket Upgrade

WebSocket connections require HTTP upgrade headers:

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

location /ws {
    proxy_pass http://127.0.0.1:8100;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $connection_upgrade;
    proxy_read_timeout 86400;    # 24 hours for long-lived WS
    proxy_send_timeout 86400;
}
```

### 3. Proxy Headers

Backend servers need to know the original client information:

| Header | Value | Purpose |
|--------|-------|---------|
| `Host` | `$host` | Original Host header |
| `X-Real-IP` | `$remote_addr` | Client's real IP |
| `X-Forwarded-For` | `$proxy_add_x_forwarded_for` | Chain of proxy IPs |
| `X-Forwarded-Proto` | `$scheme` or `https` | Original protocol |

### 4. Upstream Blocks

For load balancing or named backends:

```nginx
upstream nero_api {
    server 127.0.0.1:8100;
    # server 127.0.0.1:8102;  # Add more for load balancing
    keepalive 32;               # Connection pooling
}

location /api/ {
    proxy_pass http://nero_api;
}
```

### 5. Security Headers

Essential security headers for production:

```nginx
# Prevent MIME type sniffing
add_header X-Content-Type-Options "nosniff" always;

# Enable HSTS (force HTTPS for 2 years)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;

# Control referrer information
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Content Security Policy
add_header Content-Security-Policy "default-src 'self'; ..." always;

# Prevent clickjacking
add_header X-Frame-Options "SAMEORIGIN" always;
```

### 6. Rate Limiting

Protect backend services from abuse:

```nginx
# Define rate limiting zones (in http block)
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=3r/m;

# Apply to locations
location /api/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://127.0.0.1:8100;
}

location /api/auth/login {
    limit_req zone=login burst=5;
    proxy_pass http://127.0.0.1:8100;
}
```

### 7. Snippets Pattern

Reusable configuration fragments:

```nginx
# /etc/nginx/snippets/proxy-params.conf
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto https;

# Usage in site config:
location /api/ {
    include snippets/proxy-params.conf;
    proxy_pass http://127.0.0.1:8100;
}
```

### 8. Cloudflare Integration

When using Cloudflare as a proxy, nginx sees Cloudflare IPs instead of client IPs. Fix with:

```nginx
# /etc/nginx/snippets/cloudflare-realip.conf
set_real_ip_from 103.21.244.0/22;
set_real_ip_from 103.22.200.0/22;
# ... (all Cloudflare ranges)
real_ip_header CF-Connecting-IP;
```

### 9. X-Accel-Redirect (Internal Redirects)

Serve protected files through nginx without exposing the path:

```nginx
location /internal-attachments/ {
    internal;                       # Only accessible via X-Accel-Redirect
    alias /srv/nero/attachments/;
}
```

The backend sends `X-Accel-Redirect: /internal-attachments/file.pdf` and nginx serves the file.

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Missing trailing / in proxy_pass | URL prefix not stripped | Understand proxy_pass URI behavior |
| No WebSocket upgrade headers | WS connections fail | Use map + upgrade headers |
| Low proxy_read_timeout for WS | WebSocket disconnections | Set to 86400 for long-lived WS |
| Missing X-Real-IP with Cloudflare | Logs show Cloudflare IPs | Use set_real_ip_from + CF-Connecting-IP |
| add_header in location overrides server | Headers lost in nested blocks | Use `always` flag, repeat in location |
| Rate limiting on static files | Legitimate users blocked | Only rate-limit API endpoints |
| No error page for 502/503 | Ugly error when backend is down | Custom error pages |

## Verification Commands

```bash
# Test config syntax
sudo nginx -t

# Show effective config
sudo nginx -T

# Reload (graceful)
sudo nginx -s reload

# Check active connections
sudo nginx -T | grep worker_connections

# Test specific endpoint
curl -I http://localhost
curl -v http://localhost/api/health

# Check access logs
sudo tail -f /var/log/nginx/access.log

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Test WebSocket
websocat ws://localhost/ws
```

## Integration Points

| Component | Integration |
|-----------|------------|
| Cloudflare | Real IP restoration, SSL termination |
| certbot | SSL certificate management (if not using Cloudflare) |
| fail2ban | Monitor nginx access/error logs for banning |
| FastAPI | proxy_pass to uvicorn |
| React SPA | try_files for client-side routing |
| WebSocket | upgrade headers, long timeouts |
| Docker | proxy_pass to 127.0.0.1:port |

## References

- [nginx documentation](https://nginx.org/en/docs/)
- [nginx reverse proxy guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Mozilla SSL config generator](https://ssl-config.mozilla.org/)
- [SecurityHeaders.com](https://securityheaders.com/)
