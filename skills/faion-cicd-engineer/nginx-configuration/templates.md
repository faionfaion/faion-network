# Nginx Configuration Templates

Copy-paste templates for common configurations.

---

## Main Configuration (nginx.conf)

```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
worker_rlimit_nofile 65535;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log warn;

include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    # Basic Settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    # MIME Types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging Format - Standard
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    # Logging Format - JSON
    log_format json escape=json '{'
        '"time":"$time_iso8601",'
        '"remote_addr":"$remote_addr",'
        '"request_method":"$request_method",'
        '"request_uri":"$request_uri",'
        '"status":$status,'
        '"body_bytes_sent":$body_bytes_sent,'
        '"request_time":$request_time,'
        '"upstream_response_time":"$upstream_response_time",'
        '"http_referrer":"$http_referer",'
        '"http_user_agent":"$http_user_agent"'
    '}';

    access_log /var/log/nginx/access.log main;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 256;
    gzip_types
        application/atom+xml
        application/javascript
        application/json
        application/rss+xml
        application/vnd.ms-fontobject
        application/x-font-ttf
        application/x-web-app-manifest+json
        application/xhtml+xml
        application/xml
        font/opentype
        image/svg+xml
        image/x-icon
        text/css
        text/plain
        text/x-component;

    # SSL Settings (Global)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # Rate Limiting Zones
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    limit_conn_zone $binary_remote_addr zone=addr:10m;

    # WebSocket Upgrade Map
    map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
    }

    # Cache Paths
    proxy_cache_path /var/cache/nginx/api
        levels=1:2
        keys_zone=api_cache:10m
        max_size=1g
        inactive=60m
        use_temp_path=off;

    proxy_cache_path /var/cache/nginx/static
        levels=1:2
        keys_zone=static_cache:10m
        max_size=5g
        inactive=7d
        use_temp_path=off;

    # Upstreams
    include /etc/nginx/conf.d/upstreams/*.conf;

    # Virtual Hosts
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

---

## SSL Parameters Snippet

```nginx
# /etc/nginx/snippets/ssl-params.conf

ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;

ssl_session_cache shared:SSL:10m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 1.1.1.1 valid=300s;
resolver_timeout 5s;

# DH Parameters (generate with: openssl dhparam -out /etc/nginx/ssl/dhparam.pem 4096)
ssl_dhparam /etc/nginx/ssl/dhparam.pem;
```

---

## Security Headers Snippet

```nginx
# /etc/nginx/snippets/security-headers.conf

# HSTS (1 year, include subdomains, preload)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# Content Security Policy (adjust based on your needs)
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https:; frame-ancestors 'none'; base-uri 'self'; form-action 'self';" always;

# XSS Protection
add_header X-XSS-Protection "1; mode=block" always;

# Content Type Options
add_header X-Content-Type-Options "nosniff" always;

# Frame Options
add_header X-Frame-Options "DENY" always;

# Referrer Policy
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Permissions Policy
add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=(), usb=()" always;
```

---

## Security Headers (Relaxed for API)

```nginx
# /etc/nginx/snippets/security-headers-api.conf

add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

---

## Proxy Parameters Snippet

```nginx
# /etc/nginx/snippets/proxy-params.conf

proxy_http_version 1.1;
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

# Error handling
proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
proxy_next_upstream_tries 3;
```

---

## WebSocket Proxy Parameters

```nginx
# /etc/nginx/snippets/websocket-params.conf

proxy_http_version 1.1;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection $connection_upgrade;

# Extended timeouts for long-running connections
proxy_read_timeout 86400s;
proxy_send_timeout 86400s;

# Disable buffering for real-time
proxy_buffering off;
```

---

## Static Site Template

```nginx
# /etc/nginx/sites-available/DOMAIN.conf

server {
    listen 80;
    listen [::]:80;
    server_name DOMAIN www.DOMAIN;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name DOMAIN www.DOMAIN;

    ssl_certificate /etc/letsencrypt/live/DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMAIN/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers.conf;

    root /var/www/DOMAIN/public;
    index index.html;

    access_log /var/log/nginx/DOMAIN.access.log main;
    error_log /var/log/nginx/DOMAIN.error.log warn;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

---

## Reverse Proxy Template

```nginx
# /etc/nginx/sites-available/api.DOMAIN.conf

upstream UPSTREAM_NAME {
    least_conn;
    server 127.0.0.1:PORT weight=5 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

server {
    listen 80;
    listen [::]:80;
    server_name api.DOMAIN;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.DOMAIN;

    ssl_certificate /etc/letsencrypt/live/DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMAIN/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers-api.conf;

    access_log /var/log/nginx/api.DOMAIN.access.log json;
    error_log /var/log/nginx/api.DOMAIN.error.log warn;

    limit_req zone=api burst=50 nodelay;

    location / {
        proxy_pass http://UPSTREAM_NAME;
        include /etc/nginx/snippets/proxy-params.conf;
    }

    location /health {
        proxy_pass http://UPSTREAM_NAME/health;
        access_log off;
    }
}
```

---

## Upstream Definition Template

```nginx
# /etc/nginx/conf.d/upstreams/backend.conf

upstream backend_app {
    # Load balancing method (choose one)
    # least_conn;    # Least connections
    # ip_hash;       # Sticky sessions
    # random;        # Random selection

    # Servers
    server 127.0.0.1:8000 weight=5 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8001 weight=5 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8002 backup;

    # Keepalive connections
    keepalive 32;
}
```

---

## Cache Configuration Template

```nginx
# Add to location block

# Enable caching
proxy_cache CACHE_ZONE_NAME;
proxy_cache_key "$scheme$request_method$host$request_uri";
proxy_cache_valid 200 10m;
proxy_cache_valid 301 302 1m;
proxy_cache_valid 404 1m;

# Serve stale on errors
proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
proxy_cache_background_update on;
proxy_cache_lock on;
proxy_cache_revalidate on;

# Cache status header
add_header X-Cache-Status $upstream_cache_status;

# Bypass cache
proxy_cache_bypass $http_cache_control $http_authorization;
proxy_no_cache $http_pragma $http_authorization;
```

---

## Rate Limiting Template

```nginx
# Define in http block
limit_req_zone $binary_remote_addr zone=ZONE_NAME:10m rate=RATE;
limit_conn_zone $binary_remote_addr zone=CONN_ZONE:10m;

# Use in server/location block
limit_req zone=ZONE_NAME burst=BURST nodelay;
limit_conn CONN_ZONE MAX_CONN;

# Custom error pages
limit_req_status 429;
limit_conn_status 429;
```

---

## Let's Encrypt Renewal Hook

```bash
#!/bin/bash
# /etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh

nginx -t && systemctl reload nginx
```

---

## Logrotate Configuration

```
# /etc/logrotate.d/nginx

/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```
