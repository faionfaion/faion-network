---
slug: java-spring-boot-patterns
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Enterprise Spring Boot 3 patterns — BaseEntity (UUID PK + audit + @Version), record DTOs, MapStruct, @Transactional(readOnly=true) default, JpaSpecificationExecutor search, ProblemDetail errors, Actuator+Micrometer wired.
content_id: "4d2a57c8a756e624"
complexity: deep
produces: code
est_tokens: 4400
tags: [java, spring-boot, enterprise, jpa, patterns]
---
# Java Spring Boot Patterns

## Summary

**One-sentence:** Enterprise Spring Boot 3 patterns — BaseEntity (UUID PK + audit + @Version), record DTOs, MapStruct, @Transactional(readOnly=true) default, JpaSpecificationExecutor search, ProblemDetail errors, Actuator+Micrometer wired.

**One-paragraph:** Enterprise-grade Spring Boot 3.x layered architecture. A `BaseEntity` superclass provides a UUID `@Id`, `@CreationTimestamp`/`@UpdateTimestamp` audit columns, and `@Version` for optimistic locking. DTOs are Java records mapped via MapStruct; controllers never return entities. The service layer defaults to `@Transactional(readOnly = true)`; write methods override locally. Dynamic search endpoints use `JpaSpecificationExecutor` + `Pageable`. Global error handling via a single `@RestControllerAdvice` returning RFC 7807 `ProblemDetail`. Actuator endpoints + Micrometer metrics + OpenAPI/Swagger + Spring Security defaults are wired before the first endpoint ships.

**Ефективно для:**

- Greenfield Spring Boot 3.x service standing up the full enterprise toolbox (entity base class, audit, search, security, observability).
- Refactoring legacy Spring app onto records + MapStruct + ProblemDetail + `@Transactional` discipline.
- Adding dynamic search via Specifications + paginated results.
- Wiring Actuator, Micrometer, OpenAPI / Swagger, Spring Security defaults.

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

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Sibling for the core layered shape. |
| [[java-jpa-hibernate]] | Persistence discipline (LAZY, business-key, migrations). |
| [[java-junit-testing]] | Test layering. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: base-entity-uuid-audit-version, record-dtos-and-mapstruct, transactional-readonly-default, jpaspecificationexecutor-for-search, problemdetail-advice, actuator-and-micrometer | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the enterprise-service manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: lombok-data-on-entity, n-plus-one-after-controller, missing-version-token, custom-error-shape, no-readonly-default | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: BaseEntity + audit → DTO + MapStruct → service Tx defaults → Specification + Pageable → Actuator + ProblemDetail | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring-boot-patterns.py` | Validate the enterprise-service manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[java-spring-boot]]
- [[java-spring]]
- [[java-jpa-hibernate]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (domain richness, search shape, observability target) to a rule from `01-core-rules.xml`. Use it before standing up new service infrastructure.
