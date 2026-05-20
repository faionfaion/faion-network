---
slug: java-spring
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Spring Boot 3.
content_id: "8a0a8ae87e66df63"
tags: [spring-boot, java, rest-api, layered-architecture, jpa]
---
# Java Spring (Layered Architecture)

## Summary

**One-sentence:** Spring Boot 3.

**One-paragraph:** Spring Boot 3.x layered architecture for REST APIs: @RestController → @Service → JpaRepository with Pageable, @Async with named executor beans, MapStruct DTO mapping, Bean Validation, and slice tests (@WebMvcTest, @DataJpaTest). Covers both the MVC/JPA stack and Spring Async patterns.

## Applies If (ALL must hold)

- Greenfield REST APIs in Spring Boot 3.x, Java 17+, using JPA/Hibernate and constructor injection.
- Adding async work via @Async with named ThreadPoolTaskExecutor beans per workload.
- Migration from Spring Boot 2.x / Java EE — the patterns translate cleanly.
- Full vertical slices: entity, repo, service, controller, mapper, DTOs, tests, Flyway migration in one diff.

## Skip If (ANY kills it)

- Reactive workloads — Spring WebFlux + R2DBC; servlet patterns deadlock in reactive context.
- Lightweight microservices where JVM boot time / memory footprint hurts — Quarkus, Micronaut.
- Functions/FaaS — cold start; use GraalVM native image with explicit config.
- CQRS/event-sourced systems — service+JPA pattern fights write/read separation.

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
