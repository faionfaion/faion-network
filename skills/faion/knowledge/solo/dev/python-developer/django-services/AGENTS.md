# Django Services Layer

## Summary

The service layer pattern separates business logic from Django models, views, and serializers into
dedicated functions with keyword-only arguments, typed signatures, and explicit transaction
boundaries. Services own write operations (CREATE/UPDATE/DELETE and external API calls); selectors
handle complex read queries. The canonical naming convention is `entity_action` (`order_create`,
`user_deactivate`). Every service that performs ≥2 writes must use `@transaction.atomic`.

## Why

Fat views and fat models accumulate untestable, unreusable logic. The service layer creates a
boundary where tests inject mock dependencies, multiple entry points (API, admin, CLI) call the
same function, and transaction safety is explicit rather than implicit. The HackSoft Django
Styleguide's empirical benchmark: services reduce view line-count by ~70% while enabling 90%+
branch coverage on business rules.

## When To Use

- Any CREATE/UPDATE/DELETE that touches ≥2 models or invokes an external API.
- Replacing fat-model methods that do email + payment + audit log in one blob.
- Wrapping side-effecting operations behind `@transaction.atomic` boundaries.
- Building a testable surface for business rules with no Django request/response in tests.
- Layering DRF: serializers validate input, views delegate to services, services own writes.

## When NOT To Use

- Simple property calculations — use `@property` on the model.
- Pure querysets / chained filters — use a custom manager.
- Read-only, permission-aware fetches — use a selector, not a service.
- Trivial single-model CRUD where a direct ORM call is clearer.

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Core rules: naming convention, keyword-only args, transaction boundaries, exception hierarchy. |
| `content/02-selectors.xml` | Selector pattern for complex reads: N+1 prevention, prefetch, aggregations. |
| `content/03-examples.xml` | Good/bad code comparisons: e-commerce order, user registration, dependency injection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/service.py` | Canonical service function skeleton with docstring, TYPE_CHECKING, @transaction.atomic. |
| `templates/selector.py` | Selector function skeleton with prefetch, query-count docstring. |
| `templates/exceptions.py` | Service exception hierarchy: ServiceError, ValidationError, NotFoundError, BusinessRuleError, ExternalServiceError. |
| `templates/factories.py` | Factory Boy factories for User, Order, Product, OrderItem. |
| `templates/prompt-service.txt` | LLM prompt template for generating a complete service. |
