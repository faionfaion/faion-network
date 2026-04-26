# Java Spring Boot Patterns

## Summary

Production-grade Spring Boot 3.x layered architecture: entity → repository (JPA + Specification) → service (transactional) → controller (REST) → DTO/mapper (MapStruct). Enforces rich domain models, ProblemDetail error handling, UUID PKs, `@Version` optimistic locking, and Testcontainers-backed integration tests.

## Why

Spring Boot's opinionated defaults and convention-over-configuration eliminate boilerplate, but the layered pattern still breaks down without discipline: N+1 queries, anemic domain models, wrong `@Transactional` placement, and mixed Jakarta/Javax namespaces are the top failure modes. This methodology encodes the concrete guardrails — fetch-LAZY everywhere, service-layer transactions only, DTOs as records, ProblemDetail for errors — so the agent doesn't reinvent them.

## When To Use

- Scaffolding a Spring Boot 3.x service (Java 17/21, Hibernate 6) from a domain spec
- Generating entity/repo/service/controller/DTO/mapper verticals
- Adding Spring Security (JWT, OAuth2) to an existing app
- Reviewing PRs for N+1, transaction-boundary violations, anemic domain antipatterns
- Migrating Boot 2.x → 3.x (Jakarta EE namespace, Hibernate 6, Spring Security 6)

## When NOT To Use

- Reactive workloads — Spring WebFlux + R2DBC has different transaction semantics
- Lightweight microservices where JVM warmup and memory overhead hurt — consider Quarkus/Micronaut
- Functions/FaaS — cold start is unacceptable; use GraalVM native image with explicit config
- CQRS/event-sourced systems — JPA active-record pattern fights write/read separation

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture.xml` | Layered structure rules, project layout, entity/repo/service/controller boundaries |
| `content/02-rules.xml` | Transaction placement, fetch strategy, DTO mapping, error handling, LLM gotchas |
| `content/03-examples.xml` | Entity, repository, service, controller, mapper, DTO code examples and antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/springboot-pr-gate.sh` | CI gate script: verify, test, jacoco, ban @Transactional in controllers, enforce LAZY fetch |
| `templates/prompt-domain-coder.txt` | Subagent prompt template for generating entity/repo/spec layers |
| `templates/prompt-springsec-reviewer.txt` | Subagent prompt for Spring Security audit |
