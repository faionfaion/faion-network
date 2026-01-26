# Load Balancing Checklist

## Pre-Implementation

### Requirements Gathering

- [ ] Identify traffic patterns (steady, bursty, predictable)
- [ ] Estimate peak concurrent connections
- [ ] Determine protocol requirements (HTTP, HTTPS, TCP, UDP, gRPC)
- [ ] Identify session persistence requirements
- [ ] Define availability requirements (99.9%, 99.99%)
- [ ] Document geographic distribution needs
- [ ] List compliance requirements (PCI-DSS, HIPAA, SOC2)

### Architecture Decisions

- [ ] Choose L4 vs L7 based on requirements
- [ ] Select load balancing algorithm
- [ ] Decide on managed vs self-hosted
- [ ] Plan for high availability (active-active vs active-passive)
- [ ] Determine zone/region redundancy strategy
- [ ] Plan backend scaling approach

## Load Balancer Selection

### Cloud Managed (AWS)

- [ ] ALB for HTTP/HTTPS (L7)
- [ ] NLB for TCP/UDP (L4)
- [ ] GLB for cross-region (GSLB)
- [ ] Evaluate cost vs performance tradeoffs

### Cloud Managed (GCP)

- [ ] HTTP(S) Load Balancer (L7)
- [ ] TCP/UDP Load Balancer (L4)
- [ ] Internal Load Balancer

### Cloud Managed (Azure)

- [ ] Application Gateway (L7)
- [ ] Azure Load Balancer (L4)
- [ ] Front Door (global)

### Self-Hosted

- [ ] HAProxy for high performance
- [ ] Nginx for web applications
- [ ] Traefik for Kubernetes-native
- [ ] Envoy for service mesh

## Algorithm Selection

### Static Algorithms

- [ ] **Round Robin** - Equal capacity servers, stateless apps
- [ ] **Weighted Round Robin** - Different server capacities
- [ ] **IP Hash** - Simple session persistence needed
- [ ] **Random** - Simple stateless distribution

### Dynamic Algorithms

- [ ] **Least Connections** - Long-lived connections (WebSocket, database)
- [ ] **Weighted Least Connections** - Mixed capacity + long connections
- [ ] **Least Response Time** - Performance-critical applications
- [ ] **Resource Based** - Heterogeneous server resources

## Health Check Configuration

### Basic Setup

- [ ] Define health check endpoint (`/health`, `/healthz`, `/api/health`)
- [ ] Set appropriate interval (10-30s for production)
- [ ] Configure timeout (typically 5s)
- [ ] Set healthy threshold (2-3 consecutive successes)
- [ ] Set unhealthy threshold (2-3 consecutive failures)

### Health Check Types

- [ ] **TCP Check** - Basic connectivity verification
- [ ] **HTTP Check** - Application-level health
- [ ] **HTTPS Check** - Secure health verification
- [ ] **gRPC Check** - For gRPC services
- [ ] **Custom Script** - Complex health logic

### Health Endpoint Implementation

- [ ] Return 200 OK when healthy
- [ ] Check database connectivity
- [ ] Check external service dependencies
- [ ] Check disk space / memory (optional)
- [ ] Include version/build info in response (optional)
- [ ] Keep endpoint lightweight (< 100ms response)

## Session Persistence

### Requirements Check

- [ ] Application stores session state locally?
- [ ] Can centralize session storage instead?
- [ ] WebSocket connections needed?
- [ ] Evaluate impact on load distribution

### Configuration

- [ ] **Source IP** - Simple, works with any protocol
- [ ] **Cookie-based** - Most accurate for HTTP
- [ ] **Application Cookie** - When app manages sessions
- [ ] **SSL Session ID** - For SSL/TLS traffic

### Cookie Settings (if applicable)

- [ ] Set appropriate cookie TTL
- [ ] Configure secure flag for HTTPS
- [ ] Set HttpOnly flag
- [ ] Consider SameSite attribute

## SSL/TLS Configuration

### Certificate Management

- [ ] Obtain SSL/TLS certificates
- [ ] Configure certificate auto-renewal (Let's Encrypt, ACM)
- [ ] Set up certificate monitoring/alerting
- [ ] Plan certificate rotation procedure

### Protocol Settings

- [ ] Enable TLS 1.2 minimum (disable TLS 1.0, 1.1)
- [ ] Enable TLS 1.3 where supported
- [ ] Configure strong cipher suites
- [ ] Enable HSTS headers
- [ ] Configure OCSP stapling

### Termination Strategy

- [ ] **SSL Termination at LB** - Offload crypto from backends
- [ ] **SSL Pass-through** - End-to-end encryption
- [ ] **SSL Re-encryption** - Terminate and re-encrypt to backend

## High Availability

### Load Balancer Redundancy

- [ ] Deploy multiple LB instances
- [ ] Configure failover (active-passive or active-active)
- [ ] Test failover scenarios
- [ ] Document failover procedures

### Backend Redundancy

- [ ] Minimum 2 healthy instances per pool
- [ ] Distribute across availability zones
- [ ] Configure backup/standby servers
- [ ] Test with N-1 capacity (survive one server failure)

### Connection Draining

- [ ] Enable connection draining
- [ ] Set appropriate drain timeout (30-300s)
- [ ] Test graceful shutdown procedure

## Monitoring & Alerting

### Metrics to Monitor

- [ ] Active connections per backend
- [ ] Request rate (RPS)
- [ ] Response time / latency (p50, p95, p99)
- [ ] Error rate (4xx, 5xx)
- [ ] Health check status
- [ ] Backend server health
- [ ] Bandwidth utilization
- [ ] SSL certificate expiry

### Alerts to Configure

- [ ] Backend unhealthy (immediate)
- [ ] High error rate (> 1%)
- [ ] High latency (> SLA threshold)
- [ ] Connection pool exhaustion
- [ ] Certificate expiring (< 30 days)
- [ ] All backends unhealthy (critical)

### Logging

- [ ] Enable access logs
- [ ] Configure log retention
- [ ] Set up log aggregation (ELK, CloudWatch, etc.)
- [ ] Include relevant headers (X-Forwarded-For, X-Request-ID)

## Security

### Network Security

- [ ] Place backends in private subnets
- [ ] Configure security groups/firewall rules
- [ ] Restrict management access
- [ ] Enable VPC flow logs

### DDoS Protection

- [ ] Enable rate limiting
- [ ] Configure connection limits
- [ ] Enable cloud DDoS protection (AWS Shield, CloudFlare)
- [ ] Set up geo-blocking if needed

### Web Application Firewall (L7)

- [ ] Enable WAF for public-facing apps
- [ ] Configure OWASP rules
- [ ] Set up custom rules for app-specific threats
- [ ] Configure WAF logging

## Testing

### Functional Testing

- [ ] Verify traffic distribution
- [ ] Test health check behavior
- [ ] Verify session persistence
- [ ] Test SSL/TLS configuration
- [ ] Verify header forwarding (X-Forwarded-For, X-Real-IP)

### Failover Testing

- [ ] Test single backend failure
- [ ] Test multiple backend failures
- [ ] Test LB failover (if HA configured)
- [ ] Verify connection draining
- [ ] Test recovery after failure

### Performance Testing

- [ ] Load test at expected peak
- [ ] Test at 2x expected peak
- [ ] Measure latency under load
- [ ] Identify bottlenecks
- [ ] Test auto-scaling behavior

## Documentation

### Runbooks

- [ ] Document architecture diagram
- [ ] Create troubleshooting guide
- [ ] Document failover procedures
- [ ] Create scaling procedures
- [ ] Document certificate renewal process

### Configuration

- [ ] Store configuration in version control
- [ ] Document all settings and rationale
- [ ] Create disaster recovery plan
- [ ] Document rollback procedures

## Post-Implementation

### Ongoing Maintenance

- [ ] Review metrics weekly
- [ ] Update certificates before expiry
- [ ] Review and adjust health check settings
- [ ] Update algorithm if traffic patterns change
- [ ] Regular security patching
- [ ] Periodic failover testing

### Optimization

- [ ] Analyze latency patterns
- [ ] Review error rates
- [ ] Optimize health check intervals
- [ ] Consider HTTP/2 or HTTP/3 upgrade
- [ ] Review cost and right-size resources

---

*Load Balancing Checklist | faion-cicd-engineer*
