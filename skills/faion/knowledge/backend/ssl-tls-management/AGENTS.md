# SSL/TLS Management

## Summary

**One-sentence:** Generates a per-domain TLS plan — Cloudflare-origin OR Let's Encrypt — with cert paths, renewal cron, and ssl_params snippet — gated by an expiry-monitor cron.

**One-paragraph:** TLS on a solo VPS is two flavours: Cloudflare full(strict) with origin certs (15-year, no renewal) or Let's Encrypt with certbot (90-day, auto-renew). This methodology pins the choice per domain, declares the cert paths, the ssl_params snippet (Mozilla 'Intermediate'), the renewal cron (LE) or expiry-monitor (CF), and an OCSP stapling toggle. Output: a TlsPlan + cron entries.

**Ефективно для:**

- Multi-domain VPS behind Cloudflare full(strict).
- Apex domains where Let's Encrypt is the only option.
- Auditing existing TLS posture against Mozilla recommendations.
- Setting up expiry monitoring before the first cert lapses.

## Applies If (ALL must hold)

- Serving HTTPS on a custom domain from a VPS.
- Switching between Cloudflare-origin and Let's Encrypt.
- Auditing current TLS posture for forbidden algorithms (TLS 1.0/1.1).
- Setting up renewal automation for the first time.

## Skip If (ANY kills it)

- Managed platform that handles TLS termination (Heroku/Vercel/Netlify).
- Internal-only services behind WireGuard/Tailscale with no public TLS.
- Existing working renewal + monitoring — don't re-introduce churn.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain list + chosen TLS mode | YAML/CSV | operator inventory |
| Cloudflare API token (origin certs) OR ACME account (LE) | secret in 1Password | operator credentials |
| Allowed ciphers + protocols | Mozilla preset name | Mozilla SSL Config Generator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| nginx-reverse-proxy | TLS config is consumed by nginx vhosts produced upstream. |
| cloudflare-domain-dns | Cloudflare-origin mode requires the domain proxied through Cloudflare. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-strict-mode-only, r2-monitored-expiry, r3-modern-ciphers, r4-named-renewal-owner, r5-ocsp-stapling-when-le | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the SSL/TLS Management artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: flexible-mode-shipped, no-expiry-monitor, weak-ciphers-default, certbot-renew-no-deploy-hook | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-tls-plan` | sonnet | Per-domain decision with stakes. |
| `render-ssl-params` | haiku | Template fill from Mozilla preset. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ssl-tls-management.json` | TlsPlan JSON skeleton (domains + mode + renewal). |
| `templates/ssl-tls-management.md` | Human-readable audit trail. |
| `templates/ssl-params.conf` | Mozilla 'Intermediate' ciphers + protocols snippet. |
| `templates/site-cloudflare.conf` | Reference vhost using Cloudflare origin cert. |
| `templates/site-letsencrypt.conf` | Reference vhost using Let's Encrypt cert + ACME challenge. |
| `templates/setup-cloudflare-origin-cert.sh` | Generates origin cert via Cloudflare API + installs to /etc/nginx/ssl. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ssl-tls-management.py` | Validate TlsPlan JSON against the schema. | Pre-deploy + post-renewal. |
| `scripts/check-cert-expiry.sh` | Expiry monitor — exit 1 if any cert < 14d to expiry. | Daily cron. |
| `scripts/test-tls-config.sh` | Runs testssl.sh / sslyze against the live config. | Post-config-change + monthly. |

## Related

- [[nginx-reverse-proxy]]
- [[cloudflare-domain-dns]]
- [[monitoring-logging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ssl-tls-management.json`

```json
{
  "artefact_id": "tls-<domain>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "domain": "<example.com>",
  "mode": "letsencrypt",
  "cert_path": "/etc/letsencrypt/live/<domain>/fullchain.pem",
  "key_path": "/etc/letsencrypt/live/<domain>/privkey.pem",
  "expiry_monitor_cron": "0 6 * * * /usr/local/bin/check-cert-expiry.sh",
  "renewal_hook": "systemctl reload nginx",
  "owner": "<@handle>"
}
```

### `templates/ssl-params.conf`

```conf
# /etc/nginx/snippets/ssl-params.conf
# Reusable SSL/TLS parameters — include in every ssl server block

ssl_protocols             TLSv1.2 TLSv1.3;
ssl_ciphers               ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;

ssl_session_timeout 1d;
ssl_session_cache   shared:SSL:10m;
ssl_session_tickets off;

# DH params for TLS 1.2 DHE ciphers (generate: openssl dhparam -out /etc/nginx/dhparam.pem 2048)
# ssl_dhparam /etc/nginx/dhparam.pem;

# OCSP stapling — enable ONLY with Let's Encrypt or commercial certs
# NOT for Cloudflare origin certs (no OCSP responder)
# ssl_stapling        on;
# ssl_stapling_verify on;
# resolver 1.1.1.1 8.8.8.8 valid=300s;
# resolver_timeout 5s;
```

### `templates/site-cloudflare.conf`

```conf
# /etc/nginx/sites-available/DOMAIN.conf
# nginx site template using Cloudflare origin cert (15-year, no renewal)
# Requires: Cloudflare SSL mode set to Full (Strict)

server {
    listen 80;
    listen 443 ssl;
    server_name DOMAIN;

    ssl_certificate     /etc/nginx/ssl/cloudflare-origin.pem;
    ssl_certificate_key /etc/nginx/ssl/cloudflare-origin-key.pem;
    include snippets/ssl-params.conf;

    include snippets/security-headers.conf;
    client_max_body_size 10M;

    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:BACKEND_PORT;
    }
}
```

### `templates/site-letsencrypt.conf`

```conf
# /etc/nginx/sites-available/DOMAIN.conf
# nginx site template using Let's Encrypt certificate (with OCSP stapling)
# Requires: certbot installed, cert issued at /etc/letsencrypt/live/DOMAIN/

server {
    listen 80;
    server_name DOMAIN www.DOMAIN;

    # Allow certbot HTTP-01 challenge (required for renewal)
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name DOMAIN www.DOMAIN;

    ssl_certificate     /etc/letsencrypt/live/DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMAIN/privkey.pem;
    include snippets/ssl-params.conf;

    # Enable OCSP stapling (valid for Let's Encrypt)
    ssl_stapling        on;
    ssl_stapling_verify on;
    resolver            1.1.1.1 8.8.8.8 valid=300s;
    resolver_timeout    5s;

    include snippets/security-headers.conf;
    client_max_body_size 10M;

    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://127.0.0.1:BACKEND_PORT;
    }
}
```

### `templates/setup-cloudflare-origin-cert.sh`

```bash
# setup-cloudflare-origin-cert.sh — Place origin cert + key in /etc/nginx/ssl/, set permissions
# Prerequisites: copy cert and key content from Cloudflare Dashboard
# Usage: bash setup-cloudflare-origin-cert.sh cert.pem key.pem
set -euo pipefail

CERT_FILE="${1:?Usage: $0 <cert.pem> <key.pem>}"
KEY_FILE="${2:?Usage: $0 <cert.pem> <key.pem>}"

SSL_DIR="/etc/nginx/ssl"
sudo mkdir -p "$SSL_DIR"

sudo cp "$CERT_FILE" "$SSL_DIR/cloudflare-origin.pem"
sudo cp "$KEY_FILE"  "$SSL_DIR/cloudflare-origin-key.pem"

sudo chmod 644 "$SSL_DIR/cloudflare-origin.pem"
sudo chmod 600 "$SSL_DIR/cloudflare-origin-key.pem"
sudo chown root:root "$SSL_DIR/cloudflare-origin.pem" "$SSL_DIR/cloudflare-origin-key.pem"

echo "Cert installed:"
echo "  $SSL_DIR/cloudflare-origin.pem"
echo "  $SSL_DIR/cloudflare-origin-key.pem"
echo ""

# Show cert expiry
sudo openssl x509 -in "$SSL_DIR/cloudflare-origin.pem" -noout -dates
echo ""
echo "Test nginx config: sudo nginx -t"
echo "Then: sudo systemctl reload nginx"
echo ""
echo "IMPORTANT: Set Cloudflare SSL mode to Full (Strict)"
```
