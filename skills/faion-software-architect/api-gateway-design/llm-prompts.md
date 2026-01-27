# LLM Prompts for API Gateway Design

Effective prompts for AI-assisted API gateway design, configuration, and troubleshooting.

## Gateway Architecture Prompts

### Initial Architecture Design

```
I need to design an API gateway architecture for the following system:

**Context:**
- System type: [e-commerce / SaaS / B2B API / internal microservices]
- Expected traffic: [X RPS peak, Y average]
- Client types: [web, mobile, IoT, partner APIs]
- Backend services: [list services with protocols]
- Current infrastructure: [Kubernetes / AWS / GCP / on-premise]

**Requirements:**
- Availability target: [99.9% / 99.99%]
- Latency SLA: p95 < [X]ms
- Security: [public API / internal only / mixed]
- Compliance: [GDPR / HIPAA / PCI-DSS / none]

**Please provide:**
1. Recommended gateway pattern (simple routing / BFF / aggregation)
2. Technology recommendation with reasoning
3. High-level architecture diagram (text-based)
4. Key configuration considerations
5. Potential risks and mitigations
```

### Gateway Selection

```
Help me choose between API gateway solutions for my use case:

**Requirements:**
- Deployment: [Kubernetes / AWS / GCP / Docker]
- Scale: [X RPS, Y services]
- Features needed: [list required features]
- Team expertise: [languages/tools familiar with]
- Budget: [open source only / enterprise budget / managed OK]

**Compare:**
- Kong
- AWS API Gateway
- Traefik
- Envoy
- APISIX
- [other if relevant]

Provide a comparison matrix and final recommendation with reasoning.
```

### Migration Planning

```
I need to migrate from [current gateway] to [target gateway].

**Current State:**
- Gateway: [current solution]
- Routes: [X routes]
- Plugins/features in use: [list]
- Traffic: [X RPS]
- Pain points: [why migrating]

**Target State:**
- Gateway: [target solution]
- Additional requirements: [new features needed]

**Please provide:**
1. Migration strategy (big bang vs incremental)
2. Feature mapping from old to new
3. Risk assessment
4. Rollback plan
5. Estimated complexity (high/medium/low)
```

---

## Configuration Generation Prompts

### Route Configuration

```
Generate API gateway route configuration for the following services:

**Gateway:** [Kong / Traefik / Envoy / AWS API Gateway]
**Format:** [YAML / JSON / HCL]

**Services:**
| Service | Internal URL | Public Path | Methods |
|---------|--------------|-------------|---------|
| users   | http://users:8080 | /api/v1/users | GET, POST, PUT, DELETE |
| orders  | http://orders:8080 | /api/v1/orders | GET, POST |
| products| http://products:8080 | /api/v1/products | GET |

**Requirements:**
- Strip prefix: [yes/no]
- Host-based routing: [yes/no, if yes specify hosts]
- Path rewriting: [describe if needed]
- Load balancing: [round-robin / least-connections / weighted]

Generate the complete, production-ready configuration.
```

### Rate Limiting Configuration

```
Generate rate limiting configuration for [Gateway name].

**Requirements:**
| Tier | Requests/min | Burst | Quota/day |
|------|-------------|-------|-----------|
| Free | 60 | 10 | 1,000 |
| Pro | 600 | 100 | 100,000 |
| Enterprise | 6,000 | 1,000 | Unlimited |

**Additional requirements:**
- Rate limit by: [IP / API key / user ID / custom header]
- Storage backend: [local / Redis / distributed]
- Response headers: [include X-RateLimit-* headers]
- Exceeded response: [429 with custom body]

Provide complete configuration with:
1. Rate limit plugin/middleware config
2. Consumer/tier definitions
3. Response customization
4. Redis configuration (if applicable)
```

### Authentication Configuration

```
Generate authentication configuration for [Gateway name].

**Authentication type:** [JWT / API Key / OAuth 2.0 / mTLS / combination]

**For JWT:**
- Issuer: [URL]
- JWKS URL: [URL]
- Audience: [values]
- Header: Authorization Bearer
- Claims to forward: [user_id, email, roles]

**For API Key:**
- Header name: [X-API-Key]
- Key storage: [database / Redis / static]

**Routes:**
- /api/v1/* - requires authentication
- /health - no authentication
- /public/* - no authentication

Generate complete configuration with error responses.
```

### Security Headers Configuration

```
Generate security header configuration for [Gateway name].

**Requirements:**
- HSTS: max-age=31536000, includeSubDomains, preload
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Content-Security-Policy: [specify or default]
- Remove headers: Server, X-Powered-By

**CORS:**
- Allowed origins: [list]
- Allowed methods: [list]
- Allowed headers: [list]
- Credentials: [true/false]
- Max age: [seconds]

Generate complete middleware/plugin configuration.
```

---

## Resilience Pattern Prompts

### Circuit Breaker Configuration

```
Generate circuit breaker configuration for [Gateway name].

**Backend services:**
| Service | Failure threshold | Timeout | Recovery |
|---------|------------------|---------|----------|
| users | 5 errors in 30s | 60s | 3 successes |
| orders | 3 errors in 10s | 30s | 2 successes |
| payments | 2 errors in 10s | 120s | 5 successes |

**Behavior when open:**
- Return: [503 / cached response / fallback response]
- Fallback endpoint: [URL if applicable]

**Monitoring:**
- Expose circuit state as metric
- Alert on state change

Generate complete configuration.
```

### Retry and Timeout Configuration

```
Generate retry and timeout configuration for [Gateway name].

**Global defaults:**
- Connection timeout: 5s
- Read timeout: 30s
- Retries: 3
- Retry on: 5xx, connection errors

**Per-service overrides:**
| Service | Read timeout | Retries | Idempotent |
|---------|-------------|---------|------------|
| users | 10s | 3 | GET only |
| orders | 60s | 2 | GET only |
| payments | 120s | 0 | None |
| reports | 300s | 1 | All |

**Retry strategy:**
- Exponential backoff: yes
- Initial interval: 100ms
- Max interval: 2s
- Jitter: 20%

Generate complete configuration with comments.
```

### Health Check Configuration

```
Generate health check configuration for [Gateway name].

**Upstream services:**
| Service | Health endpoint | Interval | Thresholds |
|---------|----------------|----------|------------|
| users | /health | 5s | 2 healthy, 3 unhealthy |
| orders | /healthz | 10s | 2 healthy, 5 unhealthy |
| products | /ready | 5s | 3 healthy, 3 unhealthy |

**Health check type:** [HTTP / TCP / gRPC]
**Expected response:** 200 OK
**Timeout per check:** 3s

Generate active and passive health check configuration.
```

---

## Observability Prompts

### Metrics Configuration

```
Generate metrics configuration for [Gateway name] with Prometheus.

**Required metrics:**
- Request rate (by route, method, status)
- Latency histogram (p50, p95, p99)
- Error rate
- Active connections
- Rate limit exceeded count
- Circuit breaker state
- Upstream health

**Labels:**
- service
- route
- method
- status_code
- consumer (optional)

**Export endpoint:** /metrics on port 9090

Generate complete configuration with Prometheus scrape config.
```

### Distributed Tracing

```
Generate distributed tracing configuration for [Gateway name].

**Backend:** [Jaeger / Zipkin / Tempo / OTLP]
**Protocol:** [HTTP / gRPC]
**Collector endpoint:** [URL]

**Requirements:**
- Propagate trace context (W3C / B3 / Jaeger)
- Sample rate: [100% / 10% / adaptive]
- Add custom spans for: [authentication, rate limiting]
- Forward trace ID header to backends

Generate OpenTelemetry configuration.
```

### Logging Configuration

```
Generate structured logging configuration for [Gateway name].

**Log format:** JSON
**Output:** [stdout / file / remote]

**Fields to include:**
- timestamp (ISO8601)
- level
- request_id / correlation_id
- method
- path
- status
- latency_ms
- client_ip
- user_agent
- user_id (from JWT claim)
- upstream_latency_ms
- response_size

**Log levels by route:**
- /health - disabled
- /api/* - info
- errors - error with stack trace

Generate complete logging configuration.
```

---

## Troubleshooting Prompts

### Performance Analysis

```
I'm experiencing performance issues with my API gateway.

**Symptoms:**
- [describe symptoms: high latency, timeouts, errors]
- When it started: [date/time, after deployment, gradually]
- Affected routes: [all / specific routes]

**Current metrics:**
- Request rate: [X RPS]
- p95 latency: [X ms, compared to baseline]
- Error rate: [X%]
- CPU/Memory usage: [values]

**Configuration:**
[paste relevant config]

**Please help:**
1. Identify potential causes
2. Suggest diagnostic steps
3. Recommend configuration changes
4. Provide monitoring queries to identify root cause
```

### Error Debugging

```
I'm getting [error type] errors from my API gateway.

**Error details:**
- HTTP status: [code]
- Error message: [message]
- Frequency: [X per minute / sporadic]
- Affected endpoints: [list]

**Gateway:** [name and version]
**Configuration:** [paste relevant config]

**Logs:**
[paste relevant error logs]

**Please help:**
1. Explain what this error means
2. Identify likely causes
3. Provide debugging steps
4. Suggest fixes
```

### Capacity Planning

```
Help me plan API gateway capacity for expected growth.

**Current state:**
- Traffic: [X RPS average, Y peak]
- Gateway instances: [count, size]
- Current resource usage: [CPU %, Memory %]
- Current latency: [p50, p95, p99]

**Projected growth:**
- [X]x traffic increase in [timeframe]
- New services: [count]
- New regions: [list if applicable]

**Constraints:**
- Budget: [amount or relative]
- Latency SLA: [must maintain]
- Availability: [target]

**Please provide:**
1. Recommended scaling strategy
2. Resource estimates
3. Architecture changes if needed
4. Cost optimization suggestions
```

---

## GraphQL Gateway Prompts

### Federation Schema Design

```
Help me design a federated GraphQL schema.

**Domains:**
| Domain | Entities | Team |
|--------|----------|------|
| Users | User, Profile | Team A |
| Products | Product, Category | Team B |
| Orders | Order, OrderItem | Team C |
| Reviews | Review, Rating | Team D |

**Relationships:**
- User has many Orders
- Order has many Products (through OrderItems)
- Product has many Reviews
- Review belongs to User and Product

**Please provide:**
1. Entity definitions with @key directives
2. Type extensions for cross-domain relationships
3. Sample queries showing data requirements
4. Federation router configuration
```

### GraphQL Security

```
Generate security configuration for Apollo Router / GraphQL gateway.

**Requirements:**
- Query depth limit: 15
- Query complexity limit: 1000
- Disable introspection in production
- Rate limit by query complexity
- Persisted queries only (optional)

**Authentication:**
- JWT validation
- Forward user context to subgraphs

**Query restrictions:**
- Block mutations for anonymous users
- Limit list queries to 100 items

Generate complete configuration.
```

---

## API Versioning Prompts

### Version Strategy Design

```
Help me design API versioning strategy at the gateway level.

**Current state:**
- API version: v1
- Routes: [count]
- Active consumers: [count]
- Breaking changes planned: [yes/no, describe]

**Requirements:**
- Versioning method: [URI / header / query param]
- Simultaneous versions: [2 / 3 / more]
- Deprecation period: [X months]
- Version sunset process: [describe]

**Please provide:**
1. Routing configuration for multiple versions
2. Version detection logic
3. Deprecation header configuration
4. Migration communication strategy
5. Monitoring for version adoption
```

### Version Migration

```
Generate gateway configuration for API version migration.

**Migration:**
- From: v1
- To: v2
- Strategy: [parallel / gradual / canary]

**Changes in v2:**
- [list breaking changes]
- [list new endpoints]
- [list deprecated endpoints]

**Requirements:**
- Default version: v1 (during migration)
- Traffic split: [percentage to v2]
- Rollback capability: yes

Generate configuration for:
1. Routing rules
2. Traffic splitting
3. Version-specific middleware
4. Metrics to track migration
```

---

## Best Practices for LLM Prompts

### Do's

1. **Provide context** - Include system type, scale, constraints
2. **Specify output format** - Request YAML, JSON, specific gateway syntax
3. **Include examples** - Show current config, expected behavior
4. **Set constraints** - Budget, performance requirements, compliance
5. **Ask for alternatives** - Request multiple approaches with trade-offs

### Don'ts

1. **Don't be vague** - "Make my API faster" vs "Reduce p95 latency from 500ms to 200ms"
2. **Don't omit scale** - Traffic patterns matter for configuration
3. **Don't forget security** - Always specify authentication requirements
4. **Don't ignore existing infra** - Mention Kubernetes, cloud provider, etc.

### Iterative Refinement

Start broad, then refine:

```
1. "Design API gateway architecture for e-commerce platform"
   -> Get high-level design

2. "Now generate Kong configuration for the routing layer"
   -> Get specific config

3. "Add rate limiting for free/pro/enterprise tiers"
   -> Refine configuration

4. "What metrics should I monitor? Generate Prometheus alerts"
   -> Add observability

5. "Review this configuration for security issues"
   -> Security audit
```

---

## Prompt Templates for Common Tasks

### Quick Configuration Generation

```
Generate [Gateway] [feature] configuration:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Output format: [YAML/JSON]
Include comments explaining each section.
```

### Configuration Review

```
Review this [Gateway] configuration for:
1. Security vulnerabilities
2. Performance issues
3. Best practice violations
4. Missing recommended settings

Configuration:
```yaml
[paste config]
```

Provide specific recommendations with corrected configuration.
```

### Comparison Request

```
Compare these two [Gateway] configurations:

Config A:
```yaml
[paste config A]
```

Config B:
```yaml
[paste config B]
```

Analyze:
1. Functional differences
2. Performance implications
3. Security differences
4. Which is better for [use case]
```
