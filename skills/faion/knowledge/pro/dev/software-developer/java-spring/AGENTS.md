# Java Spring (Layered Architecture)

## Summary

Spring Boot 3.x layered architecture for REST APIs: `@RestController` → `@Service` → `JpaRepository` with Pageable, `@Async` with named executor beans, MapStruct DTO mapping, Bean Validation, and slice tests (`@WebMvcTest`, `@DataJpaTest`). Covers both the MVC/JPA stack and Spring Async patterns.

## Why

The layered pattern is the dominant Spring Boot idiom, but it produces subtle runtime bugs — lazy-load exceptions after transaction close, `@Async` swallowing exceptions in `void` returns, `@Transactional` on self-invoked methods doing nothing (proxy bypass), and `findAll()` without Pageable OOMing prod. This methodology encodes the guardrails so agents produce correct, production-safe code on the first pass.

## When To Use

- Greenfield REST APIs in Spring Boot 3.x, Java 17+, using JPA/Hibernate and constructor injection
- Adding async work via `@Async` with named `ThreadPoolTaskExecutor` beans per workload
- Migration from Spring Boot 2.x / Java EE — the patterns translate cleanly
- Full vertical slices: entity, repo, service, controller, mapper, DTOs, tests, Flyway migration in one diff

## When NOT To Use

- Reactive workloads — Spring WebFlux + R2DBC; servlet patterns deadlock in reactive context
- Lightweight microservices where JVM boot time / memory footprint hurts — Quarkus, Micronaut
- Functions/FaaS — cold start; use GraalVM native image with explicit config
- CQRS/event-sourced systems — service+JPA pattern fights write/read separation

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture.xml` | Layered structure, entity/repo/service/controller rules, transaction and fetch strategy |
| `content/02-async.xml` | @Async configuration, named executor beans, CompletableFuture return types, gotchas |
| `content/03-examples.xml` | Controller, service, entity, repository, WebMvcTest, service unit test examples and antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/maven-annotation-processors.xml` | Maven compiler plugin snippet for Lombok + MapStruct in correct dependency order |
| `templates/prompt-vertical-slice.txt` | Subagent prompt for generating a full 7-file vertical slice |
