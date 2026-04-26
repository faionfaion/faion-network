# Java Spring Boot Patterns

## Summary

Layered Spring Boot 3.x architecture: controller → service interface + impl → repository (JPA + Specifications) → entity extending `BaseEntity`. DTOs as Java records. MapStruct mappers. `@Transactional(readOnly = true)` as class-level default, `@Transactional` on write methods. `@RestControllerAdvice` returning `ProblemDetail` (RFC 7807). Never expose entities directly from controllers.

## Why

Spring Boot 3 changed namespaces from `javax.*` to `jakarta.*` and LLMs trained on older corpora mix them. The most frequent agent failures are anemic domain models (all logic in services, entities as data bags), N+1 queries from missing `JOIN FETCH` or `@EntityGraph`, and `@Transactional` on private methods or self-invocation (which silently does nothing). ArchUnit and Testcontainers enforce the layering and catch N+1 in CI.

## When To Use

- Greenfield Spring Boot 3.x service with layered architecture and JPA/Hibernate.
- Refactoring legacy Spring app to records, MapStruct, `ProblemDetail`, and `@Transactional(readOnly=true)` defaults.
- Adding `@RestControllerAdvice` global exception handlers and Bean Validation.
- Wiring `JpaSpecificationExecutor` for dynamic search endpoints and pageable results.

## When NOT To Use

- Reactive stack (`WebFlux`) — blocking JPA repos and `@Transactional` semantics differ.
- Tiny CLI tools — Spring Boot startup cost and DI overhead are unjustified.
- Serverless/functions where cold start matters (prefer Quarkus or Micronaut).
- Legacy Spring 4.x / Java 8 — records, sealed types, `ProblemDetail`, and Jakarta namespace unavailable.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure-and-entities.xml` | Project layout, `BaseEntity`, `User` entity with JPA annotations, `UserRole` enum. |
| `content/02-repository-and-service.xml` | `JpaRepository` + `JpaSpecificationExecutor`, `Specification` factory, `UserServiceImpl` with `@Transactional`. |
| `content/03-controller-and-dtos.xml` | `UserController`, DTO records, `UserMapper` with MapStruct. |
| `content/04-exception-handling.xml` | `GlobalExceptionHandler` with `ProblemDetail`, validation errors, antipatterns (N+1, anemic model, entity leaks). |

## Templates

| File | Purpose |
|------|---------|
| `templates/n-plus-one-assertion.java` | Test helper detecting N+1 via Hibernate `Statistics` per-method. |
