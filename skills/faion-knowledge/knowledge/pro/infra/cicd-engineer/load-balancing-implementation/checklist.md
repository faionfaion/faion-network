# Load Balancing Checklists

## Pre-Flight Checklist

### Requirements Gathering

- [ ] Traffic type identified (HTTP/HTTPS/TCP/gRPC)
- [ ] Expected RPS and concurrent connections estimated
- [ ] Session persistence requirements documented
- [ ] SSL/TLS termination location decided
- [ ] Health check endpoints available
- [ ] Backend server count and capacity known

### Architecture Decisions

- [ ] LB type selected (HAProxy/Nginx/Cloud/K8s)
- [ ] HA strategy defined (active-passive/active-active)
- [ ] Cross-zone balancing configured
- [ ] Failover behavior documented
- [ ] Scaling strategy planned

### Security Review

- [ ] TLS 1.2+ enforced
- [ ] Strong cipher suites configured
- [ ] Rate limiting rules defined
- [ ] DDoS protection enabled
- [ ] Security headers configured
- [ ] Access logging enabled

---

## HAProxy Production Checklist

### Configuration

- [ ] `maxconn` set appropriately (default 20000)
- [ ] `nbproc`/`nbthread` matches CPU cores
- [ ] `cpu-map` configured for process affinity
- [ ] Timeouts tuned (connect/client/server)
- [ ] Logging configured to syslog

### Health Checks

- [ ] Health check endpoint defined (`/health` or `/healthz`)
- [ ] `option httpchk` configured
- [ ] Check interval appropriate (10-30s)
- [ ] Healthy/unhealthy thresholds set
- [ ] Backup servers configured

### Security

- [ ] Rate limiting via stick-tables
- [ ] SSL certificate path correct
- [ ] Admin socket restricted (`mode 660`)
- [ ] Stats page protected or disabled
- [ ] ACLs for sensitive endpoints

### Performance

- [ ] Connection reuse enabled (`http-server-close`)
- [ ] `forwardfor` header set
- [ ] Backend weights configured
- [ ] `maxconn` per server set
- [ ] Compression enabled if needed

---

## Nginx Production Checklist

### Configuration

- [ ] Worker processes match CPU cores
- [ ] Worker connections set (default 1024)
- [ ] Upstream zone configured for shared state
- [ ] Keepalive connections enabled
- [ ] Buffering tuned for workload

### Health Checks

- [ ] `max_fails` and `fail_timeout` set
- [ ] Backup servers configured
- [ ] Health check module enabled (Plus) or external
- [ ] Passive health checks understood

### Security

- [ ] TLS 1.2+ protocols only
- [ ] `ssl_prefer_server_ciphers on`
- [ ] Security headers added (HSTS, etc.)
- [ ] Rate limiting zones configured
- [ ] Connection limits set

### Performance

- [ ] `proxy_http_version 1.1` for keepalive
- [ ] `proxy_set_header Connection ""` set
- [ ] `proxy_next_upstream` configured
- [ ] Timeouts appropriate for backend
- [ ] Gzip compression enabled

---

## AWS ALB/NLB Checklist

### Setup

- [ ] Load balancer type correct (ALB for HTTP, NLB for TCP)
- [ ] Subnets span multiple AZs
- [ ] Security groups allow required traffic
- [ ] Access logs enabled to S3
- [ ] Deletion protection enabled

### Target Groups

- [ ] Health check path correct
- [ ] Health check interval and thresholds set
- [ ] Deregistration delay configured
- [ ] Stickiness enabled if needed
- [ ] Target type appropriate (instance/IP)

### Listeners

- [ ] HTTPS listener with valid certificate
- [ ] HTTP to HTTPS redirect configured
- [ ] SSL policy appropriate (TLS 1.2+)
- [ ] Default action configured
- [ ] Path-based routing rules if needed

### Security

- [ ] WAF attached if needed
- [ ] Shield protection enabled
- [ ] Security groups least-privilege
- [ ] VPC endpoint for private access

---

## Kubernetes Ingress Checklist

### Ingress Controller

- [ ] Multiple replicas deployed (3+)
- [ ] Pod disruption budget configured
- [ ] Anti-affinity rules set
- [ ] Resource requests/limits defined
- [ ] Ingress class specified

### Ingress Resource

- [ ] TLS secret created and referenced
- [ ] Host rules configured
- [ ] Path rules appropriate (Prefix/Exact)
- [ ] Annotations for controller-specific features
- [ ] Backend services exist and healthy

### Security

- [ ] `force-ssl-redirect` enabled
- [ ] Rate limiting annotations set
- [ ] CORS configured if needed
- [ ] Body size limits set
- [ ] Whitelist/blacklist IPs if required

### High Availability

- [ ] Controller spans availability zones
- [ ] External traffic policy considered
- [ ] Session affinity configured if needed
- [ ] Timeout annotations set
- [ ] Retry annotations configured

---

## Monitoring Checklist

### Metrics

- [ ] Prometheus exporter deployed (haproxy/nginx)
- [ ] Scrape config added
- [ ] Key metrics identified:
  - Request rate
  - Error rate (4xx/5xx)
  - Latency (p50/p95/p99)
  - Active connections
  - Backend health

### Alerts

- [ ] Backend down alert configured
- [ ] High error rate alert (>1%)
- [ ] High latency alert (p99 > threshold)
- [ ] Connection pool exhaustion alert
- [ ] Certificate expiry alert

### Dashboards

- [ ] Overview dashboard created
- [ ] Per-backend metrics visible
- [ ] Error breakdown by type
- [ ] Latency histograms
- [ ] Geographic distribution if relevant

### Logging

- [ ] Access logs enabled
- [ ] Error logs captured
- [ ] Log rotation configured
- [ ] Log aggregation to central system
- [ ] Request tracing headers forwarded

---

## Troubleshooting Checklist

### Connection Issues

- [ ] Backend servers reachable from LB
- [ ] Firewall rules allow traffic
- [ ] DNS resolves correctly
- [ ] Ports match configuration
- [ ] Health checks passing

### Performance Issues

- [ ] Connection limits not exhausted
- [ ] Backend capacity sufficient
- [ ] Network latency normal
- [ ] SSL offload working
- [ ] Caching effective

### Security Issues

- [ ] Certificates valid and not expired
- [ ] TLS negotiation successful
- [ ] Rate limits not too aggressive
- [ ] Headers forwarded correctly
- [ ] Logs show request details

---

*Load Balancing Checklists | faion-cicd-engineer*
