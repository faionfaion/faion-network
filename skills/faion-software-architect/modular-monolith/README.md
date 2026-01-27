# Modular Monolith Architecture

Best of both worlds: monolith simplicity with microservices boundaries.

## What is a Modular Monolith?

A **modular monolith** is a single deployable unit with strict module boundaries. It combines the operational simplicity of a monolith with the architectural benefits of microservices.

| Aspect | Modular Monolith |
|--------|------------------|
| Deployment | Single unit |
| Communication | In-process (method calls, events) |
| Data | Separate schemas or databases, same deployment |
| Boundaries | Strict, enforced by tooling |
| Extraction | Easy to split into microservices later |

## When to Use Modular Monolith

**Choose modular monolith when:**

| Scenario | Why It Works |
|----------|--------------|
| New project with growth expectations | Start simple, scale when needed |
| Team size < 10 developers | Microservices overhead not justified |
| Unvalidated business model | Need to pivot quickly |
| Limited DevOps maturity | Single deployment is simpler |
| Learning DDD | Practice bounded contexts without distributed complexity |
| Clear domain boundaries exist | Modules map to business domains |

**Choose microservices instead when:**

| Scenario | Why Microservices |
|----------|-------------------|
| Independent scaling per module | Different load patterns |
| Multiple teams (10+) | Independent deployment cycles |
| Polyglot requirements | Different tech stacks per service |
| Strict fault isolation | Failure in one service shouldn't affect others |
| Regulatory compliance | Separate audit boundaries |

## Core Principles

### 1. Module = Bounded Context

Each module represents a distinct business domain (bounded context in DDD terms).

```
Modules align with business domains:
- Users (authentication, profiles)
- Orders (cart, checkout)
- Payments (transactions, refunds)
- Inventory (stock, warehouses)
- Notifications (email, SMS, push)
```

### 2. Public API Only

Modules communicate through defined interfaces, not direct access.

```python
# WRONG: Direct access to internal models
from orders.models import Order
order = Order.objects.get(id=123)

# RIGHT: Through public API
from orders.api import OrderService
order = OrderService.get_order(123)
```

### 3. No Shared Models

Each module owns its models. Other modules use DTOs or value objects.

```python
# users/models.py - owned by Users module
class User:
    id: int
    email: str
    name: str

# orders/models.py - Orders' view of a user
class OrderCustomer:
    user_id: int  # Reference by ID only
    name: str     # Denormalized for display
```

### 4. Data Isolation

Each module manages its own data. No cross-module database access.

```sql
-- Separate schemas per module
CREATE SCHEMA users;
CREATE SCHEMA orders;
CREATE SCHEMA payments;

-- Tables in respective schemas
CREATE TABLE users.accounts (...);
CREATE TABLE orders.orders (...);
CREATE TABLE payments.transactions (...);
```

### 5. No Cross-Schema Joins

Query data through module APIs, not SQL joins.

```sql
-- WRONG: Cross-schema join
SELECT * FROM users.accounts u
JOIN orders.orders o ON u.id = o.user_id;

-- RIGHT: Query through module API or denormalize
```

## Communication Patterns

### Synchronous (Direct Calls)

Simple, fast, and suitable for most cases.

```python
# In payment module
from orders.api import get_order

def process_payment(order_id: int):
    order = get_order(order_id)  # In-process call
    # Process payment...
```

**Pros:** Simple, type-safe, debuggable
**Cons:** Tight coupling, harder to extract later

### Asynchronous (Events)

Decoupled, enables eventual consistency.

```python
# orders/services.py
def complete_order(order_id: int):
    order = repository.complete(order_id)
    event_bus.publish(OrderCompletedEvent(order_id))

# payments/handlers.py
@event_handler(OrderCompletedEvent)
def handle_order_completed(event):
    process_payment(event.order_id)
```

**Pros:** Loose coupling, easier extraction to microservices
**Cons:** More complex, eventual consistency

### Choosing Communication Style

| Factor | Direct Call | Events |
|--------|-------------|--------|
| Consistency | Strong (same transaction) | Eventual |
| Coupling | Higher | Lower |
| Migration to microservices | Harder | Easier |
| Debugging | Easier | Harder |
| Performance | Faster | Async overhead |

**Recommendation:** Start with direct calls, introduce events for cross-cutting concerns or when preparing for extraction.

## Database Strategies

### Option 1: Shared Database, Separate Schemas

Most common approach. Single database instance with schema-per-module.

```
Database: app_db
├── Schema: users
│   ├── accounts
│   └── profiles
├── Schema: orders
│   ├── orders
│   └── order_items
└── Schema: payments
    ├── transactions
    └── refunds
```

**Pros:** Simple ops, ACID transactions possible
**Cons:** Temptation to join across schemas

### Option 2: Separate Databases

Stricter isolation, closer to microservices.

```
Databases:
├── users_db
├── orders_db
└── payments_db
```

**Pros:** True isolation, easier extraction
**Cons:** No cross-module transactions, more ops complexity

### Option 3: Hybrid

Critical modules get separate databases, others share.

```
Databases:
├── core_db (users, auth)
├── orders_db (orders, payments)
└── analytics_db (reporting)
```

## Vertical Slice Architecture Integration

Combine modular monolith with vertical slices for feature-focused organization.

```
src/
├── orders/                    # Module (Bounded Context)
│   ├── features/              # Vertical Slices
│   │   ├── create_order/
│   │   │   ├── command.py     # CQRS Command
│   │   │   ├── handler.py     # Business Logic
│   │   │   └── endpoint.py    # API Endpoint
│   │   ├── get_order/
│   │   │   ├── query.py       # CQRS Query
│   │   │   ├── handler.py
│   │   │   └── endpoint.py
│   │   └── cancel_order/
│   ├── domain/                # Domain Model
│   ├── infrastructure/        # Data Access, External Services
│   └── api.py                 # Public Module API
```

**Benefits:**
- Feature changes isolated to single folder
- High cohesion within slice
- Teams can work on different features independently
- Natural CQRS implementation

## Migration Paths

### From Traditional Monolith to Modular Monolith

1. **Identify domains** - Map business capabilities to potential modules
2. **Extract shared code** - Create a `shared/` or `common/` package
3. **Create module boundaries** - Organize code into module packages
4. **Add public APIs** - Define interfaces for cross-module communication
5. **Separate data** - Create schema per module
6. **Enforce boundaries** - Add linting rules (ArchUnit, import-linter)
7. **Introduce events** - For loosely-coupled cross-cutting concerns

### From Modular Monolith to Microservices

Use the **Strangler Fig Pattern** for incremental extraction:

1. **Select module** - Choose highest-value extraction candidate
2. **Verify boundaries** - Ensure module has clear API, own schema
3. **Create service** - Copy module to new deployable unit
4. **Add facade** - Route requests to either monolith or new service
5. **Replace communication** - In-process calls become HTTP/gRPC
6. **Replace events** - In-memory events become message queue
7. **Separate database** - Extract module's schema to own database
8. **Decommission** - Remove module from monolith

**Critical rule:** Extract the database with the service, or don't extract yet.

## Enforcing Boundaries

### Python: import-linter

```ini
# .importlinter
[importlinter]
root_package = src

[importlinter:contract:modules]
name = Module boundaries
type = independence
modules =
    src.users
    src.orders
    src.payments

[importlinter:contract:layers]
name = Clean architecture layers
type = layers
layers =
    src.api
    src.services
    src.domain
    src.infrastructure
```

### Java: ArchUnit / Spring Modulith

```java
// ArchUnit test
@Test
void moduleBoundaries() {
    classes()
        .that().resideInPackage("..orders.internal..")
        .should().onlyBeAccessedByClassesThat()
        .resideInPackage("..orders..")
        .check(importedClasses);
}

// Spring Modulith verification
@Test
void verifyModularity() {
    ApplicationModules.of(Application.class).verify();
}
```

### Go: Package visibility + linting

```go
// internal/ package prevents external access
// Use golangci-lint with depguard

// .golangci.yml
linters-settings:
  depguard:
    rules:
      main:
        deny:
          - pkg: "myapp/orders/internal"
            desc: "Orders internals are private"
```

## LLM Usage Tips

### When to Use This Methodology

- Designing new systems that may need to scale
- Refactoring monoliths for better organization
- Planning migration path from monolith to microservices
- Establishing module boundaries in existing code

### Effective Prompting

1. **Provide context:** Describe business domains and their relationships
2. **Specify tech stack:** Python/Django, Go, Java/Spring, etc.
3. **Define constraints:** Team size, deployment constraints, existing infrastructure
4. **Ask for trade-offs:** Request pros/cons of different approaches

### What LLMs Can Help With

- Identifying bounded contexts from requirements
- Designing module APIs and DTOs
- Creating event schemas
- Writing boundary enforcement tests
- Generating project scaffolding
- Reviewing module dependencies

## External Resources

### Official Documentation

- [Spring Modulith](https://spring.io/projects/spring-modulith/) - Official Spring framework for modular monoliths
- [import-linter](https://import-linter.readthedocs.io/) - Python architecture linter
- [ArchUnit](https://www.archunit.org/) - Java architecture testing

### Reference Implementations

- [modular-monolith-with-ddd](https://github.com/kgrzybek/modular-monolith-with-ddd) - Full .NET implementation by Kamil Grzybek
- [majestic-monolith-django](https://github.com/kokospapa8/majestic-monolith-django) - Django starter project
- [go-monolith-example](https://github.com/powerman/go-monolith-example) - Go monolith with Clean Architecture
- [spring-modulith-with-ddd](https://github.com/xsreality/spring-modulith-with-ddd) - Spring Boot + DDD example

### Articles & Guides

- [Modular Monolith Architecture](https://www.milanjovanovic.tech/modular-monolith-architecture) - Milan Jovanovic's comprehensive guide
- [Modular Monolith Integration Styles](https://www.kamilgrzybek.com/blog/posts/modular-monolith-integration-styles) - Communication patterns deep dive
- [Monolith vs Microservices in 2025](https://foojay.io/today/monolith-vs-microservices-2025/) - Current state of the debate
- [How Kraken Organizes Their Python Monolith](https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/) - Real-world case study

### Books

- "Fundamentals of Software Architecture" by Mark Richards & Neal Ford
- "Building Microservices" by Sam Newman (Ch. on monolith decomposition)
- "Domain-Driven Design" by Eric Evans (bounded contexts)
- "Monolith to Microservices" by Sam Newman

## Related Methodologies

| Methodology | Relationship |
|-------------|--------------|
| [monolith-architecture.md](../monolith-architecture.md) | Simpler starting point |
| [microservices-architecture/](../microservices-architecture/) | Next step when scaling |
| [event-driven-architecture/](../event-driven-architecture/) | Communication pattern |
| [architectural-patterns/](../architectural-patterns/) | Clean/Hexagonal within modules |
| [database-selection/](../database-selection/) | Choosing per-module databases |
