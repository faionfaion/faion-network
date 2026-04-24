# Nginx Configuration Checklist

## Pre-Deployment Checklist

### Main Configuration (nginx.conf)

- [ ] `user` directive set to non-privileged user (www-data)
- [ ] `worker_processes auto;` for CPU-based scaling
- [ ] `worker_connections` set appropriately (4096+)
- [ ] `worker_rlimit_nofile` set to 2x worker_connections
- [ ] `server_tokens off;` to hide version
- [ ] `sendfile on;` enabled
- [ ] `tcp_nopush on;` enabled
- [ ] `tcp_nodelay on;` enabled
- [ ] Error log level appropriate (warn or error)

### SSL/TLS Configuration

- [ ] TLS 1.0 and 1.1 disabled
- [ ] Only TLSv1.2 and TLSv1.3 enabled
- [ ] Strong cipher suites configured
- [ ] `ssl_prefer_server_ciphers on;`
- [ ] DH parameters generated (4096-bit)
- [ ] OCSP stapling enabled
- [ ] SSL session cache configured
- [ ] SSL session tickets disabled (for PFS)

### Security Headers

- [ ] HSTS header with `includeSubDomains`
- [ ] Content-Security-Policy defined
- [ ] X-Frame-Options set (DENY or SAMEORIGIN)
- [ ] X-Content-Type-Options: nosniff
- [ ] Referrer-Policy configured
- [ ] Permissions-Policy defined

### Reverse Proxy Configuration

- [ ] `proxy_http_version 1.1;` set
- [ ] X-Real-IP header forwarded
- [ ] X-Forwarded-For header forwarded
- [ ] X-Forwarded-Proto header forwarded
- [ ] Host header set correctly
- [ ] Timeouts configured (connect, send, read)
- [ ] Buffering settings optimized
- [ ] Upstream keepalive connections enabled

### WebSocket Support (if applicable)

- [ ] Upgrade header forwarded
- [ ] Connection header uses map directive
- [ ] Read timeout extended (86400s for long connections)
- [ ] Send timeout extended

### Caching Configuration (if applicable)

- [ ] `proxy_cache_path` defined with levels
- [ ] `keys_zone` sized appropriately
- [ ] `max_size` set for disk limit
- [ ] `inactive` timeout configured
- [ ] `use_temp_path=off;` set
- [ ] Cache key properly defined
- [ ] Cache validity settings configured
- [ ] Stale content serving enabled
- [ ] Cache bypass rules defined
- [ ] X-Cache-Status header added

### Rate Limiting

- [ ] Rate limit zones defined
- [ ] Connection limits configured
- [ ] Burst values set appropriately
- [ ] nodelay option considered

### Logging

- [ ] Access log format defined (JSON recommended)
- [ ] Error log configured
- [ ] Log rotation set up
- [ ] Health check endpoints excluded from logs

### File Access Security

- [ ] Hidden files denied (location ~ /\.)
- [ ] Sensitive paths blocked (.git, .env)
- [ ] Upload limits set if applicable
- [ ] Static file caching configured

### Load Balancing (if applicable)

- [ ] Upstream defined with algorithm
- [ ] Health checks configured
- [ ] Backup servers specified
- [ ] Weights assigned if needed
- [ ] Keepalive connections to upstream

### Compression

- [ ] Gzip enabled
- [ ] `gzip_vary on;`
- [ ] `gzip_proxied any;`
- [ ] `gzip_comp_level` set (4-6)
- [ ] `gzip_min_length` set (256)
- [ ] `gzip_types` includes all text formats

---

## Post-Deployment Verification

### Configuration Validation

- [ ] `nginx -t` passes without errors
- [ ] Configuration reloaded successfully
- [ ] No errors in error log after reload

### SSL/TLS Verification

- [ ] SSL Labs score A+ (or A minimum)
- [ ] HSTS preload eligible (if desired)
- [ ] Certificate chain valid
- [ ] Certificate renewal automated

### Functionality Testing

- [ ] HTTPS redirect works
- [ ] All virtual hosts accessible
- [ ] Proxy pass functioning
- [ ] WebSocket connections stable
- [ ] Caching working (check X-Cache-Status)
- [ ] Rate limiting effective

### Security Verification

- [ ] Security headers present (check with securityheaders.com)
- [ ] Hidden files return 403/404
- [ ] Version info hidden
- [ ] No sensitive paths exposed

### Performance Verification

- [ ] Response times acceptable
- [ ] Compression working (check Content-Encoding)
- [ ] Cache hit ratio satisfactory
- [ ] Connection reuse working

---

## Maintenance Checklist

### Regular Tasks

- [ ] Review access logs for anomalies
- [ ] Monitor error logs
- [ ] Check disk space for cache
- [ ] Verify SSL certificate expiry
- [ ] Review and update security headers
- [ ] Update nginx when security patches released

### Periodic Review

- [ ] Review rate limiting thresholds
- [ ] Audit access control rules
- [ ] Check for configuration drift
- [ ] Review and optimize caching
- [ ] Benchmark performance

---

## Quick Verification Commands

```bash
# Test configuration
sudo nginx -t

# Check SSL configuration
curl -I https://example.com

# Check security headers
curl -I -s https://example.com | grep -i "strict\|content-security\|x-frame\|x-content"

# Check cache status
curl -I https://example.com/api/endpoint | grep X-Cache

# Check compression
curl -I -H "Accept-Encoding: gzip" https://example.com | grep Content-Encoding

# Online tools
# - SSL Labs: https://www.ssllabs.com/ssltest/
# - Security Headers: https://securityheaders.com/
# - Mozilla Observatory: https://observatory.mozilla.org/
```
