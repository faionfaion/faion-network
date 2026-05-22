---
slug: java-jpa-hibernate
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Entity modeling and query patterns for Spring Data JPA with Hibernate.
content_id: "64d0e9006c591d53"
tags: [java, hibernate, jpa, spring-boot, orm]
---
# JPA / Hibernate Patterns

## Summary

**One-sentence:** Entity modeling and query patterns for Spring Data JPA with Hibernate.

**One-paragraph:** Entity modeling and query patterns for Spring Data JPA with Hibernate. Entities use explicit `@Table`/`@Column` constraints, `@Version` for optimistic locking, and business-key-based `equals`/`hashCode` (never ID-based, never Lombok `@Data`). All schema changes ship with a Flyway/Liquibase migration. N+1 is resolved via `JOIN FETCH` or `@EntityGraph`, never by switching to `EAGER` fetch globally.

## Applies If (ALL must hold)

- Spring Boot service with Hibernate ORM needing new entities, repositories, or query refactors.
- Fixing N+1 queries via `JOIN FETCH`, entity graphs, or projection DTOs.
- Adding optimistic locking (`@Version`), auditing (`@CreationTimestamp`/`@UpdateTimestamp`), or soft delete.
- Generating type-safe Criteria queries with the JPA Static Metamodel.

## Skip If (ANY kills it)

- Read-heavy analytics on huge tables — use `JdbcTemplate`, jOOQ, or native SQL views.
- Bulk loads / ETL — use `JdbcTemplate.batchUpdate` or COPY; Hibernate per-entity flush is a perf trap.
- Polyglot persistence where JPA's relational mapping is the wrong shape (graph, time-series, document).
- Microservices where the schema is owned by another service — consume via API or jOOQ on a read replica.

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

- parent skill: `pro/dev/backend-enterprise/`
