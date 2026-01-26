# Nginx Configuration Examples

## Example 1: Static Site with HTTPS

Basic static website with HTTPS redirect and security headers.

```nginx
# /etc/nginx/sites-available/example.com

server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
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

    # Main location
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Static assets with long cache
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Deny hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

---

## Example 2: API Reverse Proxy with Load Balancing

Backend API with load balancing, rate limiting, and caching.

```nginx
# /etc/nginx/sites-available/api.example.com

# Upstream definition with health checks
upstream api_backend {
    least_conn;

    server 127.0.0.1:8000 weight=5 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8001 weight=5 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8002 backup;

    keepalive 32;
}

# Cache zone (define in http block of nginx.conf)
# proxy_cache_path /var/cache/nginx/api
#     levels=1:2
#     keys_zone=api_cache:10m
#     max_size=1g
#     inactive=60m
#     use_temp_path=off;

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.example.com;

    # SSL
    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    # Security Headers (relaxed CSP for API)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;

    # Logging (JSON format)
    access_log /var/log/nginx/api.example.com.access.log json;
    error_log /var/log/nginx/api.example.com.error.log warn;

    # Rate Limiting
    limit_req zone=api burst=50 nodelay;
    limit_conn addr 100;

    # API endpoints
    location / {
        proxy_pass http://api_backend;
        include /etc/nginx/snippets/proxy-params.conf;

        # Caching for GET requests
        proxy_cache api_cache;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        proxy_cache_valid 200 5m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_background_update on;
        proxy_cache_lock on;

        # Cache status header
        add_header X-Cache-Status $upstream_cache_status;

        # Bypass cache for authenticated requests
        proxy_cache_bypass $http_authorization;
        proxy_no_cache $http_authorization;
    }

    # Health check (no caching, no logging)
    location /health {
        proxy_pass http://api_backend/health;
        access_log off;
        proxy_cache off;
    }

    # Metrics endpoint (restricted)
    location /metrics {
        allow 10.0.0.0/8;
        allow 127.0.0.1;
        deny all;
        proxy_pass http://api_backend/metrics;
        access_log off;
    }
}
```

---

## Example 3: WebSocket Proxy

Real-time application with WebSocket support.

```nginx
# /etc/nginx/sites-available/realtime.example.com

# WebSocket connection upgrade map (define in http block)
# map $http_upgrade $connection_upgrade {
#     default upgrade;
#     '' close;
# }

upstream ws_backend {
    server 127.0.0.1:3000;
    keepalive 32;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name realtime.example.com;

    ssl_certificate /etc/letsencrypt/live/realtime.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/realtime.example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers.conf;

    # Regular HTTP endpoints
    location / {
        proxy_pass http://ws_backend;
        include /etc/nginx/snippets/proxy-params.conf;
    }

    # WebSocket endpoint
    location /ws {
        proxy_pass http://ws_backend;
        proxy_http_version 1.1;

        # WebSocket headers
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        # Standard headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Extended timeouts for long-running connections
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;

        # Disable buffering for real-time
        proxy_buffering off;
    }

    # Socket.IO specific (if using)
    location /socket.io/ {
        proxy_pass http://ws_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400s;
        proxy_buffering off;
    }
}
```

---

## Example 4: Next.js Application

Next.js with SSR, static assets, and API routes.

```nginx
# /etc/nginx/sites-available/app.example.com

upstream nextjs_backend {
    server 127.0.0.1:3000;
    keepalive 32;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name app.example.com;

    ssl_certificate /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers.conf;

    access_log /var/log/nginx/app.example.com.access.log main;
    error_log /var/log/nginx/app.example.com.error.log warn;

    # Next.js static files (immutable)
    location /_next/static/ {
        proxy_pass http://nextjs_backend;
        proxy_cache_valid 200 365d;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # Next.js image optimization
    location /_next/image {
        proxy_pass http://nextjs_backend;
        proxy_cache_valid 200 60m;
    }

    # Public static assets
    location /static/ {
        alias /var/www/app.example.com/public/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # API routes (no caching)
    location /api/ {
        proxy_pass http://nextjs_backend;
        include /etc/nginx/snippets/proxy-params.conf;
        proxy_cache off;
    }

    # All other routes (SSR)
    location / {
        proxy_pass http://nextjs_backend;
        include /etc/nginx/snippets/proxy-params.conf;

        # Short cache for SSR pages
        proxy_cache_valid 200 1m;
        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

---

## Example 5: Multi-Domain with Shared Config

Multiple sites sharing common configuration.

```nginx
# /etc/nginx/sites-available/multi-site

# Site 1: Main website
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers.conf;

    root /var/www/example.com/public;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}

# Site 2: Blog subdomain
server {
    listen 443 ssl http2;
    server_name blog.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;
    include /etc/nginx/snippets/security-headers.conf;

    root /var/www/blog.example.com/public;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

# Site 3: API subdomain
server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    location / {
        proxy_pass http://127.0.0.1:8000;
        include /etc/nginx/snippets/proxy-params.conf;
    }
}

# Catch-all redirect to main site
server {
    listen 443 ssl http2 default_server;
    server_name _;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    return 301 https://example.com$request_uri;
}
```

---

## Example 6: Monitoring Endpoint

Prometheus-compatible monitoring setup.

```nginx
# Add to any server block

# Nginx stub status (for nginx-prometheus-exporter)
location /nginx_status {
    stub_status on;
    allow 127.0.0.1;
    allow 10.0.0.0/8;
    deny all;
    access_log off;
}

# Custom metrics location
location /metrics {
    # If using nginx-lua or VTS module
    # vhost_traffic_status_display;
    # vhost_traffic_status_display_format html;

    allow 127.0.0.1;
    allow 10.0.0.0/8;
    deny all;
    access_log off;
}

# Health check for load balancers
location /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}

# Ready check (for Kubernetes)
location /ready {
    access_log off;
    return 200 "ready\n";
    add_header Content-Type text/plain;
}
```

---

## Example 7: Docker/Container Environment

Configuration for containerized deployments.

```nginx
# /etc/nginx/nginx.conf (container version)

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # JSON logging for container environments
    log_format json escape=json '{'
        '"time":"$time_iso8601",'
        '"remote_addr":"$remote_addr",'
        '"request_method":"$request_method",'
        '"request_uri":"$request_uri",'
        '"status":$status,'
        '"body_bytes_sent":$body_bytes_sent,'
        '"request_time":$request_time,'
        '"upstream_response_time":"$upstream_response_time",'
        '"http_user_agent":"$http_user_agent"'
    '}';

    access_log /var/log/nginx/access.log json;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    server_tokens off;

    # Use environment variables (via envsubst)
    upstream backend {
        server ${BACKEND_HOST}:${BACKEND_PORT};
        keepalive 32;
    }

    server {
        listen 80;
        server_name _;

        location /health {
            access_log off;
            return 200 "OK";
        }

        location / {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Connection "";
        }
    }
}
```

Docker entrypoint script:
```bash
#!/bin/sh
# Substitute environment variables
envsubst '${BACKEND_HOST} ${BACKEND_PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
# Start nginx
nginx -g 'daemon off;'
```
