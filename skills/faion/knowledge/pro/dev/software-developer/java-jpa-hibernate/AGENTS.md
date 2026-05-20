---
slug: java-jpa-hibernate
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: JPA (Java Persistence API) with Hibernate provides a full-featured ORM for Spring Boot applications.
content_id: "64d0e9006c591d53"
tags: [java, jpa, hibernate, spring-boot, orm]
---
# JPA / Hibernate Patterns in Spring Boot

## Summary

**One-sentence:** JPA (Java Persistence API) with Hibernate provides a full-featured ORM for Spring Boot applications.

**One-paragraph:** JPA (Java Persistence API) with Hibernate provides a full-featured ORM for Spring Boot applications. Use @Entity with @CreationTimestamp/@UpdateTimestamp for auditing, JpaRepository with custom @Query and Specification for dynamic filtering, service-layer @Transactional boundaries to control session scope, and Flyway migrations co-versioned with entity changes. Always disable spring.jpa.open-in-view, use JOIN FETCH or @EntityGraph for eager loading, and map read paths to DTOs to avoid hydrating unnecessary entity graphs.

## Applies If (ALL must hold)

- Spring Boot or Jakarta EE apps with rich domain relationships (one-to-many, many-to-many, inheritance).
- Reporting / admin layers where Specification / Criteria API beats hand-rolled SQL strings.
- Multi-database deployments where dialect abstraction (Hibernate's SQL generation) has real value.
- Teams already invested in JPQL, @EntityGraph, and Spring Data Repositories.
- Projects that need auditing timestamps, optimistic locking, and lifecycle event hooks.

## Skip If (ANY kills it)

- High-write OLTP hot paths needing predictable single-statement SQL — use plain JDBC, jOOQ, or MyBatis.
- Bulk ETL / analytics — Hibernate's per-entity event hooks make 1M-row inserts orders of magnitude slower than JdbcTemplate.batchUpdate.
- Schema-less stores (Mongo, DynamoDB) — use the matching driver, not JPA over a wrapper.
- Read-only "view" services that map straight to DTOs from SQL — use Spring Data JDBC or jOOQ.
- Functional/Kotlin-first codebases that prefer Exposed or jOOQ DSL over annotation-driven mapping.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/dev/software-developer/`
