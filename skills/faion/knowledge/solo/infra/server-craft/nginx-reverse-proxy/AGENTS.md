# nginx Reverse Proxy

## Summary

Configure nginx as a multi-domain reverse proxy on a single VPS: proxy_pass to backend services, WebSocket upgrades, security headers, rate limiting, and the snippets pattern for DRY configuration. Architecture: Internet → Cloudflare → nginx (80/443) → local services on 127.0.0.1:PORT.

## Why

nginx is the standard single entry point for all domains on a VPS. It terminates SSL, handles WebSocket upgrades, applies security headers consistently, rate-limits API endpoints, and serves static files — none of which backends need to implement themselves.

## When To Use

- Deploying any web application on a VPS that needs HTTP/HTTPS routing
- Exposing multiple domains or subdomains from a single server
- Adding WebSocket support to an existing proxy setup
- Applying security headers (HSTS, CSP, X-Content-Type-Options) across all sites
- Rate limiting API endpoints against brute-force or abuse

## When NOT To Use

- When using a managed platform (Heroku, Railway, Render) — proxy is handled for you
- Kubernetes environments — use an Ingress controller instead
- When Caddy or Traefik is already in use — don't mix reverse proxies on the same server
- For TLS termination when Cloudflare Full(Strict) mode is configured — Cloudflare already handles the browser-facing TLS, nginx still needs a cert for origin

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-directives.xml` | proxy_pass trailing-slash rule, WebSocket upgrade map, proxy headers, upstream blocks |
| `content/02-security-and-limits.xml` | Security headers (HSTS, CSP, X-Frame), rate limiting zones, common pitfalls |
| `content/03-examples.xml` | Real NERO platform config, MeetingTax multi-subdomain, adding a new domain |

## Templates

| File | Purpose |
|------|---------|
| `templates/proxy-params.conf` | Reusable snippet: Host, X-Real-IP, X-Forwarded-For, X-Forwarded-Proto headers |
| `templates/websocket.conf` | Reusable snippet: HTTP/1.1 upgrade headers, 24h timeouts |
| `templates/security-headers.conf` | Reusable snippet: HSTS, X-Content-Type-Options, Referrer-Policy, X-Frame-Options |
| `templates/rate-limiting.conf` | http-context zones: api_general (10r/s), api_auth (3r/m), api_upload (5r/m) |
| `templates/cloudflare-realip.conf` | set_real_ip_from for all Cloudflare IP ranges |
| `templates/site-fullstack.conf` | Full-stack app template: API prefix-strip, WebSocket, X-Accel-Redirect, SPA |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/nginx-audit.sh` | Audit active sites, snippets, rate-limit zones, security headers, recent errors |
