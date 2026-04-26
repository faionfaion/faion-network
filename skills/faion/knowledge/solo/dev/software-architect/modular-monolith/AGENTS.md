# Modular Monolith

## Summary

A modular monolith is a single deployable unit with strict module boundaries: each module maps to one bounded context, exposes only a public API, owns its database schema, and never directly imports internals of another module. Boundary enforcement is mandatory via static analysis (import-linter, ArchUnit, depguard) wired into CI — without it, boundaries decay within weeks.

## Why

Microservices overhead (distributed tracing, network failures, polyglot ops) is only justified when modules need independent scaling, independent deployment, or polyglot stacks. Until those needs are real, a modular monolith provides the same domain isolation with in-process calls, ACID transactions, and a single deploy. It is also the safest migration path: well-isolated modules extract to services via the Strangler Fig pattern.

## When To Use

- New project: team size ≤ 10, business model not fully validated
- Refactoring a "big ball of mud" monolith — module boundaries first, extraction later
- Needing DDD bounded contexts without distributed-systems complexity
- Planning future microservices extraction (modular monolith is the required prior step)
- Establishing schema-per-module isolation on a shared PostgreSQL instance
- Adding import-boundary linting as a CI gate to an existing codebase

## When NOT To Use

- Independent scaling per module is already needed (traffic profiles differ by 10x+) — use microservices
- Multiple teams (10+) with independent release cadences requiring autonomous deploys
- Polyglot tech stacks required per domain (different languages/runtimes)
- Regulatory or fault-isolation requirements demand hard process separation
- Throwaway prototype where module ceremony adds no value
- Existing monolith already has clean package structure and passing tests — don't add ceremony

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Core rules: module = bounded context, public API only, no shared models, data isolation, no cross-schema joins |
| `content/02-communication.xml` | Sync (direct call) vs async (events) patterns, when to choose each, trade-offs |
| `content/03-migration.xml` | Monolith → modular monolith steps; modular monolith → microservices via Strangler Fig; data extraction rule |
| `content/04-enforcement.xml` | Boundary enforcement tools per language: import-linter (Python), ArchUnit/Spring Modulith (Java), depguard (Go) |

## Templates

| File | Purpose |
|------|---------|
| `templates/module-api.py` | Python module public API: OrderService Protocol, DTOs, exceptions |
| `templates/domain-events.py` | Python domain events: DomainEvent base, OrderCreatedEvent, OrderCompletedEvent |
| `templates/importlinter.ini` | import-linter contract enforcing module independence and layer ordering |
| `templates/schema-isolation.sql` | PostgreSQL schema-per-module DDL with cross-module reference-by-ID pattern |
