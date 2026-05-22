---
slug: integration-testing
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Integration tests catch the class of bugs that unit tests cannot: ORM query bugs, constraint violations, serialization mismatches between layers, and authentication middleware failures.
content_id: "5dcd59ab61d8b173"
tags: [integration-testing, testcontainers, database-testing, api-testing, mocking]
---
# Integration Testing

## Summary

**One-sentence:** Integration tests catch the class of bugs that unit tests cannot: ORM query bugs, constraint violations, serialization mismatches between layers, and authentication middleware failures.

**One-paragraph:** Integration tests catch the class of bugs that unit tests cannot: ORM query bugs, constraint violations, serialization mismatches between layers, and authentication middleware failures. This methodology covers test isolation strategies, database patterns with Testcontainers and pytest-django, FastAPI/Django API testing with dependency injection, and external service mocking with respx and WireMock.

## Applies If (ALL must hold)

- Database interactions (ORM, queries, transactions, constraints)
- API endpoints with real request/response validation
- Service-to-service communication contracts
- Authentication and authorization flows
- Message queue producers and consumers

## Skip If (ANY kills it)

- Testing a single pure function with no external calls — that is a unit test
- Testing a full user journey through the browser — that is E2E

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `free/dev/testing-developer/`
