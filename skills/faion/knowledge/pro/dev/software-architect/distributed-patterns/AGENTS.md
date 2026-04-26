# Distributed Patterns

## Summary

Patterns for data consistency, fault tolerance, and coordination in distributed systems. Covers Saga (choreography vs orchestration), CQRS, Event Sourcing, Outbox, 2PC vs Saga vs TCC trade-offs, Circuit Breaker, Bulkhead, Retry with jitter, Idempotency, Leader Election, and Rate Limiting algorithms.

## Why

Distributed systems cannot use database transactions across service boundaries. Each pattern addresses a specific class of failure: Saga handles long-running multi-service transactions with compensating actions; Outbox guarantees event publication without two-phase commits; Circuit Breaker prevents one failing dependency from cascading. Choosing the wrong pattern leads to data corruption (missing compensation) or unavailability (tight coordinator coupling).

## When To Use

- Designing a multi-service transaction that spans more than one database
- Implementing event publishing that must survive process crashes (Outbox)
- Adding resilience to service-to-service calls (Circuit Breaker + Retry + Bulkhead)
- Separating read and write models for a high read/write ratio domain (CQRS)
- Needing full audit trail or temporal queries (Event Sourcing)

## When NOT To Use

- Monolith or modular monolith — use local transactions instead; distributed patterns add complexity without benefit
- Simple CRUD service without external calls — Circuit Breaker/Bulkhead overhead is not justified
- Event Sourcing when the domain has no meaningful history requirement — storage cost is ~230% higher than snapshot-based
- 2PC for long-running processes — coordinator blocks resources; use Saga instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-data-consistency-patterns.xml` | Saga choreography vs orchestration, CQRS read/write split, Event Sourcing event store, Outbox pattern with CDC vs polling options |
| `content/02-transaction-and-fault-tolerance.xml` | 2PC vs Saga vs TCC comparison table, Circuit Breaker states and config, Bulkhead semaphore vs thread-pool, Retry with exponential backoff and jitter strategies |
| `content/03-idempotency-and-coordination.xml` | Idempotency key strategies, HTTP method idempotency, Leader Election algorithms (Raft, Redis SETNX), Rate Limiting algorithms comparison, pattern combination matrix |

## Templates

| File | Purpose |
|------|---------|
| `templates/saga-orchestrator.py` | Python saga orchestrator skeleton with compensating transaction registry |
| `templates/outbox-publisher.py` | Outbox polling publisher with at-least-once delivery and idempotency check |
