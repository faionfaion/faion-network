# Integration Testing

Patterns for testing multiple components against real dependencies — databases, APIs, message queues, external services. Covers test isolation strategies (transaction rollback, Testcontainers), FastAPI/Django API testing, and external service mocking with respx/WireMock.

## Why

Integration tests catch the class of bugs that unit tests cannot: ORM query bugs, constraint violations, serialization mismatches between layers, and authentication middleware failures. Without them, these bugs reach production.

## When To Use

- Database interactions (ORM, queries, transactions, constraints)
- API endpoints with real request/response validation
- Service-to-service communication contracts
- Authentication and authorization flows
- Message queue producers and consumers

## When NOT To Use

- Testing a single pure function with no external calls — that is a unit test
- Testing a full user journey through the browser — that is E2E

## Content

| File | What's inside |
|------|---------------|
| `content/01-isolation.xml` | Four isolation strategies (transaction rollback, truncate, Testcontainers, unique IDs), trade-off table |
| `content/02-database.xml` | SQLAlchemy + Testcontainers conftest pattern, pytest-django marks, Factory Boy |
| `content/03-api.xml` | FastAPI TestClient (sync) and AsyncClient (async) with dependency override pattern |
| `content/04-external.xml` | respx for httpx mocking, WireMock via Testcontainers for outbound HTTP, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/conftest_postgres.py` | Session-scoped Postgres container + function-scoped transaction rollback session |
| `templates/conftest_django.py` | Django conftest with Factory Boy UserFactory and admin_user fixture |
| `templates/fastapi_client.py` | FastAPI TestClient and AsyncClient fixtures with dependency override |
