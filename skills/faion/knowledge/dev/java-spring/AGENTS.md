# Java Spring (Layered Architecture)

## Summary

**One-sentence:** Spring Boot 3.x layered architecture — thin @RestController → @Transactional @Service → narrow repository; record DTOs + Bean Validation; @Async via named executor; MapStruct DTOs.

**One-paragraph:** Spring Boot misuse — `@Transactional` on controllers, services returning JPA entities, `findAll()` without `Pageable`, `@Async` invoked via `this.foo()` (self-invocation), custom error envelopes — produces hard-to-reason-about apps. This methodology pins five rules: controllers are thin (no `@Transactional`, no repo access, no business logic); services own `@Transactional` boundaries; DTOs are records with Bean Validation; list endpoints accept `Pageable` and return `Page<T>`; `@Async` lives in a separate bean with a named executor. Output: layered feature spec (Controller + Service + DTOs + AsyncConfig) conforming to `02-output-contract.xml`.

**Ефективно для:**

- Spring Boot 3.x REST APIs with non-trivial domain.
- Async workflows (`@Async`) needing named, sized executors.
- DTO mapping via MapStruct with Lombok ordering pinned.
- Bean Validation + RFC 7807 `ProblemDetail` error model.
- Pageable list endpoints with deterministic ordering.

## Applies If (ALL must hold)

- Spring Boot 3.x + Java 17+ project.
- Layered architecture (Controller/Service/Repository) is the chosen style.
- MapStruct + Lombok are accepted in the build.
- The team agrees no `@Transactional` outside services.

## Skip If (ANY kills it)

- Reactive stack (WebFlux) — different patterns; apply WebFlux methodology.
- Plain SE / non-Spring app — apply the relevant framework's methodology.
- Single-package CRUD with no domain — Active Record is enough.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | Markdown | spec |
| Existing service layout | Maven/Gradle module | repo |
| Bean Validation rules | spec | spec |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-jpa-hibernate]] | Repository + transactional service patterns this layer consumes. |
| [[java-junit-testing]] | Test conventions for the layered tests. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: thin-controller, transactional-on-service-only, record-dtos-with-validation, pageable-list-endpoints, async-via-named-executor | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for layered feature spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: transactional-on-controller, async-self-invocation, service-returns-entity, custom-error-envelope | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on layer + concern → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-feature-package` | sonnet | Layered judgment. |
| `write-controller-service` | sonnet | Scaffolding within rules. |
| `wire-async-executor` | sonnet | Named bean + properties. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Controller.java` | Thin @RestController skeleton |
| `templates/Service.java` | @Transactional service skeleton |
| `templates/AsyncConfig.java` | Named ThreadPoolTaskExecutor + @Async |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring.py` | Validate layered feature spec | Pre-commit on spec artefact |

## Related

- [[java-jpa-hibernate]]
- [[java-junit-testing]]
- [[csharp-dotnet]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (layer, async need, error contract) to a rule from `01-core-rules.xml`. Use it whenever adding a new feature to a Spring Boot app.
