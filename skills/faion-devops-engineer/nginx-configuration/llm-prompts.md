# LLM Prompts for Nginx Configuration

Prompts for AI-assisted Nginx configuration tasks.

---

## Configuration Generation

### Static Site Configuration

```
Generate an Nginx configuration for a static website with the following requirements:

Domain: [DOMAIN]
Root path: [/var/www/path]
SSL: Let's Encrypt
Features needed:
- HTTP to HTTPS redirect
- SPA support (try_files with fallback to index.html)
- Static asset caching (1 year for immutable assets)
- Security headers (HSTS, X-Frame-Options, X-Content-Type-Options)
- Gzip compression
- Rate limiting (10 requests/second with burst of 20)

Use modern TLS configuration (TLS 1.2 and 1.3 only).
Include references to snippets for SSL and security headers.
```

### Reverse Proxy Configuration

```
Generate an Nginx reverse proxy configuration:

Domain: [DOMAIN]
Backend: [HOST:PORT] (e.g., 127.0.0.1:3000)
SSL: Let's Encrypt

Requirements:
- HTTP to HTTPS redirect
- Proxy headers (X-Real-IP, X-Forwarded-For, X-Forwarded-Proto)
- WebSocket support at /ws path
- Health check endpoint at /health (no logging)
- Rate limiting for API (30 req/s, burst 50)
- Client max body size: 10MB
- Proxy timeouts: 60s connect, 60s read, 60s send

Include upstream definition with keepalive connections.
```

### Load Balancer Configuration

```
Generate an Nginx load balancer configuration:

Backend servers:
- [IP1:PORT] (weight 5)
- [IP2:PORT] (weight 5)
- [IP3:PORT] (backup)

Load balancing method: [least_conn / round_robin / ip_hash]

Requirements:
- Health checks (max_fails=3, fail_timeout=30s)
- Keepalive connections to backend (32)
- Failover to backup server
- Session persistence: [yes/no]

If session persistence is needed, use ip_hash or sticky cookie.
```

---

## Security Configuration

### Security Audit Prompt

```
Analyze this Nginx configuration for security issues:

```nginx
[PASTE CONFIGURATION HERE]
```

Check for:
1. SSL/TLS configuration (protocols, ciphers)
2. Security headers (HSTS, CSP, X-Frame-Options, etc.)
3. Information disclosure (server_tokens, version exposure)
4. Access control (sensitive file protection)
5. Rate limiting configuration
6. Logging configuration (sensitive data exposure)
7. Input validation (client_max_body_size, buffer sizes)
8. Proxy security (if applicable)

Provide specific recommendations with configuration examples.
```

### Hardening Prompt

```
Harden this Nginx configuration for production deployment:

```nginx
[PASTE CONFIGURATION HERE]
```

Apply these hardening measures:
1. Disable server version disclosure
2. Add comprehensive security headers
3. Configure rate limiting
4. Set appropriate timeouts
5. Restrict access to sensitive paths
6. Enable HSTS with preload
7. Configure proper SSL/TLS settings
8. Add logging for security monitoring

Provide the hardened configuration with comments explaining each change.
```

### CSP Generation

```
Generate a Content-Security-Policy header for my application:

Application type: [SPA / Traditional / API]
Frontend framework: [React / Vue / Angular / None]
CDN domains: [list any CDNs used, e.g., cdn.example.com]
API domains: [list API endpoints, e.g., api.example.com]
Analytics: [Google Analytics / Plausible / None]
Font providers: [Google Fonts / Self-hosted / None]
Inline styles needed: [yes/no]
Inline scripts needed: [yes/no]
WebSocket connections: [yes/no, list domains]

Generate both a restrictive CSP and a report-only version for testing.
```

---

## Performance Optimization

### Performance Audit

```
Analyze this Nginx configuration for performance optimization:

```nginx
[PASTE CONFIGURATION HERE]
```

Evaluate:
1. Worker processes and connections
2. Keepalive settings
3. Buffer sizes
4. Gzip compression settings
5. Static file caching headers
6. Proxy buffering configuration
7. Connection pooling (keepalive to upstream)
8. Logging impact

Expected traffic: [requests per second]
Server specs: [CPU cores, RAM]

Provide optimized configuration with explanations.
```

### Caching Strategy

```
Design an Nginx caching strategy for my application:

Application type: [API / Static site / Hybrid]
Content types to cache: [list, e.g., JSON responses, images, CSS/JS]
Cache invalidation strategy: [URL versioning / Cache-Control headers / Manual purge]

Requirements:
- Cache dynamic API responses for [X] minutes
- Cache static assets for [X] days
- Bypass cache for authenticated users
- Add cache status header for debugging
- Handle cache stampede (lock)
- Serve stale on backend errors

Provide proxy_cache configuration and cache control headers.
```

---

## Troubleshooting

### Debug Configuration

```
I'm experiencing this issue with my Nginx configuration:

Error/Symptom: [describe the issue]

Current configuration:
```nginx
[PASTE CONFIGURATION HERE]
```

Error log output:
```
[PASTE RELEVANT LOG ENTRIES]
```

Access log output:
```
[PASTE RELEVANT LOG ENTRIES]
```

Help me:
1. Identify the root cause
2. Explain why this error occurs
3. Provide the corrected configuration
4. Suggest additional debugging steps if needed
```

### SSL Certificate Issues

```
I'm having SSL certificate issues with Nginx:

Error message: [paste error]
Certificate source: [Let's Encrypt / Self-signed / Commercial CA]
Certificate path: [/path/to/certificate]

Current SSL configuration:
```nginx
[PASTE SSL CONFIG]
```

Help me:
1. Diagnose the certificate issue
2. Verify certificate chain
3. Fix the configuration
4. Test the SSL setup
```

---

## Migration and Conversion

### Apache to Nginx

```
Convert this Apache configuration to Nginx:

```apache
[PASTE APACHE CONFIG HERE]
```

Requirements:
- Preserve all functionality
- Use Nginx best practices
- Add modern security headers
- Optimize for performance

Explain any Apache features that don't have direct Nginx equivalents.
```

### Docker/Kubernetes Adaptation

```
Adapt this Nginx configuration for containerized deployment:

Current configuration:
```nginx
[PASTE CONFIGURATION HERE]
```

Deployment target: [Docker / Kubernetes]

Requirements:
- Environment variable substitution for:
  - Backend server addresses
  - Domain names
  - SSL certificate paths
- Health check endpoint
- Graceful shutdown handling
- Log to stdout/stderr
- ConfigMap/Secret friendly structure

Provide:
1. Modified nginx.conf
2. Dockerfile (if Docker)
3. Kubernetes manifests (if K8s)
4. Environment variable documentation
```

---

## Specific Use Cases

### Next.js/React Deployment

```
Generate Nginx configuration for Next.js deployment:

Setup: [Static export / Node.js server / Hybrid]
Domain: [DOMAIN]
Node.js port: [3000] (if server mode)

Requirements:
- Static asset caching with immutable headers
- _next/static/ path handling
- API routes proxy (if server mode)
- Image optimization caching
- ISR support (if applicable)
- Security headers compatible with Next.js
```

### WordPress/PHP Configuration

```
Generate Nginx configuration for WordPress:

Domain: [DOMAIN]
PHP-FPM socket: [/var/run/php/php8.3-fpm.sock]
WordPress path: [/var/www/wordpress]

Requirements:
- Pretty permalinks support
- PHP-FPM integration
- wp-admin protection (rate limiting)
- xmlrpc.php blocking
- wp-config.php protection
- Upload limit: [size]
- W3 Total Cache / Redis cache support
- Security headers
```

### API Gateway Configuration

```
Generate Nginx API gateway configuration:

Services:
- /api/users -> users-service:8001
- /api/orders -> orders-service:8002
- /api/products -> products-service:8003

Requirements:
- Path-based routing
- Service-specific rate limits
- JWT validation (optional)
- Request/response logging
- Circuit breaker pattern (proxy_next_upstream)
- CORS for frontend at [ORIGIN]
- API versioning support (/v1/, /v2/)
- Health check aggregation
```

---

## Validation Prompts

### Configuration Review

```
Review this Nginx configuration for a production deployment:

```nginx
[PASTE CONFIGURATION HERE]
```

Evaluate against these criteria:
- [ ] Security best practices (2025 standards)
- [ ] Performance optimization
- [ ] SSL/TLS configuration (A+ rating potential)
- [ ] Error handling
- [ ] Logging adequacy
- [ ] Maintainability
- [ ] Documentation needs

Provide:
1. Score (1-10) with reasoning
2. Critical issues (must fix)
3. Recommendations (should fix)
4. Nice-to-haves (could improve)
```

### SSL Labs A+ Checklist

```
Generate Nginx SSL configuration to achieve SSL Labs A+ rating:

Current configuration:
```nginx
[PASTE SSL CONFIG OR "start from scratch"]
```

Requirements:
- TLS 1.2 and 1.3 only
- Strong cipher suites with forward secrecy
- HSTS with preload flag
- Proper certificate chain
- Session resumption configuration
- No known vulnerabilities

Provide:
1. Complete SSL configuration
2. Commands to generate DH parameters
3. HSTS preload submission checklist
4. SSL Labs test interpretation guide
```
