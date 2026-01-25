---
name: faion-software-architect
<<<<<<< HEAD
description: "Software Architect role: system design, architecture decisions (ADRs), design patterns selection, C4 modeling, quality attributes (scalability, performance, security), technology choices, microservices vs monolith, data modeling. 28 methodologies."
=======
description: "Software Architect role: system design, architecture decisions (ADRs), design patterns selection, C4 modeling, quality attributes (scalability, performance, security), technology choices, microservices vs monolith, data modeling. 30 methodologies."
>>>>>>> claude
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task, TodoWrite
---

# Software Architect Skill

**Communication: User's language. Docs: English.**

## Purpose

<<<<<<< HEAD
Make informed architecture decisions that balance quality attributes (scalability, performance, security, maintainability) with business constraints (time, cost, team skills).

---

## When to Use This Skill

| Trigger | Example |
|---------|---------|
| System design needed | "Design the architecture for a real-time chat app" |
| Technology choice | "Should we use PostgreSQL or MongoDB?" |
| Scalability concerns | "How do we scale to 100k concurrent users?" |
| Pattern selection | "What pattern for handling payments?" |
| ADR creation | "Document why we chose microservices" |
| Design review | "Review this architecture diagram" |

---

## Agents

| Agent | Purpose |
|-------|---------|
| faion-architect-agent | Architecture design, ADRs, technology selection |
| faion-design-reviewer-agent | Architecture review, quality attribute analysis |

---

## Methodologies (28)

### Architecture Fundamentals

| Methodology | Description |
|-------------|-------------|
| system-design-process | End-to-end system design workflow |
| c4-model | Context, Container, Component, Code diagrams |
| architecture-decision-records | ADR creation and management |
| quality-attributes-analysis | Scalability, performance, security, etc. |
| trade-off-analysis | Evaluating architecture trade-offs |

### Architecture Styles

| Methodology | Description |
|-------------|-------------|
| monolith-architecture | When and how to build monoliths |
| microservices-architecture | Service decomposition, boundaries |
| modular-monolith | Modular monolith patterns |
| serverless-architecture | FaaS, event-driven serverless |
| event-driven-architecture | Event sourcing, CQRS, pub/sub |

### Design Patterns

| Methodology | Description |
|-------------|-------------|
| creational-patterns | Factory, Builder, Singleton, Prototype |
| structural-patterns | Adapter, Bridge, Composite, Decorator, Facade |
| behavioral-patterns | Strategy, Observer, Command, State, Chain |
| architectural-patterns | MVC, MVVM, Clean Architecture, Hexagonal |
| distributed-patterns | Saga, Circuit Breaker, Retry, Bulkhead |

### Data Architecture

| Methodology | Description |
|-------------|-------------|
| data-modeling | Entity relationships, normalization |
| database-selection | SQL vs NoSQL decision framework |
| caching-architecture | Cache strategies, invalidation |
| data-pipeline-design | ETL, streaming, batch processing |

### Infrastructure

| Methodology | Description |
|-------------|-------------|
| cloud-architecture | AWS, GCP, Azure best practices |
| container-orchestration | Kubernetes architecture patterns |
| api-gateway-design | Gateway patterns, rate limiting |
| service-mesh | Istio, Linkerd patterns |

### Quality & Security

| Methodology | Description |
|-------------|-------------|
| security-architecture | OWASP, threat modeling, zero trust |
| performance-architecture | Latency optimization, throughput |
| reliability-architecture | Fault tolerance, disaster recovery |
| observability-architecture | Logging, metrics, tracing strategy |

---

## Decision Trees

### Architecture Style Selection

```
Q1: Team size and experience?
    │
    ├─ Small team (<5), limited microservices exp ─────────────────────────────┐
    │   Recommendation: Monolith or Modular Monolith                           │
    │   Reason: Simpler deployment, debugging, team coordination               │
    │
    └─ Large team (5+), experienced ───────────────────────────────────────────┐
        Q2: Independent deployment needed?                                      │
            ├─ YES → Q3: Bounded contexts clear?                               │
            │             ├─ YES → Microservices                               │
            │             └─ NO → Modular Monolith (extract later)             │
            └─ NO → Monolith with clear module boundaries                      │
```

### Database Selection

```
Q1: Data structure?
    │
    ├─ Highly relational (many joins) ─────────────────────────────────────────┐
    │   → PostgreSQL / MySQL                                                   │
    │
    ├─ Document-oriented (nested, flexible schema) ────────────────────────────┐
    │   → MongoDB / DynamoDB                                                   │
    │
    ├─ Key-value (simple lookups, caching) ────────────────────────────────────┐
    │   → Redis / Memcached                                                    │
    │
    ├─ Time-series (metrics, logs) ────────────────────────────────────────────┐
    │   → InfluxDB / TimescaleDB                                               │
    │
    ├─ Graph (relationships are primary) ──────────────────────────────────────┐
    │   → Neo4j / Amazon Neptune                                               │
    │
    └─ Search (full-text, faceted) ────────────────────────────────────────────┐
        → Elasticsearch / Meilisearch                                          │
```

### Caching Strategy Selection

```
Q1: Cache use case?
    │
    ├─ Session data ───────────────────────────────────────────────────────────┐
    │   → Redis with TTL                                                       │
    │
    ├─ API response caching ───────────────────────────────────────────────────┐
    │   → HTTP caching (CDN) + Redis                                           │
    │
    ├─ Database query caching ─────────────────────────────────────────────────┐
    │   Q2: Write frequency?                                                   │
    │       ├─ Low writes → Cache-aside with TTL                               │
    │       └─ High writes → Write-through or Write-behind                     │
    │
    └─ Computed values caching ────────────────────────────────────────────────┐
        → Redis with lazy refresh / background update                          │
```

### Communication Pattern Selection

```
Q1: Communication type?
    │
    ├─ Request-Response (sync) ────────────────────────────────────────────────┐
    │   Q2: Internal or external?                                              │
    │       ├─ Internal services → gRPC (high perf) or REST (simplicity)       │
    │       └─ External APIs → REST or GraphQL                                 │
    │
    ├─ Event-driven (async) ───────────────────────────────────────────────────┐
    │   Q2: Ordering important?                                                │
    │       ├─ YES → Kafka (partitioned)                                       │
    │       └─ NO → RabbitMQ / SQS                                             │
    │
    └─ Real-time (streaming) ──────────────────────────────────────────────────┐
        Q2: Direction?                                                         │
            ├─ Server → Client → Server-Sent Events (SSE)                      │
            └─ Bidirectional → WebSockets                                      │
```

---

## Architecture Decision Record (ADR) Template

```markdown
# ADR-{NNN}: {Title}

## Status
{Proposed | Accepted | Deprecated | Superseded by ADR-XXX}

## Context
{What is the issue that we're seeing that motivates this decision?}

## Decision
{What is the change that we're proposing and/or doing?}

## Consequences
### Positive
- {benefit 1}
- {benefit 2}

### Negative
- {trade-off 1}
- {trade-off 2}

### Risks
- {risk 1}: {mitigation}

## Alternatives Considered
### {Alternative 1}
- Pros: {pros}
- Cons: {cons}
- Why rejected: {reason}

## References
- {link 1}
- {link 2}
```

---

## Quality Attributes Framework

| Attribute | Question | Metrics |
|-----------|----------|---------|
| **Scalability** | Can it handle 10x load? | RPS, concurrent users |
| **Performance** | How fast? | Latency (p50, p95, p99) |
| **Availability** | Uptime? | 99.9%, 99.99% SLA |
| **Reliability** | Failure handling? | MTBF, MTTR |
| **Security** | Attack surface? | OWASP, threat model |
| **Maintainability** | Change cost? | Deployment frequency |
| **Observability** | Debug-able? | Log, metric, trace coverage |
| **Cost** | Budget fit? | $/month, cost per user |

### Quality Attribute Trade-offs

```
                    High Performance
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
  Low Cost ───────────────┼─────────── High Scalability
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                    High Security

Common trade-offs:
- Performance vs Cost (more resources = faster but expensive)
- Security vs Usability (more checks = safer but slower UX)
- Scalability vs Simplicity (distributed = scales but complex)
- Consistency vs Availability (CAP theorem)
```

---

## C4 Model Quick Reference

| Level | Scope | Audience | Shows |
|-------|-------|----------|-------|
| **Context (C1)** | System | Business stakeholders | External systems, users |
| **Container (C2)** | System | Architects, developers | Apps, databases, services |
| **Component (C3)** | Container | Developers | Internal components |
| **Code (C4)** | Component | Developers | Classes, interfaces |

### C4 Diagram Template

```
# Context Diagram (C1)
[User] --> [System] --> [External Service]

# Container Diagram (C2)
[Web App] --> [API Server] --> [Database]
                    │
                    └──> [Cache]

# Component Diagram (C3)
[Controller] --> [Service] --> [Repository] --> [Database]
```
=======
Make informed architecture decisions balancing quality attributes (scalability, performance, security, maintainability) with business constraints (time, cost, team skills).

---

## Quick Decision Reference

| If you need... | Use | File |
|----------------|-----|------|
| **Architecture style** for small team/MVP | Monolith or Modular Monolith | [monolith-architecture.md](monolith-architecture.md), [modular-monolith.md](modular-monolith.md) |
| **Architecture style** for large team | Microservices | [microservices-architecture.md](microservices-architecture.md) |
| **Database** for relational data | PostgreSQL/MySQL | [database-selection.md](database-selection.md) |
| **Database** for documents | MongoDB/DynamoDB | [database-selection.md](database-selection.md) |
| **Database** for cache | Redis | [caching-architecture.md](caching-architecture.md) |
| **API** for external devs | REST + OpenAPI | [patterns.md](patterns.md) |
| **API** for internal | gRPC | [patterns.md](patterns.md) |
| **Communication** async | Kafka/RabbitMQ | [event-driven-architecture.md](event-driven-architecture.md) |
| **Pattern** for distributed transactions | Saga | [distributed-patterns.md](distributed-patterns.md) |
| **Pattern** for resilience | Circuit Breaker | [distributed-patterns.md](distributed-patterns.md) |

---

## Methodologies (30)

**Fundamentals (5):** system-design-process | c4-model | architecture-decision-records | quality-attributes-analysis | trade-off-analysis

**Styles (5):** monolith-architecture | microservices-architecture | modular-monolith | serverless-architecture | event-driven-architecture

**Patterns (5):** creational-patterns | structural-patterns | behavioral-patterns | architectural-patterns | distributed-patterns

**Data (4):** data-modeling | database-selection | caching-architecture | data-pipeline-design

**Infrastructure (4):** cloud-architecture | container-orchestration | api-gateway-design | service-mesh

**Quality (4):** security-architecture | performance-architecture | reliability-architecture | observability-architecture

**Templates (3):** adr-template | quality-attributes | workflows

---

## Quality Attributes

**Scalability:** Handle 10x load? | **Performance:** p95 < 200ms? | **Availability:** 99.9%+ uptime? | **Security:** Threat model done? | **Maintainability:** Deploy daily?

**Framework:** [quality-attributes.md](quality-attributes.md) | **Analysis:** [quality-attributes-analysis.md](quality-attributes-analysis.md)

---

## C4 Model

| Level | Audience | Shows | File |
|-------|----------|-------|------|
| Context (C1) | Business | External systems, users | [c4-model.md](c4-model.md) |
| Container (C2) | Architects | Apps, databases, services | [c4-model.md](c4-model.md) |
| Component (C3) | Developers | Internal components | [c4-model.md](c4-model.md) |

---

## ADR Template

```markdown
# ADR-NNN: Title
## Status: Proposed/Accepted
## Context: Why needed?
## Decision: What we decided
## Consequences: Trade-offs
## Alternatives: Other options
```

**Full template:** [adr-template.md](adr-template.md)
>>>>>>> claude

---

## Workflows

<<<<<<< HEAD
### System Design Workflow

```
1. CLARIFY Requirements
   - Functional requirements (what it does)
   - Non-functional requirements (quality attributes)
   - Constraints (budget, team, timeline)
   ↓
2. ESTIMATE Scale
   - Users (DAU, MAU, peak)
   - Data (storage, growth rate)
   - Traffic (RPS, bandwidth)
   ↓
3. DESIGN High-Level
   - C4 Context and Container diagrams
   - Major components and data flow
   - API contracts (REST/GraphQL/gRPC)
   ↓
4. DEEP DIVE Components
   - Database schema
   - Caching strategy
   - Message queues
   ↓
5. ADDRESS Quality Attributes
   - Scalability: horizontal/vertical
   - Reliability: redundancy, failover
   - Security: auth, encryption, rate limiting
   ↓
6. DOCUMENT Decisions
   - ADRs for key choices
   - Diagrams in repo
```

### Technology Selection Workflow

```
1. DEFINE Criteria
   - Must-haves (non-negotiable)
   - Nice-to-haves (preferred)
   - Constraints (team skills, cost)
   ↓
2. RESEARCH Options
   - Industry standards
   - Team familiarity
   - Community/support
   ↓
3. EVALUATE
   - Proof of concept if needed
   - Score against criteria
   ↓
4. DECIDE
   - Document in ADR
   - Get stakeholder buy-in
```

---

## Common Architecture Patterns

### Microservices Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| **API Gateway** | Multiple services to expose | Single entry point |
| **Service Discovery** | Dynamic service locations | Registry (Consul, etcd) |
| **Circuit Breaker** | Cascading failures | Fail fast, fallback |
| **Saga** | Distributed transactions | Orchestration/Choreography |
| **CQRS** | Read/write scaling | Separate read/write models |
| **Event Sourcing** | Audit, time travel | Store events, not state |

### Data Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| **Database per Service** | Service independence | Own database per service |
| **Shared Database** | Simple queries | Single database (anti-pattern for microservices) |
| **Saga** | Distributed consistency | Compensating transactions |
| **Outbox** | Reliable events | Write event to DB, publish async |

### Resilience Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| **Retry** | Transient failures | Exponential backoff |
| **Circuit Breaker** | Service down | Stop calling, fallback |
| **Bulkhead** | Isolation | Limit resources per service |
| **Timeout** | Hanging requests | Fail after limit |
| **Rate Limiting** | Overload | Reject excess requests |

---

## Integration with Other Skills

| Skill | When to Handoff |
|-------|-----------------|
| faion-software-developer | After architecture is defined, for implementation |
| faion-devops-engineer | For infrastructure implementation |
| faion-ml-engineer | For AI/ML architecture components |
| faion-product-manager | For non-functional requirements clarification |

---

## References

- [Decision Trees](decision-trees.md) - Detailed architecture decision trees
- [Patterns](patterns.md) - Design patterns reference

---

*faion-software-architect v1.0*
*28 Methodologies | 2 Agents*
=======
**System Design:** Requirements → Scale estimation → High-level design → Components → Quality attributes → Documentation

**Technology Selection:** Define criteria → Research → Evaluate → Decide → Document ADR

**Full workflows:** [workflows.md](workflows.md)

---

*faion-software-architect v1.2*
*30 Methodologies*
>>>>>>> claude
