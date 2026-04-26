# LLM Prompts for Nginx Configuration

Prompts for generating and troubleshooting Nginx configurations.

---

## Generate Static Site Configuration

```
Generate an Nginx configuration for a static website with these requirements:

Domain: {DOMAIN}
Root path: {ROOT_PATH}
Framework: {React/Vue/Next.js/Static HTML}

Requirements:
- HTTPS with Let's Encrypt certificates
- HTTP to HTTPS redirect
- Security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)
- Gzip compression
- Static asset caching (1 year for immutable assets)
- SPA routing (try_files with fallback to index.html)
- Block access to hidden files (.git, .env)
- JSON access log format

Follow 2025 best practices:
- TLS 1.2/1.3 only
- Modern cipher suites
- OCSP stapling
- DH parameters

Output the complete configuration file and any required snippets.
```

---

## Generate Reverse Proxy Configuration

```
Generate an Nginx reverse proxy configuration with these requirements:

Domain: {DOMAIN}
Backend: {BACKEND_URL} (e.g., http://127.0.0.1:8000)
Backend type: {Node.js/Python/Go/Java}

Requirements:
- HTTPS with Let's Encrypt
- Load balancing: {yes/no, if yes: number of backends}
- Health check endpoint: {/health}
- WebSocket support: {yes/no}
- Caching: {yes/no, if yes: cache duration}
- Rate limiting: {requests per second}

Include:
- Proper proxy headers (X-Real-IP, X-Forwarded-For, X-Forwarded-Proto)
- Connection keepalive
- Appropriate timeouts
- Error handling with proxy_next_upstream
- Security headers

Output:
1. Main site configuration
2. Upstream definition
3. Required snippets
4. Recommended nginx.conf settings
```

---

## Generate WebSocket Proxy Configuration

```
Generate an Nginx configuration for WebSocket proxying:

Domain: {DOMAIN}
WebSocket path: {/ws or /socket.io/}
Backend: {BACKEND_URL}
Protocol: {WebSocket/Socket.IO}

Requirements:
- HTTPS with WSS support
- HTTP upgrade headers
- Extended timeouts for long-running connections
- Fallback for non-WebSocket requests
- Connection status logging

Include the map directive for Connection header handling.
```

---

## Generate API Gateway Configuration

```
Generate an Nginx API gateway configuration:

API Domain: {api.example.com}
Services:
- {/users -> http://users-service:8001}
- {/products -> http://products-service:8002}
- {/orders -> http://orders-service:8003}

Requirements:
- Path-based routing to different backends
- Rate limiting per endpoint:
  - General: {10 req/s}
  - Write operations: {5 req/s}
  - Login: {5 req/min}
- Response caching for GET requests
- CORS headers
- JWT validation location (for auth proxy)
- Health check aggregation
- Request/response logging (JSON)
- Circuit breaker (proxy_next_upstream)

Include upstream definitions and cache configuration.
```

---

## Generate Load Balancer Configuration

```
Generate an Nginx load balancer configuration:

Domain: {DOMAIN}
Backend servers:
- {IP1:PORT} (weight: {5})
- {IP2:PORT} (weight: {5})
- {IP3:PORT} (weight: {3}, backup: {yes/no})

Requirements:
- Load balancing algorithm: {round-robin/least_conn/ip_hash}
- Health checks: {passive/active}
- Session persistence: {yes/no, method: ip_hash/cookie}
- Connection draining
- Failover configuration
- Keepalive connections to backends
- Monitoring endpoint (/nginx_status)

Include health check configuration and failover handling.
```

---

## Security Hardening Prompt

```
Review and harden this Nginx configuration for security:

{PASTE CONFIGURATION}

Check for:
1. SSL/TLS configuration (TLS 1.2+ only, strong ciphers)
2. Security headers (HSTS, CSP, X-Frame-Options, etc.)
3. Information disclosure (server_tokens, error pages)
4. Access controls (sensitive paths, hidden files)
5. Rate limiting
6. Request size limits
7. Timeout configurations
8. Buffer size limits

Provide:
1. List of security issues found
2. Severity rating for each issue
3. Corrected configuration
4. Additional recommendations
```

---

## Performance Optimization Prompt

```
Optimize this Nginx configuration for performance:

{PASTE CONFIGURATION}

Current setup:
- Expected traffic: {requests/second}
- Server specs: {CPU cores, RAM}
- Content type: {static/dynamic/mixed}
- CDN: {yes/no}

Optimize for:
1. Worker processes and connections
2. File descriptor limits
3. Keepalive settings
4. Gzip compression
5. Caching configuration
6. Buffer sizes
7. Sendfile and TCP settings
8. Connection pooling to upstreams

Provide optimized configuration with explanations for each change.
```

---

## Troubleshooting Prompt

```
Troubleshoot this Nginx issue:

Problem: {DESCRIBE THE ISSUE}

Symptoms:
- {Error message or behavior}
- {Status codes returned}
- {Logs excerpts}

Current configuration:
{PASTE RELEVANT CONFIG}

Environment:
- Nginx version: {version}
- OS: {Ubuntu/Debian/CentOS}
- Backend: {type and version}

Provide:
1. Root cause analysis
2. Step-by-step debugging commands
3. Configuration fixes
4. Prevention recommendations
```

---

## Migration Prompt

```
Migrate this Apache/HAProxy configuration to Nginx:

Source configuration:
{PASTE APACHE/HAPROXY CONFIG}

Requirements:
- Preserve all functionality
- Improve security with 2025 best practices
- Add missing features:
  - {Rate limiting}
  - {Caching}
  - {Security headers}

Output:
1. Equivalent Nginx configuration
2. Key differences to note
3. Additional recommendations
```

---

## Docker/Kubernetes Configuration Prompt

```
Generate Nginx configuration for containerized deployment:

Environment: {Docker/Kubernetes}
Architecture:
- Frontend: {service name}
- Backend API: {service name}
- Other services: {list}

Requirements:
- Environment variable substitution
- Health/readiness probes
- Graceful shutdown
- Horizontal scaling support
- Service discovery: {DNS/environment variables}
- ConfigMap/Secret integration (for K8s)

Output:
1. nginx.conf template
2. Dockerfile or ConfigMap
3. Entrypoint script (if needed)
4. Kubernetes manifests (if applicable)
```

---

## SSL Certificate Setup Prompt

```
Set up SSL/TLS for Nginx with Let's Encrypt:

Domains:
- {example.com}
- {www.example.com}
- {api.example.com}

Requirements:
- Wildcard certificate: {yes/no}
- DNS provider: {Cloudflare/Route53/manual}
- Auto-renewal
- OCSP stapling
- HSTS preload ready

Provide:
1. Certbot installation commands
2. Certificate generation commands
3. Nginx SSL configuration
4. Renewal hook script
5. Cron job for renewal
6. Verification steps
```

---

## Cache Strategy Prompt

```
Design a caching strategy for this application:

Application type: {E-commerce/Blog/API/SPA}
Content types:
- Static assets: {JS, CSS, images}
- API responses: {list endpoints}
- Dynamic pages: {list}

Traffic patterns:
- Peak traffic: {requests/second}
- Cache hit target: {percentage}

Requirements:
- Browser caching headers
- Proxy cache for API responses
- Cache invalidation strategy
- Stale-while-revalidate
- Cache bypass for authenticated users

Provide:
1. proxy_cache_path configuration
2. Per-location cache settings
3. Cache key design
4. Headers configuration
5. Purge/invalidation approach
```

---

## Usage Tips

1. Replace `{PLACEHOLDERS}` with actual values
2. Remove irrelevant optional sections
3. Add specific constraints or requirements
4. Include error messages for troubleshooting
5. Specify Nginx version if using version-specific features

## Best Practices for Prompts

- Be specific about the use case
- Include environment details
- Specify security requirements
- Mention performance expectations
- Request explanations for complex configs
- Ask for verification steps
