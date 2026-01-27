# Microservices Architecture

A methodology for decomposing applications into independently deployable services organized around business capabilities.

## When to Use Microservices

### Microservices Fit

| Scenario | Why Microservices |
|----------|-------------------|
| Large team (30+ developers) | Team autonomy, parallel development |
| Complex domain with clear bounded contexts | Natural service boundaries |
| Different scaling needs per feature | Independent scaling |
| Polyglot requirements | Different tech per service |
| Independent deployment cycles | Fast release cadence |
| High availability requirements | Fault isolation |

### Microservices Do NOT Fit

| Scenario | Better Alternative |
|----------|-------------------|
| Small team (< 10 developers) | Monolith or Modular Monolith |
| MVP / early-stage product | Monolith (extract later) |
| Unclear domain boundaries | Modular Monolith |
| Limited DevOps maturity | Monolith |
| Simple CRUD application | Monolith |
| Tight budget constraints | Monolith |

### Decision Framework

```
Is your domain well understood?
├── NO → Modular Monolith (discover boundaries first)
└── YES → Do you have 30+ developers?
          ├── NO → Modular Monolith
          └── YES → Do you have mature DevOps?
                    ├── NO → Build DevOps first, then Microservices
                    └── YES → Microservices
```

## Prerequisites

Before adopting microservices, ensure you have:

| Prerequisite | Why Required |
|--------------|--------------|
| Strong DevOps culture | Automation is essential |
| CI/CD pipelines | Each service needs its own pipeline |
| Container orchestration (K8s) | Deployment complexity |
| Monitoring & observability | Distributed tracing is mandatory |
| Clear domain boundaries | DDD or business capability mapping |
| Team autonomy | Conway's Law alignment |

## Service Decomposition Strategies

### 1. By Business Capability

Align services with what the business does:

```
E-commerce Platform:
├── Catalog Service      # Product information
├── Inventory Service    # Stock management
├── Order Service        # Purchase processing
├── Payment Service      # Transaction handling
├── Shipping Service     # Delivery coordination
├── User Service         # Account management
└── Notification Service # Email, SMS, push
```

### 2. By Subdomain (DDD)

Apply Domain-Driven Design to identify boundaries:

| Subdomain Type | Strategy | Example |
|----------------|----------|---------|
| **Core** | Build in-house, competitive advantage | Recommendation engine |
| **Supporting** | Build or buy, necessary but not differentiating | User authentication |
| **Generic** | Buy/use existing, commodity | Payment processing (Stripe) |

### 3. By Volatility

Separate stable domains from frequently changing ones:

```
Stable (change rarely):
├── Authentication
└── User Profile

Volatile (change often):
├── Pricing Engine
├── Promotions
└── Search Ranking
```

### 4. Strangler Fig Pattern

Incrementally extract from monolith:

```
Phase 1: Monolith handles all traffic
Phase 2: New service handles subset, monolith handles rest
Phase 3: Gradually shift traffic to new services
Phase 4: Retire monolith components
```

## Communication Patterns

### Synchronous Communication

**REST (HTTP/JSON)**
- Use for: External APIs, simple CRUD
- Pros: Universal, easy to debug
- Cons: Tight coupling, cascading failures

**gRPC (HTTP/2 + Protobuf)**
- Use for: Internal service-to-service, high throughput
- Pros: Fast, type-safe, streaming
- Cons: More complex, debugging harder

**GraphQL**
- Use for: BFF (Backend for Frontend), aggregation
- Pros: Flexible queries, reduces over-fetching
- Cons: Complexity, caching challenges

### Asynchronous Communication

**Message Queues (RabbitMQ, SQS)**
- Use for: Task distribution, work queues
- Pros: Decoupled, reliable delivery
- Cons: Message ordering not guaranteed

**Event Streaming (Kafka, Kinesis)**
- Use for: Event sourcing, audit logs, analytics
- Pros: Replay, high throughput, ordering
- Cons: Operational complexity

**Pub/Sub (SNS, Google Pub/Sub)**
- Use for: Notifications, fan-out
- Pros: Simple, scalable
- Cons: No replay, at-most-once delivery

### Communication Decision Tree

```
Need immediate response?
├── YES → Synchronous
│         ├── Internal high-throughput → gRPC
│         ├── External API → REST
│         └── Mobile/Web aggregation → GraphQL
└── NO → Asynchronous
         ├── Need ordering → Kafka
         ├── Need replay → Kafka
         └── Simple task queue → RabbitMQ/SQS
```

## Data Management

### Database per Service

Each service owns its data exclusively:

```
Service A          Service B
    │                  │
    ↓                  ↓
┌───────┐          ┌───────┐
│ DB A  │          │ DB B  │
└───────┘          └───────┘
```

**Why?**
- Loose coupling
- Independent schema evolution
- Technology freedom
- Independent scaling

### Data Consistency Patterns

**Saga Pattern (Choreography)**

```
Order Service → OrderCreated event
     ↓
Payment Service → PaymentCharged event
     ↓
Inventory Service → InventoryReserved event
     ↓
Order Service → OrderConfirmed

If Payment fails:
     ↓
Compensating: CancelOrder event
```

**Saga Pattern (Orchestration)**

```
Saga Orchestrator
     │
     ├── 1. Create Order (Order Service)
     ├── 2. Charge Payment (Payment Service)
     ├── 3. Reserve Inventory (Inventory Service)
     └── 4. Confirm Order (Order Service)

     If step fails → Execute compensating transactions
```

**CQRS (Command Query Responsibility Segregation)**

Separate read and write models for high-scale scenarios.

## Service Mesh

### What is a Service Mesh?

Infrastructure layer handling service-to-service communication:

```
┌─────────────────────────────────────────────┐
│              Control Plane                   │
│    (Istiod / Linkerd Control Plane)         │
└────────────────────┬────────────────────────┘
                     │ Configuration
    ┌────────────────┼────────────────┐
    ↓                ↓                ↓
┌───────┐       ┌───────┐        ┌───────┐
│Service│       │Service│        │Service│
│   A   │       │   B   │        │   C   │
├───────┤       ├───────┤        ├───────┤
│ Proxy │←─────→│ Proxy │←──────→│ Proxy │
└───────┘       └───────┘        └───────┘
    Data Plane (Envoy / linkerd-proxy)
```

### Service Mesh Capabilities

| Feature | Description |
|---------|-------------|
| mTLS | Automatic encryption between services |
| Traffic management | Canary, blue-green, traffic splitting |
| Observability | Metrics, traces, access logs |
| Resilience | Retries, circuit breakers, timeouts |
| Access control | Service-to-service authorization |

### Choosing a Service Mesh

| Mesh | Best For | Resource Usage |
|------|----------|----------------|
| **Linkerd** | Simplicity, low latency | ~10 millicores, ~20MB |
| **Istio** | Advanced features, enterprise | ~100 millicores, ~128MB |
| **Consul Connect** | Hybrid cloud, existing Consul users | Medium |

**Decision:**
- Start with Linkerd for simplicity
- Move to Istio if you need advanced traffic control
- Use Consul for hybrid cloud environments

## Kubernetes Patterns

### Sidecar Pattern

Deploy helper containers alongside main application:

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp:latest
  - name: logging-sidecar
    image: fluentd:latest
```

**Use cases:** Logging, monitoring, proxy, security

### Ambassador Pattern

Proxy for external service communication:

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp:latest
  - name: ambassador
    image: envoy:latest
    # Routes external traffic through ambassador
```

**Use cases:** Legacy integration, circuit breaking, rate limiting

### Init Container Pattern

Setup before main container starts:

```yaml
apiVersion: v1
kind: Pod
spec:
  initContainers:
  - name: init-db
    image: postgres:alpine
    command: ['sh', '-c', 'until pg_isready; do sleep 2; done;']
  containers:
  - name: app
    image: myapp:latest
```

**Use cases:** Database migrations, config loading, dependency waiting

## Observability

### Three Pillars

| Pillar | Purpose | Tools |
|--------|---------|-------|
| **Logs** | What happened | ELK, Loki, CloudWatch |
| **Metrics** | How much/often | Prometheus + Grafana |
| **Traces** | Request flow | Jaeger, Zipkin, Tempo |

### Essential Observability

- Distributed tracing with correlation IDs
- Centralized logging with structured logs
- Service-level metrics (latency, throughput, errors)
- Health checks and readiness probes

## Resilience Patterns

### Circuit Breaker

Prevent cascading failures:

```
Closed → failures exceed threshold → Open
  ↑                                   │
  │                              timeout
  │                                   ↓
  └────── success ←───────── Half-Open
```

### Retry with Exponential Backoff

```
Attempt 1 → fail → wait 1s
Attempt 2 → fail → wait 2s
Attempt 3 → fail → wait 4s
Attempt 4 → fail → wait 8s (max)
```

### Bulkhead

Isolate failures to prevent resource exhaustion:

```
┌──────────────────────────────────────┐
│              Application              │
├──────────────┬───────────────────────┤
│ Pool A (10)  │     Pool B (20)       │
│ Service A    │     Service B         │
└──────────────┴───────────────────────┘
```

### Timeout

Always set timeouts for external calls:

```
Service A ──timeout: 3s──→ Service B
                ↓
         If no response in 3s → Fail fast
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Distributed monolith | Services must deploy together | True loose coupling |
| Shared database | Coupling through data | Database per service |
| Too small services | Overhead exceeds benefits | Right-size services |
| Sync everywhere | Cascading failures | Async where possible |
| No API versioning | Breaking changes break clients | Semantic versioning |
| Chatty communication | N+1 queries across network | Aggregation, BFF |

## LLM-Assisted Design

Modern tools can help with microservices design:

| Use Case | How LLMs Help |
|----------|---------------|
| Domain analysis | Identify bounded contexts from requirements |
| API design | Generate OpenAPI specs from descriptions |
| Service decomposition | Suggest service boundaries from codebase |
| Event modeling | Design event schemas and flows |
| Documentation | Generate architecture decision records |

See [llm-prompts.md](llm-prompts.md) for practical prompts.

## Key Resources

### Books

| Book | Author | Focus |
|------|--------|-------|
| Building Microservices | Sam Newman | Comprehensive guide |
| Microservices Patterns | Chris Richardson | Patterns catalog |
| Domain-Driven Design | Eric Evans | Strategic design |
| Implementing DDD | Vaughn Vernon | Tactical patterns |

### Websites

- [microservices.io](https://microservices.io/) - Chris Richardson's patterns catalog
- [martinfowler.com/microservices](https://martinfowler.com/microservices/) - Martin Fowler's articles
- [12factor.net](https://12factor.net/) - Cloud-native principles

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview |
| [checklist.md](checklist.md) | Step-by-step implementation checklist |
| [examples.md](examples.md) | Real-world architecture examples |
| [templates.md](templates.md) | Service templates, docker-compose |
| [llm-prompts.md](llm-prompts.md) | Prompts for AI-assisted design |

## Related Methodologies

- [monolith-architecture.md](../monolith-architecture.md) - Simpler alternative
- [modular-monolith.md](../modular-monolith.md) - Middle ground
- [event-driven-architecture.md](../event-driven-architecture.md) - Async communication
- [distributed-patterns.md](../distributed-patterns.md) - Resilience patterns
- [system-design-process/](../system-design-process/) - Design methodology
