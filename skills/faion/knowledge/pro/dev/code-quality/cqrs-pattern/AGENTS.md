# CQRS Pattern

## Summary

Command Query Responsibility Segregation (CQRS) separates read and write operations into distinct models: commands change state and return void or an ID; queries return data and never modify state. The concrete rule: a handler class is either a `CommandHandler` (returns `None` or ID) or a `QueryHandler` (returns a read model) — never both.

## Why

When a single model serves both reads and writes, optimizing one side degrades the other — a normalized write model forces expensive joins for reads, while a denormalized read model complicates write-side validation. CQRS allows each side to evolve independently: write side uses the domain model with full invariant enforcement; read side uses flat projections optimized for query patterns (Redis, Elasticsearch, denormalized SQL views).

## When To Use

- High read/write ratio where each side has different optimization requirements
- Complex domain with separate read models needed per use case
- Systems requiring audit trails where events drive read model projections
- Applications with eventual consistency requirements (microservices, event-driven)
- Paired with event sourcing where projections rebuild from the event log

## When NOT To Use

- Simple CRUD apps — the two-model overhead exceeds benefit when reads and writes are symmetric
- Teams unfamiliar with eventual consistency — stale reads cause correctness bugs if the team does not design for them
- Systems that need immediate read-after-write consistency and cannot tolerate any lag
- Small domains where a single repository and DTO cover all query needs without duplication

## Content

| File | What's inside |
|------|---------------|
| `content/01-command-side.xml` | Command/CommandHandler base classes, PlaceOrderCommand, CancelOrderCommand, Mediator dispatch |
| `content/02-query-side.xml` | Query/QueryHandler base classes, read model DTOs, ListOrdersHandler with Redis read store |
| `content/03-projections.xml` | OrderProjection building read model from domain events, Redis read store implementation |
| `content/04-antipatterns.xml` | Commands returning data, queries with side effects — bad/good examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/command-handler.py` | Base Command + CommandHandler + PlaceOrderCommand skeleton |
| `templates/query-handler.py` | Base Query + QueryHandler + OrderDto read model skeleton |
| `templates/mediator.py` | Mediator for dispatching commands and queries by type |
