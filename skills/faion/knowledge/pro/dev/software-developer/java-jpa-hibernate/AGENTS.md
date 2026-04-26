# JPA / Hibernate Patterns

## Summary

Spring Data JPA entity mapping and repository patterns: `@Entity` with `@CreationTimestamp`/`@UpdateTimestamp`, `JpaRepository` with custom `@Query` and `Specification`, service-layer `@Transactional` boundaries, and Flyway migrations co-versioned with entity changes. Always disable `open-in-view`, use `JOIN FETCH` or `@EntityGraph` for known eager paths, and map read paths to DTOs directly to avoid hydrating full entity graphs.

## Why

JPA's lazy loading default silently produces N+1 queries when collections are accessed outside the transactional boundary. `open-in-view=true` (the Spring Boot default) papers over this by keeping the session open through the view layer, hiding the N+1 at the cost of long-held DB connections. Explicit fetch strategies, DTO projections, and `readOnly=true` transactions make query behavior predictable and reviewable. Co-locating entity changes with Flyway migrations prevents schema drift in CI.

## When To Use

- Spring Boot or Jakarta EE apps with rich domain relationships (one-to-many, many-to-many, inheritance).
- Reporting / admin layers where `Specification` / Criteria API beats hand-rolled SQL strings.
- Multi-database deployments where dialect abstraction has real value.
- Teams already invested in JPQL, `@EntityGraph`, and Spring Data Repositories.

## When NOT To Use

- High-write OLTP hot paths needing predictable single-statement SQL — use plain JDBC or jOOQ.
- Bulk ETL / analytics — Hibernate per-entity event hooks make 1M-row inserts orders of magnitude slower than `JdbcTemplate.batchUpdate`.
- Schema-less stores (Mongo, DynamoDB) — use the matching driver, not JPA over a wrapper.
- Read-only view services that map straight to DTOs from SQL — use Spring Data JDBC or jOOQ.

## Content

| File | What's inside |
|------|---------------|
| `content/01-entity-mapping.xml` | @Entity rules: auditing timestamps, lazy vs eager fetch, cascade justification, @Version for optimistic locking |
| `content/02-repository-queries.xml` | JpaRepository methods, @Query JPQL, Specification pattern, @Modifying bulk updates |
| `content/03-antipatterns.xml` | open-in-view, cascade ALL reflex, equals/hashCode on id, missing Flyway migration, findById().get() |

## Templates

| File | Purpose |
|------|---------|
| `templates/application-jpa.yml` | Safe JPA defaults: open-in-view=false, ddl-auto=validate, batch inserts, SQL logging |
| `templates/entity.java` | Entity skeleton with auditing, lazy relations, @Version, helper methods |
