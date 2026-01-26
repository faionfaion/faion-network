# Load Balancing Checklists

## Pre-Implementation Checklist

### Requirements Analysis

- [ ] Identify expected traffic volume (requests/second)
- [ ] Determine peak traffic patterns
- [ ] List all backend services to balance
- [ ] Define session persistence requirements
- [ ] Identify SSL/TLS requirements
- [ ] Document latency requirements (P50, P95, P99)
- [ ] List geographic distribution needs
- [ ] Define failover requirements (RTO, RPO)

### Architecture Decisions

- [ ] Choose L4 vs L7 load balancing
- [ ] Select load balancing algorithm
- [ ] Decide on SSL termination strategy
- [ ] Plan health check strategy
- [ ] Design high availability topology
- [ ] Choose cloud vs self-hosted solution

## HAProxy Implementation Checklist

### Installation

- [ ] Install HAProxy package
- [ ] Verify version supports required features
- [ ] Configure system limits (ulimit, sysctl)
- [ ] Set up logging (syslog or file)

### Configuration

- [ ] Configure global settings (logging, SSL params)
- [ ] Set appropriate timeouts (connect, client, server)
- [ ] Define frontend(s) with bind addresses
- [ ] Configure backend(s) with server pool
- [ ] Select and configure balancing algorithm
- [ ] Set up health checks for each backend
- [ ] Configure SSL certificates (if terminating)
- [ ] Add HTTP redirect (80 to 443)
- [ ] Configure stats dashboard
- [ ] Set up ACL rules for routing

### Security

- [ ] Restrict stats dashboard access
- [ ] Configure SSL/TLS properly (TLS 1.2+)
- [ ] Use strong cipher suites
- [ ] Enable HSTS headers
- [ ] Configure rate limiting (if needed)
- [ ] Set up DDoS protection rules

### Testing

- [ ] Validate configuration syntax (`haproxy -c -f`)
- [ ] Test health check endpoints
- [ ] Verify traffic distribution
- [ ] Test failover behavior
- [ ] Verify sticky sessions (if configured)
- [ ] Load test under expected traffic

## Nginx Implementation Checklist

### Installation

- [ ] Install Nginx with required modules
- [ ] Verify stream module (for L4)
- [ ] Configure worker processes
- [ ] Set up logging

### Configuration

- [ ] Define upstream blocks
- [ ] Configure server weights
- [ ] Set load balancing method
- [ ] Configure keepalive connections
- [ ] Set up proxy headers (Host, X-Real-IP, X-Forwarded-For)
- [ ] Configure timeouts (connect, send, read)
- [ ] Set up retry behavior (next_upstream)
- [ ] Configure SSL certificates
- [ ] Add health check location

### Testing

- [ ] Test configuration (`nginx -t`)
- [ ] Verify upstream health
- [ ] Test failover scenarios
- [ ] Verify header forwarding
- [ ] Load test configuration

## AWS ALB/NLB Implementation Checklist

### Setup

- [ ] Create load balancer (internet-facing or internal)
- [ ] Configure security groups
- [ ] Select availability zones
- [ ] Configure access logs (S3 bucket)

### Target Groups

- [ ] Create target group(s)
- [ ] Configure health check settings
- [ ] Set deregistration delay
- [ ] Configure stickiness (if needed)
- [ ] Register targets (instances, IPs, Lambda)

### Listeners

- [ ] Create HTTPS listener (443)
- [ ] Configure SSL certificate (ACM)
- [ ] Set SSL policy (TLS 1.2+)
- [ ] Create HTTP listener (80) with redirect
- [ ] Add listener rules for path/host routing

### High Availability

- [ ] Deploy across multiple AZs
- [ ] Configure cross-zone load balancing
- [ ] Set up CloudWatch alarms
- [ ] Configure Auto Scaling integration
- [ ] Test failover between AZs

## Kubernetes Load Balancing Checklist

### Service Configuration

- [ ] Choose service type (ClusterIP, NodePort, LoadBalancer)
- [ ] Configure selectors correctly
- [ ] Set appropriate ports
- [ ] Add service annotations for cloud LB

### Ingress Setup

- [ ] Deploy ingress controller (Nginx, Traefik, etc.)
- [ ] Create ingress resources
- [ ] Configure TLS termination
- [ ] Set up path-based routing
- [ ] Configure host-based routing
- [ ] Add annotations for advanced features

### Health & Monitoring

- [ ] Configure readiness probes
- [ ] Configure liveness probes
- [ ] Set up startup probes (for slow apps)
- [ ] Configure pod disruption budgets
- [ ] Set up horizontal pod autoscaler

## Health Check Implementation Checklist

### Endpoint Design

- [ ] Create dedicated health endpoint (`/health` or `/healthz`)
- [ ] Include dependency checks (DB, cache, etc.)
- [ ] Return appropriate status codes (200/503)
- [ ] Include response body with details
- [ ] Add version/build info
- [ ] Implement separate liveness and readiness checks

### Configuration

- [ ] Set check interval (10-30s recommended)
- [ ] Set timeout (< interval)
- [ ] Configure healthy threshold (2-3)
- [ ] Configure unhealthy threshold (2-3)
- [ ] Set startup grace period
- [ ] Configure check path and expected response

### Monitoring

- [ ] Log health check failures
- [ ] Alert on repeated failures
- [ ] Track health check latency
- [ ] Monitor backend pool health percentage

## SSL/TLS Checklist

### Certificate Management

- [ ] Obtain SSL certificate (Let's Encrypt, commercial CA)
- [ ] Configure certificate in load balancer
- [ ] Set up certificate auto-renewal
- [ ] Configure certificate chain properly
- [ ] Store private keys securely

### TLS Configuration

- [ ] Enable TLS 1.2 and 1.3 only
- [ ] Disable SSLv3, TLS 1.0, TLS 1.1
- [ ] Configure strong cipher suites
- [ ] Enable perfect forward secrecy (ECDHE)
- [ ] Set DH parameter size (2048+ bits)
- [ ] Enable OCSP stapling
- [ ] Configure HSTS header

### Validation

- [ ] Test with SSL Labs (A+ rating goal)
- [ ] Verify certificate chain
- [ ] Test TLS handshake performance
- [ ] Verify HTTP to HTTPS redirect
- [ ] Check for mixed content issues

## High Availability Checklist

### Architecture

- [ ] Deploy load balancers in multiple AZs
- [ ] Configure floating/virtual IP
- [ ] Set up active-passive or active-active
- [ ] Configure health checks for LB itself
- [ ] Plan for LB capacity limits

### Failover

- [ ] Configure automatic failover
- [ ] Set appropriate failover thresholds
- [ ] Test failover scenarios
- [ ] Document manual failover procedures
- [ ] Set up failover notifications

### Monitoring

- [ ] Monitor LB health metrics
- [ ] Track connection counts
- [ ] Monitor error rates (4xx, 5xx)
- [ ] Set up latency alerts
- [ ] Monitor SSL certificate expiry
- [ ] Track backend pool health

## Production Readiness Checklist

### Performance

- [ ] Load test at 2x expected peak
- [ ] Verify latency requirements met
- [ ] Check connection limits
- [ ] Validate SSL offload capacity
- [ ] Test auto-scaling behavior

### Operational

- [ ] Document configuration
- [ ] Create runbooks for common issues
- [ ] Set up alerting and on-call
- [ ] Plan maintenance windows
- [ ] Document rollback procedures

### Security

- [ ] Security audit completed
- [ ] DDoS protection configured
- [ ] WAF rules reviewed (if applicable)
- [ ] Access controls verified
- [ ] Audit logging enabled

### Disaster Recovery

- [ ] Backup configuration
- [ ] Document recovery procedures
- [ ] Test disaster recovery
- [ ] Verify DNS failover (if used)
- [ ] Document RTO/RPO compliance
