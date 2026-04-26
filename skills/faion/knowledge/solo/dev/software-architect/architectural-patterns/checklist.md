# Architectural Pattern Selection Checklist

Step-by-step guide to choosing the right architectural pattern.

## Phase 1: Assess Project Context

### Domain Complexity

- [ ] **Simple domain:** CRUD operations, straightforward business rules
- [ ] **Medium domain:** Some business logic, validation, workflows
- [ ] **Complex domain:** Rich business rules, multiple entities, state machines
- [ ] **Very complex domain:** Multiple subdomains, different models per context

**Result:**
| Domain Complexity | Patterns to Consider |
|-------------------|---------------------|
| Simple | Layered, Transaction Script |
| Medium | Clean Architecture |
| Complex | Clean + DDD tactical patterns |
| Very Complex | Full DDD + Hexagonal |

### Team Characteristics

- [ ] **Team size:** _____ developers
- [ ] **Average experience:** Junior / Mid / Senior
- [ ] **DDD experience:** None / Some / Extensive
- [ ] **Domain knowledge:** Learning / Partial / Expert

**Result:**
| Team | Pattern Complexity |
|------|-------------------|
| Small junior team | Keep simple (Layered) |
| Mid-level team | Clean Architecture |
| Experienced team | DDD + Hexagonal |

### Input/Output Channels

- [ ] REST API
- [ ] GraphQL API
- [ ] gRPC
- [ ] CLI
- [ ] Web UI (server-rendered)
- [ ] Message queue consumers
- [ ] Scheduled jobs
- [ ] WebSocket

**Result:**
| Channels | Pattern |
|----------|---------|
| Single (REST only) | Clean Architecture |
| Multiple (2-3) | Hexagonal |
| Many (4+) | Hexagonal with explicit ports |

### External Dependencies

- [ ] Primary database
- [ ] Cache (Redis)
- [ ] Message broker (Kafka, RabbitMQ)
- [ ] Email service
- [ ] Payment gateway
- [ ] Third-party APIs
- [ ] File storage (S3)

**Result:**
| Dependencies | Pattern |
|--------------|---------|
| Few (1-2) | Clean Architecture |
| Several (3-5) | Hexagonal (secondary adapters) |
| Many (6+) | Hexagonal with adapter factories |

---

## Phase 2: Validate Pattern Choice

### Clean Architecture Checklist

Use if you answered YES to most:

- [ ] Domain has business logic worth protecting
- [ ] Might change UI framework in future
- [ ] Might change database in future
- [ ] Need comprehensive unit testing
- [ ] Team understands SOLID principles

### Hexagonal Architecture Checklist

Use if you answered YES to most:

- [ ] Multiple input channels (REST, CLI, etc.)
- [ ] Multiple output dependencies (DB, queue, cache)
- [ ] Need symmetric treatment of inputs and outputs
- [ ] Want explicit port interfaces for all boundaries
- [ ] May add new channels/dependencies frequently

### Onion Architecture Checklist

Use if you answered YES to most:

- [ ] .NET ecosystem (C#, F#)
- [ ] Enterprise application context
- [ ] Need domain services as separate layer
- [ ] Team familiar with Onion terminology

### DDD Checklist

Use if you answered YES to most:

- [ ] Complex domain with intricate business rules
- [ ] Access to domain experts for collaboration
- [ ] Time to develop ubiquitous language
- [ ] Multiple bounded contexts identified
- [ ] Need consistency boundaries (aggregates)
- [ ] Domain events are natural fit

---

## Phase 3: Layer Validation

### Domain Layer

- [ ] No framework dependencies
- [ ] No database dependencies
- [ ] Pure business logic only
- [ ] Entities encapsulate behavior (not anemic)
- [ ] Value objects are immutable
- [ ] Repository interfaces (not implementations)

### Application Layer

- [ ] Use cases are single-purpose
- [ ] DTOs for input/output
- [ ] Orchestrates domain objects
- [ ] No direct database access
- [ ] Transaction boundaries defined

### Infrastructure Layer

- [ ] Repository implementations here
- [ ] External service adapters here
- [ ] Database-specific code isolated
- [ ] Configuration management

### Presentation Layer

- [ ] Controllers are thin
- [ ] No business logic
- [ ] Handles HTTP/CLI concerns only
- [ ] Validation for format, not business rules

---

## Phase 4: Dependency Rule Verification

### Import Analysis

Check that imports follow dependency rules:

```
Domain Layer
├── Can import: nothing external
├── Cannot import: Application, Infrastructure, Presentation
└── Allowed: language stdlib, utility libraries

Application Layer
├── Can import: Domain
├── Cannot import: Infrastructure, Presentation
└── Allowed: Domain entities, value objects, repository interfaces

Infrastructure Layer
├── Can import: Domain, Application
├── Cannot import: Presentation
└── Allowed: Frameworks, ORMs, external SDKs

Presentation Layer
├── Can import: Domain, Application
├── Cannot import: Infrastructure
└── Allowed: Web frameworks, CLI frameworks
```

### Test Your Dependencies

Run this mental test for each file:

1. Can this file be tested without a database? (Yes for Domain, Application)
2. Can this file be tested without HTTP? (Yes for Domain, Application, Infrastructure)
3. Does this file know about the web framework? (Only Presentation)
4. Does this file know about the ORM? (Only Infrastructure)

---

## Phase 5: Implementation Readiness

### Before Starting

- [ ] Folder structure decided and documented
- [ ] Naming conventions defined
- [ ] Dependency injection strategy chosen
- [ ] Testing strategy per layer defined
- [ ] Team aligned on pattern

### Documentation

- [ ] Architecture decision record (ADR) created
- [ ] CLAUDE.md includes architecture overview
- [ ] Folder README.md files explain structure
- [ ] Example file in each layer

### Tooling

- [ ] Linter rules for import restrictions (if available)
- [ ] Project references prevent wrong dependencies (if available)
- [ ] CI check for architecture violations (ArchUnit, etc.)

---

## Quick Reference Card

| Question | Answer | Pattern |
|----------|--------|---------|
| Just CRUD? | Yes | Layered |
| Business logic? | Yes | Clean |
| Multiple UIs? | Yes | Hexagonal |
| Domain experts available? | Yes | DDD |
| Enterprise .NET? | Yes | Onion |

| Risk | Mitigation |
|------|------------|
| Over-engineering | Start simple, evolve |
| Anemic domain | Review entity behavior regularly |
| Layer leaking | Enforce with imports/tooling |
| Wrong abstractions | Delay abstraction until pattern emerges |

---

## Anti-Pattern Checklist

Verify you're NOT doing these:

- [ ] **NOT** putting business logic in controllers
- [ ] **NOT** calling database directly from controllers
- [ ] **NOT** importing infrastructure in domain
- [ ] **NOT** creating god objects/classes
- [ ] **NOT** using ORM entities as domain entities
- [ ] **NOT** exposing domain entities via API
- [ ] **NOT** having circular dependencies between layers
- [ ] **NOT** putting validation in multiple places
