# SSL/TLS Management Templates

## nginx SSL Snippet

Shared SSL parameters included in all HTTPS server blocks.

```nginx
# /etc/nginx/snippets/ssl-params.conf
# SSL/TLS hardened configuration
# Generated: $(date +%Y-%m-%d)

# Protocols: TLS 1.2 + 1.3 only
ssl_protocols TLSv1.2 TLSv1.3;

# Ciphers: AEAD ciphers only, ECDHE key exchange
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;

# Let client choose cipher (important for TLS 1.3)
ssl_prefer_server_ciphers off;

# Session settings
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;  # ~40k sessions
ssl_session_tickets off;           # Forward secrecy

# DH parameters (for TLS 1.2 DHE ciphers)
ssl_dhparam /etc/nginx/dhparam.pem;

# HSTS (2 years, includeSubDomains)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;

# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
```

## nginx Server Block: Let's Encrypt

```nginx
# /etc/nginx/sites-available/example.com
# HTTPS with Let's Encrypt certificate

# HTTP -> HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    # Allow ACME challenge for certbot renewal
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com www.example.com;

    # Let's Encrypt certificate
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Shared SSL parameters
    include snippets/ssl-params.conf;

    # OCSP Stapling (works with Let's Encrypt)
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
    resolver 1.1.1.1 8.8.8.8 valid=300s;
    resolver_timeout 5s;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## nginx Server Block: Cloudflare Origin Certificate

```nginx
# /etc/nginx/sites-available/example.com
# HTTPS with Cloudflare origin certificate
# Requires: Cloudflare SSL mode = Full (Strict)

# HTTP -> HTTPS redirect (Cloudflare handles this, but belt-and-suspenders)
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com www.example.com;

    # Cloudflare origin certificate (15-year validity)
    ssl_certificate /etc/nginx/ssl/cloudflare-origin.pem;
    ssl_certificate_key /etc/nginx/ssl/cloudflare-origin-key.pem;

    # Shared SSL parameters
    include snippets/ssl-params.conf;

    # NO OCSP stapling (Cloudflare origin certs don't support it)
    # ssl_stapling off;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## nginx Server Block: Reverse Proxy with SSL

```nginx
# /etc/nginx/sites-available/app.example.com
# HTTPS reverse proxy to local application

server {
    listen 80;
    listen [::]:80;
    server_name app.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name app.example.com;

    ssl_certificate /etc/nginx/ssl/cloudflare-origin.pem;
    ssl_certificate_key /etc/nginx/ssl/cloudflare-origin-key.pem;
    include snippets/ssl-params.conf;

    # Proxy to local application
    location / {
        proxy_pass http://127.0.0.1:8100;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://127.0.0.1:8100;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400s;
    }
}
```

## Certbot Renewal Hook

```bash
#!/bin/bash
# /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh
# Reload nginx after certificate renewal

set -euo pipefail

LOG="/var/log/certbot-renewal.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') Certificate renewed, reloading nginx..." >> "$LOG"

if nginx -t >> "$LOG" 2>&1; then
    systemctl reload nginx
    echo "$(date '+%Y-%m-%d %H:%M:%S') nginx reloaded successfully" >> "$LOG"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR: nginx config test failed, NOT reloading" >> "$LOG"
    exit 1
fi
```

## Cloudflare Origin Certificate Setup Script

```bash
#!/bin/bash
# setup-cloudflare-origin-cert.sh
# Save Cloudflare origin certificate and key to server
# Run after generating cert in Cloudflare Dashboard

set -euo pipefail

CERT_DIR="/etc/nginx/ssl"
CERT_FILE="$CERT_DIR/cloudflare-origin.pem"
KEY_FILE="$CERT_DIR/cloudflare-origin-key.pem"

echo "=== Cloudflare Origin Certificate Setup ==="

# Create directory
sudo mkdir -p "$CERT_DIR"

# Paste certificate
echo "Paste the CERTIFICATE PEM (then press Ctrl+D):"
sudo tee "$CERT_FILE" > /dev/null

echo ""
echo "Paste the PRIVATE KEY PEM (then press Ctrl+D):"
sudo tee "$KEY_FILE" > /dev/null

# Set permissions
sudo chmod 644 "$CERT_FILE"
sudo chmod 600 "$KEY_FILE"
sudo chown root:root "$CERT_FILE" "$KEY_FILE"

# Verify
echo ""
echo "Certificate info:"
openssl x509 -in "$CERT_FILE" -noout -subject -dates -issuer

echo ""
echo "Key check:"
openssl rsa -in "$KEY_FILE" -check -noout 2>/dev/null && echo "RSA key OK" || \
openssl ec -in "$KEY_FILE" -check -noout 2>/dev/null && echo "EC key OK"

echo ""
echo "Modulus match:"
CERT_MOD=$(openssl x509 -in "$CERT_FILE" -noout -modulus 2>/dev/null | md5sum)
KEY_MOD=$(openssl rsa -in "$KEY_FILE" -noout -modulus 2>/dev/null | md5sum)
if [ "$CERT_MOD" = "$KEY_MOD" ]; then
    echo "Certificate and key MATCH"
else
    echo "WARNING: Certificate and key DO NOT match!"
    exit 1
fi

echo ""
echo "Done. Now configure nginx to use:"
echo "  ssl_certificate $CERT_FILE;"
echo "  ssl_certificate_key $KEY_FILE;"
```

## DH Parameters Generation Script

```bash
#!/bin/bash
# generate-dhparam.sh
# Generate Diffie-Hellman parameters for TLS 1.2

set -euo pipefail

DH_FILE="/etc/nginx/dhparam.pem"

if [ -f "$DH_FILE" ]; then
    echo "DH params already exist at $DH_FILE"
    echo "Delete it first to regenerate."
    exit 0
fi

echo "Generating 2048-bit DH parameters (takes 10-30 seconds)..."
sudo openssl dhparam -out "$DH_FILE" 2048
sudo chmod 644 "$DH_FILE"
echo "Done: $DH_FILE"
```

## Certificate Expiry Check Script

```bash
#!/bin/bash
# check-cert-expiry.sh
# Check SSL certificate expiry for all configured domains

set -euo pipefail

WARN_DAYS=14
EXIT_CODE=0

check_domain() {
    local domain="$1"
    local expiry
    expiry=$(echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null \
        | openssl x509 -noout -enddate 2>/dev/null \
        | cut -d= -f2)

    if [ -z "$expiry" ]; then
        echo "FAIL  $domain - could not connect"
        EXIT_CODE=1
        return
    fi

    local expiry_epoch
    expiry_epoch=$(date -d "$expiry" +%s)
    local now_epoch
    now_epoch=$(date +%s)
    local days_left=$(( (expiry_epoch - now_epoch) / 86400 ))

    if [ "$days_left" -lt 0 ]; then
        echo "EXPIRED  $domain - expired $((days_left * -1)) days ago"
        EXIT_CODE=2
    elif [ "$days_left" -lt "$WARN_DAYS" ]; then
        echo "WARNING  $domain - expires in $days_left days ($expiry)"
        EXIT_CODE=1
    else
        echo "OK       $domain - expires in $days_left days ($expiry)"
    fi
}

# Add your domains here
DOMAINS=(
    "example.com"
    "app.example.com"
    "api.example.com"
)

echo "=== SSL Certificate Expiry Check ==="
echo "Warning threshold: $WARN_DAYS days"
echo ""

for domain in "${DOMAINS[@]}"; do
    check_domain "$domain"
done

exit $EXIT_CODE
```
