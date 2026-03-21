# SSL/TLS Management LLM Prompts

## SSL Troubleshooting

### Prompt: Diagnose SSL Error

```
I'm getting an SSL error when accessing my website. Help me diagnose and fix it.

Server details:
- OS: [e.g., Ubuntu 24.04]
- Web server: [e.g., nginx 1.24]
- Certificate type: [Let's Encrypt / Cloudflare Origin / Commercial]
- CDN: [Cloudflare Full(Strict) / None]
- Domain: [e.g., app.example.com]

Error details:
- Browser error: [e.g., ERR_CERT_AUTHORITY_INVALID, ERR_SSL_PROTOCOL_ERROR]
- curl output: [paste curl -vI output]
- nginx error log: [paste relevant lines]

Current nginx SSL config:
[paste server block]

Provide:
1. Root cause analysis
2. Step-by-step fix
3. Verification commands
4. Prevention measures
```

### Prompt: Fix Redirect Loop

```
I have an HTTPS redirect loop on my domain. The browser shows ERR_TOO_MANY_REDIRECTS.

Setup:
- Domain: [domain]
- Cloudflare: [Yes/No, if yes what SSL mode]
- nginx config: [paste server blocks for port 80 and 443]

Diagnose the loop cause and provide the correct configuration.
Common causes to check:
- Cloudflare Flexible mode + nginx force-HTTPS redirect
- Double redirect (Cloudflare + nginx both redirecting)
- Missing listen 443 block
- Incorrect proxy_set_header X-Forwarded-Proto
```

## Certificate Management

### Prompt: Setup SSL for New Domain

```
I need to set up HTTPS for a new domain on my existing server.

Current server setup:
- OS: Ubuntu 24.04
- Web server: nginx
- Existing SSL: [describe current domains and cert types]
- CDN: [Cloudflare / None]
- Firewall: [UFW rules for 80/443]

New domain:
- Domain: [e.g., newapp.example.com]
- Application: [what runs behind it, e.g., FastAPI on port 3000]
- Certificate preference: [Let's Encrypt / Cloudflare Origin]
- Needs WebSocket: [Yes/No]

Provide:
1. Certificate acquisition steps
2. Complete nginx server block
3. SSL hardening (TLS 1.2+, HSTS, security headers)
4. Verification steps
5. Auto-renewal setup (if Let's Encrypt)
```

### Prompt: Migrate from Let's Encrypt to Cloudflare Origin

```
I want to migrate a domain from Let's Encrypt to Cloudflare origin certificate.

Current setup:
- Domain: [domain]
- Current cert: Let's Encrypt with certbot auto-renewal
- nginx config: [paste current config]

Target setup:
- Cloudflare Full (Strict) with 15-year origin certificate
- Remove certbot dependency for this domain

Provide:
1. Step-by-step migration plan (zero-downtime)
2. Cloudflare dashboard settings
3. Updated nginx configuration
4. Cleanup of old Let's Encrypt cert
5. Verification steps
```

### Prompt: Certificate Expiry Audit

```
Audit all SSL certificates on my server and create a renewal plan.

Server: [hostname]
Known domains:
- [domain1] (Cloudflare origin cert)
- [domain2] (Let's Encrypt)
- [domain3] (unknown)

Run these checks and provide a report:
1. List all certificates in /etc/nginx/ssl/ and /etc/letsencrypt/live/
2. Check expiry dates for each
3. Verify auto-renewal is configured for Let's Encrypt certs
4. Identify any certificates expiring within 30 days
5. Recommend monitoring/alerting setup

Commands to run:
- find /etc/letsencrypt/live/ -name "fullchain.pem" -exec openssl x509 -in {} -noout -dates -subject \;
- find /etc/nginx/ssl/ -name "*.pem" -exec openssl x509 -in {} -noout -dates -subject \;
- systemctl list-timers | grep certbot
```

## SSL Hardening

### Prompt: Harden nginx SSL Configuration

```
Review and harden my nginx SSL configuration.

Current config:
[paste ssl-related nginx config]

Server context:
- nginx version: [version]
- OpenSSL version: [version]
- Traffic type: [API / web app / mixed]
- Client compatibility: [modern browsers only / need IE11 / mobile apps]

Provide:
1. TLS protocol configuration (drop old versions)
2. Cipher suite optimization
3. HSTS configuration (with preload consideration)
4. OCSP stapling setup
5. Security headers
6. Session cache tuning
7. Expected SSL Labs grade after changes
8. Any compatibility warnings
```

### Prompt: Achieve SSL Labs A+ Rating

```
I want to achieve an A+ rating on SSL Labs for my domain.

Current SSL Labs result:
- Grade: [current grade]
- Issues flagged: [list issues]

Server:
- nginx [version]
- OpenSSL [version]
- Certificate: [type]

Provide specific nginx configuration changes to:
1. Fix all flagged issues
2. Enable HSTS with proper max-age
3. Configure optimal cipher suites
4. Enable OCSP stapling (if applicable)
5. Disable vulnerable features (SSLv3, TLS 1.0/1.1, RC4, etc.)

Include before/after config comparison.
```

## Cloudflare-Specific

### Prompt: Configure Cloudflare SSL Settings

```
I'm setting up Cloudflare for a domain that currently has direct Let's Encrypt SSL.

Current state:
- Domain: [domain]
- DNS: Managed by [registrar/Cloudflare]
- SSL: Let's Encrypt, auto-renewed
- Applications: [list ports and services]

Target state:
- DNS through Cloudflare (proxied)
- SSL: Full (Strict) with origin certificate
- Keep Let's Encrypt as backup

Provide:
1. Cloudflare SSL/TLS settings to configure
2. Origin certificate generation steps
3. nginx config changes
4. DNS migration steps (minimize downtime)
5. Rollback plan if something breaks
6. Post-migration verification
```

### Prompt: Debug Cloudflare 525/526 Errors

```
I'm getting Cloudflare [525/526] errors on my domain.

Error: [525 SSL Handshake Failed / 526 Invalid SSL Certificate]
Domain: [domain]
Cloudflare SSL mode: [Flexible/Full/Full(Strict)]

Server SSL config:
[paste nginx ssl config]

Origin certificate info:
[paste: openssl x509 -in /path/to/cert.pem -noout -subject -issuer -dates]

Help me fix this by checking:
1. Certificate validity and chain
2. nginx SSL configuration
3. Cloudflare SSL mode compatibility
4. Port 443 accessibility from Cloudflare IPs
5. TLS version compatibility
```
