---
name: cloudflare-dns-free-ssl
description: Add an A record pointing your domain at a server, enable Cloudflare proxy, and configure Full (Strict) SSL so your site loads over HTTPS with a green padlock.
tier: free
group: hosting-infra
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have an A record routing `yourdomain.com` (and `www.yourdomain.com`) to your server IP, Cloudflare's orange-cloud proxy active, SSL/TLS mode set to "Full (Strict)", and a valid HTTPS certificate visible in the browser.

## Prerequisites

- Your domain is already on Cloudflare nameservers and the zone shows "Active" (see `buy-domain-namecheap-cloudflare`).
- You know your server's public IPv4 address (e.g. `46.225.58.119`).
- Your origin server has a valid TLS certificate installed (self-signed is fine for Full Strict — Cloudflare validates the cert is present, not that it's from a public CA; use a Cloudflare Origin Certificate if you don't have one).
- A Cloudflare account with access to the DNS zone for your domain.

## Steps

1. Sign in at https://dash.cloudflare.com and click on your domain in the zone list.

2. In the left sidebar, click **DNS** → **Records**.

3. Click **Add record**. Fill in:
   - **Type**: `A`
   - **Name**: `@` (represents the root domain, e.g. `yourdomain.com`)
   - **IPv4 address**: your server IP, e.g. `46.225.58.119`
   - **Proxy status**: click the cloud icon so it turns orange (Proxied)
   - **TTL**: Auto
   Click **Save**.

4. Click **Add record** again to cover the `www` subdomain:
   - **Type**: `A`
   - **Name**: `www`
   - **IPv4 address**: same server IP
   - **Proxy status**: orange cloud (Proxied)
   - **TTL**: Auto
   Click **Save**.

5. In the left sidebar, click **SSL/TLS** → **Overview**.

6. Under "Your SSL/TLS encryption mode is currently:", click **Configure** (or select from the radio buttons). Choose **Full (strict)** and click **Save**.

7. In the left sidebar, click **SSL/TLS** → **Edge Certificates**. Confirm "Always Use HTTPS" is toggled **On**. If it is off, click the toggle to enable it.

8. Wait 1–2 minutes for the SSL mode change to propagate through Cloudflare's edge.

## Verify

Run the following command, replacing `yourdomain.com` with your actual domain:

```
curl -sI https://yourdomain.com | head -5
```

Expected output includes `HTTP/2 200` (or `HTTP/1.1 200 OK`). If you see `HTTP/2 301` followed by `location: https://www.yourdomain.com`, that is fine — follow up with:

```
curl -sI https://www.yourdomain.com | head -5
```

Also open `https://yourdomain.com` in a browser — the address bar must show a padlock icon with no warnings. Click the padlock → **Connection is secure** → **Certificate is valid** to confirm Cloudflare is serving the edge certificate.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Browser shows "SSL_ERROR_RX_RECORD_TOO_LONG" or "ERR_SSL_PROTOCOL_ERROR" | SSL mode is "Flexible" but origin serves HTTP only, causing a mixed redirect loop | Set SSL/TLS → Overview → **Full (strict)** and ensure origin has a valid TLS cert |
| `curl` returns `526 Invalid SSL Certificate` | Origin certificate is expired, self-signed without a Cloudflare Origin Cert, or missing entirely | Issue a Cloudflare Origin Certificate: SSL/TLS → Origin Server → Create Certificate; install the `.pem` + `.key` on your server |
| `curl` returns `525 SSL Handshake Failed` | Origin server is not listening on port 443 | Confirm your web server (nginx, caddy, etc.) is configured to listen on 443 with TLS |
| Site loads over HTTP despite "Always Use HTTPS" being on | Browser cached an HTTP redirect; or Cloudflare change not yet propagated | Clear browser cache or test in private/incognito mode; wait 2 minutes |
| DNS record shows grey cloud (DNS-only) instead of orange | Proxy status was left as "DNS only" when adding the record | Click the record → edit → click the cloud icon until it turns orange → Save |
| `curl` returns `521 Web Server Is Down` | Cloudflare cannot reach origin on port 80 or 443 | Check firewall rules — Cloudflare proxy IPs must be allowed: https://www.cloudflare.com/ips/ |

## Next

- Issue a Cloudflare Origin Certificate (SSL/TLS → Origin Server → Create Certificate) to eliminate any self-signed cert warning from origin-direct access.
- Enable **HTTP/3 (QUIC)** in SSL/TLS → Edge Certificates → HTTP/3 for faster connections on supported browsers.
- Explore `deploy-to-vercel-free` or `deploy-static-site-github-pages` if you want a zero-server static host instead of a VPS.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the read-state-first, apply-minimal-change, verify-with-a-query pattern from this methodology directly maps to how this playbook adds DNS records: inspect existing records before adding, make one targeted change per record, confirm with `curl -sI` rather than trusting the Cloudflare UI alone.
