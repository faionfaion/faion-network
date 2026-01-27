# Architectural Patterns

Domain-centric architectural patterns for building maintainable, testable software.

## Overview

| Pattern | Creator | Core Concept | Best For |
|---------|---------|--------------|----------|
| Clean Architecture | Robert C. Martin | Concentric circles, dependencies inward | Complex business logic |
| Hexagonal Architecture | Alistair Cockburn | Ports & Adapters | Multi-interface systems |
| Onion Architecture | Jeffrey Palermo | Domain at center, no outward deps | Enterprise apps |
| Domain-Driven Design | Eric Evans | Ubiquitous language, bounded contexts | Complex domains |

## Clean Architecture (Uncle Bob)

**Origin:** Robert C. Martin, 2012
**Book:** "Clean Architecture: A Craftsman's Guide to Software Structure and Design"

### Core Principle

Dependencies point inward. Inner circles know nothing about outer circles.

### Layers (Inside Out)

```
Domain Layer (Entities)
    → Application Layer (Use Cases)
        → Interface Adapters (Controllers, Presenters, Gateways)
            → Frameworks & Drivers (DB, Web, UI)
```

### Folder Structure

```
src/
├── domain/                 # Innermost - no dependencies
│   ├── entities/           # Business objects
│   │   ├── User.ts
│   │   └── Order.ts
│   ├── value-objects/      # Immutable domain concepts
│   │   ├── Money.ts
│   │   └── Email.ts
│   └── repositories/       # Interfaces only (not implementations)
│       └── IUserRepository.ts
│
├── application/            # Depends only on domain
│   ├── use-cases/          # Business operations
│   │   ├── CreateUser.ts
│   │   └── PlaceOrder.ts
│   ├── dto/                # Data transfer objects
│   │   └── UserDTO.ts
│   └── interfaces/         # Port definitions
│       └── IEmailService.ts
│
├── infrastructure/         # Depends on application
│   ├── persistence/        # Repository implementations
│   │   ├── PostgresUserRepository.ts
│   │   └── InMemoryUserRepository.ts
│   ├── services/           # External service adapters
│   │   └── SendGridEmailService.ts
│   └── config/             # Environment, DI container
│       └── container.ts
│
└── presentation/           # Depends on application
    ├── api/                # REST/GraphQL controllers
    │   └── UserController.ts
    ├── cli/                # Command-line interface
    │   └── commands/
    └── web/                # Web UI (if server-rendered)
        └── views/
```

### Dependency Rule

| Layer | Can Depend On | Cannot Depend On |
|-------|---------------|------------------|
| Domain | Nothing | Everything else |
| Application | Domain | Infrastructure, Presentation |
| Infrastructure | Application, Domain | Presentation |
| Presentation | Application, Domain | Infrastructure |

### Key Benefits

- **Testability:** Domain and use cases are pure, easily unit tested
- **Framework independence:** Framework is a detail, not the architecture
- **Database independence:** Swap databases without touching business logic
- **UI independence:** API, CLI, or Web UI share same business logic

---

## Hexagonal Architecture (Ports & Adapters)

**Origin:** Alistair Cockburn, 2005
**Alternative name:** Ports and Adapters Architecture

### Core Principle

The application core is isolated from the outside world through ports (interfaces) and adapters (implementations).

### Structure

```
                Primary Adapters              Secondary Adapters
                (Driving)                     (Driven)

                ┌─────────────────────────────────────────┐
    REST API ──→│                                         │──→ PostgreSQL
                │        ┌─────────────────┐              │
    GraphQL ───→│        │   Application   │              │──→ Redis
                │        │      Core       │              │
    CLI ───────→│        │    (Domain)     │              │──→ Email Service
                │        └─────────────────┘              │
    gRPC ──────→│                                         │──→ Payment Gateway
                └─────────────────────────────────────────┘

                        Ports = Interfaces
                        Adapters = Implementations
```

### Folder Structure

```
src/
├── core/                      # Application hexagon
│   ├── domain/                # Entities, value objects
│   │   ├── entities/
│   │   └── value-objects/
│   ├── ports/                 # Interface definitions
│   │   ├── inbound/           # Primary ports (use cases)
│   │   │   ├── CreateUserPort.ts
│   │   │   └── GetUserPort.ts
│   │   └── outbound/          # Secondary ports (driven)
│   │       ├── UserRepository.ts
│   │       └── EmailSender.ts
│   └── services/              # Domain services
│       └── UserService.ts
│
├── adapters/
│   ├── inbound/               # Primary adapters (drivers)
│   │   ├── rest/
│   │   │   └── UserController.ts
│   │   ├── graphql/
│   │   │   └── UserResolver.ts
│   │   └── cli/
│   │       └── UserCommand.ts
│   └── outbound/              # Secondary adapters (driven)
│       ├── persistence/
│       │   └── PostgresUserRepository.ts
│       └── email/
│           └── SendGridEmailAdapter.ts
│
└── config/                    # Bootstrap, DI
    └── container.ts
```

### Port Types

| Type | Direction | Purpose | Examples |
|------|-----------|---------|----------|
| Primary (Inbound) | Outside → Core | Define what the app can do | CreateUser, GetOrders |
| Secondary (Outbound) | Core → Outside | Define what the app needs | Repository, EmailSender |

### Key Benefits

- **Symmetry:** Same pattern for all external interactions
- **Testing:** Mock any adapter for isolated testing
- **Flexibility:** Add new interfaces (gRPC, WebSocket) without core changes
- **Clear boundaries:** Explicit contracts between core and outside world

---

## Onion Architecture

**Origin:** Jeffrey Palermo, 2008
**Similar to:** Clean Architecture, but domain-focused

### Core Principle

All coupling toward the center. Domain Model has no outward dependencies.

### Layers (Inside Out)

```
Domain Model (Entities)
    → Domain Services
        → Application Services
            → Infrastructure
```

### Folder Structure

```
src/
├── Domain/                    # Innermost layer
│   ├── Entities/              # Domain entities
│   │   └── User.cs
│   ├── ValueObjects/          # Domain value objects
│   │   └── Email.cs
│   └── Interfaces/            # Repository interfaces
│       └── IUserRepository.cs
│
├── Domain.Services/           # Domain logic that spans entities
│   └── UserDomainService.cs
│
├── Application/               # Use cases, orchestration
│   ├── Services/
│   │   └── UserApplicationService.cs
│   ├── DTOs/
│   │   └── UserDto.cs
│   └── Interfaces/            # External service interfaces
│       └── IEmailService.cs
│
├── Infrastructure/            # External concerns
│   ├── Persistence/
│   │   └── UserRepository.cs
│   ├── Email/
│   │   └── SmtpEmailService.cs
│   └── DependencyInjection/
│       └── ServiceCollectionExtensions.cs
│
└── Presentation/              # UI layer
    ├── API/
    │   └── Controllers/
    └── Web/
        └── Pages/
```

### Key Differences from Clean Architecture

| Aspect | Clean Architecture | Onion Architecture |
|--------|-------------------|-------------------|
| Domain Services | Part of Application layer | Separate layer |
| Use Cases | Explicit concept | Called Application Services |
| Naming | Use Case driven | Layer driven |
| Origin | Software craftsmanship | Enterprise .NET |

---

## Domain-Driven Design (DDD)

**Origin:** Eric Evans, 2003
**Book:** "Domain-Driven Design: Tackling Complexity in the Heart of Software"

### Core Concepts

| Concept | Description |
|---------|-------------|
| Ubiquitous Language | Shared vocabulary between devs and domain experts |
| Bounded Context | Explicit boundary with its own model |
| Aggregate | Cluster of entities with a root entity |
| Entity | Identity-based domain object |
| Value Object | Immutable, identity-less domain object |
| Domain Event | Something significant that happened |
| Repository | Collection-like interface for aggregates |

### Strategic vs Tactical

```
Strategic DDD                    Tactical DDD
(High-level)                     (Implementation)
────────────────                 ────────────────
Bounded Contexts                 Entities
Context Maps                     Value Objects
Subdomains                       Aggregates
Core/Supporting/Generic          Domain Events
                                 Repositories
                                 Domain Services
                                 Factories
```

### Folder Structure (DDD + Hexagonal)

```
src/
├── bounded-contexts/
│   ├── ordering/               # Ordering bounded context
│   │   ├── domain/
│   │   │   ├── aggregates/
│   │   │   │   └── Order/
│   │   │   │       ├── Order.ts          # Aggregate root
│   │   │   │       ├── OrderItem.ts      # Entity
│   │   │   │       └── OrderStatus.ts    # Value object
│   │   │   ├── events/
│   │   │   │   └── OrderPlaced.ts        # Domain event
│   │   │   ├── repositories/
│   │   │   │   └── IOrderRepository.ts
│   │   │   └── services/
│   │   │       └── OrderPricingService.ts
│   │   ├── application/
│   │   │   ├── commands/
│   │   │   │   └── PlaceOrder.ts
│   │   │   └── queries/
│   │   │       └── GetOrderHistory.ts
│   │   └── infrastructure/
│   │       └── persistence/
│   │           └── PostgresOrderRepository.ts
│   │
│   └── inventory/              # Inventory bounded context
│       ├── domain/
│       ├── application/
│       └── infrastructure/
│
└── shared-kernel/              # Shared between contexts
    ├── domain/
    │   └── Money.ts
    └── events/
        └── EventBus.ts
```

### Aggregate Rules

1. **Reference by identity:** Aggregates reference each other by ID, not direct object reference
2. **Consistency boundary:** One aggregate = one transaction
3. **Root controls access:** All access to entities goes through the aggregate root
4. **Delete together:** When root is deleted, all entities in aggregate are deleted

---

## Pattern Selection Guide

### By Project Characteristics

| Characteristic | Recommended Pattern |
|----------------|---------------------|
| Simple CRUD | Layered or Transaction Script |
| Complex business rules | Clean / Hexagonal / Onion |
| Multiple UIs | Hexagonal (explicit ports) |
| Multiple databases | Clean Architecture |
| Large team, complex domain | DDD + Hexagonal |
| Microservices | DDD Bounded Contexts |

### By Team Experience

| Team Experience | Pattern |
|-----------------|---------|
| Junior team | Layered Architecture |
| Mid-level team | Clean Architecture |
| Senior team | DDD + Hexagonal |

### Decision Flowchart

```
Is the domain complex?
├─ No → Layered Architecture or Transaction Script
└─ Yes → Do you have multiple input channels?
         ├─ No → Clean Architecture
         └─ Yes → Do you need explicit ports for testing?
                  ├─ No → Clean Architecture
                  └─ Yes → Hexagonal Architecture
                           └─ Is the domain very complex with multiple subdomains?
                              ├─ No → Hexagonal alone
                              └─ Yes → DDD + Hexagonal
```

---

## LLM-Assisted Development

These patterns work exceptionally well with LLM coding assistants because:

1. **Clear boundaries:** LLMs understand and respect layer boundaries
2. **Explicit dependencies:** Dependency injection makes intent clear
3. **Testability:** Easy to generate unit tests for isolated components
4. **Predictable structure:** Consistent folder structure aids navigation

### Best Practices for LLM Development

- Keep files focused (one class/module per file)
- Use explicit interfaces for all external dependencies
- Name files consistently with their content
- Document the pattern in CLAUDE.md or README.md

---

## References

### Books

- [Clean Architecture](https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/) - Robert C. Martin (2017)
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) - Eric Evans (2003)
- [Implementing Domain-Driven Design](https://vaughnvernon.com/) - Vaughn Vernon (2013)

### Articles

- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Robert C. Martin
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) - Jeffrey Palermo

### Online Resources

- [Domain-Driven Hexagon](https://github.com/Sairyss/domain-driven-hexagon) - Comprehensive example
- [Explicit Architecture](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/) - Herberto Graca

---

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pattern selection checklist |
| [examples.md](examples.md) | Pattern implementations |
| [templates.md](templates.md) | Code templates by pattern |
| [llm-prompts.md](llm-prompts.md) | Prompts for architecture discussions |
