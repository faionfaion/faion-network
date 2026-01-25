# API Gateway Design

Patterns for API gateway architecture.

## What is an API Gateway?

Single entry point for all API requests.

```
        ┌──────────────────┐
Clients │   API Gateway    │
   ────▶│ - Authentication │
        │ - Rate limiting  │
        │ - Routing        │
        │ - Transformation │
        └────────┬─────────┘
        ┌────────┼────────┐
        ▼        ▼        ▼
    Service A  Service B  Service C
```

## Core Functions

| Function | Description |
|----------|-------------|
| Routing | Direct requests to appropriate service |
| Authentication | Validate tokens, API keys |
| Rate Limiting | Prevent abuse |
| Load Balancing | Distribute traffic |
| Caching | Cache responses |
| Request/Response Transformation | Modify payloads |
| Monitoring | Metrics, logging |
| Circuit Breaker | Handle failures |

## Gateway Patterns

### Simple Routing

```
/users/*    → User Service
/orders/*   → Order Service
/products/* → Product Service
```

### Backend for Frontend (BFF)

```
Mobile App ───▶ Mobile BFF ───┬───▶ Services
                              │
Web App ──────▶ Web BFF ──────┤
                              │
Admin ────────▶ Admin BFF ────┘
```

**Each BFF optimized for its client's needs.**

### Aggregation

```
Client Request: GET /dashboard
                     │
              ┌──────┼──────┐
              ▼      ▼      ▼
           Users  Orders  Stats
              │      │      │
              └──────┼──────┘
                     ▼
              Aggregated Response
```

## Authentication Patterns

### Token Validation

```
Client ──Token──▶ Gateway ──Validate──▶ Auth Service
                     │
                     ▼ (if valid)
                  Backend
```

### JWT Pass-through

```yaml
# Gateway validates JWT signature
# Passes claims to backend in headers
x-user-id: "123"
x-user-role: "admin"
```

### API Keys

```
Client ──API-Key──▶ Gateway
                      │
              Look up in store
                      │
                ┌─────┴─────┐
                ▼           ▼
             Valid       Invalid
               │           │
            Forward     401 Error
```

## Rate Limiting

### Strategies

| Strategy | Description |
|----------|-------------|
| Fixed Window | X requests per time window |
| Sliding Window | Rolling window average |
| Token Bucket | Tokens replenish over time |
| Leaky Bucket | Fixed rate outflow |

### Implementation

```yaml
# Rate limit configuration
rate_limit:
  - path: /api/*
    limit: 100
    window: 60s
    key: client_ip

  - path: /api/heavy
    limit: 10
    window: 60s
    key: api_key
```

### Response Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1609459200
```

## Gateway Solutions

| Solution | Type | Best For |
|----------|------|----------|
| Kong | Open source | Kubernetes, plugins |
| AWS API Gateway | Managed | AWS ecosystem |
| Apigee | Enterprise | Large organizations |
| nginx | Open source | Simple routing |
| Traefik | Open source | Kubernetes native |
| Envoy | Open source | Service mesh |

## Kong Example

```yaml
# Service
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: rate-limit
config:
  minute: 100
  policy: local

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    konghq.com/plugins: rate-limit
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        backend:
          service:
            name: my-service
            port:
              number: 80
```

## Security Considerations

1. **TLS termination** - HTTPS at gateway
2. **Input validation** - Reject malformed requests
3. **CORS** - Configure allowed origins
4. **IP whitelisting** - For internal services
5. **Request size limits** - Prevent DoS
6. **Header sanitization** - Remove sensitive headers

## Monitoring

**Key Metrics:**
- Request rate (RPS)
- Latency (p50, p95, p99)
- Error rate (4xx, 5xx)
- Rate limit hits
- Authentication failures

```prometheus
# Example Prometheus metrics
http_requests_total{service="users", status="200"}
http_request_duration_seconds{service="orders", quantile="0.95"}
rate_limit_exceeded_total{service="api"}
```

## Anti-patterns

| Anti-pattern | Problem |
|--------------|---------|
| Business logic in gateway | Should be in services |
| Gateway as orchestrator | Creates coupling |
| No rate limiting | DoS vulnerability |
| No caching strategy | Unnecessary backend load |
| Single gateway for everything | Single point of failure |

## Related

- [microservices-architecture.md](microservices-architecture.md) - Service design
- [security-architecture.md](security-architecture.md) - Security patterns
