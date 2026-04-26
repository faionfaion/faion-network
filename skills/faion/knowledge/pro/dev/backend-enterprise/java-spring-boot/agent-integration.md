# Agent Integration — Spring Boot Patterns

## When to use
- Bootstrapping or extending a Spring Boot 3.x service with the canonical Controller → Service → Repository layering, DTOs separate from JPA entities, and `@Transactional` boundaries on the service layer.
- Generating new resource endpoints (REST or gRPC) that follow existing project conventions: Lombok, MapStruct, Bean Validation, ProblemDetail error handling.
- Refactoring legacy Spring MVC code toward constructor injection, immutable DTOs, and `Pageable`/`Page<T>` paging.
- Adding cross-cutting concerns via filters, interceptors, or `@RestControllerAdvice` rather than duplicating logic.

## When NOT to use
- The team chose Quarkus, Micronaut, or Helidon — Spring's reflection-heavy startup and AOT story differs; don't backport patterns.
- Pure event-driven workers without HTTP — use Spring Modulith or plain `@KafkaListener`/`@RabbitListener` services; the controller layer is dead weight.
- Reactive stack (`spring-webflux`) — most templates here assume blocking servlet stack; `Mono`/`Flux` plumbing is different.
- Native image (GraalVM) without explicit reachability config — Lombok + reflection-based Jackson causes hidden failures at runtime.

## Where it fails / limitations
- LLM-generated controllers often skip Bean Validation (`@Valid`) on `@RequestBody`, leaving 500s instead of 400s on bad input.
- Auto-mapping with `BeanUtils.copyProperties` or naive constructor mapping skips `null` checks and silently overwrites IDs; force MapStruct or explicit mappers.
- Agents put business logic in controllers ("just for this one case") which then propagates; require a service-layer call from every handler, even thin pass-through.
- `@Transactional` on private methods is a no-op (Spring AOP proxies); agents add it without noticing.
- N+1 lazy-loading inside the controller layer after the transaction closed → `LazyInitializationException`. Force projection DTOs at repository level.
- Spring Boot 3 migration: `javax.*` → `jakarta.*`; agents trained on Boot 2 examples produce broken imports.

## Agentic workflow
A subagent generates a vertical slice (DTOs + Controller + Service + Repository + tests) from an endpoint spec. It runs `./mvnw test` or `./gradlew test` in a sandbox, iterating until green. A second pass reviews `application.yml` for missing actuator endpoints, security defaults, and DataSource pool settings. For schema work, the agent generates Flyway/Liquibase migrations alongside the JPA entity in the same commit.

### Recommended subagents
- `faion-sdd-executor-agent` — drives feature task with quality gates (compile, lint via Checkstyle/Spotless, test, coverage).
- `faion-feature-executor` — sequential delivery of multi-task Spring features (entity → repo → service → controller → test → migration).
- A custom `spring-test-runner` agent scoped to `Bash(./mvnw test:*)`, `Bash(./gradlew test:*)`, `Read`, `Edit` — limited blast radius.
- Pair with `faion-backend-agent` for domain modeling decisions (aggregate boundaries, entity vs. DTO).

### Prompt pattern
```
Implement endpoint POST /api/v1/orders. Follow project conventions:
constructor injection, Lombok @RequiredArgsConstructor, MapStruct mapper,
@Valid @RequestBody, ProblemDetail on errors, @Transactional on service.
Add OrderRepository (Spring Data JPA), Flyway migration V<next>__add_orders.sql,
and @WebMvcTest + @DataJpaTest tests. Run ./mvnw verify.
```

```
Review <Controller>.java + <Service>.java for:
1) business logic in controller, 2) missing @Valid, 3) @Transactional on
private/non-public methods, 4) lazy access outside tx, 5) missing
ProblemDetail on exceptions. Output a checklist with line numbers.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `./mvnw` / `./gradlew` | Build, test, package — wrapper avoids version drift | bundled in project |
| Spring Boot CLI | `spring init` for new modules | https://docs.spring.io/spring-boot/installing.html |
| Spotless / Checkstyle | Format + lint Java | Maven/Gradle plugin |
| `mvn versions:display-dependency-updates` | Find stale deps | Maven plugin |
| `dependency-check` (OWASP) | CVE scan of deps | Maven/Gradle plugin |
| Flyway / Liquibase CLI | Apply / preview SQL migrations | https://flywaydb.org |
| jcmd / async-profiler | JVM diagnostics during load test | bundled / async-profiler.com |
| Testcontainers (Java) | Real Postgres/Kafka/Redis in tests | Maven `org.testcontainers` |
| `httpie` / `curl` | Smoke-test endpoints | OS package |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Spring Initializr | SaaS / OSS | Yes | `curl https://start.spring.io/starter.zip ...` works headless. |
| GitHub Actions + setup-java | SaaS | Yes | Standard Maven/Gradle CI, Testcontainers via Docker layer. |
| New Relic / Datadog APM | SaaS | Yes | Spring Boot auto-instrumentation; agent reads traces. |
| Sonatype Nexus / Artifactory | SaaS / OSS | Yes | Internal artifact hosting; Maven settings.xml driven. |
| Spring Boot Admin | OSS | Partial | Operator dashboard; humans monitor, agents query Actuator JSON. |
| Sentry, Honeybadger | SaaS | Yes | Spring starter integration. |

## Templates & scripts
See `templates.md` for controller/service/repository skeletons and Lombok+MapStruct setup. Helper script for an agent verification loop:

```bash
#!/usr/bin/env bash
# verify-spring.sh - run before any commit
set -euo pipefail
./mvnw -q -DskipTests=false verify
./mvnw -q spotless:check
./mvnw -q org.owasp:dependency-check-maven:check -DskipDataUpdate=true
echo "OK: build + tests + format + dep-check passed"
```

## Best practices
- Constructor injection only — `@RequiredArgsConstructor` + `final` fields. Field injection breaks testability and immutability.
- Separate JPA entities from DTOs always; never expose `@Entity` over HTTP. Auto-map with MapStruct.
- `@Transactional(readOnly = true)` on read-paths — Postgres skips snapshotting overhead, hibernate skips dirty checks.
- Define exceptions as a small hierarchy (`DomainException`, `NotFoundException`, `ConflictException`) and one `@RestControllerAdvice` translating to ProblemDetail.
- Configure pools explicitly: HikariCP `maximum-pool-size`, JVM heap, Tomcat threads — defaults are wrong above 100 RPS.
- Use `spring-boot-actuator` + `/actuator/health` `/actuator/info` `/actuator/metrics` and lock down with security; expose Prometheus via `/actuator/prometheus`.
- Pin Boot/Spring versions via `spring-boot-dependencies` BOM — never mix manually upgraded `spring-core`.

## AI-agent gotchas
- Agents emit `@Autowired` field injection from training data; force constructor + `final` in the prompt.
- Lombok requires annotation processor configuration; agents add `@RequiredArgsConstructor` but skip `pom.xml` plugin entry, producing "constructor not found".
- `application.properties` vs `application.yml` mix — pick one; agents will create both.
- `@Transactional` from `org.springframework.transaction.annotation` (not `javax.transaction`) — wrong import is a silent functional bug.
- `@MockBean` is deprecated in Spring Boot 3.4+ — use `@MockitoBean` or `@MockitoSpyBean`. Pin Boot version in prompt.
- Generated tests overuse `@SpringBootTest` (full context, slow) — push agents toward slice tests: `@WebMvcTest`, `@DataJpaTest`, `@JsonTest`.
- Human-in-loop checkpoint: any change to `SecurityFilterChain`, `application.yml`, or Flyway migrations on prod-shared schemas.
- Agents bake secrets into `application.yml`; always require Spring Cloud Config / env vars / Vault references and reject literal credentials.

## References
- Spring Boot reference: https://docs.spring.io/spring-boot/reference/
- Spring Framework: https://docs.spring.io/spring-framework/reference/
- Spring Data JPA: https://docs.spring.io/spring-data/jpa/reference/
- Baeldung Spring Boot tag: https://www.baeldung.com/category/spring-boot
- Josh Long, "Reactive Spring" + "Bootiful Podcast"
- Testcontainers Java: https://java.testcontainers.org
- ProblemDetail RFC 7807: https://datatracker.ietf.org/doc/html/rfc7807
