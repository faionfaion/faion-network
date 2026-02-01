# Nginx Configuration

## Overview

Nginx is a high-performance HTTP server, reverse proxy, and load balancer. This methodology covers configuration patterns for reverse proxy setups, SSL/TLS termination, caching, and security hardening based on 2025-2026 best practices.

## When to Use

- Setting up web servers for static or dynamic content
- Configuring reverse proxy for backend services
- Implementing SSL/TLS termination with TLS 1.2/1.3
- Setting up load balancing
- Optimizing web application performance with caching
- Implementing security headers (HSTS, CSP, X-Frame-Options)
- WebSocket proxy configuration

## Directory Structure

```
/etc/nginx/
├── nginx.conf              # Main configuration
├── mime.types              # MIME type definitions
├── conf.d/                 # Additional configurations
│   ├── upstreams/          # Upstream definitions
│   └── default.conf
├── sites-available/        # Available site configs
│   ├── example.com
│   └── api.example.com
├── sites-enabled/          # Enabled sites (symlinks)
│   └── example.com -> ../sites-available/example.com
├── snippets/               # Reusable config snippets
│   ├── ssl-params.conf
│   ├── security-headers.conf
│   └── proxy-params.conf
└── ssl/                    # SSL certificates
    ├── dhparam.pem         # DH parameters (4096-bit)
    └── certificates/
```

## Key Concepts

### Reverse Proxy

Nginx acts as intermediary between clients and backend servers:
- Hides backend infrastructure
- Provides load balancing
- Handles SSL/TLS termination
- Enables caching and compression

### SSL/TLS Configuration (2025 Standards)

| Setting | Recommendation |
|---------|----------------|
| Protocols | TLSv1.2, TLSv1.3 only |
| Ciphers | ECDHE with AES-GCM |
| DH Parameters | 4096-bit |
| OCSP Stapling | Enabled |
| Session Cache | Shared, 10MB |

### Security Headers

| Header | Purpose |
|--------|---------|
| Strict-Transport-Security | Force HTTPS (HSTS) |
| Content-Security-Policy | Prevent XSS/injection |
| X-Frame-Options | Prevent clickjacking |
| X-Content-Type-Options | Prevent MIME sniffing |
| Referrer-Policy | Control referrer info |
| Permissions-Policy | Control browser features |

### Caching Strategy

| Cache Type | Use Case |
|------------|----------|
| Static assets | Long TTL (1 year), immutable |
| API responses | Short TTL (1-10 min), stale-while-revalidate |
| Dynamic content | No cache or conditional |

## Process/Steps

### 1. Initial Setup

```bash
# Install nginx
sudo apt update && sudo apt install nginx

# Generate DH parameters (4096-bit for production)
sudo openssl dhparam -out /etc/nginx/ssl/dhparam.pem 4096

# Test configuration
sudo nginx -t

# Reload
sudo nginx -s reload
```

### 2. Configure Main nginx.conf

See `templates.md` for complete main configuration.

### 3. Create Snippets

Create reusable snippets for:
- SSL/TLS parameters
- Security headers
- Proxy parameters

### 4. Configure Virtual Hosts

Create site configurations in `sites-available/` and symlink to `sites-enabled/`.

### 5. Set Up SSL Certificates

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d example.com -d www.example.com

# Verify auto-renewal
sudo certbot renew --dry-run
```

## Best Practices

### Performance

1. **Worker processes** - Set to `auto` to match CPU cores
2. **Worker connections** - 4096+ for high traffic
3. **File descriptors** - Set `worker_rlimit_nofile` to 2x worker_connections
4. **Keepalive** - Enable for connection reuse
5. **Gzip compression** - Enable for text-based content
6. **Sendfile** - Enable for static file serving

### Security

1. **Hide version** - `server_tokens off;`
2. **TLS 1.2+ only** - Remove TLS 1.0/1.1
3. **Security headers** - HSTS, CSP, X-Frame-Options
4. **Rate limiting** - Prevent abuse
5. **Access control** - Restrict sensitive endpoints
6. **Deny hidden files** - Block `.git`, `.env`, etc.

### Configuration

1. **Modular structure** - Use includes and snippets
2. **Test before reload** - Always run `nginx -t`
3. **Version control** - Track all config changes
4. **Comments** - Document non-obvious settings

### Monitoring

1. **Access logs** - JSON format for parsing
2. **Error logs** - Set appropriate level
3. **Stub status** - Enable for basic metrics
4. **Prometheus exporter** - For advanced monitoring

## Quick Commands

```bash
# Test configuration
sudo nginx -t

# Reload configuration
sudo nginx -s reload

# Show parsed configuration
sudo nginx -T

# Check open connections
ss -s | grep tcp

# View access log (real-time)
tail -f /var/log/nginx/access.log

# Check error log
tail -100 /var/log/nginx/error.log
```

## Performance Benchmarks

Properly configured Nginx can handle:
- 400K-500K requests/sec (clustered)
- 50K-80K requests/sec (single instance)
- With ~30% CPU load

## Related Files

- [checklist.md](checklist.md) - Configuration checklist
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - Copy-paste templates
- [llm-prompts.md](llm-prompts.md) - LLM prompts for generation

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Set up GitHub Actions workflow from template | haiku | Pattern application, simple configuration |
| Design CI/CD pipeline architecture | opus | Complex system design with many variables |
| Write terraform code for infrastructure | sonnet | Implementation with moderate complexity |
| Debug failing pipeline step | sonnet | Debugging and problem-solving |
| Implement AIOps anomaly detection | opus | Novel ML approach, complex decision |
| Configure webhook and secret management | haiku | Mechanical setup using checklists |


## Sources

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Nginx Admin Guide](https://docs.nginx.com/nginx/admin-guide/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [F5 NGINX Best Practices](https://www.f5.com/company/blog/nginx/avoiding-top-10-nginx-configuration-mistakes)
- [nginx-admins-handbook](https://github.com/trimstray/nginx-admins-handbook)
- [Qualys SSL Labs A+ Guide](https://beguier.eu/nicolas/articles/nginx-tls-security-configuration.html)

---

*Last updated: 2026-01 | Focus: Reverse proxy, SSL/TLS, caching, security headers*
