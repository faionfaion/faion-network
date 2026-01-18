# M-DO-015: SSL/TLS Certificates

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Beginner
- **Tags:** #devops, #security, #ssl, #tls, #certificates, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Unencrypted traffic exposes sensitive data. Manual certificate management leads to expirations. Self-signed certificates cause browser warnings.

## Promise

After this methodology, you will manage SSL/TLS certificates with automation. Your sites will be secure with trusted certificates that auto-renew.

## Overview

SSL/TLS encrypts traffic between clients and servers. Let's Encrypt provides free certificates. Cert-manager automates Kubernetes certificates.

---

## Framework

### Step 1: Let's Encrypt with Certbot

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate (Nginx)
sudo certbot --nginx -d example.com -d www.example.com

# Obtain certificate (standalone)
sudo certbot certonly --standalone -d example.com

# Obtain certificate (DNS challenge)
sudo certbot certonly --manual --preferred-challenges dns -d example.com

# Test renewal
sudo certbot renew --dry-run

# Auto-renewal (cron)
# Already set up by certbot, check:
cat /etc/cron.d/certbot
```

### Step 2: Nginx SSL Configuration

```nginx
# /etc/nginx/sites-available/example.com
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # Certificate paths
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
    resolver 8.8.8.8 8.8.4.4 valid=300s;

    # Session settings
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 3: AWS Certificate Manager

```bash
# Request certificate
aws acm request-certificate \
  --domain-name example.com \
  --subject-alternative-names "*.example.com" \
  --validation-method DNS

# List certificates
aws acm list-certificates

# Describe certificate
aws acm describe-certificate --certificate-arn arn:aws:acm:...

# Add DNS validation records (shown in describe output)
# Certificates auto-renew when used with AWS services
```

```hcl
# Terraform ACM
resource "aws_acm_certificate" "main" {
  domain_name               = "example.com"
  subject_alternative_names = ["*.example.com"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
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

  zone_id = aws_route53_zone.main.zone_id
  name    = each.value.name
  type    = each.value.type
  ttl     = 60
  records = [each.value.record]
}

resource "aws_acm_certificate_validation" "main" {
  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}

# Use with ALB
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate_validation.main.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}
```

### Step 4: Cert-Manager (Kubernetes)

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml
```

```yaml
# ClusterIssuer for Let's Encrypt
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx
      # Or DNS challenge for wildcards
      - dns01:
          route53:
            region: us-east-1
            hostedZoneID: Z123456

---
# Certificate resource
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-com
  namespace: default
spec:
  secretName: example-com-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - example.com
    - www.example.com

---
# Or use Ingress annotation
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
    - hosts:
        - example.com
      secretName: example-com-tls
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
```

### Step 5: Cloudflare SSL

```
Cloudflare SSL Modes:

Off         → No encryption
Flexible    → HTTPS to Cloudflare, HTTP to origin
Full        → HTTPS to Cloudflare, HTTPS to origin (any cert)
Full Strict → HTTPS to Cloudflare, HTTPS to origin (valid cert)

Recommendation: Full (Strict) with Origin Certificate
```

```bash
# Generate Cloudflare Origin Certificate (via Dashboard or API)
# Valid for 15 years, trusted by Cloudflare only

# Or use Let's Encrypt with DNS validation
sudo certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials /etc/cloudflare.ini \
  -d example.com -d "*.example.com"
```

### Step 6: Testing SSL

```bash
# Test SSL configuration
openssl s_client -connect example.com:443 -servername example.com

# Check certificate details
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -text

# Check expiration
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# SSL Labs test
curl https://api.ssllabs.com/api/v3/analyze?host=example.com

# testssl.sh
docker run --rm -ti drwetter/testssl.sh example.com
```

---

## Templates

### Docker with Traefik

```yaml
# docker-compose.yml
version: "3.9"

services:
  traefik:
    image: traefik:v3.0
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt:/letsencrypt

  app:
    image: myapp:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`example.com`)"
      - "traefik.http.routers.app.entrypoints=websecure"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"
      # Redirect HTTP to HTTPS
      - "traefik.http.routers.app-http.rule=Host(`example.com`)"
      - "traefik.http.routers.app-http.entrypoints=web"
      - "traefik.http.routers.app-http.middlewares=redirect-to-https"
      - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"

volumes:
  letsencrypt:
```

### Certificate Monitoring

```yaml
# Prometheus Blackbox Exporter
modules:
  http_2xx:
    prober: http
    timeout: 5s
    http:
      valid_http_versions: ["HTTP/1.1", "HTTP/2.0"]
      valid_status_codes: []
      method: GET
      fail_if_ssl: false
      fail_if_not_ssl: true
      tls_config:
        insecure_skip_verify: false
```

```yaml
# Alert rule
- alert: SSLCertExpiringSoon
  expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 14
  for: 1h
  labels:
    severity: warning
  annotations:
    summary: "SSL certificate expiring soon for {{ $labels.instance }}"
    description: "Certificate expires in {{ $value | humanizeDuration }}"
```

---

## Common Mistakes

1. **Not auto-renewing** - Certbot renewal cron missing
2. **Mixed content** - HTTP resources on HTTPS pages
3. **Expired certificates** - No monitoring for expiry
4. **Wrong chain order** - Certificate before intermediate
5. **Weak ciphers** - Use modern TLS 1.2/1.3 only

---

## Checklist

- [ ] Certificates from trusted CA
- [ ] Auto-renewal configured
- [ ] HTTPS redirect (HTTP to HTTPS)
- [ ] HSTS header enabled
- [ ] Modern TLS configuration
- [ ] Certificate monitoring
- [ ] OCSP stapling enabled
- [ ] No mixed content

---

## Next Steps

- M-DO-014: Secrets Management
- M-DO-010: Infrastructure Patterns
- M-DO-003: Docker Basics

---

*Methodology M-DO-015 v1.0*
