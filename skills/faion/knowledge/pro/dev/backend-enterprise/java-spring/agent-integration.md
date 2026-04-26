# Agent Integration — Java Spring Boot Backend (controller / service / JPA)

## When to use
- New Spring Boot 3.x service implementing the canonical layered architecture: `@RestController` → `@Service` → `JpaRepository`.
- Adding CRUD endpoints with Bean Validation, MapStruct DTO mapping, and `@Transactional` write methods.
- Refactoring code that mixes controller/service/repository concerns or returns entities directly to clients.
- Wiring `Pageable` defaults, `ResponseEntity` semantics, and `ResourceNotFoundException` handling in a global advice.
- Integrating Spring Security (BCrypt + `PasswordEncoder`) for password hashing in the service layer.

## When NOT to use
- WebFlux/reactive stack — blocking JPA, `@Transactional` semantics, and `ResponseEntity` paradigms differ.
- Apps already using Hexagonal/Clean Architecture with explicit ports/adapters — reintroducing service-on-top-of-repo doubles up.
- CQRS or event-sourced systems — service+JPA layering hides command/query split.
- Quarkus / Micronaut / serverless contexts — pattern translates conceptually but the annotations differ.

## Where it fails / limitations
- This methodology is the "starter" version of `java-spring-boot-patterns` (no Specifications, no Lombok hints, less detail). For richer search, validation, ProblemDetail, and Specifications, agents should also consult `java-spring-boot-patterns/`.
- Returning `ResponseEntity<UserResponse>` everywhere is verbose; agents add it even where direct return + `@ResponseStatus` would suffice.
- Service methods missing `@Transactional` on writes silently rely on auto-commit per JDBC call — partial failures leave inconsistent state.
- LazyInitializationException happens when controllers serialize entities outside the tx — agents miss DTO conversion under time pressure.
- `findAll(pageable)` over a 10M-row table on a missing index is a prod incident waiting to happen; agents skip pagination guards.

## Agentic workflow
Drive feature work as SDD tasks: migration → entity → repository → service (with `@Transactional` defaults) → MapStruct mapper → controller → integration test. Reviewer agent must run `./mvnw verify`, parse Hibernate SQL logs for N+1, and check that controllers never expose entities. When the project graduates beyond simple CRUD (search, complex validation, ProblemDetail), switch to `java-spring-boot-patterns`.

### Recommended subagents
- `faion-sdd-executor-agent` — task runner, executes Maven/Gradle build per task.
- `faion-feature-executor` — feature-level orchestration with quality gates.
- General reviewer subagent — flag missing `@Transactional`, entity leaks, missing `Pageable` on list endpoints.

### Prompt pattern
Plan: "Feature `<name>`: Flyway migration, entity (Long id, audited via `@CreationTimestamp`/`@UpdateTimestamp`), `JpaRepository`, service with `@Transactional(readOnly=true)` default and `@Transactional` writes, MapStruct mapper, `@RestController` with `@Valid` request bodies, integration test using Testcontainers + Postgres."

Review: "Run `./mvnw test`. Check controllers do not return entity types, all writes are `@Transactional`, all list endpoints accept `Pageable`. Flag findings."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mvnw` / `gradlew` | Project build wrappers | shipped |
| `spring init` (Spring Initializr CLI) | Scaffold projects | sdkman + `sdk install springboot` |
| Spotless | Format with Google Java style | spotless.dev |
| Checkstyle | Lint | checkstyle.org |
| Error Prone + NullAway | Bug + null-safety static analysis | errorprone.info |
| Testcontainers | Integration tests with real DBs | testcontainers.org |
| ArchUnit | Enforce package-layer rules | archunit.org |
| `flyway` / `liquibase` CLI | Apply migrations from CI | flywaydb.org / liquibase.org |
| Lombok plugin | `@RequiredArgsConstructor`, `@Slf4j` | projectlombok.org |
| MapStruct annotation processor | DTO ↔ entity mapping | mapstruct.org |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Spring Initializr API | SaaS | Yes | `curl https://start.spring.io/starter.zip ...` is fully scriptable |
| GitHub Actions / GitLab CI | SaaS | Yes | Standard JDK + cache templates |
| Sentry / Bugsnag | SaaS | Yes | `sentry-spring-boot-starter` |
| OpenTelemetry Java agent | OSS | Yes | `-javaagent:` zero-code instrumentation |
| Datadog / New Relic / Dynatrace | SaaS | Yes | Auto-attaches to JVM |
| SonarQube / SonarCloud | OSS/SaaS | Yes | Quality gate in CI |

## Templates & scripts
See `templates.md` for entity, repository, service, mapper, controller. Pre-commit gate:

```bash
#!/usr/bin/env bash
# scripts/check.sh — block PR if entities leak from controllers
set -euo pipefail
./mvnw -q -DskipTests compile spotless:check checkstyle:check
# Forbid returning entity types from REST controllers
if rg -nP 'public\s+(ResponseEntity<[A-Z]\w+>|[A-Z]\w+)\s+\w+\([^)]*\)\s*\{' src/main/java -g '*Controller.java' \
   | grep -vE 'Response|Dto|ProblemDetail|Page<|Void|String|byte\[\]'; then
  echo "Controller appears to return an entity directly — return a DTO."
  exit 1
fi
```

## Best practices
- Default `@Service` to `@Transactional(readOnly = true)` at class level; override `@Transactional` per write method.
- Constructor injection via `@RequiredArgsConstructor`; never field injection.
- DTOs are records (Java 17+); never expose entities from controllers or include Hibernate proxies in JSON.
- Always paginate list endpoints; reject unbounded `findAll()` on tables that may grow.
- Use Bean Validation on request DTOs; map `MethodArgumentNotValidException` in `@RestControllerAdvice` (see `java-spring-boot-patterns`).
- Hash passwords with `PasswordEncoder` (BCrypt) inside the service layer; never store cleartext, never accept the hash from the client.
- Run integration tests against a real DB via Testcontainers; H2 in-memory hides PostgreSQL-specific behaviour.

## AI-agent gotchas
- Agents return entities from controllers, then add `@JsonIgnore` to fields trying to fix Lazy loading — DTOs are the fix, not annotations.
- LLMs forget `@Transactional` on multi-step writes; partial commits look fine in tests but corrupt prod data.
- Self-invocation: calling another `@Transactional` method on `this` does not start a tx. Reviewer must catch this.
- Agents miss the MapStruct annotation processor in `pom.xml` and the mapper class fails to generate — looks like a mysterious "interface cannot be instantiated" error.
- `findAll(Pageable)` is sometimes converted to `findAll()` "for simplicity"; require pagination on every list endpoint.
- Generated tests mock `JpaRepository` with `@MockBean`, hiding query bugs; require Testcontainers for repository tests.
- Spring Boot 3 + `jakarta.*` vs Spring Boot 2 + `javax.*` namespace mixing is a frequent LLM error; pin Spring Boot version in the prompt.

## References
- Spring Boot reference — https://docs.spring.io/spring-boot/docs/current/reference/html/
- Spring Data JPA reference — https://docs.spring.io/spring-data/jpa/reference/
- Bean Validation — https://beanvalidation.org/
- MapStruct — https://mapstruct.org/
- Testcontainers Java — https://java.testcontainers.org/
- ArchUnit — https://www.archunit.org/
- Sister methodology with richer patterns: `../java-spring-boot-patterns/`
