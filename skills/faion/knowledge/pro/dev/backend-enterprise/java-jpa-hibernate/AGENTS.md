# JPA / Hibernate Patterns

## Summary

Entity modeling and query patterns for Spring Data JPA with Hibernate. Entities use explicit `@Table`/`@Column` constraints, `@Version` for optimistic locking, and business-key-based `equals`/`hashCode` (never ID-based, never Lombok `@Data`). All schema changes ship with a Flyway/Liquibase migration. N+1 is resolved via `JOIN FETCH` or `@EntityGraph`, never by switching to `EAGER` fetch globally.

## Why

Hibernate's defaults are correct for simple CRUD but produce silent perf traps at scale: lazy `@OneToMany` without a JOIN FETCH generates N+1 queries; `FetchType.EAGER` causes Cartesian explosions on multi-collection fetches; `@Data` on entities causes `equals`/`hashCode` cycles via collections. DTO projections avoid `LazyInitializationException` across transaction boundaries. `@Transactional(readOnly = true)` on read paths skips dirty-checking for a significant throughput gain.

## When To Use

- Spring Boot service with Hibernate ORM needing new entities, repositories, or query refactors.
- Fixing N+1 queries via `JOIN FETCH`, entity graphs, or projection DTOs.
- Adding optimistic locking (`@Version`), auditing (`@CreationTimestamp`/`@UpdateTimestamp`), or soft delete.
- Generating type-safe Criteria queries with the JPA Static Metamodel.

## When NOT To Use

- Read-heavy analytics on huge tables — use `JdbcTemplate`, jOOQ, or native SQL views.
- Bulk loads / ETL — use `JdbcTemplate.batchUpdate` or COPY; Hibernate per-entity flush is a perf trap.
- Polyglot persistence where JPA's relational mapping is the wrong shape (graph, time-series, document).
- Microservices where the schema is owned by another service — consume via API or jOOQ on a read replica.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Entity modeling rules: `@Table`, indexes, `@Version`, business-key equals/hashCode, migration pairing. |
| `content/02-examples.xml` | User entity with `@ManyToMany`/`@OneToMany`, repository with `JOIN FETCH` and search query. |
| `content/03-antipatterns.xml` | `@Data` on entities, `EAGER` fetch, `CascadeType.ALL` on `@ManyToOne`, skipped migration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity.java` | Entity skeleton: `@Table`, `@Column` constraints, `@Version`, `@CreationTimestamp`, business-key `equals`. |
| `templates/repository.java` | Repository with derived methods, `@Query` JOIN FETCH, pageable search, `@Modifying` bulk update. |
| `templates/application-test.yml` | JPA test config: Hibernate statistics, batch inserts, Flyway, SQL debug logging. |
