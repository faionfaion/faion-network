# Nginx Configuration

## Overview

Nginx is a high-performance HTTP server, reverse proxy, and load balancer. This methodology covers configuration patterns for web serving, reverse proxy setups, SSL/TLS termination, caching, and security hardening.

## When to Use

- Setting up web servers for static or dynamic content
- Configuring reverse proxy for backend services
- Implementing SSL/TLS termination
- Setting up load balancing
- Optimizing web application performance
- Implementing security headers and access controls

## Directory Structure

```
/etc/nginx/
├── nginx.conf              # Main configuration
├── mime.types              # MIME type definitions
├── conf.d/                 # Additional configurations
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
    ├── example.com.crt
    └── example.com.key
```

## Key Concepts

### Performance Optimization

| Setting | Purpose | Recommendation |
|---------|---------|----------------|
| `worker_processes` | Parallel processing | Set to `auto` (matches CPU cores) |
| `worker_connections` | Connections per worker | 4096+ for high traffic |
| `sendfile` | Efficient file transfer | Enable (`on`) |
| `tcp_nopush` | Optimize packet sending | Enable with sendfile |
| `tcp_nodelay` | Disable Nagle's algorithm | Enable for real-time |
| `keepalive_timeout` | Persistent connections | 65s (balance between resources and UX) |
| `gzip` | Response compression | Enable for text content |

### Security Hardening

| Directive | Purpose | Value |
|-----------|---------|-------|
| `server_tokens` | Hide version | `off` |
| `ssl_protocols` | TLS versions | `TLSv1.2 TLSv1.3` |
| `ssl_ciphers` | Cipher suites | Strong ECDHE ciphers |
| `add_header X-Frame-Options` | Clickjacking protection | `DENY` |
| `add_header X-Content-Type-Options` | MIME sniffing protection | `nosniff` |
| `add_header Strict-Transport-Security` | Force HTTPS | `max-age=31536000` |

### Reverse Proxy

| Directive | Purpose |
|-----------|---------|
| `proxy_pass` | Forward requests to backend |
| `proxy_set_header` | Pass client info to backend |
| `proxy_cache` | Cache backend responses |
| `upstream` | Define backend server pools |

### Load Balancing Methods

| Method | Use Case |
|--------|----------|
| Round Robin | Default, equal distribution |
| `least_conn` | Route to least busy server |
| `ip_hash` | Sticky sessions by client IP |
| `hash` | Custom key-based routing |

## Files in This Methodology

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview |
| [checklist.md](checklist.md) | Configuration verification checklist |
| [examples.md](examples.md) | Real-world configuration examples |
| [templates.md](templates.md) | Copy-paste configuration templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for AI-assisted configuration |

## Quick Commands

```bash
# Test configuration syntax
sudo nginx -t

# Reload configuration (graceful)
sudo nginx -s reload

# Show compiled configuration
sudo nginx -T

# Check running modules
nginx -V 2>&1 | grep -o -- '--[^ ]*'

# Test SSL configuration
curl -I https://example.com
```

## SSL/TLS Best Practices (2025-2026)

### Protocol Selection

- **Minimum:** TLS 1.2 (required for PCI DSS compliance)
- **Recommended:** TLS 1.3 (better performance, forward secrecy)
- **Deprecated:** TLS 1.0, TLS 1.1, SSL 3.0

### OCSP Stapling Note

As of August 2025, Let's Encrypt no longer supports OCSP. While Mozilla's SSL Configuration Generator still recommends it, evaluate whether OCSP stapling is beneficial for your CA.

### Certificate Management

- Use Let's Encrypt for free, automated certificates
- Certificates expire every 90 days - automate renewal
- Store certificates securely with proper permissions (600)

## Performance Benchmarks

A properly configured Nginx can handle:

| Configuration | Requests/Second |
|---------------|-----------------|
| Clustered | 400K - 500K |
| Single instance | 50K - 80K |

## Monitoring

| Tool | Purpose |
|------|---------|
| `stub_status` | Basic metrics endpoint |
| Nginx Amplify | SaaS monitoring |
| Prometheus + nginx-exporter | Metrics collection |
| ELK Stack | Log analysis |

## Sources

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Nginx Admin Guide](https://docs.nginx.com/nginx/admin-guide/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)
- [Nginx Security Hardening Guide](https://www.secopsolution.com/blog/nginx-security-hardening-guide)
- [nixCraft Nginx Security Best Practices](https://www.cyberciti.biz/tips/linux-unix-bsd-nginx-webserver-security.html)
- [NGINX Reverse Proxy Guide](https://www.getpagespeed.com/server-setup/nginx/nginx-reverse-proxy)
- [Modern SSL/TLS Configuration](https://www.linuxmalaysia.com/2025/03/modern-ssltls-for-nginx-practical-guide.html)
