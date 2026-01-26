# Load Balancing Concepts

## Overview

Load balancing distributes network traffic across multiple servers to ensure high availability, reliability, and performance. This methodology covers load balancing strategies, algorithms, health checks, session persistence, and L4 vs L7 architecture patterns.

## When to Use

- Scaling applications horizontally
- Ensuring high availability (HA)
- Improving application performance
- Implementing zero-downtime deployments
- Managing traffic spikes
- Distributing workloads across regions

## Key Concepts

### Load Balancer Types

| Type | OSI Layer | Features | Use Case |
|------|-----------|----------|----------|
| L4 (Transport) | Layer 4 | TCP/UDP routing, fast, low latency | High throughput, gaming, streaming |
| L7 (Application) | Layer 7 | HTTP routing, SSL termination, content-based | Web applications, APIs, microservices |
| DNS | Layer 3 | Geographic distribution | Global load balancing |
| Global | Multi-layer | Cross-region failover | Multi-cloud, disaster recovery |

### L4 vs L7 Load Balancing

| Aspect | Layer 4 | Layer 7 |
|--------|---------|---------|
| OSI Layer | Transport | Application |
| Routing basis | IP address, TCP/UDP port | HTTP headers, URL, cookies, content |
| Performance | Faster, less CPU-intensive | Slower, more resource-intensive |
| SSL/TLS | Pass-through | Termination supported |
| Content inspection | No | Yes |
| Use cases | High-throughput, simple routing | Content routing, API gateway |
| Features | Basic forwarding | URL rewriting, header manipulation |

**When to use L4:**
- Maximum performance is critical
- Simple TCP/UDP load balancing
- SSL pass-through required
- Protocol-agnostic routing

**When to use L7:**
- Content-based routing needed
- SSL termination at load balancer
- HTTP header manipulation
- API gateway functionality
- A/B testing, canary deployments

### Load Balancing Algorithms

#### Static Algorithms

| Algorithm | Description | Pros | Cons | Use Case |
|-----------|-------------|------|------|----------|
| Round Robin | Sequential distribution | Simple, fair | Ignores server load | Equal capacity servers |
| Weighted Round Robin | Round robin with weights | Accounts for capacity | Static weights | Mixed capacity servers |
| IP Hash | Routes based on client IP | Sticky sessions | Uneven distribution | Session persistence |
| Random | Random server selection | Simple, no state | May cause uneven distribution | Stateless applications |

#### Dynamic Algorithms

| Algorithm | Description | Pros | Cons | Use Case |
|-----------|-------------|------|------|----------|
| Least Connections | Fewest active connections | Adapts to load | Connection tracking overhead | Long-lived connections |
| Weighted Least Connections | Least connections + weights | Best overall distribution | Complex calculation | Mixed capacity, long connections |
| Least Response Time | Fastest responding server | Optimizes response time | Requires health probes | Performance critical |
| Resource Based | Based on server resources | Optimal utilization | Agent required | Heterogeneous environments |

### Health Checks

Health checks monitor backend server status and route traffic only to healthy instances.

#### Health Check Types

| Type | Protocol | Use Case | Depth |
|------|----------|----------|-------|
| TCP | TCP connection | Basic connectivity | Shallow |
| HTTP/HTTPS | HTTP request | Web application health | Medium |
| gRPC | gRPC health protocol | gRPC services | Medium |
| Custom Script | Application-specific | Complex health logic | Deep |

#### Health Check Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| Interval | Time between checks | 10-30 seconds |
| Timeout | Response timeout | 5 seconds |
| Healthy Threshold | Consecutive successes to mark healthy | 2-3 |
| Unhealthy Threshold | Consecutive failures to mark unhealthy | 2-3 |
| Path | HTTP health check endpoint | `/health`, `/healthz` |

### Session Persistence (Sticky Sessions)

Session persistence ensures requests from the same client go to the same backend server.

#### Persistence Methods

| Method | Description | Pros | Cons |
|--------|-------------|------|------|
| Source IP | Based on client IP | Simple, no cookies | NAT issues, uneven distribution |
| Cookie-based | LB-generated cookie | Accurate, configurable | Cookie overhead |
| Application Cookie | App-generated cookie | Application control | Requires app changes |
| SSL Session ID | Based on SSL session | Secure | Limited to SSL traffic |

#### When to Use Sticky Sessions

**Use when:**
- Application stores session state locally
- Shopping carts, login sessions
- In-memory caching per server
- WebSocket connections

**Avoid when:**
- Stateless applications
- Centralized session storage (Redis)
- Maximum distribution needed
- Auto-scaling environments

## Architecture Patterns

### Single Region

```
Internet
    |
[Load Balancer]
    |
+---+---+---+
|   |   |   |
S1  S2  S3  S4  (Backend Servers)
```

### Multi-Region with GSLB

```
                    [DNS/GSLB]
                        |
         +--------------+--------------+
         |                             |
    [Regional LB]                [Regional LB]
    US-East                      EU-West
         |                             |
    +----+----+                   +----+----+
    |    |    |                   |    |    |
   S1   S2   S3                  S1   S2   S3
```

### High Availability

```
        [Active LB] <---> [Standby LB]
              |                |
              +-------+--------+
                      |
              +-------+-------+
              |       |       |
             S1      S2      S3
```

## Best Practices (2025-2026)

### High Availability

1. **Avoid single points of failure** - Use active-active or active-passive LB pairs
2. **Zone redundancy** - Deploy across availability zones
3. **Minimum 2 healthy instances** per backend pool
4. **Health check endpoints** - Deeper checks (API endpoints) over basic pings

### Performance

1. **Use HTTP/2 or HTTP/3** - Better pipelining and connection handling
2. **Enable connection keepalive** - Reduce connection overhead
3. **SSL/TLS offloading** - Let LB handle encryption
4. **Connection draining** - Graceful backend removal

### Security

1. **TLS 1.2 minimum** - Disable older protocols
2. **DDoS protection** - Rate limiting, connection limits
3. **Web Application Firewall (WAF)** - For L7 load balancers
4. **Private backend networks** - Backend servers not publicly accessible

### Monitoring

1. **Active and passive health checks** - Combine for faster detection
2. **Connection metrics** - Track active connections per server
3. **Latency monitoring** - Response time per backend
4. **Error rate tracking** - 4xx/5xx responses

## Market Share (2025)

| Load Balancer | Market Share | Type |
|---------------|--------------|------|
| AWS ELB | ~67% | Cloud managed |
| Nginx | ~15% | Open source / Plus |
| HAProxy | ~8% | Open source / Enterprise |
| F5 BIG-IP | ~5% | Enterprise hardware/software |
| Traefik | ~3% | Cloud native |
| Others | ~2% | Various |

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Configuration examples |
| [templates.md](templates.md) | Ready-to-use templates |
| [llm-prompts.md](llm-prompts.md) | AI assistant prompts |

## Sources

- [Kemp - Load Balancing Best Practices](https://kemptechnologies.com/blog/load-balancing-best-practices)
- [Google Cloud - Load Balancing Best Practices](https://cloud.google.com/load-balancing/docs/https/http-load-balancing-best-practices)
- [Azure - Load Balancer Best Practices](https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-best-practices)
- [Gcore - Load Balancing Algorithms](https://gcore.com/learning/load-balancing-algorithms)
- [HAProxy - L4 vs L7](https://www.haproxy.com/blog/layer-4-vs-layer-7-load-balancing)
- [HAProxy - Sticky Sessions](https://www.haproxy.com/blog/load-balancing-affinity-persistence-sticky-sessions-what-you-need-to-know)
- [A10 Networks - L4 vs L7](https://www.a10networks.com/glossary/how-do-layer-4-and-layer-7-load-balancing-differ/)
- [Cloudflare - Load Balancing Algorithms](https://www.cloudflare.com/learning/performance/types-of-load-balancing-algorithms/)
- [AWS - Health Checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)

---

*Load Balancing Concepts | faion-cicd-engineer*
