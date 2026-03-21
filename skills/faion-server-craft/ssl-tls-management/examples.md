# SSL/TLS Management Examples

## Example 1: NERO Platform -- Cloudflare Full(Strict) with Origin Certificate

The NERO AI platform runs at `nero.faion.net` behind Cloudflare with a 15-year origin certificate. This eliminates certificate renewal entirely.

### Architecture

```
Browser
  -> Cloudflare Edge (TLS 1.3, Cloudflare's cert)
    -> Origin Server (TLS 1.2/1.3, Cloudflare origin cert)
      -> nginx (127.0.0.1:8100 API, 127.0.0.1:8101 SPA)
```

### Cloudflare Settings

```
SSL/TLS Mode: Full (Strict)
Always Use HTTPS: On
Minimum TLS Version: 1.2
TLS 1.3: On
Automatic HTTPS Rewrites: On
HSTS:
  Status: On
  Max-Age: 6 months
  Include subdomains: On
  No-Sniff: On
```

### Origin Certificate Setup

```bash
# 1. Generated in Cloudflare Dashboard:
#    - Hostnames: faion.net, *.faion.net
#    - Validity: 15 years
#    - Key type: RSA 2048

# 2. Saved to server:
sudo mkdir -p /etc/nginx/ssl
sudo nano /etc/nginx/ssl/cloudflare-origin.pem      # paste cert
sudo nano /etc/nginx/ssl/cloudflare-origin-key.pem   # paste key
sudo chmod 600 /etc/nginx/ssl/cloudflare-origin-key.pem
```

### nginx Configuration

```nginx
# /etc/nginx/snippets/ssl-params.conf
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;

add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# /etc/nginx/sites-available/nero.faion.net
server {
    listen 80;
    server_name nero.faion.net;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name nero.faion.net;

    ssl_certificate /etc/nginx/ssl/cloudflare-origin.pem;
    ssl_certificate_key /etc/nginx/ssl/cloudflare-origin-key.pem;
    include snippets/ssl-params.conf;

    # React SPA
    location / {
        proxy_pass http://127.0.0.1:8101;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API
    location /api/ {
        proxy_pass http://127.0.0.1:8100;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket
    location /ws {
        proxy_pass http://127.0.0.1:8100;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400s;
    }
}
```

### Verification

```bash
# From external machine (through Cloudflare):
curl -vI https://nero.faion.net 2>&1 | grep -E "(TLS|subject|issuer)"
# TLS 1.3, issuer: Cloudflare Inc ECC CA-3

# From the server directly (origin cert):
echo | openssl s_client -connect 127.0.0.1:443 -servername nero.faion.net 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
# issuer: Cloudflare Inc, notAfter: 15 years from creation
```

---

## Example 2: Let's Encrypt for Direct-Exposed Server

A personal project at `app.example.com` without Cloudflare, using Let's Encrypt with auto-renewal.

### Initial Setup

```bash
# Install certbot
sudo apt update && sudo apt install -y certbot python3-certbot-nginx

# Generate DH parameters
sudo openssl dhparam -out /etc/nginx/dhparam.pem 2048

# Get certificate (nginx plugin auto-configures)
sudo certbot --nginx \
  -d app.example.com \
  --non-interactive \
  --agree-tos \
  --email admin@example.com \
  --redirect
```

### Manual nginx Config (if not using certbot nginx plugin)

```nginx
# /etc/nginx/sites-available/app.example.com
server {
    listen 80;
    server_name app.example.com;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name app.example.com;

    ssl_certificate /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;
    include snippets/ssl-params.conf;

    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/app.example.com/chain.pem;
    resolver 1.1.1.1 8.8.8.8 valid=300s;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Renewal Setup

```bash
# Create post-renewal hook
sudo mkdir -p /etc/letsencrypt/renewal-hooks/post
sudo tee /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh << 'EOF'
#!/bin/bash
nginx -t && systemctl reload nginx
echo "$(date) nginx reloaded after cert renewal" >> /var/log/certbot-renewal.log
EOF
sudo chmod +x /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh

# Test renewal
sudo certbot renew --dry-run

# Verify timer is active
systemctl list-timers | grep certbot
# certbot.timer  loaded active waiting  twice daily certbot renewal
```

---

## Example 3: Dual SSL Setup (Let's Encrypt + Cloudflare)

For a multi-domain server where some domains use Cloudflare and others don't.

### Scenario

| Domain | CDN | Certificate | Mode |
|--------|-----|-------------|------|
| `app.faion.net` | Cloudflare | Origin cert | Full (Strict) |
| `meetingtax.io` | Cloudflare | Origin cert | Full (Strict) |
| `staging.example.com` | None | Let's Encrypt | Direct |

### nginx Configuration

```nginx
# Shared SSL params for all sites
# /etc/nginx/snippets/ssl-params.conf
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;

# Site 1: Cloudflare origin cert (shared wildcard)
# /etc/nginx/sites-available/app.faion.net
server {
    listen 443 ssl http2;
    server_name app.faion.net;
    ssl_certificate /etc/nginx/ssl/cloudflare-origin.pem;       # *.faion.net
    ssl_certificate_key /etc/nginx/ssl/cloudflare-origin-key.pem;
    include snippets/ssl-params.conf;
    # ... app config
}

# Site 2: Separate Cloudflare origin cert
# /etc/nginx/sites-available/meetingtax.io
server {
    listen 443 ssl http2;
    server_name meetingtax.io www.meetingtax.io;
    ssl_certificate /etc/nginx/ssl/meetingtax-origin.pem;
    ssl_certificate_key /etc/nginx/ssl/meetingtax-origin-key.pem;
    include snippets/ssl-params.conf;
    # ... app config
}

# Site 3: Let's Encrypt (no Cloudflare)
# /etc/nginx/sites-available/staging.example.com
server {
    listen 443 ssl http2;
    server_name staging.example.com;
    ssl_certificate /etc/letsencrypt/live/staging.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/staging.example.com/privkey.pem;
    include snippets/ssl-params.conf;
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/staging.example.com/chain.pem;
    resolver 1.1.1.1 8.8.8.8 valid=300s;
    # ... app config
}
```

---

## Example 4: Auto-Renewal Monitoring Cron

Monitor certificate expiry and send alerts.

```bash
#!/bin/bash
# /usr/local/bin/check-certs.sh
# Check certificate expiry and alert via Telegram

set -euo pipefail

BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
CHAT_ID="${TELEGRAM_CHAT_ID}"
WARN_DAYS=14

send_alert() {
    local msg="$1"
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d text="$msg" \
        -d parse_mode="Markdown" > /dev/null
}

check_cert() {
    local domain="$1"
    local expiry
    expiry=$(echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null \
        | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)

    [ -z "$expiry" ] && { send_alert "SSL FAIL: Cannot connect to $domain"; return; }

    local days_left=$(( ($(date -d "$expiry" +%s) - $(date +%s)) / 86400 ))

    if [ "$days_left" -lt "$WARN_DAYS" ]; then
        send_alert "SSL WARNING: *$domain* expires in *$days_left days* ($expiry)"
    fi
}

check_cert "nero.faion.net"
check_cert "meetingtax.io"
```

```cron
# Check cert expiry daily at 9:00
0 9 * * * /usr/local/bin/check-certs.sh
```
