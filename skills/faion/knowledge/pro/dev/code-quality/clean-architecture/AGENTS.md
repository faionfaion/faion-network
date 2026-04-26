# Clean Architecture

## Summary

Clean Architecture organizes code into four concentric layers — Entities, Use Cases, Interface Adapters, Frameworks — where dependencies point only inward. The concrete rule: nothing in `domain/` may import from `infrastructure/`, `application/`, or any framework (SQLAlchemy, FastAPI, Django). Violations make the domain untestable and couple business logic to deployment choices.

## Why

When domain entities depend on ORM models or HTTP frameworks, changing the database or web framework forces changes to business logic. Dependency inversion (domain defines the repository interface; infrastructure implements it) keeps business rules stable while infrastructure is swappable. This also enables pure unit tests of business logic without a running database.

## When To Use

- Complex business logic that must survive infrastructure changes (DB migration, framework upgrade)
- Long-lived enterprise system where testability and onboarding speed justify the layer overhead
- Domain-Driven Design projects — Clean Architecture layers map directly to DDD layers
- Applications that may need to run in multiple delivery mechanisms (REST API + CLI + event handler)
- Teams that need to enforce layer boundaries via architecture tests (import-linter, ArchUnit)

## When NOT To Use

- CRUD apps with trivial logic — four layers for a `GET /users` endpoint is over-engineering
- Rapid prototypes where the goal is feature exploration, not stability
- Teams not willing to enforce the dependency rule via tests — without enforcement it degrades into a layered monolith with import cycles
- Small scripts or ETL jobs where a single file is appropriate

## Content

| File | What's inside |
|------|---------------|
| `content/01-layer-rules.xml` | Dependency rule, layer definitions, forbidden import directions, folder layout |
| `content/02-domain-layer.xml` | User entity, Email value object, UserRepository interface, domain events |
| `content/03-application-layer.xml` | CreateUserUseCase, GetUserUseCase, UnitOfWork interface, UserDTO |
| `content/04-infrastructure-layer.xml` | SQLAlchemyUserRepository, SQLAlchemyUnitOfWork, ORM model mapping |
| `content/05-antipatterns.xml` | Domain logic in controller, ORM in domain entity — bad/good examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/use-case.py` | Use case skeleton with Input/Output dataclasses and dependency injection |
| `templates/repository-interface.py` | Abstract repository interface for a domain entity |
| `templates/import-linter.ini` | import-linter contracts enforcing layer dependency rules |
