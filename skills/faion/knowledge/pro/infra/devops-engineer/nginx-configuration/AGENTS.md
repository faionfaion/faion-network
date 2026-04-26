# Nginx Configuration

## Summary

Nginx as high-performance HTTP server, reverse proxy, and load balancer. Key production requirements: TLS 1.2/1.3 only, `server_tokens off`, all security headers (HSTS, X-Frame-Options, X-Content-Type-Options), rate limiting, and gzip compression. Always test with `nginx -t` before reload.

## Why

Misconfigured Nginx is the most common vector for information leakage (version in headers), clickjacking, and MITM attacks. A properly configured instance achieves SSL Labs A+ grade with zero extra cost and handles 400k-500k req/s at cluster scale. TLS 1.0/1.1 must be disabled; Let's Encrypt deprecated OCSP in August 2025.

## When To Use

- Serving static sites or SPA frontends with aggressive cache headers
- Reverse proxying backend services with proper `X-Forwarded-*` headers
- SSL/TLS termination with Let's Encrypt certificates
- Load balancing across multiple upstream backends
- Rate limiting login/API endpoints to prevent brute-force

## When NOT To Use

- Dynamic application logic — Nginx is a proxy, not an app server
- Complex routing rules that require request body inspection — use Envoy or Traefik
- Kubernetes ingress at scale — use a dedicated ingress controller (nginx-ingress, Traefik)
- Service mesh traffic management — that's Istio/Linkerd territory

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-config.xml` | worker_processes, keepalive, gzip, security directives, TLS configuration rules |
| `content/02-patterns.xml` | Reverse proxy pattern, load balancing methods, WebSocket support, caching setup |
| `content/03-checklist.xml` | Pre-deployment checklist rules: SSL, headers, rate limiting, compression, logging |

## Templates

| File | Purpose |
|------|---------|
| `templates/ssl-params.conf` | TLS protocol/cipher/session snippet (include in server blocks) |
| `templates/security-headers.conf` | HSTS, X-Frame-Options, CSP, Referrer-Policy, Permissions-Policy snippet |
| `templates/proxy-params.conf` | Proxy headers, timeouts, buffering snippet |
| `templates/static-site.conf` | Full static site vhost with HTTPS redirect and cache headers |
| `templates/reverse-proxy.conf` | Full reverse proxy vhost template |
| `templates/rate-limit.conf` | Rate limiting zones and location-level directives |
