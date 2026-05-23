# JPA / Hibernate Patterns

## Summary

**One-sentence:** Spring Data JPA + Hibernate methodology — LAZY by default, business-key equality, expand-contract migrations, @DataJpaTest slices, OSIV off, DTO projections in controllers.

**One-paragraph:** Production-grade JPA / Hibernate for Spring Boot 3 services. Entity associations are LAZY by default; eager loading is per-query via `JOIN FETCH` or `@EntityGraph`. `equals` / `hashCode` are implemented over a business key (never Lombok `@Data` on entities). Migrations are versioned with Flyway; every entity diff lands with a paired migration. Bulk modifying queries use `@Modifying(clearAutomatically = true)`. Tests use `@DataJpaTest` + Testcontainers; controllers return DTO projections rather than entities to avoid `LazyInitializationException` once OSIV is disabled.

**Ефективно для:**

- Greenfield Spring Boot 3 services using Spring Data JPA + Hibernate 6.
- Migrating from `FetchType.EAGER` defaults that produce Cartesian explosions under load.
- Hardening test suites that mistakenly use `@SpringBootTest` for repository slices.
- Locking schema-change discipline with Flyway expand-contract migrations.

## Applies If (ALL must hold)

- Java 17+ service running Spring Boot 3 with Spring Data JPA and Hibernate 6.
- Entity model with ≥3 aggregate roots and non-trivial associations.
- Production deployment that requires zero-downtime schema migrations.

## Skip If (ANY kills it)

- Read-only reporting layer — use Spring Data JDBC or jOOQ; JPA change tracking is overhead.
- Hot-path microservice under sub-ms latency requirements — JPA proxy + first-level cache cost dominates.
- Schema-less / event-store services — JPA's relational assumptions fight the grain.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Domain entity model | Java classes or ERD | domain modelling |
| Migration policy | Flyway expand-contract checklist | DBA / SRE |
| Testcontainers DB image | Docker image name | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Sub-module for service / controller layering. |
| [[java-junit-testing]] | Test layering that drives `@DataJpaTest` vs `@SpringBootTest`. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: lazy-by-default, business-key-equality, flyway-migration-per-entity-change, modifying-clearautomatically, datajpatest-for-repositories, dto-projection-in-controllers | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the JPA-layer manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: lombok-data-on-entities, eager-fetch-default, cascade-all-on-manytoone, missing-migration, modifying-without-clear, springboottest-for-slice | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: entity modelling → repository slice → migration → bulk op safety → test slice | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-entity` | sonnet | Translating domain to JPA mappings requires judgment. |
| `generate-migration` | sonnet | Expand-contract reasoning. |
| `audit-fetch-strategy` | haiku | Mechanical scan for EAGER fetches. |
| `design-bulk-operation` | opus | L1 cache + clearAutomatically reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity.java` | Entity skeleton with LAZY associations + business-key equals/hashCode. |
| `templates/repository.java` | Spring Data JPA repository with @Modifying + clearAutomatically. |
| `templates/application-test.yml` | `@DataJpaTest` configuration with Testcontainers DB. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-jpa-hibernate.py` | Validate the JPA-layer manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[java-spring-boot]]
- [[java-junit-testing]]
- [[java-spring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (read vs write path, fetch strategy, test layer) to a rule from `01-core-rules.xml`. Use it before scaffolding a new entity or refactoring a hot query.
