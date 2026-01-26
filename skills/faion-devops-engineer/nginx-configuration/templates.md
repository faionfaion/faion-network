# Nginx Configuration Templates

Copy-paste templates for common configurations.

---

## SSL Parameters Snippet

```nginx
# /etc/nginx/snippets/ssl-params.conf

# Protocol - TLS 1.2 and 1.3 only
ssl_protocols TLSv1.2 TLSv1.3;

# Ciphers - Modern, secure ciphers
ssl_prefer_server_ciphers off;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;

# Session caching
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# DH parameters (generate with: openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048)
ssl_dhparam /etc/nginx/ssl/dhparam.pem;

# OCSP Stapling (evaluate based on your CA - Let's Encrypt deprecated OCSP in 2025)
# ssl_stapling on;
# ssl_stapling_verify on;
# resolver 1.1.1.1 8.8.8.8 valid=300s;
# resolver_timeout 5s;
```

---

## Security Headers Snippet

```nginx
# /etc/nginx/snippets/security-headers.conf

# HSTS - Force HTTPS (2 years, include subdomains, preload ready)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# Prevent MIME type sniffing
add_header X-Content-Type-Options "nosniff" always;

# Clickjacking protection
add_header X-Frame-Options "DENY" always;

# XSS protection (legacy, but still useful for older browsers)
add_header X-XSS-Protection "1; mode=block" always;

# Referrer policy
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Permissions policy (formerly Feature-Policy)
add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=(), accelerometer=()" always;

# Content Security Policy (customize per application)
# add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';" always;
```

---

## Proxy Parameters Snippet

```nginx
# /etc/nginx/snippets/proxy-params.conf

# HTTP version for keepalive
proxy_http_version 1.1;

# Headers to pass to upstream
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-Port $server_port;
proxy_set_header Connection "";

# Timeouts
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;

# Buffering
proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 16k;
proxy_busy_buffers_size 24k;

# Error handling - try next upstream on failure
proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
proxy_next_upstream_tries 3;
```

---

## Static Site Template

```nginx
# /etc/nginx/sites-available/DOMAIN.conf
# Replace: DOMAIN, /path/to/webroot

server {
    listen 80;
    listen [::]:80;
    server_name DOMAIN www.DOMAIN;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name DOMAIN www.DOMAIN;

    ssl_certificate /etc/letsencrypt/live/DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMAIN/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers.conf;

    root /path/to/webroot;
    index index.html;

    access_log /var/log/nginx/DOMAIN.access.log main;
    error_log /var/log/nginx/DOMAIN.error.log warn;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|webp|avif)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    location ~ /\. {
        deny all;
    }
}
```

---

## Reverse Proxy Template

```nginx
# /etc/nginx/sites-available/DOMAIN.conf
# Replace: DOMAIN, BACKEND_HOST, BACKEND_PORT

upstream DOMAIN_backend {
    server BACKEND_HOST:BACKEND_PORT;
    keepalive 32;
}

server {
    listen 80;
    listen [::]:80;
    server_name DOMAIN;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name DOMAIN;

    ssl_certificate /etc/letsencrypt/live/DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMAIN/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers.conf;

    access_log /var/log/nginx/DOMAIN.access.log main;
    error_log /var/log/nginx/DOMAIN.error.log warn;

    client_max_body_size 10M;

    location / {
        proxy_pass http://DOMAIN_backend;
        include /etc/nginx/snippets/proxy-params.conf;
    }

    location /health {
        proxy_pass http://DOMAIN_backend/health;
        access_log off;
    }
}
```

---

## WebSocket Proxy Template

```nginx
# Add to your server block
# Replace: BACKEND_HOST, BACKEND_PORT, /ws-path

location /ws-path {
    proxy_pass http://BACKEND_HOST:BACKEND_PORT;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 86400;
    proxy_send_timeout 86400;
}
```

---

## Load Balancer Template

```nginx
# /etc/nginx/conf.d/upstreams/APP_NAME.conf
# Replace: APP_NAME, server IPs

upstream APP_NAME_backend {
    least_conn;
    server 10.0.0.1:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.2:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.3:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.4:8080 backup;
    keepalive 64;
}
```

---

## Rate Limiting Template

```nginx
# In http block (nginx.conf)
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

# In server/location block
limit_req zone=general burst=20 nodelay;
limit_conn conn_limit 50;

# For login/auth endpoints
location /api/auth {
    limit_req zone=login burst=5 nodelay;
    proxy_pass http://backend;
}
```

---

## Caching Template

```nginx
# In http block (nginx.conf)
proxy_cache_path /var/cache/nginx/CACHE_NAME
    levels=1:2
    keys_zone=CACHE_NAME:10m
    max_size=1g
    inactive=60m
    use_temp_path=off;

# In location block
location /api/public {
    proxy_pass http://backend;

    proxy_cache CACHE_NAME;
    proxy_cache_key "$scheme$request_method$host$request_uri";
    proxy_cache_valid 200 10m;
    proxy_cache_valid 404 1m;

    proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
    proxy_cache_background_update on;
    proxy_cache_lock on;

    add_header X-Cache-Status $upstream_cache_status always;

    proxy_cache_bypass $http_authorization;
    proxy_no_cache $http_authorization;
}
```

---

## CORS Template

```nginx
# For API servers allowing cross-origin requests
# Replace: ALLOWED_ORIGIN

# Handle preflight OPTIONS requests
if ($request_method = 'OPTIONS') {
    add_header Access-Control-Allow-Origin "ALLOWED_ORIGIN";
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, PATCH, OPTIONS";
    add_header Access-Control-Allow-Headers "Authorization, Content-Type, Accept, Origin, X-Requested-With";
    add_header Access-Control-Max-Age 86400;
    add_header Content-Length 0;
    add_header Content-Type text/plain;
    return 204;
}

# Add CORS headers to all responses
add_header Access-Control-Allow-Origin "ALLOWED_ORIGIN" always;
add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, PATCH, OPTIONS" always;
add_header Access-Control-Allow-Headers "Authorization, Content-Type, Accept, Origin, X-Requested-With" always;
```

---

## Let's Encrypt Setup

```bash
# Install certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Obtain certificate (will auto-configure nginx)
sudo certbot --nginx -d example.com -d www.example.com

# Obtain certificate (standalone, manual nginx config)
sudo certbot certonly --standalone -d example.com -d www.example.com

# Test auto-renewal
sudo certbot renew --dry-run

# Cron for renewal (add to crontab)
0 0,12 * * * /usr/bin/certbot renew --quiet --post-hook "systemctl reload nginx"
```

---

## Generate DH Parameters

```bash
# Generate 2048-bit DH parameters (faster, still secure)
sudo openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048

# Generate 4096-bit DH parameters (more secure, slower generation)
sudo openssl dhparam -out /etc/nginx/ssl/dhparam.pem 4096
```

---

## Nginx Installation (Ubuntu/Debian)

```bash
# Install nginx
sudo apt update
sudo apt install nginx

# Create snippet directory
sudo mkdir -p /etc/nginx/snippets

# Create SSL directory
sudo mkdir -p /etc/nginx/ssl

# Create cache directory
sudo mkdir -p /var/cache/nginx

# Set permissions
sudo chown www-data:www-data /var/cache/nginx

# Test configuration
sudo nginx -t

# Enable and start
sudo systemctl enable nginx
sudo systemctl start nginx
```
