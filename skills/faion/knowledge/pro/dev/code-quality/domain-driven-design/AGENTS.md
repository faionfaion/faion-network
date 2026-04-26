# Domain-Driven Design

## Summary

Domain-Driven Design (DDD) is a software development approach that models complex business domains through a shared ubiquitous language, explicit bounded contexts, and rich domain objects (entities, value objects, aggregates) that enforce business invariants. The core rule: domain logic lives inside the model, not in services — an `Order` that cannot be placed when empty is safer than a service that checks emptiness before calling `order.place()`.

## Why

Without DDD, business rules scatter across controllers, services, and database queries, creating the anemic domain model antipattern where the same invariant is enforced in multiple places and breaks silently when one copy is missed. DDD solves this by making the domain model the single authority for business rules, with bounded contexts preventing model pollution across team boundaries.

## When To Use

- Complex business domain where rules will keep changing (orders, billing, inventory, claims, pricing)
- Splitting a monolith — DDD bounded contexts define service boundaries before you draw service lines
- Refactoring an anemic codebase where logic has leaked into controllers/services
- A team includes a domain expert who can sit in modeling sessions
- Multiple teams share a codebase and need explicit context maps to negotiate ownership

## When NOT To Use

- CRUD admin tools, reporting dashboards, or scrapers — the "domain" is just data; DDD adds ceremony with no payoff
- Solo prototype or MVP under ~2k LOC where requirements still flip weekly
- Hot data-pipeline / ETL code — the model is rows and transformations, not aggregates with invariants
- Real-time / latency-critical paths where repository hydration and event dispatch cost is not justified
- Team has no access to a domain expert — you will produce a developer-invented model the business does not recognize

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-patterns.xml` | Entities, value objects, aggregates, domain services, bounded contexts — rules and antipatterns |
| `content/02-examples.xml` | Order aggregate, Money/Address value objects, domain events, anti-corruption layer, repository pattern |

## Templates

| File | Purpose |
|------|---------|
| `templates/domain-purity-check.sh` | Pre-commit script: fails if domain/ imports infrastructure libs |
| `templates/import-linter.ini` | import-linter contract: domain layer must not import infrastructure |
| `templates/ddd-prompt.txt` | LLM prompt pattern for aggregate modeling with ubiquitous language |
