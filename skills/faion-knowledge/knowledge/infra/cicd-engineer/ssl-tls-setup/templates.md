# SSL/TLS Setup Templates

## Nginx Modern Configuration

### ssl-params.conf

```nginx
# /etc/nginx/snippets/ssl-params.conf
# Modern TLS configuration (2025)

# Protocols
ssl_protocols TLSv1.2 TLSv1.3;

# Ciphers (TLS 1.2 only - TLS 1.3 uses built-in secure ciphers)
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;

# Session
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# DH parameters
ssl_dhparam /etc/nginx/dhparam.pem;

# HSTS
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

### Site Configuration

```nginx
# /etc/nginx/sites-available/{{DOMAIN}}.conf

server {
    listen 80;
    listen [::]:80;
    server_name {{DOMAIN}} www.{{DOMAIN}};
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name {{DOMAIN}} www.{{DOMAIN}};

    ssl_certificate /etc/letsencrypt/live/{{DOMAIN}}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{{DOMAIN}}/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/{{DOMAIN}}/chain.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    root /var/www/{{DOMAIN}};
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## Apache Modern Configuration

```apache
# /etc/apache2/sites-available/{{DOMAIN}}-ssl.conf

<VirtualHost *:80>
    ServerName {{DOMAIN}}
    ServerAlias www.{{DOMAIN}}
    Redirect permanent / https://{{DOMAIN}}/
</VirtualHost>

<VirtualHost *:443>
    ServerName {{DOMAIN}}
    ServerAlias www.{{DOMAIN}}
    DocumentRoot /var/www/{{DOMAIN}}

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/{{DOMAIN}}/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/{{DOMAIN}}/privkey.pem

    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305
    SSLHonorCipherOrder off

    SSLUseStapling on
    SSLStaplingResponderTimeout 5
    SSLStaplingReturnResponderErrors off

    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"

    <Directory /var/www/{{DOMAIN}}>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>

SSLStaplingCache shmcb:/var/run/ocsp(128000)
```

---

## Kubernetes Templates

### cert-manager ClusterIssuer

```yaml
# clusterissuer-letsencrypt.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: {{ADMIN_EMAIL}}
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx

---
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: {{ADMIN_EMAIL}}
    privateKeySecretRef:
      name: letsencrypt-staging
    solvers:
      - http01:
          ingress:
            class: nginx
```

### Certificate Resource

```yaml
# certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: {{NAME}}-tls
  namespace: {{NAMESPACE}}
spec:
  secretName: {{NAME}}-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: {{DOMAIN}}
  dnsNames:
    - {{DOMAIN}}
    - www.{{DOMAIN}}
  privateKey:
    algorithm: ECDSA
    size: 256
```

### Ingress with TLS

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{NAME}}-ingress
  namespace: {{NAMESPACE}}
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/hsts: "true"
    nginx.ingress.kubernetes.io/hsts-max-age: "63072000"
    nginx.ingress.kubernetes.io/hsts-include-subdomains: "true"
    nginx.ingress.kubernetes.io/hsts-preload: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - {{DOMAIN}}
        - www.{{DOMAIN}}
      secretName: {{NAME}}-tls
  rules:
    - host: {{DOMAIN}}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{SERVICE_NAME}}
                port:
                  number: {{SERVICE_PORT}}
```

---

## Certificate Monitoring Script

```bash
#!/bin/bash
# check_ssl_expiry.sh

DOMAINS=(
  "example.com"
  "api.example.com"
  "www.example.com"
)

ALERT_DAYS=30
CRITICAL_DAYS=7

for domain in "${DOMAINS[@]}"; do
    expiry_date=$(echo | openssl s_client -connect "$domain:443" -servername "$domain" 2>/dev/null | \
        openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)

    if [ -z "$expiry_date" ]; then
        echo "ERROR: Cannot connect to $domain"
        continue
    fi

    expiry_epoch=$(date -d "$expiry_date" +%s)
    current_epoch=$(date +%s)
    days_left=$(( (expiry_epoch - current_epoch) / 86400 ))

    if [ $days_left -lt $CRITICAL_DAYS ]; then
        echo "CRITICAL: $domain expires in $days_left days ($expiry_date)"
        # Add alerting here (email, Slack, PagerDuty)
    elif [ $days_left -lt $ALERT_DAYS ]; then
        echo "WARNING: $domain expires in $days_left days ($expiry_date)"
    else
        echo "OK: $domain valid for $days_left days ($expiry_date)"
    fi
done
```

---

## Systemd Renewal Hook

```bash
#!/bin/bash
# /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh

systemctl reload nginx
```

---

## Docker Compose with Traefik

```yaml
# docker-compose.yml
version: "3.8"

services:
  traefik:
    image: traefik:v3.0
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email={{ADMIN_EMAIL}}"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - "letsencrypt:/letsencrypt"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dashboard.rule=Host(`traefik.{{DOMAIN}}`)"
      - "traefik.http.routers.dashboard.entrypoints=websecure"
      - "traefik.http.routers.dashboard.tls.certresolver=letsencrypt"
      - "traefik.http.routers.dashboard.service=api@internal"

  app:
    image: {{APP_IMAGE}}
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`{{DOMAIN}}`)"
      - "traefik.http.routers.app.entrypoints=websecure"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"
      - "traefik.http.services.app.loadbalancer.server.port=3000"

volumes:
  letsencrypt:
```

---

## Terraform - AWS ACM Certificate

```hcl
# acm.tf
resource "aws_acm_certificate" "main" {
  domain_name               = var.domain_name
  subject_alternative_names = ["*.${var.domain_name}"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name        = "${var.domain_name}-cert"
    Environment = var.environment
  }
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.main.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = var.route53_zone_id
}

resource "aws_acm_certificate_validation" "main" {
  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
```

---

## DNS CAA Records Template

```
; CAA records for {{DOMAIN}}
{{DOMAIN}}.  IN  CAA  0  issue "letsencrypt.org"
{{DOMAIN}}.  IN  CAA  0  issuewild "letsencrypt.org"
{{DOMAIN}}.  IN  CAA  0  iodef "mailto:{{SECURITY_EMAIL}}"
```

---

## Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{{DOMAIN}}` | Primary domain | `example.com` |
| `{{NAME}}` | Resource name | `my-app` |
| `{{NAMESPACE}}` | Kubernetes namespace | `production` |
| `{{ADMIN_EMAIL}}` | Admin email for CA | `admin@example.com` |
| `{{SECURITY_EMAIL}}` | Security contact | `security@example.com` |
| `{{SERVICE_NAME}}` | K8s service name | `web-service` |
| `{{SERVICE_PORT}}` | K8s service port | `80` |
| `{{APP_IMAGE}}` | Docker image | `nginx:latest` |

---

*SSL/TLS Setup Templates | faion-cicd-engineer*
