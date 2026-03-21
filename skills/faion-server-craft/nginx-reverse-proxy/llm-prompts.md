# nginx Reverse Proxy LLM Prompts

Prompts for AI assistants to configure, troubleshoot, and optimize nginx reverse proxy setups.

## Prompt 1: nginx Configuration Audit

```
Audit the nginx reverse proxy configuration on this Ubuntu server.

Steps:
1. Check nginx version: `nginx -v`
2. Test config syntax: `sudo nginx -t`
3. List enabled sites: `ls -la /etc/nginx/sites-enabled/`
4. Read each site config: `cat /etc/nginx/sites-enabled/*`
5. Check main config: `cat /etc/nginx/nginx.conf`
6. List snippets: `ls /etc/nginx/snippets/`
7. Check listening ports: `sudo ss -tlnp | grep nginx`
8. Check error log: `sudo tail -20 /var/log/nginx/error.log`
9. Test each site externally: `curl -I http://domain`

For each site, check:
| Check | Status |
|-------|--------|
| Security headers (HSTS, X-Content-Type, CSP) | ... |
| Proxy headers (X-Real-IP, X-Forwarded-For) | ... |
| WebSocket support (if applicable) | ... |
| Rate limiting | ... |
| Error pages | ... |
| SSL/TLS (or Cloudflare) | ... |

Provide specific fixes for any issues found.
```

## Prompt 2: New Site Setup

```
Set up nginx reverse proxy for a new site.

Domain: {domain}
Backend: {host:port}
Type: {API / SPA / Static / Full-stack}
SSL: {Cloudflare / Let's Encrypt / Self-signed}
WebSocket: {yes/no, path}
Rate limiting: {yes/no}

Steps:
1. Create snippets if they don't exist (proxy-params, security-headers, websocket)
2. Create site config in sites-available
3. Enable with symlink
4. Test configuration
5. Reload nginx
6. Verify the site works

For the site config, include:
- Appropriate proxy_pass directives
- Security headers
- WebSocket support (if needed)
- Rate limiting (if needed)
- Static file caching (if applicable)
- Custom error pages

Test:
- HTTP response
- API endpoints
- WebSocket connection (if applicable)
- Security headers
```

## Prompt 3: nginx Troubleshooting

```
I'm having an issue with nginx: {describe the problem}

Common issues and diagnostics:

1. 502 Bad Gateway:
   - Is the backend running? `curl http://127.0.0.1:{port}`
   - Check upstream connection: `sudo tail -f /var/log/nginx/error.log`
   - Check backend logs

2. 504 Gateway Timeout:
   - Increase proxy_read_timeout
   - Check backend performance
   - Check if request is long-running

3. WebSocket not connecting:
   - Check map block for $connection_upgrade
   - Check proxy_http_version 1.1
   - Check Upgrade/Connection headers
   - Check proxy_read_timeout (needs to be high)

4. SSL/HTTPS issues:
   - Check certificate paths
   - Check Cloudflare SSL mode
   - Test with curl -vk

5. 403 Forbidden:
   - Check file permissions
   - Check nginx user (www-data)
   - Check root/alias paths

6. Config won't reload:
   - Run `sudo nginx -t` for syntax errors
   - Check error log: `sudo tail -20 /var/log/nginx/error.log`

Run the appropriate diagnostics and provide the fix.
```

## Prompt 4: Performance Tuning

```
Optimize nginx performance for this server.

Current setup:
- {number} sites/domains
- {number} concurrent connections expected
- Backend: {describe backends}
- Server: {CPUs} CPUs, {RAM} GB RAM

Tune:
1. Worker processes and connections:
   ```
   worker_processes auto;  # Match CPU cores
   worker_connections 8192;  # Max connections per worker
   ```

2. Keepalive connections:
   ```
   upstream backend {
       server 127.0.0.1:8100;
       keepalive 32;  # Connection pool
   }
   ```

3. Gzip compression:
   ```
   gzip on;
   gzip_types text/plain text/css application/json application/javascript;
   gzip_min_length 1000;
   ```

4. Static file caching:
   ```
   location ~* \.(js|css|png|jpg|ico|svg|woff2)$ {
       expires 30d;
       add_header Cache-Control "public, immutable";
   }
   ```

5. Buffer sizes:
   ```
   proxy_buffer_size 128k;
   proxy_buffers 4 256k;
   proxy_busy_buffers_size 256k;
   ```

Apply and benchmark with: `ab -n 1000 -c 100 http://domain/api/health`
```

## Prompt 5: Security Audit

```
Perform a security audit of the nginx configuration.

Checks:
1. Security headers on all sites (HSTS, CSP, X-Content-Type-Options, X-Frame-Options)
2. SSL/TLS configuration (if applicable):
   - TLS version (1.2+ only)
   - Cipher suite
   - OCSP stapling
3. Information disclosure:
   - server_tokens off (hide nginx version)
   - No directory listing
4. Rate limiting on API endpoints
5. File upload limits (client_max_body_size)
6. Proxy headers (X-Real-IP, X-Forwarded-For)
7. No exposed internal services
8. Error pages don't leak info

For each site, test with:
```bash
curl -sI https://domain | grep -E "Server:|X-Content|Strict|X-Frame|Content-Security|Referrer"
```

Report findings and provide fixes for each issue.
```

## Prompt 6: SSL/TLS Configuration

```
Configure SSL/TLS for nginx.

Option A: Cloudflare (SSL termination at Cloudflare)
- Server listens on HTTP only
- Cloudflare handles HTTPS
- Set SSL mode to "Full" in Cloudflare

Option B: Let's Encrypt (SSL termination at nginx)
- Install certbot
- Generate certificates
- Configure nginx with ssl
- Set up auto-renewal

Option C: Origin Certificate (Cloudflare origin cert)
- Generate origin certificate in Cloudflare dashboard
- Install on server
- Configure nginx with ssl

For the selected option:
1. Install/generate certificates
2. Configure nginx ssl directives
3. Set up auto-renewal (if applicable)
4. Test HTTPS connectivity
5. Test with SSL Labs / SecurityHeaders.com
```

## Prompt 7: Add Rate Limiting

```
Add rate limiting to nginx for the following endpoints:

Endpoints to protect:
{list endpoints with desired rates}

Example:
- /api/* : 10 requests/second, burst 20
- /api/auth/login : 3 requests/minute, burst 5
- /api/upload : 5 requests/minute, burst 10

Implementation:
1. Define limit_req_zone directives in http context
2. Apply limit_req to specific locations
3. Set custom 429 response
4. Whitelist trusted IPs (if needed)
5. Test rate limiting works
6. Check fail2ban integration (nginx-limit-req jail)

Verify:
```bash
# Send burst of requests
for i in $(seq 1 30); do
    curl -s -o /dev/null -w "%{http_code} " http://domain/api/test
done
echo
# Should see 200 200 200 ... 429 429 429
```
```

## Prompt 8: Migrate Site Configuration

```
Migrate/restructure nginx configuration to use the snippets pattern.

Current state: {describe current setup}

Goal:
1. Extract common patterns into snippets:
   - /etc/nginx/snippets/proxy-params.conf
   - /etc/nginx/snippets/websocket.conf
   - /etc/nginx/snippets/security-headers.conf
   - /etc/nginx/snippets/cloudflare-realip.conf
   - /etc/nginx/snippets/rate-limiting.conf

2. Refactor each site config to use `include snippets/...`

3. Move WebSocket map to /etc/nginx/conf.d/websocket-map.conf

4. Ensure no functionality changes (test before and after)

Steps:
1. Create all snippet files
2. Modify one site at a time
3. Test after each modification: `sudo nginx -t`
4. Reload: `sudo systemctl reload nginx`
5. Verify site still works: `curl -I https://domain`
6. Repeat for all sites

Show the diff for each file change.
```
