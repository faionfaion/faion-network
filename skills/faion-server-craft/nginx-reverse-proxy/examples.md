# nginx Reverse Proxy Examples

Real-world nginx configurations from the NERO server hosting multiple projects.

## Example 1: NERO Platform (nero.faion.net)

**Architecture:** Cloudflare -> nginx -> FastAPI (8100) + React SPA (8101)
**Features:** API proxy with prefix stripping, WebSocket, X-Accel-Redirect, CSP headers

### Current Config: `/etc/nginx/sites-enabled/nero.faion.net`

```nginx
# nero.faion.net — NERO AI Agent (Cloudflare proxied)

map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 80;
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/meetingtax.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/meetingtax.io/privkey.pem;
    listen [::]:80;
    server_name nero.faion.net;

    # Security headers
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://telegram.org; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' wss://nero.faion.net https://nero.faion.net; frame-ancestors https://web.telegram.org https://*.telegram.org;" always;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # API — strip /api prefix, proxy to nero-channel-web (:8100)
    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        proxy_pass http://127.0.0.1:8100;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }

    # Health (direct, no prefix)
    location /health {
        proxy_pass http://127.0.0.1:8100;
        proxy_set_header Host $host;
    }

    # WebSocket
    location /ws {
        proxy_pass http://127.0.0.1:8100;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }

    # Attachments — internal only, served via X-Accel-Redirect from FastAPI
    location /internal-attachments/ {
        internal;
        alias /srv/nero/attachments/;
    }

    # React SPA — nero-web (:8101)
    location / {
        proxy_pass http://127.0.0.1:8101;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

### Key Design Decisions

| Decision | Reason |
|----------|--------|
| `rewrite ^/api/(.*) /$1 break` | FastAPI routes don't have /api prefix |
| `proxy_read_timeout 86400` for /ws | WebSocket connections are long-lived (24h) |
| `internal` for /internal-attachments | Only FastAPI can trigger file serving |
| CSP includes telegram.org | NERO web app runs inside Telegram WebApp |
| Listens on both 80 and 443 | Cloudflare handles SSL, sends traffic to either |

## Example 2: MeetingTax (meetingtax.io)

**Architecture:** Cloudflare -> nginx -> Static landing + FastAPI (8000) + Next.js (3000)
**Features:** Multi-subdomain, static + dynamic content

```nginx
# meetingtax.io — Landing Page (Cloudflare proxied, SSL at CF)
server {
    listen 80;
    server_name meetingtax.io www.meetingtax.io;
    client_max_body_size 10M;

    root /var/www/meetingtax;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}

# app.meetingtax.io — Dashboard + API
server {
    listen 80;
    server_name app.meetingtax.io;
    client_max_body_size 10M;

    # API
    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }

    # API docs
    location /docs { proxy_pass http://127.0.0.1:8000; proxy_set_header Host $host; }
    location /openapi.json { proxy_pass http://127.0.0.1:8000; proxy_set_header Host $host; }
    location /redoc { proxy_pass http://127.0.0.1:8000; proxy_set_header Host $host; }

    # WebSocket
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Next.js frontend
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}

# api.meetingtax.io — API direct
server {
    listen 80;
    server_name api.meetingtax.io;
    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

## Example 3: EulaGuard (eulaguard.com)

**Architecture:** Cloudflare -> nginx -> Static pages + FastAPI (8001)

```nginx
# eulaguard.com — Landing + App (Cloudflare proxied)
server {
    listen 80;
    server_name eulaguard.com www.eulaguard.com;
    client_max_body_size 10M;

    root /var/www/eulaguard;
    index index.html;

    # API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }

    # Named app pages
    location = /app { try_files /app.html =404; }
    location = /login { try_files /login.html =404; }
    location = /register { try_files /register.html =404; }
    location = /privacy { try_files /privacy.html =404; }

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## Example 4: Adding a New Domain

### Steps to Add scanmecard.com

```bash
# 1. Create the site config
sudo tee /etc/nginx/sites-available/scanmecard.com << 'NGINX'
server {
    listen 80;
    server_name scanmecard.com www.scanmecard.com;

    include snippets/security-headers.conf;
    client_max_body_size 5M;

    root /var/www/scanmecard;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
NGINX

# 2. Enable the site
sudo ln -sf /etc/nginx/sites-available/scanmecard.com /etc/nginx/sites-enabled/

# 3. Test config
sudo nginx -t

# 4. Reload
sudo systemctl reload nginx

# 5. Verify
curl -I http://scanmecard.com
```

## Example 5: Troubleshooting Common Issues

### 502 Bad Gateway

```bash
# Check if backend is running
$ curl http://127.0.0.1:8100/health
curl: (7) Failed to connect to 127.0.0.1 port 8100: Connection refused

# Backend is down! Check service
$ systemctl --user status nero-channel-web
# Fix: restart the service
$ systemctl --user restart nero-channel-web
```

### WebSocket Connection Drops

```bash
# Check nginx error log
$ sudo tail -f /var/log/nginx/error.log
# "upstream timed out (110: Connection timed out)"

# Fix: increase proxy_read_timeout
# In /ws location:
proxy_read_timeout 86400;  # 24 hours
proxy_send_timeout 86400;
```

### 413 Request Entity Too Large

```bash
# Error: client intended to send too large body
# Fix: increase client_max_body_size
client_max_body_size 50M;  # or whatever you need
```

### Mixed Content Warnings

```bash
# Problem: HTTP resources loaded on HTTPS page
# Fix: ensure proxy_set_header X-Forwarded-Proto https
# Backend should use this to generate HTTPS URLs
```
