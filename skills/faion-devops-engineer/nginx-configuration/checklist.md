# Nginx Configuration Checklist

## Pre-Deployment Checklist

### Basic Configuration

- [ ] `worker_processes auto` set
- [ ] `worker_connections` appropriate for expected load (4096+)
- [ ] `sendfile on` enabled
- [ ] `tcp_nopush on` enabled
- [ ] `tcp_nodelay on` enabled
- [ ] `keepalive_timeout` configured (65s recommended)
- [ ] `types_hash_max_size` set (2048+)

### Security Hardening

- [ ] `server_tokens off` - Hide Nginx version
- [ ] Non-root user configured (`user www-data`)
- [ ] Unnecessary modules disabled
- [ ] File permissions verified (config: 644, ssl keys: 600)
- [ ] Access to sensitive files denied (`.git`, `.env`, etc.)

### SSL/TLS Configuration

- [ ] TLS 1.2 and 1.3 only (`ssl_protocols TLSv1.2 TLSv1.3`)
- [ ] TLS 1.0 and 1.1 disabled
- [ ] Strong cipher suites configured
- [ ] `ssl_prefer_server_ciphers on`
- [ ] SSL session cache configured
- [ ] SSL session timeout set (1d recommended)
- [ ] Session tickets disabled (`ssl_session_tickets off`)
- [ ] DH parameters generated (2048-bit minimum)
- [ ] HTTP to HTTPS redirect configured
- [ ] SSL certificate valid and not expiring soon

### Security Headers

- [ ] `Strict-Transport-Security` (HSTS) enabled
- [ ] `X-Frame-Options DENY` or `SAMEORIGIN`
- [ ] `X-Content-Type-Options nosniff`
- [ ] `X-XSS-Protection 1; mode=block`
- [ ] `Referrer-Policy` configured
- [ ] `Permissions-Policy` configured
- [ ] `Content-Security-Policy` configured (if applicable)

### Rate Limiting

- [ ] Rate limit zones defined
- [ ] Connection limits configured
- [ ] Burst settings appropriate
- [ ] Rate limit applied to sensitive endpoints

### Reverse Proxy (if applicable)

- [ ] `proxy_pass` configured correctly
- [ ] `proxy_set_header Host $host`
- [ ] `proxy_set_header X-Real-IP $remote_addr`
- [ ] `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for`
- [ ] `proxy_set_header X-Forwarded-Proto $scheme`
- [ ] Proxy timeouts configured
- [ ] Proxy buffering configured appropriately
- [ ] Health check endpoint accessible
- [ ] WebSocket support configured (if needed)

### Load Balancing (if applicable)

- [ ] Upstream servers defined
- [ ] Load balancing method selected
- [ ] Keepalive connections to upstream
- [ ] Failover configured (`max_fails`, `fail_timeout`)
- [ ] Backup servers defined (if needed)

### Caching (if applicable)

- [ ] Cache path configured with appropriate size
- [ ] Cache keys defined
- [ ] Cache validity rules set
- [ ] Stale cache behavior configured
- [ ] Cache bypass rules defined
- [ ] Cache status header added for debugging

### Compression

- [ ] Gzip enabled
- [ ] `gzip_vary on`
- [ ] `gzip_proxied any`
- [ ] `gzip_comp_level` set (6 is good balance)
- [ ] `gzip_min_length` set (256 bytes)
- [ ] `gzip_types` includes all text content

### Logging

- [ ] Access log configured with appropriate format
- [ ] Error log configured with appropriate level
- [ ] Log rotation configured (logrotate)
- [ ] JSON log format for parsing (if using log aggregation)
- [ ] Sensitive data not logged (passwords, tokens)

### Static Files

- [ ] Cache headers set for static assets
- [ ] `expires` directive configured
- [ ] `add_header Cache-Control` configured
- [ ] `access_log off` for static files (optional)

---

## Testing Checklist

### Configuration Testing

- [ ] `nginx -t` passes without errors
- [ ] `nginx -T` shows expected configuration
- [ ] Configuration reload works (`nginx -s reload`)

### SSL Testing

- [ ] SSL Labs test score A or A+ ([ssllabs.com](https://www.ssllabs.com/ssltest/))
- [ ] Certificate chain valid
- [ ] HSTS preload requirements met (if submitting)
- [ ] Mixed content warnings resolved

### Security Testing

- [ ] Version not exposed in headers
- [ ] Security headers present (check with [securityheaders.com](https://securityheaders.com))
- [ ] Directory listing disabled
- [ ] Sensitive files inaccessible
- [ ] Rate limiting works as expected

### Performance Testing

- [ ] Response times acceptable
- [ ] Compression working (`Accept-Encoding: gzip`)
- [ ] Cache headers correct
- [ ] Keepalive working
- [ ] Load tested with expected traffic

### Functionality Testing

- [ ] All routes respond correctly
- [ ] HTTP to HTTPS redirect works
- [ ] WebSocket connections work (if applicable)
- [ ] File uploads work (if applicable)
- [ ] Proxy passes requests correctly (if applicable)

---

## Maintenance Checklist

### Regular Tasks

- [ ] Certificate renewal automated and working
- [ ] Logs rotated and archived
- [ ] Disk space monitored
- [ ] SSL configuration reviewed quarterly
- [ ] Security headers reviewed for new standards

### Monitoring

- [ ] Metrics endpoint exposed (stub_status)
- [ ] Alerting configured for errors
- [ ] Response time monitoring active
- [ ] SSL certificate expiry monitoring
- [ ] Log analysis for anomalies

### Updates

- [ ] Nginx version current (security patches)
- [ ] SSL/TLS configuration aligned with current best practices
- [ ] Cipher suites updated for new vulnerabilities
- [ ] Dependencies updated

---

## Quick Validation Commands

```bash
# Test configuration
sudo nginx -t

# Check SSL grade
curl -s "https://api.ssllabs.com/api/v3/analyze?host=example.com" | jq '.endpoints[0].grade'

# Verify security headers
curl -I https://example.com 2>/dev/null | grep -E '^(Strict-Transport|X-Frame|X-Content|Content-Security)'

# Check compression
curl -H "Accept-Encoding: gzip" -I https://example.com 2>/dev/null | grep -i content-encoding

# Check certificate expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Benchmark
ab -n 1000 -c 100 https://example.com/
```
