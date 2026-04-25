# Agent Integration — SSL/TLS Management

## When to use
- Setting up HTTPS for a new domain on nginx
- Migrating from Cloudflare "Flexible" mode to "Full (Strict)" with a proper origin certificate
- Auditing TLS configuration for grade (SSL Labs A+) and header completeness
- Diagnosing SSL errors: redirect loops, mixed content, certificate mismatch, 526 errors
- Rotating or renewing Let's Encrypt certificates
- Issuing a 15-year Cloudflare origin certificate to eliminate renewal complexity

## When NOT to use
- Domains served behind Cloudflare where the backend is localhost-only and Full(Strict) is already configured — the work is done
- Internal services only reachable via WireGuard VPN — self-signed certs are acceptable there
- Short-lived development environments — use `mkcert` for local HTTPS, not production certs

## Where it fails / limitations
- Cloudflare origin certificates are only trusted by Cloudflare edge — a client connecting directly to the origin IP will get an untrusted certificate error; always use Let's Encrypt if bypassing Cloudflare is possible
- OCSP stapling does not work with Cloudflare origin certificates — they have no OCSP responder; enabling `ssl_stapling on` with an origin cert causes nginx to log errors
- `ssl_session_tickets off` is correct for forward secrecy but breaks TLS session resumption — slight performance cost for high-traffic sites; acceptable for most solo developer platforms
- HSTS `preload` is permanent — once a domain is in the browser preload list, removal takes 6-18 months; only add after all subdomains reliably serve HTTPS
- certbot `--nginx` plugin modifies the nginx config in place and may produce awkward formatting or duplicate directives on re-run; review after first issuance
- Wildcard Let's Encrypt certificates require DNS-01 challenge (Cloudflare DNS API), not HTTP-01; HTTP-based issuance only works for exact domain matches

## Agentic workflow
An agent handles TLS work by identifying the current certificate type (Cloudflare origin vs Let's Encrypt vs self-signed) via `openssl s_client`, checking expiry, verifying Cloudflare SSL mode via the API, and either configuring certbot or generating the nginx config for origin certs. For audits, the agent runs `curl -vI` against the domain and parses the response headers against the expected security header set. For Cloudflare origin cert setup, the agent generates the nginx SSL block using the stored cert path and verifies with `nginx -t` before reloading.

### Recommended subagents
- `faion-sdd-executor-agent` — execute multi-domain SSL setup as part of a server provisioning SDD feature

### Prompt pattern
```
Set up HTTPS for domain example.faion.net on this nginx server.
Context: domain is behind Cloudflare proxy, SSL mode is Full(Strict).
Certificate: Cloudflare origin cert stored at /etc/nginx/ssl/cf-origin.pem (key at cf-origin-key.pem).
Output: complete nginx server block with TLS 1.2/1.3, session settings, HSTS, OCSP stapling OFF,
and security headers. Use Mozilla Intermediate profile cipher suites.
```

```
Audit the TLS configuration for api.example.com.
Run these checks and report findings:
1. Certificate type, issuer, expiry date
2. TLS protocols supported (1.0/1.1/1.2/1.3)
3. Security headers present (HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy)
4. Redirect chain from HTTP to HTTPS
Report issues and exact nginx config lines to fix each.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `certbot` | Let's Encrypt certificate management | `apt install certbot python3-certbot-nginx` / [docs](https://certbot.eff.org/) |
| `openssl s_client` | TLS handshake inspection and cert details | Built-in (openssl package) |
| `openssl x509` | Parse certificate fields (dates, subject, SANs) | Built-in |
| `openssl dhparam` | Generate DH parameters for TLS 1.2 DHE | Built-in |
| `testssl.sh` | Comprehensive CLI TLS audit | [GitHub](https://github.com/drwetter/testssl.sh) |
| `mkcert` | Locally-trusted dev certificates | [GitHub](https://github.com/FiloSottile/mkcert) |
| `curl` | HTTP/HTTPS header inspection | Built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Let's Encrypt | OSS CA | Yes | Free, automated via certbot; 90-day certs with auto-renewal timer |
| Cloudflare SSL | SaaS | Yes | API for SSL mode, origin cert generation, HSTS settings; REST API at `api.cloudflare.com` |
| SSL Labs | SaaS | Partial | Free TLS audit; rate-limited API; use for one-time audit, not CI |
| Mozilla SSL Config Generator | SaaS | Yes | Generates nginx/Apache TLS config for Modern/Intermediate/Old profiles |
| Mozilla Observatory | SaaS | Yes | HTTP header audit with grading; API available |
| Hardenize | SaaS | Partial | Combined SSL + email + DNS audit |

## Templates & scripts
See templates.md for complete nginx SSL blocks. Key nginx TLS block:

```nginx
# Paste into server block after ssl_certificate directives
ssl_protocols              TLSv1.2 TLSv1.3;
ssl_ciphers                ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers  off;
ssl_session_timeout        1d;
ssl_session_cache          shared:SSL:10m;
ssl_session_tickets        off;

# OCSP stapling — only with Let's Encrypt or commercial certs, NOT Cloudflare origin
# ssl_stapling               on;
# ssl_stapling_verify        on;
# resolver                   1.1.1.1 8.8.8.8 valid=300s;

# Security headers (repeat in every location block that uses add_header)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
add_header X-Content-Type-Options   "nosniff"                              always;
add_header X-Frame-Options          "SAMEORIGIN"                           always;
add_header Referrer-Policy          "strict-origin-when-cross-origin"      always;
add_header Permissions-Policy       "camera=(), microphone=()"             always;
```

## Best practices
- For Cloudflare-proxied sites, use Cloudflare origin certificates (15-year validity) over Let's Encrypt — eliminates renewal risk entirely and avoids rate limits
- Always use Full (Strict) Cloudflare SSL mode — Flexible mode sends HTTP to the origin and creates a false sense of security
- Do not enable OCSP stapling with Cloudflare origin certs — they have no OCSP responder and nginx will log connection errors to Cloudflare's non-existent OCSP endpoint
- Include `ssl_session_tickets off` — TLS session tickets, if compromised, allow retroactive decryption of all sessions
- Test with `curl -vI https://domain 2>&1 | grep -E "(SSL|HTTP|<)"` before and after config changes
- Run `sudo certbot renew --dry-run` after initial certbot setup to verify the renewal flow works
- Store Cloudflare origin cert private keys with `chmod 600 /etc/nginx/ssl/*.pem`

## AI-agent gotchas
- Agent must not enable `ssl_stapling on` for Cloudflare origin certificates — they have no OCSP endpoint; enabling it causes error log spam and potential nginx startup delay
- Cloudflare "Flexible" SSL mode means the agent sees `$scheme = https` at the nginx level even though the backend received plain HTTP — this makes `X-Forwarded-Proto` unreliable; always use Full(Strict)
- Let's Encrypt issues certificates for specific domains; if certbot is configured with `--nginx` and multiple domains exist, it may insert config into the wrong server block — agent must verify which block received the cert directives
- certbot timer creates `/etc/cron.d/certbot` or a systemd timer depending on installation method — agent must check both to confirm auto-renewal is configured
- `add_header Strict-Transport-Security ... always;` in a `server` block is silently overridden in any `location` block that has its own `add_header` — agent must add HSTS to every `location` block or use a snippet include pattern
- After adding `preload` to HSTS, the domain must be submitted to `hstspreload.org` — the browser list is not automatically updated; do not add `preload` unless the intent is to submit

## References
- https://certbot.eff.org/instructions
- https://ssl-config.mozilla.org/
- https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/
- https://github.com/drwetter/testssl.sh
- https://hstspreload.org/
- https://observatory.mozilla.org/
