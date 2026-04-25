# Agent Integration — nginx Reverse Proxy

## When to use
- Setting up a new domain on the server (creating a site config in sites-available)
- Adding WebSocket proxy support to an existing site
- Diagnosing a 502/504 or header-related bug between nginx and a backend
- Auditing nginx configs for security header completeness
- Migrating a site from HTTP-only to HTTPS with Cloudflare or certbot
- Adding rate limiting to an API endpoint

## When NOT to use
- Serving pure static sites where a CDN (Cloudflare Pages, Netlify) handles routing entirely
- Microservices behind a managed load balancer (AWS ALB, GCP LB) — nginx adds unnecessary hops
- Development environments — use Caddy or the framework's dev server directly

## Where it fails / limitations
- `add_header` in a `location` block silently overrides all `add_header` directives from the parent `server` block — security headers defined at server level disappear for matching locations
- Trailing slash behavior in `proxy_pass` is non-obvious and inconsistent: `proxy_pass http://backend/` strips the location prefix; `proxy_pass http://backend` does not
- WebSocket connections need `proxy_read_timeout 86400` — default 60s causes silent disconnects for long-lived connections
- Cloudflare real IP restoration (`set_real_ip_from`) must cover all Cloudflare CIDR ranges; Cloudflare periodically adds new ranges without notice
- Rate limiting applies per worker process unless the zone uses shared memory (`zone=api:10m`); using per-worker zones causes inconsistent limiting under load

## Agentic workflow
An agent handles nginx tasks by reading the existing config structure, identifying the snippet files in use, then generating or patching site configs. For new domains, the agent creates a file in `sites-available/` and symlinks it to `sites-enabled/`, runs `nginx -t` to validate, then reloads. For debugging, the agent reads access/error logs, correlates with the backend service logs, and identifies the failure point. The agent must always validate with `nginx -t` before reloading and must check for the `add_header` inheritance pitfall when modifying location blocks.

### Recommended subagents
- `faion-sdd-executor-agent` — execute SDD tasks that include nginx config changes as part of a larger deploy feature

### Prompt pattern
```
Create an nginx site config for domain api.example.com that proxies:
- /api/ → http://127.0.0.1:8100/ (FastAPI)
- /ws   → http://127.0.0.1:8100 (WebSocket, long-lived)
- /     → /var/www/api.example.com/public (static SPA)
Include security headers, rate limiting (10r/s for /api/, 3r/m for /api/auth/login),
and include snippets/proxy-params.conf for proxy headers.
Output the complete site config file.
```

```
Review /etc/nginx/sites-available/nero.faion.net and identify any issues with:
header inheritance across server/location blocks, missing WebSocket timeout,
rate limiting zones, and Cloudflare real IP configuration.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `nginx -t` | Validate config syntax | Built-in |
| `nginx -T` | Print full effective config | Built-in |
| `nginx -s reload` | Graceful reload (zero downtime) | Built-in |
| `websocat` | Test WebSocket connections from CLI | `cargo install websocat` / [GitHub](https://github.com/vi/websocat) |
| `curl -vI` | Inspect HTTP response headers | Built-in (system) |
| `testssl.sh` | Comprehensive TLS/cipher audit | [GitHub](https://github.com/drwetter/testssl.sh) |
| `logrotate` | Rotate nginx access/error logs | `apt install logrotate` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cloudflare (proxy mode) | SaaS | Partial | REST API for zone/DNS management; real IP header requires `CF-Connecting-IP` configuration |
| Let's Encrypt / certbot | OSS | Yes | CLI-driven cert issuance; `--nginx` plugin auto-edits site configs |
| Mozilla SSL Config Generator | SaaS | Yes | Generates nginx TLS config for chosen policy (modern/intermediate) |
| SecurityHeaders.com | SaaS | Yes | HTTP header audit by URL; returns letter grade |
| SSL Labs | SaaS | Partial | Deep TLS audit; rate-limited for automation |
| ModSecurity (nginx module) | OSS | Partial | WAF for nginx; config is complex, rarely needed behind Cloudflare |

## Templates & scripts
See templates.md for complete site config templates. Key snippet pattern:

```nginx
# /etc/nginx/snippets/proxy-params.conf
proxy_set_header Host              $host;
proxy_set_header X-Real-IP         $remote_addr;
proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto https;
proxy_http_version                 1.1;
proxy_buffering                    off;
proxy_connect_timeout              10s;
proxy_send_timeout                 60s;
proxy_read_timeout                 60s;
```

```nginx
# /etc/nginx/snippets/security-headers.conf
add_header X-Content-Type-Options  "nosniff"                          always;
add_header X-Frame-Options         "SAMEORIGIN"                       always;
add_header Referrer-Policy         "strict-origin-when-cross-origin"  always;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
add_header Permissions-Policy      "camera=(), microphone=()"         always;
```

## Best practices
- Use the snippets pattern (`include snippets/proxy-params.conf`) — repeat `add_header` in every `location` block that needs headers, because nginx does not inherit them from parent blocks
- Always add `always` flag to `add_header` — without it, headers are only sent on 2xx/3xx responses, not on 4xx/5xx
- Set `proxy_http_version 1.1` and `proxy_set_header Connection ""` for upstream keepalive connection pooling (reduces latency)
- Define `upstream` blocks with `keepalive 32` even for single-server setups — enables connection reuse
- Use `try_files $uri $uri/ /index.html` for SPAs to handle client-side routing
- Rate limit only `/api/` and auth endpoints, not static assets — blocking legitimate users causes support issues
- Test config with `nginx -t` before and after every change; never edit production configs without a rollback plan
- Keep Cloudflare IP ranges current by fetching `https://www.cloudflare.com/ips-v4` and `ips-v6` periodically

## AI-agent gotchas
- Agent must not use `nginx -s reload` before `nginx -t` passes — reloading an invalid config causes nginx worker crash with no automatic recovery on some configs
- The trailing-slash rule in `proxy_pass` is a common source of 404 bugs: `proxy_pass http://backend/api/` (trailing slash) strips the location prefix; `proxy_pass http://backend/api` (no slash) does not — agent must verify intent
- `add_header` in a nested `location` block silently drops all headers from the enclosing `server` block — agent must repeat all security headers in every `location` block, or use `include snippets/security-headers.conf` inside each location
- Symlink creation for sites-enabled must use relative paths (`ln -s ../sites-available/domain sites-enabled/domain`), not absolute paths, to survive directory moves
- After certbot renews a certificate, nginx must be reloaded — agent should ensure the renewal hook exists at `/etc/letsencrypt/renewal-hooks/post/reload-nginx.sh`

## References
- https://nginx.org/en/docs/http/ngx_http_proxy_module.html
- https://nginx.org/en/docs/http/ngx_http_limit_req_module.html
- https://ssl-config.mozilla.org/
- https://securityheaders.com/
- https://www.cloudflare.com/ips/
- https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/
