# SSL/TLS Management

SSL/TLS configuration and certificate management for Linux servers. Covers Let's Encrypt with certbot, Cloudflare origin certificates, nginx SSL hardening, and automated renewal workflows.

## Overview

Modern HTTPS setup for solo developers typically involves one of two patterns:

| Pattern | Stack | Use Case |
|---------|-------|----------|
| **Let's Encrypt direct** | certbot + nginx | No CDN, direct server exposure |
| **Cloudflare Full(Strict)** | Cloudflare + origin cert + nginx | CDN/WAF in front, best security |
| **Hybrid** | Let's Encrypt + Cloudflare proxy | Flexible, both certs valid |

For NERO-style platforms behind Cloudflare, the recommended setup is **Cloudflare Full(Strict)** with a 15-year origin certificate, eliminating renewal complexity entirely.

## Key Concepts

### TLS Versions

| Version | Status | Support |
|---------|--------|---------|
| TLS 1.0 | Deprecated | Drop immediately |
| TLS 1.1 | Deprecated | Drop immediately |
| TLS 1.2 | Current | Minimum acceptable |
| TLS 1.3 | Current | Preferred, fastest handshake |

### Certificate Types

| Type | Issuer | Validity | Auto-Renew | Cost |
|------|--------|----------|------------|------|
| Let's Encrypt | ISRG | 90 days | Yes (certbot) | Free |
| Cloudflare Origin | Cloudflare | 15 years | No (long-lived) | Free |
| Self-signed | You | Any | Manual | Free |
| Commercial (EV/OV) | DigiCert, etc. | 1 year | Manual | $50-500/yr |

### Cloudflare SSL Modes

| Mode | Browser-to-CF | CF-to-Origin | Security |
|------|--------------|--------------|----------|
| Off | HTTP | HTTP | None |
| Flexible | HTTPS | HTTP | Partial (false sense) |
| Full | HTTPS | HTTPS (any cert) | Good |
| Full (Strict) | HTTPS | HTTPS (valid cert) | Best |

**Always use Full (Strict)** with either a Cloudflare origin cert or a valid Let's Encrypt cert on the origin.

## HSTS (HTTP Strict Transport Security)

Forces browsers to always use HTTPS. Once enabled, cannot be easily disabled.

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

| Directive | Value | Purpose |
|-----------|-------|---------|
| max-age | 63072000 (2 years) | How long browser remembers HTTPS-only |
| includeSubDomains | - | Apply to all subdomains |
| preload | - | Submit to browser preload list |

**Warning:** Only add `preload` after confirming all subdomains support HTTPS. Removing from the preload list takes months.

## OCSP Stapling

Server fetches OCSP response and "staples" it to the TLS handshake, improving privacy and performance.

```nginx
ssl_stapling on;
ssl_stapling_verify on;
resolver 1.1.1.1 8.8.8.8 valid=300s;
resolver_timeout 5s;
```

**Note:** OCSP stapling does not work with Cloudflare origin certificates (they don't have OCSP responders). Only enable with Let's Encrypt or commercial certs.

## Certificate Chain

A properly configured certificate chain:

```
Browser trusts Root CA
    Root CA signs Intermediate CA
        Intermediate CA signs your certificate
```

- **Let's Encrypt:** Chain is automatic (certbot provides `fullchain.pem`)
- **Cloudflare Origin:** Chain includes Cloudflare CA (only trusted by Cloudflare edge)
- **Commercial:** You must concatenate cert + intermediate into a bundle

## nginx SSL Configuration

### Cipher Suites

For TLS 1.3 (server does not select ciphers, client does):
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
```

### Session Management

```nginx
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;
```

| Setting | Value | Why |
|---------|-------|-----|
| session_timeout | 1d | Balance between performance and security |
| session_cache | shared:SSL:10m | ~40,000 sessions in 10MB |
| session_tickets | off | Forward secrecy (tickets compromise PFS) |

### DH Parameters

For TLS 1.2 with DHE ciphers, generate strong DH params:

```bash
openssl dhparam -out /etc/nginx/dhparam.pem 2048
```

Not needed for TLS 1.3 (uses X25519/X448 key exchange).

## Let's Encrypt with Certbot

### Installation

```bash
sudo apt update
sudo apt install -y certbot python3-certbot-nginx
```

### Certificate Issuance

```bash
# Nginx plugin (auto-configures nginx)
sudo certbot --nginx -d example.com -d www.example.com

# Standalone (stops nginx temporarily)
sudo certbot certonly --standalone -d example.com

# Webroot (nginx keeps running)
sudo certbot certonly --webroot -w /var/www/html -d example.com
```

### Auto-Renewal

Certbot installs a systemd timer automatically:

```bash
# Check timer status
systemctl list-timers | grep certbot

# Test renewal
sudo certbot renew --dry-run
```

### Renewal Hooks

```bash
# Post-renewal hook to reload nginx
sudo mkdir -p /etc/letsencrypt/renewal-hooks/post
sudo tee /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh << 'HOOK'
#!/bin/bash
systemctl reload nginx
HOOK
sudo chmod +x /etc/letsencrypt/renewal-hooks/post/reload-nginx.sh
```

## Cloudflare Origin Certificates

### Setup Flow

1. Cloudflare Dashboard: SSL/TLS -> Origin Server -> Create Certificate
2. Choose key type: RSA (2048) or ECDSA (P-256)
3. Set hostnames: `example.com`, `*.example.com`
4. Set validity: 15 years (maximum)
5. Save certificate and private key to server
6. Configure nginx to use them
7. Set SSL mode to Full (Strict)

### File Placement

```bash
sudo mkdir -p /etc/nginx/ssl
sudo tee /etc/nginx/ssl/cloudflare-origin.pem    # Certificate
sudo tee /etc/nginx/ssl/cloudflare-origin-key.pem # Private key
sudo chmod 600 /etc/nginx/ssl/cloudflare-origin-key.pem
```

## Security Headers

Beyond HSTS, add these security headers:

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
```

## Testing

| Tool | URL | What It Tests |
|------|-----|---------------|
| SSL Labs | ssllabs.com/ssltest | Full SSL audit (aim for A+) |
| testssl.sh | github.com/drwetter/testssl.sh | CLI-based comprehensive test |
| Mozilla Observatory | observatory.mozilla.org | Security headers |
| Hardenize | hardenize.com | SSL + email + DNS |

```bash
# Quick CLI test
curl -vI https://example.com 2>&1 | grep -E "(SSL|TLS|subject|expire)"

# Check certificate details
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates -subject

# Test specific TLS version
openssl s_client -connect example.com:443 -tls1_3
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| ERR_CERT_AUTHORITY_INVALID | Self-signed or expired cert | Renew or use valid CA |
| ERR_SSL_VERSION_OR_CIPHER_MISMATCH | Old TLS version or weak cipher | Update ssl_protocols |
| Mixed content warnings | HTTP resources on HTTPS page | Fix URLs in application |
| Redirect loop | Cloudflare Flexible + nginx force-HTTPS | Use Full(Strict) mode |
| 526 Invalid SSL Certificate | Cloudflare can't verify origin cert | Use origin cert or Let's Encrypt |

## Related Methodologies

- `nginx-reverse-proxy/` -- nginx server blocks and proxy configuration
- `firewall-management/` -- allow ports 80/443
- `multi-project-hosting/` -- SSL for multiple domains
