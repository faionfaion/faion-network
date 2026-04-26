# Java Spring Boot Backend

## Summary

Canonical layered architecture for Spring Boot 3.x: `@RestController` → `@Service` → `JpaRepository`. Covers CRUD endpoints with Bean Validation, MapStruct DTO mapping, `@Transactional` write methods, and `Pageable` list endpoints. This is the starter Spring Boot pattern; for richer search, Specifications, and ProblemDetail see `java-spring-boot-patterns/`.

## Why

The layered pattern separates HTTP concerns (controller), business logic (service), and persistence (repository). Without explicit DTO mapping, controllers leak entity internals (Hibernate proxies, lazy fields). Without `@Transactional` on writes, multi-step operations rely on auto-commit per JDBC call, leaving inconsistent state on partial failure.

## When To Use

- New Spring Boot 3.x service with standard CRUD endpoints.
- Adding endpoints with Bean Validation, MapStruct DTO mapping, and paginated list queries.
- Refactoring code that mixes controller/service/repository concerns or returns entity types to clients.
- Wiring BCrypt `PasswordEncoder` and paginated `Pageable` defaults in the service layer.

## When NOT To Use

- WebFlux/reactive stack — blocking JPA, `@Transactional`, and `ResponseEntity` semantics differ.
- Hexagonal/Clean Architecture with explicit ports/adapters — layering on top doubles up indirection.
- CQRS or event-sourced systems — service+JPA hides the command/query split.
- Quarkus, Micronaut, or serverless — annotations differ; pattern translates conceptually but not literally.

## Content

| File | What's inside |
|------|---------------|
| `content/01-controller-service.xml` | Controller + service layer patterns with ResponseEntity semantics, @Transactional defaults, and Pageable. |
| `content/02-entity-repository.xml` | JPA entity definition, JpaRepository with custom JPQL queries, and N+1 guard via JOIN FETCH. |
| `content/03-testing.xml` | @WebMvcTest controller tests and @ExtendWith(MockitoExtension) service unit tests. |
| `content/04-rules-and-gotchas.xml` | Mandatory rules and common AI-agent mistakes for Spring Boot layered pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/check.sh` | Pre-commit gate: compile + Spotless + block controllers returning entity types. |
