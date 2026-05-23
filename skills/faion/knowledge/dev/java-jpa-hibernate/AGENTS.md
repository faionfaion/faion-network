# JPA / Hibernate Patterns in Spring Boot

## Summary

**One-sentence:** JPA/Hibernate patterns — auditing timestamps, narrow repositories, justified cascade/fetch, optimistic locking, JOIN FETCH for eager loads, DTO projections for reads.

**One-paragraph:** JPA misuse — open-in-view enabled, `CascadeType.ALL` everywhere, lazy collections accessed outside transactions, N+1 from naive `findAll()` — produces "Hibernate is slow" complaints. This methodology pins five rules: every entity has audit timestamps + version where editable; cascade + fetch choices carry a written justification; repositories are narrow interfaces (no raw `JpaRepository` exposure); reads project to DTOs; eager loading uses explicit `JOIN FETCH`/`@EntityGraph`. Output: entity + narrow repository + transactional service spec conforming to `02-output-contract.xml`.

**Ефективно для:**

- Spring Boot 3.x + Hibernate 6.x services with non-trivial domain.
- High-throughput read paths needing DTO projection.
- Inventory / balance domains requiring optimistic locking.
- Teams that have suffered N+1 + open-in-view incidents.
- AI-generated code that defaults to `CascadeType.ALL`.

## Applies If (ALL must hold)

- Spring Boot 3.x project with JPA/Hibernate.
- Spring Data JPA repositories are in place.
- The team accepts narrow repository discipline (no raw `JpaRepository` in services).
- Flyway/Liquibase manage schema migrations.

## Skip If (ANY kills it)

- Reactive stack (Spring Data R2DBC) — different idioms.
- Plain JDBC / MyBatis — apply that stack's methodology.
- Single-table CRUD with no domain — Active Record on the entity is enough.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Entity sketch | Markdown / source | spec |
| Flyway migration baseline | SQL | repo |
| Performance budget | Markdown | spec |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring]] | Layered architecture + DI conventions this layers on. |
| [[ddd-repositories]] | Narrow-repository pattern referenced here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: audit-timestamps, justified-cascade-fetch, narrow-repo-interface, dto-projection-on-reads, joinfetch-for-eager | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for entity+repo+service spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: open-in-view, cascade-all, lazy-outside-tx, n-plus-1 | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on read/write shape → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-entity-mapping` | sonnet | Cascade + fetch judgment. |
| `write-narrow-repository` | sonnet | Interface naming + method set. |
| `audit-existing-queries` | sonnet | Look for N+1 + cascade misuse. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Entity.java` | Entity with audit + version + justified mappings |
| `templates/NarrowRepository.java` | Narrow read/write repository interfaces |
| `templates/Service.java` | Transactional service with JOIN FETCH + DTO projection |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-jpa-hibernate.py` | Validate entity+repo+service spec | Pre-commit on spec artefact |

## Related

- [[java-spring]]
- [[java-junit-testing]]
- [[ddd-repositories]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (read vs write, association depth, list vs single) to a rule from `01-core-rules.xml`. Use it whenever adding an entity, a repository method, or a slow query.
