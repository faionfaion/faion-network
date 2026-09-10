# JPA / Hibernate Patterns

## Summary

**One-sentence:** Spring Data JPA + Hibernate methodology — LAZY by default, business-key equality, expand-contract migrations, @DataJpaTest slices, OSIV off, DTO projections in controllers.

**One-paragraph:** Production-grade JPA / Hibernate for Spring Boot 3 services. Entity associations are LAZY by default; eager loading is per-query via `JOIN FETCH` or `@EntityGraph`. `equals` / `hashCode` are implemented over a business key (never Lombok `@Data` on entities). Every entity carries audit timestamps, and user-editable aggregates carry `@Version`; every cascade / `orphanRemoval` / fetch choice carries a written justification. Migrations are versioned with Flyway; every entity diff lands with a paired migration. Bulk modifying queries use `@Modifying(clearAutomatically = true)`. Services consume narrow repository interfaces — never raw `JpaRepository` — and own the transaction boundary (`readOnly = true` on reads). Tests use `@DataJpaTest` + Testcontainers; reads project to DTOs and controllers return DTO projections rather than entities, so `LazyInitializationException` cannot fire once OSIV is disabled.

**Ефективно для:**

- Greenfield Spring Boot 3 services using Spring Data JPA + Hibernate 6.
- Migrating from `FetchType.EAGER` defaults that produce Cartesian explosions under load.
- Hardening test suites that mistakenly use `@SpringBootTest` for repository slices.
- Locking schema-change discipline with Flyway expand-contract migrations.
- High-throughput read paths that need DTO projection instead of entity hydration.
- Inventory / balance domains requiring optimistic or pessimistic locking.
- Teams that have suffered N+1 or open-in-view incidents.
- AI-generated code that defaults to `CascadeType.ALL` on every relation.

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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Sub-module for service / controller layering. |
| [[java-junit-testing]] | Test layering that drives `@DataJpaTest` vs `@SpringBootTest`. |
| [[ddd-repositories]] | Narrow-repository pattern the `narrow-repo-interface` rule builds on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 rules: lazy-by-default, business-key-equality, flyway-migration-per-entity-change, modifying-clearautomatically, datajpatest-for-repositories, dto-projection-in-controllers, audit-timestamps, justified-cascade-fetch, optimistic-locking-on-editable-aggregates, narrow-repo-interface, dto-projection-on-reads, service-owns-transaction-boundary | 2000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the JPA-layer manifest (+ optional narrow-repository / service spec) + valid/invalid examples | 1200 |
| `content/03-failure-modes.xml` | essential | 15 antipatterns: lombok-data-on-entities, id-based-equality, eager-fetch-default, cascade-all-on-manytoone, missing-migration, modifying-without-clear, springboottest-for-slice, open-in-view, lazy-outside-tx, n-plus-1, cascade-all-unjustified, optional-get-without-context, entity-serialised-directly, native-query-string-concat, entitymanager-in-singleton | 1700 |
| `content/04-procedure.xml` | essential | 5-step procedure: entity modelling → paired migration → narrow repository + bulk-op safety → transactional service with DTOs → test slice | 900 |
| `content/05-examples.xml` | reference | Worked fragments for the mapping / repository / narrow-repository / service rules; full bodies in templates/ | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-entity` | sonnet | Translating domain to JPA mappings requires judgment. |
| `generate-migration` | sonnet | Expand-contract reasoning. |
| `audit-fetch-strategy` | haiku | Mechanical scan for EAGER fetches. |
| `design-bulk-operation` | opus | L1 cache + clearAutomatically reasoning. |
| `design-entity-mapping` | sonnet | Cascade + orphanRemoval + fetch judgment. |
| `write-narrow-repository` | sonnet | Interface naming + method-set segregation. |
| `audit-existing-queries` | sonnet | Hunt N+1 and cascade misuse in an existing codebase. |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity.java` | Entity skeleton with LAZY associations + business-key equals/hashCode. |
| `templates/repository.java` | Spring Data JPA repository with @Modifying + clearAutomatically. |
| `templates/NarrowRepository.java` | Narrow read/write repository interfaces per `narrow-repo-interface`. |
| `templates/Service.java` | Transactional service with JOIN FETCH + DTO projection. |
| `templates/application-test.yml` | `@DataJpaTest` configuration with Testcontainers DB. |
| `templates/application-jpa.yml` | Runtime JPA defaults: OSIV off, ddl-auto=validate, batch inserts, Hikari pool sizing. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-jpa-hibernate.py` | Validate the JPA-layer manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[java-spring-boot]]
- [[java-junit-testing]]
- [[java-spring]]
- [[ddd-repositories]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (read vs write path, fetch strategy, test layer) to a rule from `01-core-rules.xml`. Use it before scaffolding a new entity or refactoring a hot query.
