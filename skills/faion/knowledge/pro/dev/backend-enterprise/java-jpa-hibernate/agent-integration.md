# Agent Integration — JPA / Hibernate Patterns

## When to use
- Spring Data JPA / Spring Boot service that already uses Hibernate as the ORM and needs new entities, repositories, or query refactors.
- Refactoring N+1 queries via `JOIN FETCH`, entity graphs, or projection DTOs.
- Adding optimistic locking (`@Version`), auditing (`@CreationTimestamp`/`@UpdateTimestamp`), or soft delete via Hibernate filters.
- Generating type-safe Criteria queries with the JPA Static Metamodel.

## When NOT to use
- Read-heavy analytics workloads on huge tables — drop to `JdbcTemplate`, jOOQ, or native SQL views.
- Bulk loads / ETL — Hibernate's per-entity flush is a perf trap; use `JdbcTemplate.batchUpdate` or COPY.
- Polyglot persistence where JPA's relational mapping is the wrong shape (graph, time-series, document).
- Microservices where the schema is owned elsewhere — consume via API or jOOQ on a read replica.

## Where it fails / limitations
- LazyInitializationException outside session: agents naively serialize entities with lazy associations across REST boundaries. Use DTO projections.
- N+1 by default for `@OneToMany` / `@ManyToOne` lazy: must use `JOIN FETCH`, `@EntityGraph`, or `@BatchSize`.
- Cartesian explosion when fetching multiple `@OneToMany` together — use `@SqlResultSetMapping` or split queries (`MultipleBagFetchException`).
- `@Modifying` queries bypass first-level cache — must `@Modifying(clearAutomatically=true, flushAutomatically=true)`.
- Equality/hashCode on entities: implement on a stable business key, never on the auto-generated ID (broken pre-persist) and never on all fields (cycles via collections).
- `cascade=CascadeType.ALL` + `orphanRemoval=true` is a frequent footgun — deletes parent → wipes all children.
- `@ManyToMany` is rarely what you want; use an explicit join entity for any non-trivial relation.

## Agentic workflow
A coding subagent should: (1) sketch the entity ER diagram in a comment before writing code, (2) generate the entity with explicit `@Table`, `@Column`, indexes, and version field, (3) build `@Repository extends JpaRepository<T, ID>` with derived methods + named `@Query` for joins, (4) generate Flyway/Liquibase migration matching the entity, (5) add a `@DataJpaTest` slice covering each query, (6) run `mvn -DfailIfNoTests=false test -Dtest=*Repository*`. Pause for human review before: changing existing entity column types, adding cascading deletes, dropping indexes, or running migrations against shared environments.

### Recommended subagents
- `general-purpose` Claude subagent — entity + repository + migration scaffolding.
- Code-review subagent (Sonnet) — flags N+1, missing fetch strategies, broken equals/hashCode, missing indexes.

### Prompt pattern
```
Add entity <Name> with fields <list>, @Column constraints, unique index on <field>, @Version Long version, @CreationTimestamp/@UpdateTimestamp. Build repository extends JpaRepository<Name, Long> with: derived findByX, @Query "SELECT n FROM Name n JOIN FETCH n.<rel> WHERE …", paging variant. Generate Flyway V<seq>__create_<name>_table.sql matching the entity. Write @DataJpaTest covering each query and the version increment on update.
```
```
Fix N+1 in <Service>.<method>: profile with hibernate.generate_statistics=true, then choose JOIN FETCH or @EntityGraph(attributePaths={...}). Show before/after query count in the test.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mvn flyway:migrate` / `gradle flywayMigrate` | Schema migrations | https://flywaydb.org |
| Liquibase CLI | Alternative migrations | https://www.liquibase.org |
| `mvn -Dhibernate.generate_statistics=true test` | Per-query stats during tests | Hibernate built-in |
| Hibernate Static Metamodel generator (`hibernate-jpamodelgen`) | Type-safe Criteria | annotation processor in pom.xml |
| `pg_stat_statements` | Find missing indexes / N+1 in production | Postgres extension |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hibernate ORM | OSS | Yes | The implementation behind Spring Data JPA |
| Spring Data JPA | OSS | Yes | Repository abstraction; agent codegen sweet spot |
| Testcontainers | OSS | Yes | Real Postgres/MySQL in `@SpringBootTest` |
| Datasource Proxy | OSS | Yes (dev) | Logs every SQL with params; pair with N+1 detector |
| QuickPerf / Hypersistence Utils | OSS | Yes | Assert max query count per test method |
| AWS RDS Performance Insights | SaaS | Yes | Per-query wait analysis in production |

## Templates & scripts
See `templates.md` for entity + repository skeletons. Inline `application-test.yml` snippet for fast, query-count-aware integration tests:

```yaml
spring:
  jpa:
    show-sql: false
    properties:
      hibernate:
        format_sql: true
        generate_statistics: true
        jdbc.batch_size: 50
        order_inserts: true
        order_updates: true
  flyway:
    enabled: true
logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.stat: DEBUG
    org.hibernate.orm.jdbc.bind: TRACE
```

## Best practices
- Always pair an entity change with a Flyway/Liquibase migration. Never rely on `hibernate.hbm2ddl.auto=update` outside dev.
- Use DTO projections (`interface UserView { String getName(); String getEmail(); }`) to avoid loading whole entities and to dodge LazyInitializationException.
- Mark service read paths `@Transactional(readOnly = true)` — Hibernate skips dirty-checking, big perf win.
- Prefer `@OneToMany` with `Set<>` not `List<>` to avoid `MultipleBagFetchException` when fetching siblings.
- Always set `spring.jpa.open-in-view=false` in `application.yml`. The default OSIV is a footgun.
- Use `@Filter`/`@Where` for soft delete, never bolt it on with `WHERE deleted_at IS NULL` everywhere.
- Index any column referenced in `findBy*`, `WHERE`, `ORDER BY`, and FK columns.

## AI-agent gotchas
- LLM emits `@Data` (Lombok) on entities — generates `equals`/`hashCode` over all fields including collections, causing infinite loops and broken `Set` semantics. Use `@Getter @Setter` + manual `equals/hashCode` over business key.
- LLM defaults to `FetchType.EAGER` "to be safe" — kills perf. Force `LAZY` and explicit fetch joins.
- Agent adds `cascade = CascadeType.ALL` everywhere, including on `@ManyToOne` (semantic nonsense). Reject in review.
- `@Transactional` on `private` methods is a no-op (proxy). Self-invocation also breaks. Static analysis should flag.
- LLM tends to skip the migration when changing entity columns. Mandate: every entity diff requires a migration diff.
- Generated tests use `@SpringBootTest` even for repository slices — slow. Prefer `@DataJpaTest` + Testcontainers.
- Human checkpoint: any schema change touching production data (rename, type change, drop column) requires migration plan review (expand-contract pattern).

## References
- https://docs.spring.io/spring-data/jpa/reference/jpa.html
- https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html
- "High-Performance Java Persistence" — Vlad Mihalcea (https://vladmihalcea.com)
- https://thorben-janssen.com/jpa-best-practices/
- https://github.com/jOOQ/jOOR (when JPA is the wrong tool)
