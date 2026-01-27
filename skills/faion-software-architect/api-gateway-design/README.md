# API Gateway Design

Comprehensive methodology for designing, implementing, and operating API gateways in modern distributed systems.

## What is an API Gateway?

An API Gateway is a single entry point for all client requests to backend services. It acts as a reverse proxy that handles cross-cutting concerns like authentication, rate limiting, routing, and observability.

**Core Value Proposition:**
- Decouples clients from backend service topology
- Centralizes cross-cutting concerns
- Enables independent service evolution
- Simplifies client development

## Gateway Functions

| Function | Description | Priority |
|----------|-------------|----------|
| **Routing** | Direct requests to appropriate backend services | Critical |
| **Authentication** | Validate tokens, API keys, mTLS | Critical |
| **Authorization** | Enforce access policies | Critical |
| **Rate Limiting** | Prevent abuse, protect backends | High |
| **Load Balancing** | Distribute traffic across instances | High |
| **Circuit Breaking** | Handle backend failures gracefully | High |
| **Request Transformation** | Modify headers, body, path | Medium |
| **Response Aggregation** | Combine multiple backend responses | Medium |
| **Caching** | Cache responses to reduce backend load | Medium |
| **Observability** | Metrics, logging, distributed tracing | High |
| **API Versioning** | Route to different API versions | Medium |

## Gateway Patterns

### Pattern 1: Simple Routing Gateway

Routes requests to appropriate backend services based on path, host, or headers.

```
Client Request: GET /users/123
                    |
              API Gateway
                    |
                    v
            User Service (GET /123)

Client Request: GET /orders/456
                    |
              API Gateway
                    |
                    v
            Order Service (GET /456)
```

**Use When:**
- Simple microservices architecture
- Direct mapping between client requests and backend services
- Minimal transformation needed

### Pattern 2: Backend for Frontend (BFF)

Separate gateways optimized for each client type.

```
Mobile App --> Mobile BFF Gateway --> Backend Services
Web App   --> Web BFF Gateway    --> Backend Services
Admin     --> Admin BFF Gateway  --> Backend Services
Partner   --> Partner API Gateway --> Backend Services
```

**Use When:**
- Different clients have vastly different data needs
- Mobile needs optimized payloads
- Third-party integrations require different contracts
- Different security requirements per client type

### Pattern 3: Aggregation Gateway

Combines responses from multiple backend services into a single response.

```
Client Request: GET /dashboard
                    |
              API Gateway
        ____________|____________
       |            |            |
       v            v            v
   User Svc    Order Svc    Stats Svc
       |            |            |
       +------------+------------+
                    |
                    v
          Aggregated Response
```

**Use When:**
- Reducing client-side complexity
- Minimizing network round trips
- Creating composite API views

### Pattern 4: Edge Gateway with Service Mesh

Gateway handles north-south traffic; service mesh handles east-west.

```
External Traffic --> Edge Gateway (Kong/Envoy)
                           |
                    +------+------+
                    |      |      |
                    v      v      v
                 Service A  B  C (with Sidecar Proxies)
                    |______|______|
                    East-West via Service Mesh (Istio/Linkerd)
```

**Use When:**
- Complex microservices requiring mutual TLS
- Fine-grained traffic management between services
- Need zero-trust security model

## Gateway Solution Comparison (2025-2026)

| Solution | Type | Best For | Performance | Ecosystem |
|----------|------|----------|-------------|-----------|
| **Kong** | Open-source/Enterprise | Multi-cloud, plugin extensibility | ~50k TPS/node | 100+ plugins |
| **AWS API Gateway** | Managed | AWS-native, serverless | Auto-scaling | AWS integrations |
| **Traefik** | Open-source | Kubernetes-native, GitOps | ~30k QPS | Middleware plugins |
| **Envoy** | Open-source | Service mesh, high performance | ~35k QPS | WASM extensible |
| **APISIX** | Open-source | High performance, dashboard | ~50k+ QPS | 80+ plugins |
| **Apigee** | Enterprise | API management, monetization | Auto-scaling | Google Cloud |
| **Tyk** | Open-source/Enterprise | GraphQL support, analytics | High | OpenAPI native |

### Selection Decision Tree

```
Need managed service + AWS ecosystem?
    YES --> AWS API Gateway
    NO --> Continue

Need extensive plugin ecosystem + multi-cloud?
    YES --> Kong or APISIX
    NO --> Continue

Kubernetes-native with GitOps workflow?
    YES --> Traefik
    NO --> Continue

Building service mesh architecture?
    YES --> Envoy (with Istio/Solo)
    NO --> Continue

Need GraphQL federation?
    YES --> Apollo Router or Tyk
    NO --> Continue

Enterprise API management with monetization?
    YES --> Apigee or Kong Enterprise
```

## Rate Limiting Strategies

### Algorithm Comparison

| Algorithm | Description | Use Case |
|-----------|-------------|----------|
| **Fixed Window** | X requests per time window | Simple scenarios |
| **Sliding Window** | Rolling window average | Smoother traffic distribution |
| **Token Bucket** | Tokens replenish over time | Allows bursts |
| **Leaky Bucket** | Fixed rate outflow | Consistent rate |

### Multi-Level Rate Limiting

Apply rate limits at multiple levels for comprehensive protection:

| Level | Scope | Example |
|-------|-------|---------|
| Global | All traffic | 100,000 RPS |
| Per-API | Specific endpoint | 10,000 RPS for `/api/users` |
| Per-Consumer | API key/user | 1,000 RPM per API key |
| Per-Route | Specific route | 500 RPM for `/api/expensive` |

### Dynamic Rate Limiting

Modern gateways support adaptive rate limiting based on:
- Current error rates (lower limits when errors > 5%)
- Response latency (adjust when p95 > 500ms)
- Backend health (reduce when backends degraded)
- Time-based patterns (higher limits during off-peak)

## Circuit Breaker Patterns

### Three States

| State | Behavior | Transition |
|-------|----------|------------|
| **Closed** | Normal operation, requests pass through | Opens when failure threshold exceeded |
| **Open** | Requests immediately fail | Half-opens after timeout |
| **Half-Open** | Limited requests to test recovery | Closes on success, opens on failure |

### Configuration Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| Failure Threshold | Failures before opening | 5-10 failures |
| Success Threshold | Successes before closing | 3-5 successes |
| Timeout | Duration before half-open | 30-60 seconds |
| Failure Rate Window | Time window for failures | 10-30 seconds |

## API Versioning at Gateway

### Strategy Comparison

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| **URI Path** | `/v1/users`, `/v2/users` | Clear, cacheable | Pollutes URI |
| **Query Parameter** | `/users?version=1` | Easy to implement | Not RESTful |
| **Header** | `X-API-Version: 1` | Clean URIs | Harder to test |
| **Media Type** | `Accept: application/vnd.api.v1+json` | RESTful | Complex |

### Gateway Implementation

Path-based versioning is most common at gateway level:

```
/v1/* --> Service v1 instances
/v2/* --> Service v2 instances
```

Or using header-based routing:
```
Header: X-API-Version: 2 --> Service v2
Default --> Service v1 (backward compatible)
```

## GraphQL Gateway (Federation)

### Apollo Federation Architecture

```
Client --> Apollo Router (Gateway)
               |
    +----------+----------+
    |          |          |
    v          v          v
Users       Orders     Products
Subgraph    Subgraph   Subgraph
```

**Key Concepts:**
- **Router:** Single entry point, query planning, execution
- **Subgraph:** Independent GraphQL service for a domain
- **Supergraph:** Composed schema from all subgraphs
- **Entity Resolution:** Cross-subgraph data fetching

### Federation vs Stitching

| Aspect | Federation | Stitching |
|--------|------------|-----------|
| Ownership | Subgraphs own their types | Central gateway owns schema |
| Scaling | Each team deploys independently | Central gateway must coordinate |
| Complexity | Simpler subgraph development | Gateway becomes complex |
| Version | Apollo Federation v2 | Legacy approach |

## Observability

### Three Pillars

| Pillar | Purpose | Tools |
|--------|---------|-------|
| **Metrics** | Quantitative measurements | Prometheus, CloudWatch |
| **Logs** | Event records | Loki, Elasticsearch |
| **Traces** | Request flow across services | Jaeger, Zipkin, Tempo |

### Key Gateway Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Request Rate | Requests per second | Baseline + 50% |
| Latency p50 | Median response time | < 100ms |
| Latency p95 | 95th percentile latency | < 500ms |
| Latency p99 | 99th percentile latency | < 1s |
| Error Rate | 4xx/5xx responses | > 1% |
| Circuit Breaker Opens | Backend failures | Any |
| Rate Limit Hits | Throttled requests | > 5% |

### OpenTelemetry Integration

OpenTelemetry provides vendor-neutral observability:

```
Gateway --> OTEL Collector --> Backends
                |
        +-------+-------+
        |       |       |
        v       v       v
    Prometheus Loki   Jaeger
      (metrics) (logs) (traces)
```

## Security Best Practices

### Authentication Patterns

| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| API Keys | Service-to-service, simple auth | Header: `X-API-Key` |
| JWT | User authentication | Header: `Authorization: Bearer <token>` |
| OAuth 2.0 | Delegated authorization | Token validation at gateway |
| mTLS | Service mesh, high security | Client certificate validation |

### Security Checklist

- [ ] TLS termination at gateway (HTTPS only)
- [ ] Input validation and sanitization
- [ ] Rate limiting to prevent DoS
- [ ] Request size limits
- [ ] Header sanitization (remove internal headers)
- [ ] CORS configuration
- [ ] IP whitelisting for admin endpoints
- [ ] WAF integration for threat detection
- [ ] Audit logging for compliance

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Business logic in gateway | Gateway becomes monolith | Keep gateway thin, logic in services |
| Gateway as orchestrator | Tight coupling, bottleneck | Use choreography or dedicated orchestrator |
| No rate limiting | DoS vulnerability | Implement at multiple levels |
| No circuit breakers | Cascading failures | Add circuit breakers for all backends |
| Single gateway | Single point of failure | Regional gateways, high availability |
| No caching strategy | Unnecessary backend load | Cache static/semi-static responses |
| Sync transformations | Latency | Use streaming where possible |

## LLM-Assisted Gateway Design

### When to Use LLM

LLMs excel at:
- Generating initial gateway configurations
- Creating OpenAPI-compliant route definitions
- Writing rate limiting policies
- Drafting circuit breaker configurations
- Explaining complex gateway patterns

### Prompt Tips

1. **Provide context:** Specify traffic patterns, security requirements, backend services
2. **Request specific formats:** Ask for Kong YAML, Envoy xDS, AWS CloudFormation
3. **Include constraints:** Rate limits, latency requirements, compliance needs
4. **Ask for alternatives:** Request multiple approaches with trade-offs

See [llm-prompts.md](llm-prompts.md) for detailed prompts.

## External Resources

### Official Documentation

- [Kong Gateway Documentation](https://docs.konghq.com/)
- [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Envoy Proxy Documentation](https://www.envoyproxy.io/docs/envoy/latest/)
- [Apollo Federation Documentation](https://www.apollographql.com/docs/federation/)
- [APISIX Documentation](https://apisix.apache.org/docs/)

### Patterns and Best Practices

- [Microservices.io API Gateway Pattern](https://microservices.io/patterns/apigateway.html)
- [Microsoft API Gateway Documentation](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/gateway)
- [AWS API Gateway Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-integrating-microservices/api-gateway-pattern.html)
- [Kong API Versioning Guidelines](https://konghq.com/blog/engineering/service-design-guidelines-api-versioning)

### Benchmarks and Comparisons

- [Gateway API Benchmarks](https://github.com/howardjohn/gateway-api-bench)
- [Grafbase Federation Gateway Benchmarks](https://grafbase.com/blog/benchmarking-graphql-federation-gateways)
- [API Gateway Comparison 2025](https://blog.serverlessapigateway.com/api-gateway-software-comparison-2025-serverless-api-gateway-vs-aws-kong-apigee-nginx/)

### OpenTelemetry

- [OpenTelemetry Gateway Deployment](https://opentelemetry.io/docs/collector/deployment/gateway/)
- [OpenTelemetry for API Observability](https://github.com/TykTechnologies/demo-api-observability-opentelemetry)

## Related Methodologies

| Methodology | Relationship |
|-------------|--------------|
| [microservices-architecture/](../microservices-architecture/) | Gateway is entry point for microservices |
| [security-architecture/](../security-architecture/) | Authentication and security patterns |
| [observability-architecture/](../observability-architecture/) | Metrics, logging, tracing setup |
| [caching-architecture/](../caching-architecture/) | Gateway caching strategies |
| [event-driven-architecture/](../event-driven-architecture/) | Async patterns complement gateway |

## Files in This Methodology

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview document |
| [checklist.md](checklist.md) | Step-by-step gateway design checklist |
| [examples.md](examples.md) | Real-world gateway configurations |
| [templates.md](templates.md) | Copy-paste gateway templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted design |
