# Agent Integration — JPA / Hibernate

## When to use
- Spring Boot or Jakarta EE apps that need an ORM with a wide ecosystem (transactions, caching, validation, projections).
- Domain models with rich relationships (one-to-many, many-to-many, inheritance) and stable schemas.
- Reporting/admin layers where dynamic queries via `Specification` / Criteria API beat hand-rolled SQL strings.
- Multi-database deployments where dialect abstraction is genuinely useful.
- Teams already invested in JPQL, `@EntityGraph`, and Spring Data Repositories.

## When NOT to use
- High-write OLTP hot paths where you need predictable single-statement SQL — plain JDBC, jOOQ, or MyBatis are simpler.
- Bulk ETL / analytics — Hibernate's per-entity event hooks make 1M-row inserts orders of magnitude slower than `JdbcTemplate.batchUpdate`.
- Schema-less stores (Mongo, DynamoDB) — pick the matching driver, not JPA over a wrapper.
- Read-only "view" services that should map straight to DTOs from SQL — use Spring Data JDBC or jOOQ.
- Functional/Kotlin-first codebases that want Exposed or jOOQ DSL instead of annotation-driven mapping.

## Where it fails / limitations
- N+1 is the default outcome of `FetchType.LAZY` collections plus naive iteration; needs `@EntityGraph` or `JOIN FETCH`.
- `@OneToMany(cascade = ALL, orphanRemoval = true)` looks tidy but corrupts data if the same entity is referenced elsewhere.
- `merge()` vs `save()` vs `persist()` semantics confuse even experienced devs; test agents will pick the wrong one and produce duplicate rows or detached-entity exceptions.
- LazyInitializationException outside transactions — agents access lazy collections in controllers and crash at runtime.
- Hibernate 6+ changed query parameter handling and many implicit casts; copy-pasted code from old Stack Overflow answers compiles but throws at runtime.
- Schema drift between `@Entity` and Flyway/Liquibase migrations is silent. `spring.jpa.hibernate.ddl-auto=update` masks bugs in dev and is dangerous in prod.

## Agentic workflow
Have the subagent generate the entity, the Spring Data Repository (interface + custom queries), a Flyway migration matching the entity, and the service that orchestrates transactions. Tests must include one slice test (`@DataJpaTest`) per repository plus one transactional integration test (`@SpringBootTest` + Testcontainers Postgres). Quality gates: `./mvnw verify` (or `./gradlew check`), `./mvnw spring-javaformat:validate`, and a SQL log review for N+1 patterns.

### Recommended subagents
- `/faion` (sdd-batch-orchestrator workflow) — slice-by-slice generation; Spring Boot's layering matches well.
- `faion-sdd-executor-agent` — runs build, tests, and lint as quality gates.

### Prompt pattern
```
Add JPA aggregate <Name>: entity with auditing, repository interface extending JpaRepository + JpaSpecificationExecutor, service @Transactional, Flyway migration V<n>__create_<name>.sql matching the entity columns + indexes. Add @DataJpaTest covering a custom @Query and one specification. Verify no LAZY access happens outside the transactional boundary.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `./mvnw` / `./gradlew` | Build, test, run, package | Wrapper in repo |
| Spring Boot CLI (`spring`) | Project scaffolding | https://docs.spring.io/spring-boot/cli |
| `flyway` / `liquibase` | Schema migrations | https://flywaydb.org / https://www.liquibase.org |
| Hibernate `schema-generation` | Validate entity ↔ schema | `spring.jpa.hibernate.ddl-auto=validate` in prod |
| `jbang` | Run single-file Java scripts (handy for one-off checks) | https://jbang.dev |
| `p6spy` | Logs JDBC + bind params for N+1 hunting | NuGet/Maven |
| Testcontainers CLI | Docker-driven DB containers in tests | https://testcontainers.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostgreSQL / MySQL / Oracle / SQL Server | OSS / SaaS | Yes | Hibernate dialect support out of the box. |
| Hibernate Tools | OSS | Yes | Schema export / reverse engineering. |
| Datasource Proxy + p6spy | OSS | Yes | Logs every SQL with params for review by an agent. |
| Spring Cloud Gateway / OpenFeign | OSS | Yes | Adjacent stack pieces. |
| New Relic / Datadog Java APM | SaaS | Yes | Surfaces slow queries, JDBC pool starvation, N+1 hot spots. |
| Liquibase Hub | SaaS | Yes | Migration drift detection; integrates with CI. |
| Spring Boot starters via faion-net | OSS | Yes | See `projects/faion-net/faion-starter-spring` (if present) for bootstrap. |

## Templates & scripts
See templates.md and README (Entity Definition, Repository with Custom Queries). Sample `application.yml` snippet for safe defaults:

```yaml
spring:
  jpa:
    open-in-view: false
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        jdbc.batch_size: 50
        order_inserts: true
        order_updates: true
        generate_statistics: true
  datasource:
    hikari:
      maximum-pool-size: 20
logging:
  level:
    org.hibernate.SQL: debug
    org.hibernate.orm.jdbc.bind: trace
```

## Best practices
- Always disable `open-in-view` (`spring.jpa.open-in-view=false`) — without it, lazy loading silently fires queries from the controller layer.
- Use `@EntityGraph` or `JOIN FETCH` for known eager paths; never rely on lazy in transient layers.
- Mark service methods `@Transactional(readOnly = true)` for queries; `@Transactional` (read-write) only where you write.
- Map projections directly to DTOs (interface or class projections) when you don't need the entity graph.
- Use `LockModeType.PESSIMISTIC_WRITE` on the repository method for inventory/balance-style writes; document why.
- Pair every entity change with a Flyway/Liquibase migration in the same PR; CI must run `validate`.
- Index FKs and unique constraints explicitly in migrations; Hibernate doesn't always create them.
- Use `@Version` for optimistic locking on user-editable aggregates.
- Treat `EntityManager` as scoped to a transaction; never inject it into singletons that outlive a request.

## AI-agent gotchas
- Agents emit `cascade = CascadeType.ALL` reflexively on every relation. This is rarely correct and can delete sibling data. Force a written justification per cascade.
- Bidirectional relations missing the `@JsonIgnore` / DTO boundary cause infinite recursion when serialized. Always serialize via DTOs / Resources, never the entity.
- Agents copy code with `equals`/`hashCode` on the `id` field — broken for entities not yet persisted. Use a UUID/business-key approach or generated `equals` that handles transient entities.
- The agent often skips the Flyway migration step. Pre-commit hook should fail if `@Entity` files changed without a corresponding `db/migration/V*` file.
- Hibernate 6 dropped some implicit conversions; agents pasting JPQL from older snippets get `IllegalArgumentException` at startup. Verify against the active Hibernate major version.
- Human checkpoint: review every `@Query(nativeQuery = true)` for SQL injection (must use named parameters), and review every `@Transactional` boundary for nesting / propagation gotchas.
- `findById()` returns `Optional<T>` — agents `.get()` it directly. Steer to `.orElseThrow(() -> new NotFoundException(...))`.

## References
- https://docs.spring.io/spring-data/jpa/reference/
- https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html
- https://vladmihalcea.com (definitive JPA performance blog)
- https://www.thoughts-on-java.org
- https://www.baeldung.com/spring-data-jpa-tutorial
