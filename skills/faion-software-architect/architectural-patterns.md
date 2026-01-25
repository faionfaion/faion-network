# Architectural Patterns

High-level patterns for system structure.

## Overview

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Layered | Horizontal layers | Most web apps |
| Clean/Hexagonal | Dependency inversion | Complex domain logic |
| MVC/MVP/MVVM | UI separation | Frontend, mobile |
| CQRS | Separate read/write | High-scale reads |
| Pipes & Filters | Sequential processing | Data pipelines |

## Layered Architecture

Horizontal separation of concerns.

```
┌─────────────────────────┐
│    Presentation Layer   │  Controllers, Views
├─────────────────────────┤
│     Application Layer   │  Use cases, DTOs
├─────────────────────────┤
│      Domain Layer       │  Business logic, Entities
├─────────────────────────┤
│   Infrastructure Layer  │  DB, External services
└─────────────────────────┘

Rule: Each layer only depends on layer below
```

**Pros:** Simple, well understood
**Cons:** Can lead to anemic domain, tight coupling

## Clean Architecture

Dependency points inward toward domain.

```
        ┌─────────────────────────────────────┐
        │          Frameworks & Drivers        │
        │   ┌─────────────────────────────┐   │
        │   │    Interface Adapters       │   │
        │   │   ┌─────────────────────┐   │   │
        │   │   │   Application       │   │   │
        │   │   │  ┌─────────────┐    │   │   │
        │   │   │  │   Domain    │    │   │   │
        │   │   │  └─────────────┘    │   │   │
        │   │   └─────────────────────┘   │   │
        │   └─────────────────────────────┘   │
        └─────────────────────────────────────┘

                   Dependencies →
                   (always inward)
```

```
domain/           # Entities, value objects (no dependencies)
├── entities/
├── value_objects/
└── repositories/  # Interfaces only

application/      # Use cases (depends on domain)
├── services/
└── dto/

infrastructure/   # Implementations (depends on application)
├── db/
├── api/
└── external/

presentation/     # UI (depends on application)
├── controllers/
└── views/
```

## Hexagonal Architecture (Ports & Adapters)

Domain at center, adapters for external world.

```
                 ┌─────────────────┐
    Primary      │                 │     Secondary
    Adapters     │                 │     Adapters
                 │                 │
  ┌──────┐       │    ┌───────┐   │       ┌──────┐
  │ REST │◀──────│────│ Core  │───│──────▶│  DB  │
  │ API  │       │    │Domain │   │       │      │
  └──────┘       │    └───────┘   │       └──────┘
                 │        │       │
  ┌──────┐       │        │       │       ┌──────┐
  │ CLI  │◀──────│────────│───────│──────▶│Email │
  └──────┘       │                │       └──────┘
                 └─────────────────┘

Ports = Interfaces (in domain)
Adapters = Implementations (in infrastructure)
```

## MVC (Model-View-Controller)

```
         User
           │
           ▼
    ┌────────────┐
    │   View     │────────┐
    └────────────┘        │
           │              │
           ▼              │
    ┌────────────┐        │
    │ Controller │        │
    └────────────┘        │
           │              │
           ▼              │
    ┌────────────┐        │
    │   Model    │◀───────┘
    └────────────┘
```

- **Model:** Data and business logic
- **View:** Display (observes Model)
- **Controller:** Handles input, updates Model

## MVVM (Model-View-ViewModel)

```
    ┌────────────┐
    │   View     │
    └─────┬──────┘
          │ Data binding
          ▼
    ┌────────────┐
    │ ViewModel  │
    └─────┬──────┘
          │
          ▼
    ┌────────────┐
    │   Model    │
    └────────────┘
```

- **ViewModel:** Exposes data for View, handles UI logic
- Two-way data binding between View and ViewModel
- Popular in: WPF, SwiftUI, Vue.js

## CQRS (Command Query Responsibility Segregation)

```
        Commands                    Queries
            │                          │
            ▼                          ▼
    ┌───────────────┐          ┌───────────────┐
    │ Write Model   │          │  Read Model   │
    │ (normalized)  │──events─▶│ (denormalized)│
    └───────────────┘          └───────────────┘
            │                          │
            ▼                          ▼
       Write DB                   Read DB
       (PostgreSQL)               (Elasticsearch)
```

**Commands:** Create, Update, Delete
**Queries:** Read only

**When to use:**
- Different scaling needs for read/write
- Complex domain with simple reads
- Need different data models

## Pipes and Filters

```
Input ─▶ Filter A ─▶ Filter B ─▶ Filter C ─▶ Output

Example:
Raw Log ─▶ Parse ─▶ Transform ─▶ Enrich ─▶ Store
```

- Each filter is independent
- Easy to add/remove/reorder
- Use for: ETL, data processing, streaming

## Pattern Selection

| Scenario | Pattern |
|----------|---------|
| Simple CRUD app | Layered |
| Complex business logic | Clean/Hexagonal |
| UI-heavy application | MVC/MVVM |
| High read volume | CQRS |
| Data pipeline | Pipes & Filters |

## Related

- [distributed-patterns.md](distributed-patterns.md) - Distributed systems
- [event-driven-architecture.md](event-driven-architecture.md) - Event patterns
