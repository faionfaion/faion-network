# SSL/TLS Configuration Templates

## Nginx SSL Parameters Template

Use this as `/etc/nginx/snippets/ssl-params.conf`:

```nginx
# SSL/TLS Configuration - Mozilla Intermediate (2025)
# Generated for TLS 1.2 and TLS 1.3 compatibility
# Source: https://ssl-config.mozilla.org/

# Protocols
ssl_protocols TLSv1.2 TLSv1.3;

# Ciphers (TLS 1.2)
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;

# Session configuration
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
# Note: Update path to your trusted certificate
# ssl_trusted_certificate /etc/letsencrypt/live/DOMAIN/chain.pem;
resolver 8.8.8.8 8.8.4.4 1.1.1.1 valid=300s;
resolver_timeout 5s;

# DH parameters (generate with: openssl dhparam -out /etc/nginx/dhparam.pem 2048)
ssl_dhparam /etc/nginx/dhparam.pem;

# HSTS (2 years)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# Security headers
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

---

## Nginx Server Block Template

```nginx
# /etc/nginx/sites-available/DOMAIN.conf

# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name DOMAIN www.DOMAIN;

    # ACME challenge for Let's Encrypt
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name DOMAIN www.DOMAIN;

    # SSL certificate
    ssl_certificate /etc/letsencrypt/live/DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMAIN/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/DOMAIN/chain.pem;

    # SSL parameters
    include /etc/nginx/snippets/ssl-params.conf;

    # Logging
    access_log /var/log/nginx/DOMAIN.access.log;
    error_log /var/log/nginx/DOMAIN.error.log;

    # Document root
    root /var/www/DOMAIN;
    index index.html index.htm;

    # Main location
    location / {
        try_files $uri $uri/ =404;
    }

    # Security: deny hidden files
    location ~ /\. {
        deny all;
    }
}
```

---

## Nginx Reverse Proxy Template

```nginx
# /etc/nginx/sites-available/DOMAIN-proxy.conf

upstream backend_DOMAIN {
    server 127.0.0.1:PORT;
    keepalive 64;
}

server {
    listen 80;
    listen [::]:80;
    server_name DOMAIN;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name DOMAIN;

    ssl_certificate /etc/letsencrypt/live/DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMAIN/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/DOMAIN/chain.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    # Logging
    access_log /var/log/nginx/DOMAIN.access.log;
    error_log /var/log/nginx/DOMAIN.error.log;

    # Proxy settings
    location / {
        proxy_pass http://backend_DOMAIN;
        proxy_http_version 1.1;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
}
```

---

## Apache SSL VirtualHost Template

```apache
# /etc/apache2/sites-available/DOMAIN-ssl.conf

# HTTP redirect
<VirtualHost *:80>
    ServerName DOMAIN
    ServerAlias www.DOMAIN

    # ACME challenge
    Alias /.well-known/acme-challenge/ /var/www/certbot/.well-known/acme-challenge/
    <Directory "/var/www/certbot/.well-known/acme-challenge/">
        Options None
        AllowOverride None
        Require all granted
    </Directory>

    # Redirect all other traffic
    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^/.well-known/acme-challenge/
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
</VirtualHost>

# HTTPS server
<VirtualHost *:443>
    ServerName DOMAIN
    ServerAlias www.DOMAIN
    DocumentRoot /var/www/DOMAIN

    # SSL configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/DOMAIN/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/DOMAIN/privkey.pem

    # Protocols and ciphers
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off

    # HSTS
    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"

    # OCSP Stapling
    SSLUseStapling on
    SSLStaplingResponderTimeout 5
    SSLStaplingReturnResponderErrors off

    # Logging
    ErrorLog ${APACHE_LOG_DIR}/DOMAIN-error.log
    CustomLog ${APACHE_LOG_DIR}/DOMAIN-access.log combined

    <Directory /var/www/DOMAIN>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>

# OCSP Stapling cache (add to main apache config)
# SSLStaplingCache shmcb:/var/run/ocsp(128000)
```

---

## Kubernetes Ingress Template

```yaml
# ingress-DOMAIN.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: DOMAIN-ingress
  namespace: NAMESPACE
  annotations:
    # TLS redirect
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    # HSTS
    nginx.ingress.kubernetes.io/configuration-snippet: |
      add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    # cert-manager
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - DOMAIN
        - www.DOMAIN
      secretName: DOMAIN-tls
  rules:
    - host: DOMAIN
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: SERVICE_NAME
                port:
                  number: 80
    - host: www.DOMAIN
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: SERVICE_NAME
                port:
                  number: 80
```

---

## cert-manager ClusterIssuer Template

```yaml
# cluster-issuer-letsencrypt.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: ADMIN_EMAIL
    privateKeySecretRef:
      name: letsencrypt-prod-account
    solvers:
      # HTTP-01 solver (default)
      - http01:
          ingress:
            class: nginx
---
# Staging issuer for testing
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: ADMIN_EMAIL
    privateKeySecretRef:
      name: letsencrypt-staging-account
    solvers:
      - http01:
          ingress:
            class: nginx
```

---

## Certificate Monitoring Script Template

```bash
#!/bin/bash
# check_ssl_expiry.sh
# Monitor SSL certificate expiration and send alerts

set -euo pipefail

# Configuration
DOMAINS=(
    "example.com"
    "api.example.com"
    "www.example.com"
)
ALERT_DAYS_WARNING=30
ALERT_DAYS_CRITICAL=14
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"  # Optional Slack webhook

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

check_certificate() {
    local domain=$1
    local port=${2:-443}

    # Get expiration date
    local expiry_date
    expiry_date=$(echo | openssl s_client -connect "$domain:$port" -servername "$domain" 2>/dev/null | \
        openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)

    if [[ -z "$expiry_date" ]]; then
        echo -e "${RED}ERROR${NC}: Could not get certificate for $domain"
        return 1
    fi

    local expiry_epoch
    expiry_epoch=$(date -d "$expiry_date" +%s 2>/dev/null || date -j -f "%b %d %T %Y %Z" "$expiry_date" +%s 2>/dev/null)
    local current_epoch
    current_epoch=$(date +%s)
    local days_left=$(( (expiry_epoch - current_epoch) / 86400 ))

    # Output result
    if [[ $days_left -lt $ALERT_DAYS_CRITICAL ]]; then
        echo -e "${RED}CRITICAL${NC}: $domain expires in $days_left days ($expiry_date)"
        send_alert "CRITICAL" "$domain" "$days_left"
    elif [[ $days_left -lt $ALERT_DAYS_WARNING ]]; then
        echo -e "${YELLOW}WARNING${NC}: $domain expires in $days_left days ($expiry_date)"
        send_alert "WARNING" "$domain" "$days_left"
    else
        echo -e "${GREEN}OK${NC}: $domain valid for $days_left days ($expiry_date)"
    fi
}

send_alert() {
    local level=$1
    local domain=$2
    local days=$3

    # Slack notification (if configured)
    if [[ -n "$SLACK_WEBHOOK" ]]; then
        local color="warning"
        [[ "$level" == "CRITICAL" ]] && color="danger"

        curl -s -X POST "$SLACK_WEBHOOK" \
            -H 'Content-type: application/json' \
            -d "{
                \"attachments\": [{
                    \"color\": \"$color\",
                    \"title\": \"SSL Certificate $level\",
                    \"text\": \"Certificate for $domain expires in $days days\",
                    \"footer\": \"SSL Monitor\"
                }]
            }" > /dev/null
    fi
}

# Main
echo "=== SSL Certificate Expiry Check ==="
echo "Date: $(date)"
echo ""

for domain in "${DOMAINS[@]}"; do
    check_certificate "$domain"
done
```

---

## Certbot Renewal Hook Template

```bash
#!/bin/bash
# /etc/letsencrypt/renewal-hooks/deploy/reload-services.sh
# Runs after successful certificate renewal

set -euo pipefail

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> /var/log/letsencrypt/renewal.log
}

log "Certificate renewed for: $RENEWED_DOMAINS"
log "Certificate lineage: $RENEWED_LINEAGE"

# Reload Nginx
if systemctl is-active --quiet nginx; then
    log "Reloading Nginx..."
    systemctl reload nginx
    log "Nginx reloaded successfully"
fi

# Reload Apache
if systemctl is-active --quiet apache2; then
    log "Reloading Apache..."
    systemctl reload apache2
    log "Apache reloaded successfully"
fi

# Reload HAProxy
if systemctl is-active --quiet haproxy; then
    log "Reloading HAProxy..."
    # HAProxy needs combined cert
    cat "$RENEWED_LINEAGE/fullchain.pem" "$RENEWED_LINEAGE/privkey.pem" > /etc/haproxy/certs/combined.pem
    systemctl reload haproxy
    log "HAProxy reloaded successfully"
fi

# Optional: Send notification
# curl -X POST "https://hooks.slack.com/..." -d '{"text":"Certificate renewed for: '"$RENEWED_DOMAINS"'"}'

log "Renewal hook completed"
```

---

## Docker Compose with Traefik Template

```yaml
# docker-compose.yml with Traefik and Let's Encrypt
version: "3.8"

services:
  traefik:
    image: traefik:v3.0
    container_name: traefik
    restart: unless-stopped
    command:
      # API and dashboard
      - "--api.dashboard=true"
      # Docker provider
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      # Entrypoints
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      # HTTP to HTTPS redirect
      - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
      - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
      # Let's Encrypt
      - "--certificatesresolvers.letsencrypt.acme.email=ADMIN_EMAIL"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - "traefik-letsencrypt:/letsencrypt"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dashboard.rule=Host(`traefik.DOMAIN`)"
      - "traefik.http.routers.dashboard.service=api@internal"
      - "traefik.http.routers.dashboard.tls.certresolver=letsencrypt"
      - "traefik.http.routers.dashboard.middlewares=auth"
      - "traefik.http.middlewares.auth.basicauth.users=admin:$$apr1$$..."

  webapp:
    image: nginx:alpine
    container_name: webapp
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.webapp.rule=Host(`DOMAIN`)"
      - "traefik.http.routers.webapp.tls.certresolver=letsencrypt"
      - "traefik.http.services.webapp.loadbalancer.server.port=80"

volumes:
  traefik-letsencrypt:
```

---

## Placeholder Reference

Replace these placeholders in templates:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `DOMAIN` | Your domain name | `example.com` |
| `NAMESPACE` | Kubernetes namespace | `production` |
| `SERVICE_NAME` | Kubernetes service | `web-service` |
| `PORT` | Backend port number | `3000` |
| `ADMIN_EMAIL` | Admin email address | `admin@example.com` |
