---
name: nginx-ssl-config
description: Configure nginx as a production reverse proxy with Let's Encrypt SSL, HSTS, gzip, and HTTP→HTTPS redirect in a single server block.
tier: solo
group: server-craft
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a single `/etc/nginx/sites-available/myapp` config that proxies HTTPS traffic to your app on `localhost:3000`, issues and auto-renews a Let's Encrypt certificate via Certbot, enforces HSTS, enables gzip compression, hides the nginx version, and permanently redirects all HTTP traffic to HTTPS.

## Prerequisites

- Ubuntu 22.04 or 24.04 VPS with a public IP address.
- A domain (e.g. `myapp.acmestartup.com`) with an A record pointing at that IP. Replace this with your real domain throughout. Propagation must be complete before Certbot can issue the certificate — confirm with `dig +short A <your-domain>`.
- Root or sudo access on the server.
- nginx installed: `sudo apt install nginx`.
- Certbot installed: `sudo apt install certbot python3-certbot-nginx`.
- Your application already running and listening on `localhost:3000` (e.g., `systemctl status myapp.service` shows `active (running)`).
- Port 80 and 443 open in your firewall (`ufw allow 'Nginx Full'` or equivalent).

## Steps

### Step 1 — Write the initial HTTP-only server block

Create `/etc/nginx/sites-available/myapp`:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name <your-domain>;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Replace `<your-domain>` with your actual domain (e.g. `myapp.acmestartup.com`). Replace `3000` with your app's actual port if different.

### Step 2 — Enable the site and reload nginx

```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/myapp
sudo nginx -t
sudo systemctl reload nginx
```

`nginx -t` must print `syntax is ok` and `test is successful` before you reload. If it reports an error, fix the config before continuing.

### Step 3 — Issue the Let's Encrypt certificate with Certbot

```bash
sudo certbot --nginx -d <your-domain>
```

Certbot will:
1. Ask for an email address for renewal notices.
2. Ask whether to redirect HTTP to HTTPS (choose option **2: Redirect**).
3. Automatically rewrite `/etc/nginx/sites-available/myapp` to add the `ssl` and `443` blocks plus a redirect from port 80.

### Step 4 — Replace the Certbot-generated config with the hardened version

After Certbot finishes, open `/etc/nginx/sites-available/myapp` and replace its full content with the production config below. This version adds HSTS, gzip, and `server_tokens off`. Use your real domain in place of `<your-domain>`:

```nginx
# Redirect HTTP → HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name <your-domain>;
    return 301 https://$host$request_uri;
}

# HTTPS — production config
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name <your-domain>;

    # Let's Encrypt certificate (Certbot manages these paths)
    ssl_certificate     /etc/letsencrypt/live/<your-domain>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<your-domain>/privkey.pem;
    include             /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam         /etc/letsencrypt/ssl-dhparams.pem;

    # Security headers
    server_tokens off;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Gzip
    gzip            on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_proxied    any;
    gzip_types
        text/plain
        text/css
        text/javascript
        application/javascript
        application/json
        application/xml
        image/svg+xml;

    # Reverse proxy to app
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade           $http_upgrade;
        proxy_set_header Connection        "upgrade";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 10s;
    }
}
```

### Step 5 — Validate and reload

```bash
sudo nginx -t && sudo systemctl reload nginx
```

Both commands must succeed. If `nginx -t` fails, re-check that the certificate paths in `ssl_certificate` and `ssl_certificate_key` match what Certbot created (look in `/etc/letsencrypt/live/`).

### Step 6 — Confirm auto-renewal is scheduled

```bash
sudo systemctl status certbot.timer
```

The timer should show `active (waiting)`. Certbot on Ubuntu 22.04+ runs via systemd; it renews certificates that expire within 30 days twice daily. No manual cron job needed.

## Verify

Run a single curl that follows redirects and prints only the HTTP status code and the `Strict-Transport-Security` header:

```bash
curl -sI https://<your-domain> | grep -E "^HTTP|Strict-Transport-Security"
```

Expected output:

```
HTTP/2 200
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

If you see `HTTP/2 200` and the HSTS header, the full stack — proxy pass, TLS, HSTS — is working. If you get a redirect loop, see Troubleshooting below.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `curl: (60) SSL certificate problem` or browser shows "Not secure" | Certificate not yet issued or wrong domain in `ssl_certificate` path | Run `sudo certbot certificates` to list issued certs and confirm the domain matches. Re-issue with `sudo certbot --nginx -d <your-domain>` if missing. |
| Infinite redirect loop (`301 → 301 → …`) | App on port 3000 itself redirects HTTP → HTTPS and nginx is forwarding the HTTPS request as HTTP | Add `proxy_set_header X-Forwarded-Proto https;` (already in the Step 4 config) and configure your app to trust the `X-Forwarded-Proto` header instead of inspecting the raw connection. |
| `nginx -t` fails with `unknown directive "ssl_dhparam"` | `/etc/letsencrypt/ssl-dhparams.pem` missing — Certbot did not run yet | Complete Step 3 first, or generate the file manually: `sudo openssl dhparam -out /etc/letsencrypt/ssl-dhparams.pem 2048`. |
| `502 Bad Gateway` | App on port 3000 is not running | Check `sudo systemctl status myapp.service` and `sudo journalctl -u myapp.service -n 50`. |
| HSTS header missing after reload | Config has `add_header` inside a `location` block, not the `server` block | In nginx, `add_header` inside a child context overrides, not merges, the parent. Keep all `add_header` directives directly in the `server {}` block as shown in Step 4. |
| Certbot renewal dry-run fails | Port 80 blocked by firewall or another process | Run `sudo ufw status` and confirm port 80 is open; `sudo lsof -i :80` to find conflicting processes. |

## Next

- Add rate limiting to protect your proxy: `limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;` in `/etc/nginx/nginx.conf` and `limit_req zone=api burst=10 nodelay;` in the `location` block.
- Harden the server before exposing port 443: `vps-first-deploy` playbook sets up `ufw`, `fail2ban`, and disables root SSH.
- Upgrade HSTS to preload-ready once traffic is stable: `max-age=63072000; includeSubDomains; preload` and submit at https://hstspreload.org.

## References

- [knowledge/solo/infra/server-craft/nginx-reverse-proxy](../../../knowledge/solo/infra/server-craft/nginx-reverse-proxy) — proxy_pass patterns, upstream header forwarding, and the `Upgrade`/`Connection` headers required for WebSocket pass-through used verbatim in the Step 4 location block.
- [knowledge/solo/infra/server-craft/ssl-tls-management](../../../knowledge/solo/infra/server-craft/ssl-tls-management) — Certbot issuance flow, `options-ssl-nginx.conf` include, and the dhparam file path that backs Steps 3–5 and the ssl_dhparam troubleshooting entry.
