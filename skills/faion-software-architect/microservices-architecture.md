# Microservices Architecture

Decomposing applications into independently deployable services.

## What are Microservices?

Collection of small, autonomous services that:
- Own their data
- Communicate via APIs
- Deploy independently
- Organized around business capabilities

```
┌──────┐  ┌──────┐  ┌──────┐
│User  │  │Order │  │Payment│
│Svc   │  │Svc   │  │Svc    │
└──┬───┘  └──┬───┘  └──┬────┘
   │         │         │
   DB        DB        DB
```

## When to Choose Microservices

| Scenario | Microservices is good |
|----------|----------------------|
| Large team | 30+ developers |
| Complex domain | Clear bounded contexts |
| Different scaling needs | Some features hot |
| Polyglot requirements | Different tech per service |
| Independent deployment | Fast release cycles |

## Prerequisites

Before microservices, you need:
- ✅ Strong DevOps culture
- ✅ CI/CD pipelines
- ✅ Container orchestration (K8s)
- ✅ Monitoring & observability
- ✅ Clear domain boundaries
- ✅ Team autonomy

## Service Decomposition

### By Business Capability
```
E-commerce:
├── Catalog Service (products)
├── Inventory Service (stock)
├── Order Service (purchases)
├── Payment Service (transactions)
├── Shipping Service (delivery)
└── User Service (accounts)
```

### By Subdomain (DDD)
```
Core Domain    → Build in-house, competitive advantage
Supporting     → Build or buy, necessary but not differentiating
Generic        → Buy/use existing, commodity
```

## Communication Patterns

### Synchronous (REST/gRPC)
```
Service A ──HTTP──▶ Service B
          ◀─────────
```
- Simple, immediate response
- Creates coupling
- Use for: Queries, real-time needs

### Asynchronous (Events)
```
Service A ──Event──▶ Message Queue ──Event──▶ Service B
```
- Decoupled, resilient
- Eventually consistent
- Use for: Commands, notifications

## Data Management

### Database per Service
Each service owns its data. No shared databases.

```
❌ WRONG: Shared database
┌──────┐  ┌──────┐
│Svc A │  │Svc B │
└──┬───┘  └──┬───┘
   │         │
   └────┬────┘
        │
    ┌───┴───┐
    │  DB   │
    └───────┘

✅ RIGHT: Database per service
┌──────┐  ┌──────┐
│Svc A │  │Svc B │
└──┬───┘  └──┬───┘
   │         │
┌──┴──┐   ┌──┴──┐
│ DB  │   │ DB  │
└─────┘   └─────┘
```

### Data Consistency

**Saga Pattern** for distributed transactions:
```
Order Created → Payment Charged → Inventory Reserved → Order Confirmed
                    │
                    └─▶ If fails: Compensating transactions
```

## Resilience Patterns

### Circuit Breaker
```
Closed ──failures──▶ Open ──timeout──▶ Half-Open
   ▲                                      │
   └────────────success───────────────────┘
```

### Retry with Backoff
```
Attempt 1 → fail → wait 1s
Attempt 2 → fail → wait 2s
Attempt 3 → fail → wait 4s
...
```

### Bulkhead
Isolate failures to prevent cascade.

## API Gateway

```
        ┌──────────────────┐
Client ─│   API Gateway    │
        │ - Auth           │
        │ - Rate limiting  │
        │ - Routing        │
        └────────┬─────────┘
        ┌────────┼────────┐
        ▼        ▼        ▼
    Service A  Service B  Service C
```

## Observability

**Three Pillars:**
1. **Logs** - What happened
2. **Metrics** - How much/often
3. **Traces** - Request flow across services

**Essential:**
- Distributed tracing (Jaeger, Zipkin)
- Centralized logging (ELK)
- Metrics (Prometheus + Grafana)

## Service Template

Each service should have:
```
service-name/
├── src/
├── tests/
├── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── openapi.yaml
└── README.md
```

## Anti-patterns

| Anti-pattern | Problem |
|--------------|---------|
| Distributed monolith | Microservices that must deploy together |
| Shared database | Coupling through data |
| Too small services | Overhead exceeds benefits |
| Sync everywhere | Tight coupling, cascading failures |

## Related

- [monolith-architecture.md](monolith-architecture.md) - Simpler alternative
- [modular-monolith.md](modular-monolith.md) - Middle ground
- [event-driven-architecture.md](event-driven-architecture.md) - Communication
- [distributed-patterns.md](distributed-patterns.md) - Resilience
