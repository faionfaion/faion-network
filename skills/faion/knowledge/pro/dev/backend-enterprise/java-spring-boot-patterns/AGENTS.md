---
slug: java-spring-boot-patterns
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Layered Spring Boot 3.
content_id: "0eeda30a3c35a8b3"
tags: [java, spring-boot, enterprise, jpa, patterns]
---
# Java Spring Boot Patterns

## Summary

**One-sentence:** Layered Spring Boot 3.

**One-paragraph:** Layered Spring Boot 3.x architecture with BaseEntity providing UUID primary key, auditing via @CreationTimestamp/@UpdateTimestamp, optimistic locking via @Version, and entities extending this superclass. DTOs as Java records. MapStruct mappers for entity conversion. @Transactional(readOnly = true) as class-level default, @Transactional on write methods. @RestControllerAdvice returning ProblemDetail (RFC 7807). Never expose entities directly from controllers. Prevent N+1 queries with JOIN FETCH or @EntityGraph.

## Applies If (ALL must hold)

- Greenfield Spring Boot 3.x service following the layered architecture (controller → service → repository) with JPA/Hibernate.
- Refactoring a legacy Spring app to use records for DTOs, MapStruct mappers, @Transactional(readOnly = true) defaults, and ProblemDetail exception handling.
- Adding @RestControllerAdvice global exception handlers and Bean Validation (@Valid, @NotBlank).
- Wiring Specifications (JpaSpecificationExecutor) for dynamic search endpoints and pageable results.
- Standing up Actuator, Micrometer, OpenAPI/Swagger, and Spring Security defaults.

## Skip If (ANY kills it)

- Reactive stack (WebFlux) — patterns like blocking JPA repos, @Transactional, and ResponseEntity semantics differ; use a reactive-specific knowledge base.
- Tiny CLI tools — Spring Boot's startup cost and DI overhead are unjustified.
- Functions/serverless deployments where cold start matters; prefer Quarkus or Micronaut.
- Legacy Spring 4.x / Java 8 — record types, sealed types, ProblemDetail, and Jakarta namespace are not available.

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

- parent skill: `pro/dev/backend-enterprise/`
