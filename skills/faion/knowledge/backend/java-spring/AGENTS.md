# Java Spring Boot Backend

## Summary

**One-sentence:** Canonical layered Spring Boot 3 architecture — @RestController → @Service → JpaRepository, Bean Validation, MapStruct DTOs, @Transactional writes, Pageable lists, BCrypt password hashing.

**One-paragraph:** Canonical layered architecture for Spring Boot 3.x: `@RestController` validates input via Bean Validation, delegates to `@Service`, which calls `JpaRepository`. Controllers return record-based DTOs (never entities). Write methods are `@Transactional`; list endpoints accept `Pageable`; passwords are hashed via `PasswordEncoder` (BCrypt) inside the service. MapStruct generates DTO ↔ entity mappers via the annotation processor. Spring Boot 3 means `jakarta.*` imports throughout. This is the starter Spring Boot pattern; for richer search (Specifications) and CQRS see related methodologies.

**Ефективно для:**

- New Spring Boot 3.x service with standard CRUD endpoints.
- Adding endpoints with Bean Validation, MapStruct DTO mapping, and paginated list queries.
- Refactoring code that mixes controller/service/repository concerns or returns entity types to clients.
- Wiring BCrypt `PasswordEncoder` and `Pageable` defaults in the service layer.

## Applies If (ALL must hold)

- New Spring Boot 3.x service with standard CRUD endpoints.
- Standard JPA persistence (Hibernate) with `JpaRepository`.
- Java 17+ codebase with record support.

## Skip If (ANY kills it)

- WebFlux / reactive stack — blocking JPA, `@Transactional`, and `ResponseEntity` semantics differ.
- Hexagonal / Clean Architecture with explicit ports/adapters — layering on top doubles up indirection.
- CQRS or event-sourced systems — service + JPA hides the command/query split.
- Quarkus / Micronaut / serverless — annotations differ; pattern translates conceptually but not literally.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| API contract | OpenAPI YAML or Markdown | product / API design |
| Entity model | ERD or Markdown table | data modelling |
| Target Spring Boot version | `3.x` | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Sibling for richer enterprise-grade patterns. |
| [[java-jpa-hibernate]] | Repository layer discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 rules: dto-record-never-entity, transactional-on-writes, pageable-on-list, bcrypt-in-service, mapstruct-annotation-processor, jakarta-not-javax, thin-controller, transactional-on-service-only, record-dtos-with-validation, async-via-named-executor | 1700 |
| `content/02-output-contract.xml` | essential | JSON Schema for the service-scaffold manifest (+ optional controller / DTO / async / ProblemDetail blocks) + valid/invalid examples | 1400 |
| `content/03-failure-modes.xml` | essential | 10 antipatterns: entity-leak-via-jsonignore, missing-transactional, unbounded-findall, mapstruct-missing-from-pom, jakarta-vs-javax-mix, transactional-self-invocation, transactional-on-controller, fat-controller-with-repository, async-self-invocation, custom-error-envelope | 1400 |
| `content/04-procedure.xml` | essential | 5-step procedure: thin controller + validated record DTOs → service → repository → DTO + mapper → ProblemDetail advice, async config and tests | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-crud-endpoint` | sonnet | Layered code generation with judgment on validation. |
| `wire-mapstruct-mapper` | sonnet | Mapper interface design. |
| `audit-transactional-discipline` | haiku | Mechanical scan for missing `@Transactional` on writes. |
| `audit-controller-thinness` | haiku | Mechanical scan for `@Transactional` / repository autowiring in controllers. |
| `design-async-executor` | sonnet | Pool sizing + bean extraction for `@Async`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/check.sh` | CI script verifying jakarta imports + MapStruct annotation processor + @Transactional on writes. |
| `templates/Controller.java` | Thin @RestController skeleton per `thin-controller`. |
| `templates/Service.java` | @Transactional service skeleton returning DTOs only. |
| `templates/AsyncConfig.java` | Named ThreadPoolTaskExecutor + @Async target bean. |
| `templates/maven-annotation-processors.xml` | pom.xml `annotationProcessorPaths` block with Lombok + MapStruct in the required order. |
| `templates/prompt-vertical-slice.txt` | Codegen prompt for a full vertical slice of this pattern. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring.py` | Validate the service-scaffold manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[java-spring-boot]]
- [[java-jpa-hibernate]]
- [[java-junit-testing]]
- [[java-spring-async]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (Spring stack, endpoint shape, architecture style) to a rule from `01-core-rules.xml`. Use it before scaffolding a new endpoint or wiring DTO mapping.
