# Agent Integration — Java Spring (Boot)

## When to use
- Building Spring Boot 3.x services (Java 17+) using the standard layered cake: `@RestController` → `@Service` → `@Repository` (Spring Data JPA).
- Adding async work via `@Async` with named `ThreadPoolTaskExecutor` beans.
- Greenfield REST APIs needing validation (`@Valid`), pagination (`Pageable`), DTO mapping (MapStruct), and JUnit 5 + Mockito tests.
- Migration target when porting Java EE / Spring 4 apps to modern stack — the patterns here translate cleanly.

## When NOT to use
- Reactive workloads — use Spring WebFlux + R2DBC; `@Transactional` and JPA semantics differ enough that copying servlet patterns will deadlock.
- Lightweight microservices where Spring's boot time and memory footprint hurt — consider Quarkus, Micronaut, or Helidon.
- Functions / FaaS — cold start kills you; use lighter frameworks or GraalVM native image.
- CQRS / event-sourced systems — service+JPA pattern fights write/read separation.

## Where it fails / limitations
- "Service that returns DTO" pattern hides JPA lazy-loading bugs; agents often write code that touches lazy associations after `@Transactional` boundary closes → `LazyInitializationException`.
- `@Async` swallows exceptions in `void` returns; only `CompletableFuture<T>` propagates — generated code rarely uses the right return type.
- `@Transactional` on a self-invoked method does nothing (proxy bypass) — common LLM mistake.
- MapStruct codegen breaks when DTOs change but Maven/Gradle isn't re-run; subagents need to trigger a build.
- Spring Security defaults change between minor versions; permitting endpoints in 6.x uses `authorizeHttpRequests` not `authorizeRequests`.

## Agentic workflow
A subagent should generate the full vertical slice in one diff: `Entity` → `Repository` → `Service` (interface + impl) → `Controller` → `Mapper` → `*Request`/`*Response` DTOs → `*Test` (WebMvcTest + service unit). Use Spring's "Slice Test" annotations (`@WebMvcTest`, `@DataJpaTest`) so tests are fast. For DB changes, generate a Flyway/Liquibase migration alongside the entity. Always require integration tests with Testcontainers for repos that use Postgres-specific SQL.

### Recommended subagents
- `faion-sdd-executor-agent` — TDD loop with quality gate check before commit.
- A `spring-vertical-slice` subagent (project-local) — produces 7 files (entity, repo, service, controller, mapper, dtos, tests) plus the migration.

### Prompt pattern
```
Add a vertical slice for "ApiKey" under com.example.apikey:
- entity ApiKey (id Long, hash String unique, name String, createdAt)
- repo ApiKeyRepository extends JpaRepository<ApiKey, Long>
- service ApiKeyService { create(req): Resp; revoke(id) }
- controller POST /api/v1/api-keys, DELETE /{id}, with @Valid
- mapper via MapStruct
- WebMvcTest for controller, @ExtendWith(MockitoExtension.class) for service
- Flyway V20260424__api_keys.sql
Use constructor injection (@RequiredArgsConstructor). No field injection.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `spring init` (Spring CLI) | Scaffolds projects, deps | https://docs.spring.io/spring-boot/installing.html |
| `mvn spring-boot:run` / `gradle bootRun` | Local run | https://docs.spring.io/spring-boot/maven-plugin/ |
| `spring-boot-devtools` | Hot reload during agent loop | https://docs.spring.io/spring-boot/reference/using/devtools.html |
| Flyway CLI / `mvn flyway:migrate` | Schema migrations | https://flywaydb.org |
| `gradle test --tests *Test` | Run targeted tests | https://docs.gradle.org |
| `mvn dependency:tree` | Diagnose Spring dep conflicts | core Maven |
| Testcontainers | Real Postgres/Redis in tests | https://testcontainers.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Spring Initializr | SaaS (web) | Yes | Programmatic API at `https://start.spring.io/starter.zip?...` for scaffolding |
| Spring Cloud Config | OSS | Partially | Externalized config; ok to drive but versioning gets tricky |
| Micrometer + Prometheus | OSS | Yes | Auto-exposed at `/actuator/prometheus` — add counters/timers in services |
| Sentry / Datadog Java | SaaS | Yes | Java agent does most work; agents only add `Sentry.captureException(e)` calls |
| Liquibase / Flyway | OSS | Yes | Prefer Flyway for SQL-first; Liquibase for cross-DB |
| MapStruct | OSS (annotation processor) | Yes | Generates DTO mappers at compile time |

## Templates & scripts
See `templates.md` for full slice. Pom snippet to enforce annotation processing for Lombok + MapStruct (LLMs forget the order):

```xml
<plugin>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <annotationProcessorPaths>
      <path><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><version>${lombok.version}</version></path>
      <path><groupId>org.mapstruct</groupId><artifactId>mapstruct-processor</artifactId><version>${mapstruct.version}</version></path>
      <path><groupId>org.projectlombok</groupId><artifactId>lombok-mapstruct-binding</artifactId><version>0.2.0</version></path>
    </annotationProcessorPaths>
  </configuration>
</plugin>
```

## Best practices
- Use constructor injection + `@RequiredArgsConstructor` (Lombok) or explicit constructors. Ban `@Autowired` field injection in lint rules.
- Mark service methods read or write: `@Transactional(readOnly = true)` on queries.
- Never return JPA entities from controllers — always map to DTOs at the service boundary.
- Use DTOs as Java `record`s (Java 17+) for immutability, especially for `*Request`/`*Response`.
- Validate at the edge with `@Valid` + Bean Validation (`jakarta.validation.constraints.*`); throw `MethodArgumentNotValidException` is auto-handled by `@RestControllerAdvice`.
- For `@Async`, always declare an explicit `Executor` bean per workload (email vs reports) — sharing the default executor causes head-of-line blocking.
- Pair every JPA query that uses `JOIN FETCH` with a test that asserts `Hibernate.isInitialized(...)` or use `@EntityGraph`.

## AI-agent gotchas
- Agents call `@Async` methods from inside the same class — the call bypasses the proxy and runs synchronously. Pin "must be called from a different bean" in prompts and verify in code review.
- They write `@Transactional` on `private` or `final` methods — proxies can't intercept; require `public` non-final.
- LLMs default to `findAll()` without `Pageable`, OOMing prod. Force `Pageable` arg in every list endpoint.
- They mix MapStruct + Lombok without `lombok-mapstruct-binding`, causing null mappers at runtime. Lock the dep in templates.
- `JpaRepository` derived queries silently match wrong fields (e.g., `findByEmail` on a renamed column). Always include a repo `@DataJpaTest`.
- Human-in-loop checkpoint: review N+1 queries before merge; agents do not catch them. Run with `spring.jpa.show-sql=true` + Hibernate statistics in dev.

## References
- Spring Boot reference: https://docs.spring.io/spring-boot/docs/current/reference/html/
- Spring Data JPA: https://docs.spring.io/spring-data/jpa/docs/current/reference/html/
- Vlad Mihalcea — "High-Performance Java Persistence": https://vladmihalcea.com/books/high-performance-java-persistence/
- "Spring in Action, 6th ed." — Craig Walls
- Baeldung — Spring patterns reference: https://www.baeldung.com/spring-tutorial
