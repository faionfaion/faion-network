# Agent Integration — Nginx Configuration

## When to use
- Reverse-proxying app servers (Django/FastAPI/Node/Go) on Linux VMs (the faion-net pattern: Django on `:8000`, nginx as TLS+vhost router).
- Static-site hosting (Gatsby/Hugo/Next.js export) with cache-control + gzip/brotli.
- TLS termination + automatic ACME (certbot / acme.sh / `lego`).
- Per-vhost rate limiting, security headers, WebSocket proxying, gRPC proxying.
- Multi-tenant subdomain routing under one server with includes/snippets.
- Lightweight load balancing (round-robin / least_conn) before introducing a proper LB.

## When NOT to use
- High-throughput global edge (use Cloudflare / Fastly / Front Door).
- Application-aware routing with complex rule engines (use Envoy/Kong/Traefik with config-from-CRD).
- Service mesh sidecars (use Envoy/Linkerd-proxy; nginx isn't xDS-native).
- Kubernetes ingress at scale (`nginx-ingress` works but ingress-nginx CRDs are different from raw nginx; don't conflate).
- Anywhere you need OIDC/SSO at the proxy without nginx-plus or third-party Lua/njs modules.

## Where it fails / limitations
- `proxy_pass http://upstream;` with trailing slash vs without changes path semantics — agents flip a slash and break routing silently.
- `proxy_set_header Host $host;` is required for vhost routing on the upstream; default `proxy_set_header Host $proxy_host;` sends the upstream's IP — agents miss it and the upstream returns 404.
- `client_max_body_size` defaults to 1MB; file upload endpoints break with 413; needs to be set at `server` or `location` level, not just `http`.
- WebSockets need `Upgrade` + `Connection` headers; HTTP/1.1 forced; without `proxy_http_version 1.1;` the connection downgrades and breaks.
- TLSv1.0/1.1 still appear in `ssl-config.mozilla.org` legacy presets — agents copy the legacy preset and Qualys grade drops to B.
- `gzip on;` plus a CDN that compresses again can corrupt response bodies; force one layer.
- Rate limiting (`limit_req_zone`) keyed on `$binary_remote_addr` behind a CDN/LB rate-limits the LB IP, not the user. Use `$http_x_forwarded_for` after `set_real_ip_from` is configured — and only those.
- `location /` order pitfalls: prefix vs regex matching — agents reorder and inadvertently shadow auth gates.
- `add_header` does NOT inherit if a child `location` declares any `add_header`; security headers vanish in subroutes. Use `more_set_headers` (headers-more module) or repeat per location.
- Reload (`nginx -s reload`) preserves SSL cert pinning state; if certs rotated but workers didn't, browsers see stale certs. Always `nginx -t && systemctl reload nginx` and verify with `openssl s_client`.

## Agentic workflow
Treat nginx config as code with strict CI gates: `nginx -t` inside a container with the same nginx version as prod; if it passes, render diffs against the live `nginx -T` output; require human review for any change to TLS, security headers, or rate limits; auto-merge for routine vhost adds. One agent generates config from a template (variables: domain, upstream, port, TLS cert path, headers); a reviewer agent (Opus) checks for the failure modes above. Deploy via SCP + `systemctl reload nginx` with a rollback symlink.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → config → review → deploy → verify.
- A custom `nginx-config-auditor` (Opus, read-only) — given the diff + `nginx -T` output, checks: trailing-slash mismatch, missing `Host` header, missing WebSocket headers, weak TLS, header-inheritance loss, rate-limit keying.
- `password-scrubber-agent` — auth_basic_user_file paths, GitHub deploy keys.

### Prompt pattern
```
Generate nginx vhost for <domain>.
Inputs: upstream (host:port), TLS provider (certbot/cloudflare-origin), HTTP/2 + HTTP/3?, websocket?, max upload size, security headers preset (strict|moderate|legacy), rate limit (rps|off).
Output: (1) /etc/nginx/sites-available/<domain> file, (2) snippet usage list, (3) certbot/acme commands, (4) reload + verify steps (curl -I, openssl s_client, qualys link), (5) rollback steps.
Forbid: TLSv1.0/1.1, server_tokens on, missing security headers, missing `proxy_set_header Host`, missing `client_max_body_size`, gzip+CDN double compression.
```

```
Audit diff. Produce JSON: {trailing_slash_changes:[], host_header_changes:[], tls_changes:[], header_inheritance_breaks:[], rate_limit_changes:[], approve:bool}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `nginx -t` / `nginx -T` | Test + dump effective config | builtin |
| `nginx -s reload` / `systemctl reload nginx` | Hot reload | builtin |
| `certbot` / `acme.sh` / `lego` | ACME issuance + renewal | https://eff-certbot.readthedocs.io / https://acme.sh / https://go-acme.github.io/lego/ |
| `openssl s_client -connect host:443 -servername host` | TLS handshake debug | builtin |
| `curl -I` / `curl -v --resolve` | Header + cache + cert checks | builtin |
| `ngxtop` | Live access-log analysis | https://github.com/lebinh/ngxtop |
| `goaccess` | Real-time log analyzer dashboard | https://goaccess.io/ |
| `nginx-prometheus-exporter` | Stub-status → Prometheus | https://github.com/nginxinc/nginx-prometheus-exporter |
| `gixy` | nginx config security linter | https://github.com/yandex/gixy |
| `nginxconfig.io` | Mozilla-aligned config generator | https://www.digitalocean.com/community/tools/nginx |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| nginx OSS | OSS | Yes | Default; bundled in Debian/Ubuntu/RHEL. |
| nginx Plus (F5) | Commercial | Yes | API-driven dynamic upstreams, JWT auth, OIDC. |
| OpenResty | OSS | Yes | nginx + Lua; powerful but agents must understand `*_by_lua_block` semantics. |
| Caddy | OSS | Yes | Automatic HTTPS; simpler than nginx — consider for greenfield. |
| Traefik | OSS | Yes | Better with K8s/Docker labels; if you're on a VM, nginx is simpler. |
| Cloudflare Origin Cert + nginx | SaaS + OSS | Yes | 15-year origin cert; pair with `authenticated origin pulls`. |
| Let's Encrypt | SaaS (free) | Yes | ACME via certbot/acme.sh; rate limits real. |
| ZeroSSL | SaaS | Yes | Alternative ACME CA; useful when LE rate-limits. |
| nginx-prometheus-exporter | OSS | Yes | `/stub_status` to Prometheus. |
| Mozilla SSL Configuration Generator | tool | Yes | Authoritative for cipher suite presets. |

## Templates & scripts
See `templates.md` for full main + snippets + vhost. Inline secure-vhost skeleton (≤40 lines):

```nginx
# /etc/nginx/sites-available/example.com
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    return 301 https://example.com$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;       # TLS1.2/1.3, OCSP, modern ciphers
    include /etc/nginx/snippets/security-headers.conf; # HSTS, CSP, X-Frame-Options, ...

    client_max_body_size 25m;
    server_tokens off;

    # Rate limit at server scope; key by real client IP.
    limit_req zone=api_burst burst=20 nodelay;

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Real-IP         $remote_addr;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_set_header   Upgrade           $http_upgrade;
        proxy_set_header   Connection        $connection_upgrade;  # via map
        proxy_read_timeout 60s;
    }

    location ~ /\.(git|env|hg|svn) { deny all; access_log off; log_not_found off; }
}
```

## Best practices
- One snippet per concern (`ssl-params.conf`, `security-headers.conf`, `proxy-params.conf`); include into vhosts. Keeps drift centralized.
- Pin nginx version (apt pin or container digest) — major versions change defaults (e.g. http2 + http3 syntax).
- TLS via Mozilla "Intermediate" preset by default; "Modern" only when you control all clients.
- HSTS: start with `max-age=300` for one week, validate, then `max-age=63072000; includeSubDomains; preload` and submit to hstspreload.org.
- CSP: deploy in `Content-Security-Policy-Report-Only` mode for a week, collect violations via report-uri, then enforce.
- `error_log` at `warn` in prod; `info`/`debug` only when debugging — debug at scale fills disk.
- Access logs in JSON (`log_format json escape=json`) → ship to Loki/ELK.
- Run `gixy` in CI; treat findings as blockers.
- Keep `/etc/nginx` in Git; deploy via rsync + `nginx -t` precheck.
- For HTTP/3: needs nginx 1.25+ with QUIC build, UDP/443 open, separate `listen 443 quic;`.

## AI-agent gotchas
- LLMs hallucinate `proxy_pass` semantics: `proxy_pass http://up/;` strips matched prefix, `proxy_pass http://up;` doesn't. Always show both forms in tests before merging.
- Agents copy "Modern" Mozilla TLS preset onto a B2C site with old Android clients; users get handshake failures. Always check client compat.
- `add_header` overshadowing: agent adds a single new header in a `location` block, suddenly the global HSTS header disappears for that route. Use `headers-more` or repeat `add_header always`.
- Rate-limit zones are per-worker by default; aggregate is rps × workers. Agents calculate as if zones are global.
- Agents enable `proxy_buffering off;` to "fix" SSE/streaming and inadvertently expose memory pressure on the upstream. Scope it to the streaming endpoint only.
- WebSocket fix involves both `Upgrade` and `Connection` headers AND `proxy_http_version 1.1;`. Agents ship two of three and chase ghosts.
- ACME renewal failure mode: certbot writes to `/etc/letsencrypt/live/...` but nginx caches old fd; without `systemctl reload nginx` post-renew, certs go stale. Add a `--deploy-hook` to certbot.
- Human-in-loop checkpoint: any change to TLS suite, HSTS, CSP, or auth-gating routes must be human-approved with a staging-domain test plan.
- Reload vs restart: `reload` preserves connections; `restart` drops them. Agents `restart` when `reload` would do, causing user-visible blips.
- When proxying to localhost, always use `127.0.0.1:PORT`, not `localhost:PORT` — `localhost` resolves to IPv6 first on dual-stack and the upstream may not listen on `[::1]`.

## References
- nginx docs — https://nginx.org/en/docs/
- nginx admin guide (F5) — https://docs.nginx.com/nginx/admin-guide/
- Mozilla SSL Configuration Generator — https://ssl-config.mozilla.org/
- nginx-admins-handbook — https://github.com/trimstray/nginx-admins-handbook
- Yandex Gixy linter — https://github.com/yandex/gixy
- Mozilla observatory — https://observatory.mozilla.org/
- Qualys SSL Labs — https://www.ssllabs.com/ssltest/
- F5 nginx common mistakes — https://www.f5.com/company/blog/nginx/avoiding-top-10-nginx-configuration-mistakes
- HSTS preload — https://hstspreload.org/
