# Java Spring Boot Patterns

## Summary

**One-sentence:** Enterprise Spring Boot 3 patterns — BaseEntity (UUID PK + audit + @Version), record DTOs, MapStruct, @Transactional(readOnly=true) default, JpaSpecificationExecutor search, ProblemDetail errors, Actuator+Micrometer wired — plus a configuration-binding group (@ConfigurationProperties, @Validated, @ConditionalOnProperty, no System.getenv).

**One-paragraph:** Enterprise-grade Spring Boot 3.x layered architecture. A `BaseEntity` superclass provides a UUID `@Id`, `@CreationTimestamp`/`@UpdateTimestamp` audit columns, and `@Version` for optimistic locking. DTOs are Java records mapped via MapStruct; controllers never return entities. The service layer defaults to `@Transactional(readOnly = true)`; write methods override locally. Dynamic search endpoints use `JpaSpecificationExecutor` + `Pageable`. Global error handling via a single `@RestControllerAdvice` returning RFC 7807 `ProblemDetail`. Actuator endpoints + Micrometer metrics + OpenAPI/Swagger + Spring Security defaults are wired before the first endpoint ships. A second, clearly delimited concern covers how configuration reaches a bean: related properties bind to one `@ConfigurationProperties` record per concern, `@Validated` with Jakarta constraints so a bad value fails startup rather than the first request, optional beans wired by `@ConditionalOnProperty` / `@Profile` rather than runtime `if (env)` checks, and `System.getenv` banned outright. Those rules carry a `config-` id prefix.

**Ефективно для:**

- Greenfield Spring Boot 3.x service standing up the full enterprise toolbox (entity base class, audit, search, security, observability).
- Refactoring legacy Spring app onto records + MapStruct + ProblemDetail + `@Transactional` discipline.
- Adding dynamic search via Specifications + paginated results.
- Wiring Actuator, Micrometer, OpenAPI / Swagger, Spring Security defaults.
- Collapsing scattered `@Value` fields into typed, validated `@ConfigurationProperties` records.
- Replacing runtime `if (env.equals("prod"))` branches with `@Profile` / `@ConditionalOnProperty` bean wiring.

## Applies If (ALL must hold)

- Spring Boot 3.x on Java 17+, blocking (Servlet) stack.
- Multi-entity domain that benefits from a shared `BaseEntity` superclass.
- Need for dynamic search endpoints (`q=name~%foo%&status=ACTIVE&sort=-created`).

## Skip If (ANY kills it)

- Reactive stack (WebFlux) — patterns differ.
- Tiny CLI tools — Spring Boot startup is unjustified.
- Functions / serverless where cold start dominates — prefer Quarkus / Micronaut.
- Legacy Spring 4.x / Java 8 — records, sealed types, ProblemDetail, Jakarta namespace are not available.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Entity model | ERD or Markdown table | data modelling |
| Search filter contract | text / JSON | product / API design |
| Observability targets (Prometheus / OTel) | text | platform team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Sibling for the core layered shape. |
| [[java-jpa-hibernate]] | Persistence discipline (LAZY, business-key, migrations). |
| [[java-junit-testing]] | Test layering. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 rules — enterprise patterns: base-entity-uuid-audit-version, record-dtos-and-mapstruct, transactional-readonly-default, jpaspecificationexecutor-for-search, problemdetail-advice, actuator-and-micrometer; configuration binding: config-properties-typed, config-validation-on-properties, config-conditional-on-property, config-no-system-getenv | 1700 |
| `content/02-output-contract.xml` | essential | JSON Schema for the enterprise-service manifest, including the `configuration` block + valid/invalid examples | 1400 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns: lombok-data-on-entity, n-plus-one-after-controller, missing-version-token, custom-error-shape, no-readonly-default, config-value-blast, config-startup-misconfig, config-runtime-env-branch | 1300 |
| `content/04-procedure.xml` | essential | 6-step procedure: BaseEntity + audit → DTO + MapStruct → service Tx defaults → Specification + Pageable → Actuator + ProblemDetail → configuration binding | 1100 |
| `content/05-examples.xml` | essential | Worked mailer refactor: 8 @Value fields → one validated properties record, profile-wired beans, ProblemDetail replacing a leaking 500 | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `add-base-entity` | sonnet | Audit + version + UUID design choices. |
| `wire-search-with-specifications` | opus | Dynamic filter composition reasoning. |
| `audit-n-plus-one` | haiku | Mechanical scan via assertion script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/n-plus-one-assertion.java` | Test assertion enforcing query count budget on a list endpoint. |
| `templates/MailProperties.java` | Typed `@ConfigurationProperties` record with `@Validated` + Jakarta constraints. |
| `templates/GlobalExceptionHandler.java` | `@RestControllerAdvice` translating domain exceptions to `ProblemDetail`. |
| `templates/application-prod.yml` | Profile overlay binding the properties prefix + actuator exposure allow-list. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring-boot-patterns.py` | Validate the enterprise-service manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[java-spring-boot]]
- [[java-spring]]
- [[java-jpa-hibernate]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (domain richness, search shape, observability target) to a rule from `01-core-rules.xml`. Use it before standing up new service infrastructure.
