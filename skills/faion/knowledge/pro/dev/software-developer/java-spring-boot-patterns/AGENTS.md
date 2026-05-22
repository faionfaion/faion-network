---
slug: java-spring-boot-patterns
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-grade Spring Boot 3.
content_id: "0eeda30a3c35a8b3"
tags: [spring-boot, java, layered-architecture, jpa, rest-api]
---
# Java Spring Boot Patterns

## Summary

**One-sentence:** Production-grade Spring Boot 3.

**One-paragraph:** Production-grade Spring Boot 3.x layered architecture: entity → repository (JPA + Specification) → service (transactional) → controller (REST) → DTO/mapper (MapStruct). Enforces rich domain models, ProblemDetail error handling, UUID PKs, @Version optimistic locking, and Testcontainers-backed integration tests.

## Applies If (ALL must hold)

- Scaffolding a Spring Boot 3.x service (Java 17/21, Hibernate 6) from a domain spec
- Generating entity/repo/service/controller/DTO/mapper verticals
- Adding Spring Security (JWT, OAuth2) to an existing app
- Reviewing PRs for N+1, transaction-boundary violations, anemic domain antipatterns
- Migrating Boot 2.x → 3.x (Jakarta EE namespace, Hibernate 6, Spring Security 6)

## Skip If (ANY kills it)

- Reactive workloads — Spring WebFlux + R2DBC has different transaction semantics
- Lightweight microservices where JVM warmup and memory overhead hurt — consider Quarkus/Micronaut
- Functions/FaaS — cold start is unacceptable; use GraalVM native image with explicit config
- CQRS/event-sourced systems — JPA active-record pattern fights write/read separation

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

- parent skill: `pro/dev/software-developer/`
