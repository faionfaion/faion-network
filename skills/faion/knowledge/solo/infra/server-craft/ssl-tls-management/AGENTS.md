# SSL/TLS Management

## Summary

Configure HTTPS on a Linux VPS with one of three certificate strategies: Let's Encrypt (direct exposure, 90-day auto-renew via certbot), Cloudflare origin cert (15-year cert behind Cloudflare proxy, no renewal), or hybrid. Always use Cloudflare Full(Strict) mode — never Flexible. nginx SSL hardening: TLS 1.2/1.3 only, strong ciphers, OCSP stapling (Let's Encrypt only), HSTS.

## Why

Flexible mode sends traffic from Cloudflare to the origin over plain HTTP, creating a false sense of security and causing redirect loops when nginx also forces HTTPS. A 15-year Cloudflare origin cert eliminates the 90-day renewal cycle entirely for proxied domains. TLS 1.0/1.1 must be dropped — both are deprecated with known downgrade attacks.

## When To Use

- New domain needing HTTPS on any nginx virtual host
- Migrating from Let's Encrypt to a Cloudflare origin cert (eliminating renewal ops)
- Auditing TLS configuration for SSL Labs A+ score
- Adding HSTS or OCSP stapling to an existing nginx site
- Configuring SSL for a domain behind Cloudflare proxy

## When NOT To Use

- Cloudflare Flexible mode — causes redirect loops when nginx redirects HTTP to HTTPS
- OCSP stapling with Cloudflare origin certs — they have no OCSP responder; only enable with Let's Encrypt or commercial certs
- Self-signed certs for production — use origin certs instead (trusted by Cloudflare edge)
- Adding `preload` to HSTS before confirming all subdomains support HTTPS — removal takes months

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Cert types comparison, TLS versions, Cloudflare SSL modes, HSTS directives, OCSP stapling rules |
| `content/02-nginx-config.xml` | ssl_protocols, cipher suites, session settings, DH params, security headers, HTTP→HTTPS redirect |
| `content/03-examples.xml` | NERO platform Cloudflare origin cert setup, Let's Encrypt direct domain, mixed-strategy multi-domain |

## Templates

| File | Purpose |
|------|---------|
| `templates/ssl-params.conf` | Reusable nginx snippet: TLS versions, ciphers, session settings, OCSP stapling toggle |
| `templates/site-cloudflare.conf` | nginx site template using Cloudflare origin cert |
| `templates/site-letsencrypt.conf` | nginx site template using Let's Encrypt cert with OCSP stapling |
| `templates/setup-cloudflare-origin-cert.sh` | Place origin cert + key in /etc/nginx/ssl/, set permissions |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/check-cert-expiry.sh` | Report cert expiry for all configured domains, warn at 30 days |
| `scripts/test-tls-config.sh` | Verify TLS versions, cipher score, HSTS header, OCSP response |
