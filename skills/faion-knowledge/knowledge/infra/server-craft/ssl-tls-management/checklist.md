# SSL/TLS Management Checklist

## Pre-Setup Assessment

- [ ] Identify all domains and subdomains requiring HTTPS
- [ ] Decide certificate strategy: Let's Encrypt, Cloudflare Origin, or both
- [ ] Check DNS configuration (A/AAAA records point to server)
- [ ] Verify ports 80 and 443 are open in firewall (`sudo ufw status`)
- [ ] Check if Cloudflare proxy is enabled (orange cloud) or DNS-only (gray cloud)
- [ ] Back up existing nginx configuration

## Let's Encrypt Setup

### Installation

- [ ] Install certbot: `sudo apt install certbot python3-certbot-nginx`
- [ ] Verify nginx is running and serving the domain
- [ ] Ensure `.well-known/acme-challenge/` is accessible (for webroot method)

### Certificate Issuance

- [ ] Run certbot with appropriate plugin (nginx, standalone, or webroot)
- [ ] Verify certificate files exist in `/etc/letsencrypt/live/{domain}/`
- [ ] Check `fullchain.pem` includes both cert and intermediate
- [ ] Verify private key permissions are 600

### Auto-Renewal

- [ ] Confirm systemd timer is active: `systemctl list-timers | grep certbot`
- [ ] Test dry-run: `sudo certbot renew --dry-run`
- [ ] Create post-renewal hook to reload nginx
- [ ] Make hook executable: `chmod +x`

## Cloudflare Origin Certificate Setup

### Certificate Generation

- [ ] Generate origin certificate in Cloudflare Dashboard (SSL/TLS -> Origin Server)
- [ ] Include both apex domain and wildcard (`example.com`, `*.example.com`)
- [ ] Set maximum validity (15 years)
- [ ] Save certificate PEM to `/etc/nginx/ssl/cloudflare-origin.pem`
- [ ] Save private key PEM to `/etc/nginx/ssl/cloudflare-origin-key.pem`
- [ ] Set key file permissions: `chmod 600`

### Cloudflare Configuration

- [ ] Set SSL/TLS mode to **Full (Strict)**
- [ ] Enable **Always Use HTTPS**
- [ ] Enable **Automatic HTTPS Rewrites**
- [ ] Set **Minimum TLS Version** to 1.2
- [ ] Enable TLS 1.3
- [ ] Enable HSTS in Cloudflare (if not doing it in nginx)

## nginx SSL Configuration

### SSL Server Block

- [ ] Create SSL snippet file (`/etc/nginx/snippets/ssl-params.conf`)
- [ ] Set `ssl_protocols TLSv1.2 TLSv1.3;`
- [ ] Configure strong cipher suites
- [ ] Set `ssl_prefer_server_ciphers off;` (let client choose for TLS 1.3)
- [ ] Configure session cache: `ssl_session_cache shared:SSL:10m;`
- [ ] Set `ssl_session_timeout 1d;`
- [ ] Disable session tickets: `ssl_session_tickets off;`

### Certificate References

- [ ] Point `ssl_certificate` to fullchain/origin cert
- [ ] Point `ssl_certificate_key` to private key
- [ ] If using Let's Encrypt with OCSP: enable `ssl_stapling on;`
- [ ] Set resolver for OCSP: `resolver 1.1.1.1 8.8.8.8;`

### HTTP to HTTPS Redirect

- [ ] Create port 80 server block with 301 redirect to HTTPS
- [ ] Exception: Keep `.well-known/acme-challenge/` on port 80 for certbot
- [ ] Test redirect: `curl -I http://example.com`

### Security Headers

- [ ] Add HSTS header: `Strict-Transport-Security: max-age=63072000;`
- [ ] Add `X-Frame-Options: SAMEORIGIN`
- [ ] Add `X-Content-Type-Options: nosniff`
- [ ] Add `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] Add `Permissions-Policy` with restrictive defaults

### DH Parameters (TLS 1.2)

- [ ] Generate: `openssl dhparam -out /etc/nginx/dhparam.pem 2048`
- [ ] Reference in nginx: `ssl_dhparam /etc/nginx/dhparam.pem;`

## Verification

### Certificate Checks

- [ ] Verify HTTPS loads in browser without warnings
- [ ] Check certificate chain: `echo | openssl s_client -connect domain:443`
- [ ] Verify TLS 1.3 works: `openssl s_client -connect domain:443 -tls1_3`
- [ ] Verify TLS 1.0/1.1 rejected: `openssl s_client -connect domain:443 -tls1`
- [ ] Test with curl: `curl -vI https://domain 2>&1 | grep TLS`

### Security Scoring

- [ ] Run SSL Labs test (aim for A+): `https://ssllabs.com/ssltest`
- [ ] Run Mozilla Observatory: `https://observatory.mozilla.org`
- [ ] Check security headers: `curl -I https://domain`

### Renewal Verification

- [ ] For Let's Encrypt: confirm renewal timer fires correctly
- [ ] For Cloudflare Origin: note expiry date (15 years), set calendar reminder
- [ ] Test nginx reload after renewal: `sudo nginx -t && sudo systemctl reload nginx`

## Post-Setup

- [ ] Document certificate type and expiry in server runbook
- [ ] If using Let's Encrypt: set monitoring alert for cert expiry (14 days warning)
- [ ] Remove any unused/old certificates
- [ ] Verify no mixed content warnings in browser console
- [ ] Test all subdomains are covered by certificate
