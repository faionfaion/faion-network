# Agent Integration — Java Spring Boot Patterns

## When to use
- Greenfield Spring Boot 3.x service following the layered architecture (controller → service → repository) with JPA/Hibernate.
- Refactoring a legacy Spring app to use records for DTOs, MapStruct mappers, `@Transactional(readOnly = true)` defaults, and `ProblemDetail` exception handling.
- Adding `@RestControllerAdvice` global exception handlers and Bean Validation (`@Valid`, `@NotBlank`).
- Wiring Specifications (`JpaSpecificationExecutor`) for dynamic search endpoints and pageable results.
- Standing up Actuator, Micrometer, OpenAPI/Swagger, and Spring Security defaults.

## When NOT to use
- Reactive stack (`WebFlux`) — patterns like blocking JPA repos, `@Transactional`, and `ResponseEntity` semantics differ; use a reactive-specific knowledge base.
- Tiny CLI tools — Spring Boot's startup cost and DI overhead are unjustified.
- Functions/serverless deployments where cold start matters; prefer Quarkus or Micronaut.
- Legacy Spring 4.x / Java 8 — record types, sealed types, `ProblemDetail`, and Jakarta namespace are not available.

## Where it fails / limitations
- Rich layered structure encourages anemic domain models — agents will pile logic into services and leave entities as data bags.
- N+1 queries are the most common LLM failure: missing `JOIN FETCH` or `@EntityGraph`. Reviewer must check Hibernate logs in tests.
- `@Transactional` on private methods or self-invocation silently does nothing — agents miss this and assume a tx exists.
- `MapStruct` annotation processing must be wired in `pom.xml`/`build.gradle`; agents often produce mappers that don't compile.
- Lombok hides constructor visibility — `@RequiredArgsConstructor` plus `final` fields breaks if a non-final field is added.
- Spring Boot 3 uses `jakarta.*` not `javax.*`; LLMs trained on older corpora will mix namespaces.

## Agentic workflow
Drive feature work through SDD-style tasks: spec → entity + migration → repository + specifications → service + tests → controller + exception handler. The reviewer agent must run `./mvnw verify` (or `./gradlew check`) after each task and parse Hibernate SQL logs for N+1 patterns. Agents should never bypass `@Transactional` boundaries by calling private methods on the same bean. Keep DTO records immutable; never expose entities directly from controllers.

### Recommended subagents
- `faion-sdd-executor-agent` — sequential task execution against `implementation-plan.md`, runs build + tests per task.
- `faion-feature-executor` — feature-level orchestration with quality gates.
- General reviewer subagent — flags N+1, `@Transactional` on private methods, entity leaks in controllers.

### Prompt pattern
Plan: "For feature `<name>`: produce migration (Flyway V<n>__<name>.sql), entity extending `BaseEntity`, repository with specifications, service interface + impl with `@Transactional(readOnly=true)` default and `@Transactional` on writes, DTO records, MapStruct mapper, `@RestController` with Bean Validation, integration test using Testcontainers."

Review: "Run `./mvnw -q test`. Parse Hibernate SQL logs in `target/test-output/`. List any query repeated per element of a collection (N+1). For each, propose a `JOIN FETCH` or `@EntityGraph` fix."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mvnw` / `gradlew` wrappers | Reproducible builds | shipped with project |
| `spring-boot-cli` | Quickly init projects via `spring init` | sdkman: `sdk install springboot` |
| Spotless | Format Java to Google/Palantir style | spotless.dev |
| Checkstyle | Style + structure rules (anemic-model heuristics via custom rules) | checkstyle.org |
| Error Prone + NullAway | Catch nullability + common bugs at compile time | errorprone.info, github.com/uber/NullAway |
| Testcontainers | Spin up Postgres/Mongo/Kafka in tests | testcontainers.org |
| ArchUnit | Architecture rules: enforce package boundaries (controller → service → repo) | archunit.org |
| Flyway / Liquibase CLI | Apply DB migrations from CI | flywaydb.org |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Spring Initializr | SaaS (api.start.spring.io) | Yes | `curl https://start.spring.io/starter.zip -d ...` is fully scriptable |
| GitHub Actions / GitLab CI | SaaS | Yes | Maven/Gradle caching templates are stable |
| New Relic / Datadog APM | SaaS | Yes | Java agents attach via env var; one CI step |
| Sentry | SaaS | Yes | `sentry-spring-boot-starter` autoconfigures via app props |
| OpenTelemetry Java agent | OSS | Yes | `-javaagent:opentelemetry-javaagent.jar` zero-code |
| Sonarqube/SonarCloud | SaaS/OSS | Yes | Quality gate enforces coverage + smell limits |

## Templates & scripts
See `templates.md` for `BaseEntity`, repository specifications, `GlobalExceptionHandler`, MapStruct mapper, and Testcontainers integration test. Quick N+1 detector for tests:

```java
// src/test/java/.../NPlusOneAssertion.java
public final class NPlusOneAssertion {
  public static void assertNoNPlusOne(Statistics stats, String entity, int max) {
    long count = stats.getEntityStatistics(entity).getFetchCount();
    if (count > max) {
      throw new AssertionError("N+1 on " + entity + ": " + count + " > " + max);
    }
  }
}
```

Wire in test base class via `SessionFactory.getStatistics().setStatisticsEnabled(true)` and assert per-method.

## Best practices
- Default services to `@Transactional(readOnly = true)` at class level; override with `@Transactional` for write methods.
- Use Java 17+ records for DTOs (request and response) — immutable and compact.
- Prefer constructor injection (`@RequiredArgsConstructor`) — never field injection (`@Autowired` on field).
- Map errors via `@RestControllerAdvice` returning `ProblemDetail` (RFC 7807) instead of custom JSON shapes.
- Keep `@Service` interfaces only when there are multiple impls or AOP-around-interface needs; otherwise concrete classes are simpler.
- Use Specifications + Pageable for dynamic search; never build SQL strings by concatenation.
- Always paginate list endpoints — set a `@PageableDefault(size = 20)` and a max page size guard.

## AI-agent gotchas
- LLMs often place business logic in services and leave entities anemic — reviewer should require at least one domain method per non-trivial entity.
- Self-invocation: `this.someTransactionalMethod()` from another method in the same bean does NOT start a transaction. Agents miss this consistently.
- Agents return entities (with lazy proxies) directly from controllers, causing `LazyInitializationException` after the tx ends. Always map to a DTO.
- Mixing `javax.*` and `jakarta.*` imports in Spring Boot 3 produces cryptic errors; pin namespace in the prompt.
- Lombok's `@Data` on JPA entities breaks `equals`/`hashCode` for managed entities — require `@Getter @Setter` and a manual id-based `equals`.
- Agents commonly skip `@EnableJpaAuditing` and the `@CreationTimestamp` / `@UpdateTimestamp` annotations don't fire — verify in a smoke test.
- Generated tests often use `@MockBean` everywhere, eliminating integration coverage; require Testcontainers for repository and integration layers.

## References
- Spring Boot reference — https://docs.spring.io/spring-boot/docs/current/reference/html/
- Spring Data JPA — https://docs.spring.io/spring-data/jpa/reference/
- ProblemDetail (RFC 7807) — https://www.rfc-editor.org/rfc/rfc7807
- Testcontainers Java — https://java.testcontainers.org/
- ArchUnit — https://www.archunit.org/
- Vlad Mihalcea: High-Performance Java Persistence — https://vladmihalcea.com/books/high-performance-java-persistence/
- Baeldung Spring tutorials — https://www.baeldung.com/spring-boot
