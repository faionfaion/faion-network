# Load Balancing Implementation

## Overview

Production-ready load balancing implementation guide covering health checks, best practices, monitoring, and security for HAProxy, Nginx, cloud load balancers, and Kubernetes Ingress.

## When to Use

- Implementing load balancer health checks
- Configuring HAProxy or Nginx for production
- Setting up AWS/GCP/Azure load balancers
- Deploying Kubernetes Ingress controllers
- Optimizing LB performance and security

## Quick Decision Matrix

| Scenario | Recommended Solution |
|----------|---------------------|
| Raw TCP performance, high concurrency | HAProxy |
| Web server + reverse proxy combo | Nginx |
| Kubernetes simple HTTP routing | Nginx Ingress |
| Kubernetes advanced L4/L7 | HAProxy Ingress |
| AWS managed, auto-scaling | ALB/NLB |
| Multi-cloud, future-proof | Gateway API |

## HAProxy vs Nginx Selection (2025-2026)

### Choose HAProxy When

- **TCP-heavy environments** - 10-15% better raw connection handling
- **High concurrency needs** - Superior under extreme loads
- **Fine-grained connection control** - Advanced retries, circuit breaking
- **Native HTTP/3 and gRPC support** required
- **Microservices/IoT** - Rapid connection establishment patterns
- **Bare metal/self-hosted** - Maximum performance control

### Choose Nginx When

- **Web server + LB combo** - Versatile out-of-box
- **Static content caching** - Built-in cache layer
- **Simpler configuration** - Easier for basic setups
- **WebSocket proxying** - Native support
- **Path-based routing** - Clean HTTP routing rules

### Combined Pattern (HA Architecture)

```
HAProxy (L4 TCP LB)
    |
    +-- Nginx Ingress Pod 1 (Node A)
    +-- Nginx Ingress Pod 2 (Node B)
    +-- Nginx Ingress Pod 3 (Node C)
            |
            +-- Backend Services
```

Use HAProxy as TCP load balancer in front of Ingress-NGINX for bare-metal and on-premise Kubernetes clusters.

## Health Check Types

| Type | Use Case | Example |
|------|----------|---------|
| TCP | Basic connectivity | `option tcp-check` |
| HTTP | Application health | `GET /health` |
| HTTPS | SSL-enabled services | Verify SSL cert |
| Script | Complex logic | Custom shell script |
| gRPC | gRPC services | `grpc.health.v1.Health/Check` |

## Best Practices Summary

### High Availability

1. Multiple LB instances across AZs
2. Active-passive with keepalived
3. Health check tuning (balance sensitivity/stability)
4. Graceful degradation on partial failures

### Performance

1. Connection pooling and keepalive
2. SSL termination at LB layer
3. Response caching for static content
4. Tune worker processes to CPU cores

### Security

1. TLS 1.2+ only, strong ciphers
2. Rate limiting and WAF
3. Security headers (HSTS, X-Frame-Options)
4. Access logging for audit trail

### Monitoring

1. Prometheus metrics exporters
2. Real-time dashboards (Grafana)
3. Alerting on unhealthy backends
4. Log aggregation for troubleshooting

## Kubernetes Ingress Best Practices (2025-2026)

### High Availability

- Deploy multiple Ingress controller replicas
- Spread across availability zones
- Configure pod disruption budgets
- Use anti-affinity rules

### Traffic Separation

- Separate internal/external Ingress controllers
- Different controllers per team/department
- Public vs private ingress classes

### Resource Optimization

- Set CPU/memory requests and limits
- Ingress controllers are CPU-intensive (TLS, regex)
- Monitor and tune based on traffic patterns

### Modern Alternatives

- **Gateway API** - Successor to Ingress API
- **Traefik** - Dynamic routing, auto TLS
- **Envoy** - Retries, circuit breaking, HTTP/2

## Folder Contents

| File | Description |
|------|-------------|
| README.md | This overview document |
| checklist.md | Pre-flight and production checklists |
| examples.md | Complete configuration examples |
| templates.md | Copy-paste production templates |
| llm-prompts.md | AI prompts for LB tasks |

## Related Methodologies

- [load-balancing-concepts](../load-balancing-concepts.md) - Theory and algorithms
- [nginx-configuration](../nginx-configuration.md) - Nginx basics
- [ssl-tls-setup](../ssl-tls-setup.md) - SSL/TLS configuration

## Sources

- [HAProxy Documentation](https://www.haproxy.com/documentation/)
- [Nginx Performance Tuning](https://www.nginx.com/blog/tuning-nginx/)
- [HAProxy Kubernetes Ingress](https://www.haproxy.com/documentation/kubernetes-ingress/overview/)
- [Kubernetes Ingress Best Practices](https://www.devopstraininginstitute.com/blog/10-kubernetes-ingress-best-practices)
- [HAProxy vs NGINX Performance](https://last9.io/blog/haproxy-vs-nginx-performance/)
- [Top Load Balancers 2026](https://www.xurrent.com/blog/top-load-balancers)

---

*Load Balancing Implementation | faion-cicd-engineer*
