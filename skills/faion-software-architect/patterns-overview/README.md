# Design Patterns Overview

Comprehensive guide to software design patterns for building maintainable, scalable, and flexible systems.

## What Are Design Patterns?

Design patterns are reusable solutions to commonly occurring problems in software design. They represent best practices evolved over time by experienced developers and provide a shared vocabulary for discussing solutions.

**Key characteristics:**
- Language-agnostic conceptual blueprints
- Proven solutions refined across countless implementations
- Communication tools for team alignment
- Building blocks for complex systems

## Pattern Categories

### Creational Patterns

Handle object creation mechanisms, controlling how and when objects are instantiated.

| Pattern | Problem Solved | When to Use |
|---------|----------------|-------------|
| **Factory Method** | Single creation point, type varies | PaymentProcessor, NotificationService |
| **Abstract Factory** | Object family that varies | UI toolkit (Windows/Mac), database drivers |
| **Builder** | Complex object with many parameters | QueryBuilder, RequestBuilder, ConfigBuilder |
| **Prototype** | Expensive object, reuse instances | Game object spawning, document cloning |
| **Singleton** | Only one instance ever | Configuration, Logger, Connection pool |

**Modern alternative:** Dependency Injection (DI) containers often replace Factory and Singleton patterns.

### Structural Patterns

Deal with object composition, forming larger structures from classes and objects.

| Pattern | Problem Solved | When to Use |
|---------|----------------|-------------|
| **Adapter** | Incompatible interface | Legacy API wrapper, third-party integration |
| **Bridge** | Multiple implementations x abstractions | Notification (Email/SMS) x (Urgent/Normal) |
| **Composite** | Tree structure, uniform treatment | File system, UI components, org charts |
| **Decorator** | Add behavior dynamically | Middleware, stream wrappers, logging |
| **Facade** | Simplify complex subsystem | Payment service hiding card/fraud/ledger |
| **Flyweight** | Many similar objects, share state | Character rendering, game particles |
| **Proxy** | Control access to object | Lazy loading, caching, access control |

### Behavioral Patterns

Concerned with algorithms and assignment of responsibilities between objects.

| Pattern | Problem Solved | When to Use |
|---------|----------------|-------------|
| **Strategy** | Vary algorithm at runtime | Sorting, payment methods, pricing rules |
| **Observer** | Notify multiple objects of changes | Event systems, pub/sub, reactive UIs |
| **Command** | Encapsulate request as object | Undo/redo, job queues, transaction logging |
| **State** | Behavior changes with state | Order status, media player, workflows |
| **Chain of Responsibility** | Pass request along chain | Middleware, validation, approval flows |
| **Template Method** | Define skeleton, defer steps | Test frameworks, ETL pipelines |
| **Iterator** | Traverse collection uniformly | Database cursors, pagination |
| **Mediator** | Reduce direct dependencies | Chat rooms, air traffic control |
| **Visitor** | Add operations without changing classes | AST processing, report generation |
| **Memento** | Capture and restore state | Undo mechanisms, snapshots |

## Architectural Patterns

### Layered Architecture

```
Presentation Layer     →  Controllers, Views, DTOs
Application Layer      →  Use Cases, Services, Orchestration
Domain Layer           →  Entities, Business Logic, Domain Services
Infrastructure Layer   →  Databases, APIs, File Systems, Cache
```

**When to use:** Traditional web applications, clear separation needed, team familiarity.

### Clean Architecture

```
External Systems       →  DB, UI, Web, Devices (outer)
Interface Adapters     →  Controllers, Gateways, Presenters
Use Cases              →  Application-specific rules
Entities               →  Business objects, domain rules (inner)
```

**Key principle:** Dependencies point inward only (Dependency Inversion).

### Hexagonal Architecture (Ports & Adapters)

- **Ports:** Interfaces defining how to interact with core
- **Adapters:** Implementations of ports (PostgresAdapter, RestAdapter)
- **Core:** Domain logic isolated from external concerns

**When to use:** Multiple entry points (REST, GraphQL, CLI), heavy testing requirements.

## Distributed System Patterns

### Resilience Patterns

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| **Circuit Breaker** | Prevent cascade failures | CLOSED → OPEN → HALF-OPEN states |
| **Bulkhead** | Isolate failures | Separate thread pools, rate limits |
| **Retry** | Handle transient failures | Exponential backoff, jitter |
| **Timeout** | Bound waiting time | Request deadlines, cancellation |
| **Fallback** | Graceful degradation | Default values, cached responses |

### Data Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **CQRS** | Separate read/write models | Different read/write patterns, scale independently |
| **Event Sourcing** | Store events, not state | Audit trails, time-travel debugging |
| **Saga** | Distributed transactions | Cross-service consistency, compensating actions |
| **Outbox** | Reliable event publishing | At-least-once delivery, avoid dual-write |
| **Repository** | Abstract data access | Testability, decouple from database |

### Cloud-Native Patterns (2025)

| Pattern | Purpose | Tools |
|---------|---------|-------|
| **Service Mesh** | Service-to-service communication | Istio, Linkerd, Cilium |
| **Sidecar** | Cross-cutting concerns | Envoy proxy, logging agents |
| **Ambassador** | Proxy for legacy services | API translation, protocol bridging |
| **Database per Service** | Service independence | PostgreSQL, MongoDB per service |
| **API Gateway** | Centralized entry point | Kong, AWS API Gateway, Traefik |

## Modern Pattern Trends (2025-2026)

### Language Features Replacing Patterns

Many classic patterns are simplified by modern language features:

| Classic Pattern | Modern Alternative |
|-----------------|-------------------|
| Iterator | Native `for..of`, generators |
| Strategy | First-class functions, lambdas |
| Command | Closures, async/await |
| Observer | Reactive streams (RxJS, Kotlin Flow) |
| Singleton | Module systems, DI containers |
| Factory | DI frameworks (Spring, FastAPI) |

### AI-Influenced Patterns

- **RAG Pipeline Pattern:** Retrieval-augmented generation architecture
- **Agent Pattern:** Autonomous AI agents with tool use
- **Prompt Template Pattern:** Reusable prompt structures
- **Guardrail Pattern:** Input/output validation for LLMs

### Event-Driven Evolution

- **CloudEvents:** Standardized event format
- **Event Mesh:** Cross-cloud event routing
- **Async API:** OpenAPI for event-driven systems

## LLM-Assisted Pattern Design

### When to Use LLM for Patterns

| Task | LLM Effectiveness |
|------|-------------------|
| Pattern selection based on requirements | High |
| Implementation examples in any language | High |
| Trade-off analysis between patterns | High |
| Code review for pattern misuse | Medium-High |
| Refactoring to apply patterns | Medium |

### Effective Prompting Strategies

1. **Describe the problem, not the solution**
   - Let LLM suggest appropriate patterns
   - Provide context about constraints

2. **Request multiple alternatives**
   - Compare trade-offs
   - Consider hybrid approaches

3. **Ask for anti-pattern warnings**
   - Identify potential misuse
   - Understand when NOT to use a pattern

## External Resources

### Books

- "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF) - Foundation
- "Patterns of Enterprise Application Architecture" (Fowler) - Enterprise patterns
- "Enterprise Integration Patterns" (Hohpe, Woolf) - Messaging patterns
- "Building Microservices" (Newman) - Distributed patterns

### Online Resources

- [Patterns.dev](https://www.patterns.dev/) - Modern JavaScript/React patterns
- [Refactoring.Guru](https://refactoring.guru/design-patterns) - Pattern catalog with examples
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/) - Messaging patterns
- [Cloud Design Patterns (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/patterns/) - Cloud-native patterns

### Industry Adoption

Tech giants embed design patterns into their architecture:
- **Amazon:** Strategy pattern in recommendation engine
- **Netflix:** Proxy pattern for service access
- **Google:** Observer and Mediator in event-driven tools
- **Microsoft:** CQRS in .NET APIs

## Related Methodologies

| Methodology | Path |
|-------------|------|
| Creational Patterns | [creational-patterns/](../creational-patterns/) |
| Structural Patterns | [structural-patterns/](../structural-patterns/) |
| Behavioral Patterns | [behavioral-patterns/](../behavioral-patterns/) |
| Distributed Patterns | [distributed-patterns/](../distributed-patterns/) |
| Architectural Patterns | [architectural-patterns/](../architectural-patterns/) |

---

*Design Patterns Overview v1.0*
*Part of faion-software-architect skill*
