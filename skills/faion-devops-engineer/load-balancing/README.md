# Load Balancing

Comprehensive guide to load balancing strategies, algorithms, and implementation patterns for high availability and performance.

## Overview

Load balancing distributes network traffic across multiple servers to ensure high availability, reliability, and performance. This methodology covers strategies from basic algorithms to cloud-native implementations.

## When to Use

- Scaling applications horizontally
- Ensuring high availability (HA)
- Improving application performance
- Implementing zero-downtime deployments
- Managing traffic spikes
- Geographic distribution of traffic

## Load Balancer Types

| Type | OSI Layer | Features | Use Case |
|------|-----------|----------|----------|
| L4 (Transport) | Layer 4 | TCP/UDP routing, fast, low latency | High throughput, gaming, streaming |
| L7 (Application) | Layer 7 | HTTP routing, SSL termination, content-based | Web applications, APIs, microservices |
| DNS | Layer 3 | Geographic distribution, simple failover | Global load balancing, CDN routing |
| Global | Multi-layer | Cross-region failover, latency-based | Multi-cloud, disaster recovery |

### L4 vs L7 Trade-offs

| Aspect | L4 Load Balancer | L7 Load Balancer |
|--------|------------------|------------------|
| Speed | Faster (no payload inspection) | Slower (parses HTTP) |
| Flexibility | Limited (IP/port only) | High (headers, cookies, paths) |
| SSL | Passthrough or terminate | Terminate and inspect |
| Routing | Connection-based | Request-based |
| Use Cases | Database, mail, gaming | Web apps, APIs, microservices |

## Algorithms

### Algorithm Comparison

| Algorithm | Best For | Pros | Cons |
|-----------|----------|------|------|
| Round Robin | Equal capacity servers | Simple, fair | Ignores server load |
| Weighted Round Robin | Mixed capacity servers | Accounts for capacity | Static weights |
| Least Connections | Long-lived connections | Adapts to load | Tracking overhead |
| Weighted Least Conn | Mixed capacity + long conn | Best distribution | Complex calculation |
| IP Hash | Session persistence | Sticky sessions | Uneven distribution |
| Least Response Time | Performance critical | Optimizes latency | Requires health probes |
| Random | Stateless apps | No state needed | May be uneven |
| Consistent Hashing | Caching, sharding | Minimal rehashing | Complex implementation |

### Algorithm Selection Guide

```
START
  |
  v
Need session persistence? --YES--> IP Hash or Cookie-based
  |
  NO
  v
Servers have equal capacity? --NO--> Weighted algorithms
  |
  YES
  v
Long-lived connections? --YES--> Least Connections
  |
  NO
  v
Performance critical? --YES--> Least Response Time
  |
  NO
  v
Use Round Robin (simplest)
```

## Health Checks

### Health Check Types

| Type | Layer | Check Method | Best For |
|------|-------|--------------|----------|
| TCP Connect | L4 | Port accepts connections | Basic availability |
| HTTP/HTTPS | L7 | Status code check | Web applications |
| gRPC | L7 | gRPC health protocol | gRPC services |
| Script/Custom | L7 | Custom health logic | Complex dependencies |

### Health Check Parameters

| Parameter | Description | Recommended Value |
|-----------|-------------|-------------------|
| Interval | Time between probes | 10-30 seconds |
| Timeout | Wait for response | 5-10 seconds (< interval) |
| Healthy Threshold | Probes to mark healthy | 2-3 consecutive |
| Unhealthy Threshold | Probes to mark unhealthy | 2-3 consecutive |
| Start Period | Grace period on startup | 30-60 seconds |

### Health Check Best Practices

1. **Check dependencies** - Include database, cache, external services
2. **Use dedicated endpoints** - `/health` or `/healthz` for probes
3. **Separate liveness/readiness** - Different endpoints for different purposes
4. **Include version info** - Return app version in health response
5. **Set appropriate timeouts** - Timeout must be less than interval
6. **Log health check failures** - For debugging and alerting

## SSL/TLS Termination

### Termination Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Termination at LB | LB decrypts, sends HTTP to backends | Most common, offloads CPU |
| Re-encryption | LB decrypts, re-encrypts to backends | End-to-end encryption required |
| TLS Passthrough | LB forwards encrypted traffic | Backends must see original TLS |

### SSL Best Practices (2025-2026)

| Practice | Recommendation |
|----------|---------------|
| TLS Version | TLS 1.3 preferred, TLS 1.2 minimum |
| Cipher Suites | ECDHE + AES-GCM, disable weak ciphers |
| Certificate | Automate renewal (Let's Encrypt, ACME) |
| Key Protection | HSM for production, vault for secrets |
| HSTS | Enable with long max-age |
| OCSP Stapling | Enable for faster validation |

## High Availability

### HA Patterns

| Pattern | Description | Failover Time |
|---------|-------------|---------------|
| Active-Passive | Standby takes over on failure | 1-30 seconds |
| Active-Active | Both handle traffic | Near-zero |
| DNS Failover | DNS switches to backup | TTL-dependent (minutes) |
| Anycast | Same IP, multiple locations | Near-zero |

### HA Checklist

- [ ] Deploy LB in multiple availability zones
- [ ] Configure health checks for LB itself
- [ ] Use floating/virtual IP for failover
- [ ] Test failover procedures regularly
- [ ] Monitor LB health and capacity
- [ ] Document failover runbooks

## Cloud Load Balancers

### AWS

| Service | Layer | Use Case |
|---------|-------|----------|
| ALB (Application) | L7 | HTTP/HTTPS, WebSocket |
| NLB (Network) | L4 | TCP/UDP, extreme performance |
| GLB (Gateway) | L3 | Firewalls, appliances |
| CLB (Classic) | L4/L7 | Legacy (avoid for new) |

### GCP

| Service | Layer | Use Case |
|---------|-------|----------|
| HTTP(S) LB | L7 | Global HTTP/HTTPS |
| TCP/UDP LB | L4 | Regional TCP/UDP |
| Internal LB | L4/L7 | Private network traffic |

### Azure

| Service | Layer | Use Case |
|---------|-------|----------|
| Application Gateway | L7 | HTTP/HTTPS, WAF |
| Azure Load Balancer | L4 | TCP/UDP |
| Front Door | L7 | Global, CDN integration |
| Traffic Manager | DNS | DNS-based routing |

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview document |
| [checklist.md](checklist.md) | Implementation checklists |
| [examples.md](examples.md) | Configuration examples |
| [templates.md](templates.md) | Ready-to-use templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for load balancing tasks |

## Sources

- [HAProxy Documentation](https://www.haproxy.org/documentation.html)
- [Nginx Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)
- [AWS ELB Documentation](https://docs.aws.amazon.com/elasticloadbalancing/)
- [GCP Load Balancing](https://cloud.google.com/load-balancing/docs)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [How Load Balancers Work](https://blog.algomaster.io/p/how-load-balancers-actually-work)
- [Load Balancing Methods](https://www.loadbalancer.org/blog/load-balancing-methods/)
- [SSL Termination Guide 2025](https://livingdevops.com/devops/ssl-termination-complete-guide-2025/)
