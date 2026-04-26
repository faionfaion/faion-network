# Microservices Design

## Summary

Microservices architecture structures an application as independently deployable services where each service owns its data, exposes a well-defined API, and communicates through HTTP or async messaging. The core rules: each service has exactly one database (no shared tables); services never import each other's code directly; failures in one service must not cascade to others.

## Why

A monolith scales as a unit even when only one feature is under load, and deploys as a unit even when only one team is ready. Microservices allow each team to deploy independently and scale individual services to their actual demand. The organizational alignment (Conway's Law) is as important as the technical benefit: services mirror team boundaries, reducing cross-team coordination overhead.

## When To Use

- Large application where multiple teams work on different features simultaneously
- Systems requiring independent scaling (checkout scales at 10x normal during flash sales; user service does not)
- Organizations practicing continuous deployment where lockstep releases are a bottleneck
- Technology diversity is justified (ML service in Python, billing in Java, web frontend in Node)
- High availability requirement where a single service failure must not take down the whole product

## When NOT To Use

- Single team or early-stage startup — operational overhead (observability, CI/CD per service, networking) exceeds benefit
- Domain not yet stable — premature service boundaries become costly to re-draw as the model evolves
- Team lacks experience with distributed systems — eventual consistency, network failures, and distributed tracing require operational maturity
- Transactions must be ACID across multiple business entities — sagas add significant complexity compared to a monolith with a single DB
- Tight latency budget — each service hop adds network round-trip time

## Content

| File | What's inside |
|------|---------------|
| `content/01-service-structure.xml` | Folder layout, FastAPI service skeleton, health check, lifespan pattern |
| `content/02-communication.xml` | Sync HTTP client, async message publish/consume with aio_pika, service discovery |
| `content/03-resilience.xml` | Circuit breaker implementation (CLOSED/OPEN/HALF_OPEN), resilient client usage |
| `content/04-sagas.xml` | Orchestration-based saga with compensation, SagaState enum |
| `content/05-antipatterns.xml` | Distributed monolith via sync calls, shared database — bad/good examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/service-main.py` | FastAPI service entrypoint with lifespan, health router, versioned API |
| `templates/circuit-breaker.py` | CircuitBreaker class ready to wrap any async callable |
| `templates/message-bus.py` | MessagePublisher + MessageConsumer with aio_pika and JSON encoding |
