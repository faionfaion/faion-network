# Nginx Configuration Examples

## Example 1: Main Configuration (nginx.conf)

Optimized main configuration for high-performance servers.

```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log warn;

# Load modules
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

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    log_format json escape=json '{'
        '"time": "$time_iso8601",'
        '"remote_addr": "$remote_addr",'
        '"request_method": "$request_method",'
        '"request_uri": "$request_uri",'
        '"status": $status,'
        '"body_bytes_sent": $body_bytes_sent,'
        '"request_time": $request_time,'
        '"upstream_response_time": "$upstream_response_time",'
        '"http_referrer": "$http_referer",'
        '"http_user_agent": "$http_user_agent"'
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
    ssl_prefer_server_ciphers off;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # Rate Limiting Zones
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    limit_conn_zone $binary_remote_addr zone=addr:10m;

    # Upstream Backends
    include /etc/nginx/conf.d/upstreams/*.conf;

    # Virtual Hosts
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

---

## Example 2: Static Site with SSL

Next.js or React static export deployment.

```nginx
# /etc/nginx/sites-available/example.com

# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com www.example.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    # Security Headers
    include /etc/nginx/snippets/security-headers.conf;

    # Root Directory
    root /var/www/example.com/public;
    index index.html;

    # Logging
    access_log /var/log/nginx/example.com.access.log main;
    error_log /var/log/nginx/example.com.error.log warn;

    # Rate Limiting
    limit_req zone=general burst=20 nodelay;

    # Main location - SPA support
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Static Assets - Long cache
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|webp|avif)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Next.js specific
    location /_next/static/ {
        alias /var/www/example.com/public/_next/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Deny access to sensitive files
    location ~* (\.env|\.git|\.htaccess|\.htpasswd|\.DS_Store)$ {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

---

## Example 3: Reverse Proxy for API

Backend API service behind Nginx.

```nginx
# /etc/nginx/sites-available/api.example.com

# Upstream definition
upstream api_backend {
    least_conn;
    server 127.0.0.1:8000 weight=5;
    server 127.0.0.1:8001 weight=5;
    server 127.0.0.1:8002 backup;
    keepalive 32;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name api.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.example.com;

    # SSL
    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    # Security Headers (API-specific - no CSP frame-ancestors)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;

    # CORS (if needed)
    add_header Access-Control-Allow-Origin "https://example.com" always;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Authorization, Content-Type" always;

    # Logging (JSON format for parsing)
    access_log /var/log/nginx/api.example.com.access.log json;
    error_log /var/log/nginx/api.example.com.error.log warn;

    # Rate Limiting
    limit_req zone=api burst=50 nodelay;
    limit_conn addr 100;

    # Client body size (for uploads)
    client_max_body_size 10M;

    # Proxy Settings
    location / {
        proxy_pass http://api_backend;
        include /etc/nginx/snippets/proxy-params.conf;
    }

    # Health Check Endpoint (no rate limit)
    location /health {
        proxy_pass http://api_backend/health;
        access_log off;
        limit_req off;
    }

    # WebSocket Support
    location /ws {
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;
    }

    # Handle OPTIONS for CORS preflight
    location @cors_preflight {
        add_header Access-Control-Allow-Origin "https://example.com";
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
        add_header Access-Control-Allow-Headers "Authorization, Content-Type";
        add_header Access-Control-Max-Age 86400;
        add_header Content-Length 0;
        add_header Content-Type text/plain;
        return 204;
    }
}
```

---

## Example 4: Load Balancing with Health Checks

Multiple backend servers with failover.

```nginx
# /etc/nginx/conf.d/upstreams/app.conf

# Round Robin (default)
upstream app_backend_rr {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080;
    keepalive 32;
}

# Least Connections - best for varied request times
upstream app_backend_lc {
    least_conn;
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080;
    keepalive 32;
}

# IP Hash - sticky sessions
upstream app_backend_sticky {
    ip_hash;
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080;
    keepalive 32;
}

# Weighted distribution with failover
upstream app_backend_weighted {
    server 10.0.0.1:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.2:8080 weight=3 max_fails=3 fail_timeout=30s;
    server 10.0.0.3:8080 weight=2 max_fails=3 fail_timeout=30s;
    server 10.0.0.4:8080 backup;  # Only used when others fail
    keepalive 32;
}
```

---

## Example 5: Caching Proxy

Cache backend responses for improved performance.

```nginx
# Cache zone definition (in http block of nginx.conf)
proxy_cache_path /var/cache/nginx/api
    levels=1:2
    keys_zone=api_cache:10m
    max_size=1g
    inactive=60m
    use_temp_path=off;

# In server block
location /api/public {
    proxy_pass http://api_backend;
    include /etc/nginx/snippets/proxy-params.conf;

    # Enable caching
    proxy_cache api_cache;
    proxy_cache_key "$scheme$request_method$host$request_uri";
    proxy_cache_valid 200 10m;
    proxy_cache_valid 404 1m;
    proxy_cache_valid any 5m;

    # Serve stale content on errors
    proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
    proxy_cache_background_update on;
    proxy_cache_lock on;

    # Cache headers for debugging
    add_header X-Cache-Status $upstream_cache_status always;

    # Bypass cache for authenticated requests
    proxy_cache_bypass $http_authorization $cookie_session;
    proxy_no_cache $http_authorization $cookie_session;
}

# No cache for authenticated endpoints
location /api/private {
    proxy_pass http://api_backend;
    include /etc/nginx/snippets/proxy-params.conf;
    proxy_cache off;
}
```

---

## Example 6: PHP-FPM (Laravel/WordPress)

```nginx
# /etc/nginx/sites-available/laravel.example.com

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name laravel.example.com;

    ssl_certificate /etc/letsencrypt/live/laravel.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/laravel.example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers.conf;

    root /var/www/laravel/public;
    index index.php index.html;

    access_log /var/log/nginx/laravel.access.log main;
    error_log /var/log/nginx/laravel.error.log warn;

    # Laravel URL rewriting
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # PHP-FPM
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_hide_header X-Powered-By;
    }

    # Static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Deny access to sensitive files
    location ~ /\.(?!well-known).* {
        deny all;
    }

    location ~ ^/(\.env|composer\.json|composer\.lock|package\.json)$ {
        deny all;
    }
}
```

---

## Example 7: Monitoring Endpoint

```nginx
# /etc/nginx/conf.d/monitoring.conf

server {
    listen 8080;
    server_name localhost;

    # Nginx status for Prometheus exporter
    location /nginx_status {
        stub_status on;
        allow 127.0.0.1;
        allow 10.0.0.0/8;
        allow 172.16.0.0/12;
        deny all;
    }

    # Health check for load balancers
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }

    # Readiness check
    location /ready {
        access_log off;
        return 200 "READY\n";
        add_header Content-Type text/plain;
    }
}
```

---

## Example 8: Docker/Container Deployment

```nginx
# /etc/nginx/sites-available/docker-app

upstream docker_app {
    server app:3000;  # Docker service name
    keepalive 32;
}

server {
    listen 80;
    server_name _;

    # For development/internal use
    location / {
        proxy_pass http://docker_app;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection "";
    }

    # Health check
    location /health {
        access_log off;
        proxy_pass http://docker_app/health;
    }
}
```
