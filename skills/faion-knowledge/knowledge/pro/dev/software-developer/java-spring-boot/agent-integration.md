# Agent Integration — Spring Boot Patterns

## When to use
- Greenfield enterprise Java services where the team standardises on a layered Controller → Service → Repository stack with Spring Data JPA + Bean Validation.
- Migrating legacy Java EE / older Spring MVC apps onto Spring Boot 3.x (Jakarta EE 10, virtual threads, Native Image option).
- Building REST APIs that already commit to dependency injection, AOP, declarative transactions, and Actuator-based observability.
- Multi-module Gradle/Maven monorepos where you want a uniform skeleton (controller / service / mapper / dto / entity) generated per module.
- Teams that are JVM-bound (JDK licensing, existing Kafka/Cassandra/Oracle drivers, internal Spring Cloud config server).

## When NOT to use
- Sub-200ms cold-start serverless (Lambda, Cloud Run min-instances=0). Spring Boot startup is heavy; pick Quarkus or Micronaut, or compile to GraalVM native — but then most Spring "magic" silently breaks.
- Polyglot reactive pipelines where the dominant pattern is async streams; Spring WebFlux exists but most teams writing Boot apps default to blocking servlet stack which dilutes the win.
- Tiny solo projects / scripts. The annotation surface and starter explosion (`spring-boot-starter-*`) is overkill for a CRUD <5 entities.
- When the team has no Spring expertise — Boot's autoconfig debugging is a senior-Java skill (`--debug` + `ConditionEvaluationReport` reading).
- Anywhere tight, predictable memory matters (embedded, edge). JVM + Spring is not the right footprint.

## Where it fails / limitations
- **Autoconfig surprises.** A starter on the classpath silently wires beans you didn't ask for; agents add `spring-boot-starter-security` and now every endpoint is 401. Always pin actuator/security explicitly and read `ConditionEvaluationReport`.
- **N+1 via JPA defaults.** `@OneToMany(fetch = LAZY)` looks safe but every controller iteration triggers extra SELECTs. The README service layer doesn't show fetch joins / `@EntityGraph` — production needs them.
- **Open-session-in-view.** Boot enables it by default; a controller can lazy-load entities post-transaction and hide N+1 problems until production load. Disable in `application.yml` (`spring.jpa.open-in-view: false`).
- **Lombok lock-in.** `@RequiredArgsConstructor` + `@Data` are convenient but obscure equals/hashCode bugs on JPA entities (use `@EqualsAndHashCode(onlyExplicitlyIncluded=true)` or hand-written).
- **Transactional boundary leaks.** `@Transactional` on a private/self-call method silently does nothing (proxy-based AOP). Junior agents move logic into a private helper and lose the transaction.
- **Mapper sprawl.** MapStruct/manual mappers explode when DTOs diverge per endpoint version; without discipline you get `UserMapperV1`, `UserMapperV2`, `UserAdminMapper` — review pressure stays high.
- **Bean validation isn't business validation.** `@NotBlank` on the DTO doesn't replace the domain invariant in the entity; agents conflate them and ship request-level checks as if they were business rules.
- **Slow tests.** `@SpringBootTest` boots the whole context (~5–15s). Without slicing (`@WebMvcTest`, `@DataJpaTest`) the test suite balloons and CI gets gamed via skip.

## Agentic workflow
Drive Spring Boot scaffolding as a four-stage pipeline: (1) a design agent extracts entity + endpoint inventory from the spec; (2) a code-gen agent emits Controller, Service, Repository, Entity, DTOs, Mapper, and exception handler aligned to the existing module's package layout; (3) a test agent generates `@WebMvcTest` for controllers and `@DataJpaTest` for repositories with Testcontainers Postgres; (4) a review agent runs the anti-pattern checklist (open-session-in-view, missing transactional, public-method-only checks, fetch type, equals/hashCode on entity). Use `faion-sdd-executor-agent` to wrap each new endpoint as one SDD task containing controller + service + test as a unit. Keep autoconfig deltas in `.aidocs/product_docs/spring-autoconfig.md` so agents never re-debug `ConditionalOnMissingBean` from scratch.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task = controller + service + repository + WebMvcTest + DataJpaTest. Sonnet is enough for standard CRUD; opus for transactional boundary design.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — run before committing `application.yml` / fixtures; Spring properties readily leak DB URLs with creds.
- A dedicated **spring-review-agent** (worth adding under `agents/`): single-pass linter that flags `@Transactional` on private methods, missing `@EntityGraph` on `@OneToMany` controller paths, raw `@Autowired` field injection, and DTO-as-entity returns from controllers.
- `faion-feature-executor` skill — sequential mode keeps controller→service→repository→test ordering correct; out-of-order task execution leaves dangling beans / failing context loads.

### Prompt pattern
Endpoint inventory pass:
```
You are a Spring Boot architect. Given the spec in <spec>, produce a
table of endpoints. Columns: HTTP verb, path, request DTO, response DTO,
service method, transactional? (yes/no), validation groups, security
role(s), idempotency strategy. Reject endpoints that mutate without
@Transactional. Reject endpoints that return JPA entities directly.
```

Anti-pattern review pass:
```
You are reviewing a Spring Boot PR. Flag:
(1) @Transactional on private or self-invoked method,
(2) JPA entity returned from a controller (must be DTO),
(3) field-injection (@Autowired on a field) instead of constructor,
(4) @OneToMany without @EntityGraph or fetch join used in a list endpoint,
(5) spring.jpa.open-in-view not explicitly set to false,
(6) password / secret in application.yml committed.
Cite file:line. No fixes — only flags.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Spring Boot CLI | `spring init` scaffolding, run apps without Maven/Gradle | https://docs.spring.io/spring-boot/cli/ |
| `spring-boot-devtools` | Hot reload, LiveReload | starter dependency |
| Spring Initializr (web/CLI) | Generate Boot projects with chosen starters | https://start.spring.io |
| Maven `./mvnw` / Gradle `./gradlew` | Wrapper builds — pin to project | bundled |
| `actuator` HTTP endpoints | Health, metrics, env, beans, mappings, conditions | `/actuator/*` |
| `jib` (Maven/Gradle plugin) | Build OCI images without Dockerfile, layered for fast rebuilds | https://github.com/GoogleContainerTools/jib |
| `pack` (CNB) | Cloud-Native Buildpacks alt to jib | https://buildpacks.io |
| `spring-native` / GraalVM | AOT compile to native image (cold-start gains) | https://docs.spring.io/spring-boot/reference/packaging/native-image/ |
| Testcontainers | Real Postgres/Kafka/Redis in tests | https://testcontainers.com |
| `flyway` / `liquibase` CLI | Schema migrations driven by CI/CD | https://flywaydb.org / https://www.liquibase.org |
| `httpie` / `curl` / `bruno` | Endpoint smoke tests | https://httpie.io |
| `jstack` / `jcmd` / `async-profiler` | JVM diagnostics for blocking, GC, hot methods | bundled JDK / https://github.com/async-profiler/async-profiler |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Spring Initializr | OSS / SaaS at start.spring.io | yes | Reproducible scaffold; agents can call the HTTP API to generate a baseline. |
| Spring Cloud Config Server | OSS | yes | Externalised properties; agents read/write via REST. |
| Eureka / Consul / Nacos | OSS | yes | Service discovery for Spring Cloud microservices. |
| Resilience4j | OSS | yes | Circuit breaker, retry, bulkhead — annotation-driven. |
| Micrometer + Prometheus + Grafana | OSS | yes | Boot Actuator exports metrics natively. |
| Sentry / Datadog APM Java agent | SaaS | yes | Tracing+errors without code changes. |
| JFrog Artifactory / Sonatype Nexus | SaaS / OSS | yes | Internal Maven repo, dependency vulnerability scanning. |
| Snyk / OWASP Dependency-Check | SaaS / OSS | yes | CVE checks for Spring/Java deps. |
| Renovate / Dependabot | SaaS | yes | Auto-PR Spring Boot version bumps; agents review the changelog. |
| Testcontainers Cloud | SaaS | yes | Offload Docker for CI; same API as local Testcontainers. |
| Spring AI | OSS | yes | Boot starter for LLM apps if the project already lives in Spring. |

## Templates & scripts
See `templates.md` for Controller/Service/Repository skeletons and `examples.md` for end-to-end CRUD. Add `application-test.yml` with `spring.jpa.open-in-view=false`, `spring.jpa.hibernate.ddl-auto=validate`, and Testcontainers JDBC URLs (`jdbc:tc:postgresql:16:///test`). Inline anti-pattern grep:

```bash
#!/usr/bin/env bash
# spring-lint.sh — quick anti-pattern scan
set -euo pipefail
root="${1:?usage: spring-lint.sh SRC_MAIN_JAVA}"
fail=0
echo "## @Transactional on private methods"
grep -rEn '@Transactional' "$root" -A 1 | grep -E 'private ' && fail=1 || true
echo "## Field injection (use constructor injection)"
grep -rEn '^\s*@Autowired$' "$root" -A 1 | grep -E '\s+(private|protected) ' && fail=1 || true
echo "## Controller returning JPA entity (must be DTO)"
grep -rEn '@RestController|@Controller' "$root" -A 50 | grep -E 'ResponseEntity<[A-Z][a-zA-Z]*Entity>|return [a-z]+Repository\.' && fail=1 || true
echo "## open-in-view not pinned"
grep -rEn 'spring\.jpa\.open-in-view' "$root/../resources" || { echo "MISSING"; fail=1; }
exit "$fail"
```

## Best practices
- **Constructor injection only.** Use `@RequiredArgsConstructor` (Lombok) or hand-written constructor; never field-inject. Makes beans testable without reflection and immutable.
- **DTO at every boundary.** Controllers in/out are DTOs; entities never cross the controller line. Eliminates accidental lazy-init, recursive serialization, and mass-assignment.
- **Transactional only on `@Service` public methods.** Annotation on a controller is a smell; on a private method is dead. Use `propagation = REQUIRED` default; only use `REQUIRES_NEW` deliberately.
- **Pin `spring.jpa.open-in-view: false`** in every profile. Forces lazy access into the service layer where it belongs.
- **`@EntityGraph` for read endpoints.** List endpoints with associations always specify the graph; never let the framework decide.
- **Bean validation = request shape; domain methods = invariants.** Don't conflate. `@NotBlank` on DTO is fine; business rules belong in the entity/aggregate.
- **Slice tests.** `@WebMvcTest` (controllers, MockMvc), `@DataJpaTest` (repositories, Testcontainers), `@SpringBootTest` only for end-to-end. Slicing keeps suite under ~30s.
- **Actuator security.** Expose `/actuator/health` publicly; gate `/actuator/env`, `/actuator/beans`, `/actuator/mappings` behind a role. They leak structure.
- **Externalise config.** `application.yml` per profile, secrets via env or Vault (`spring-cloud-vault`), never committed.
- **Native-image gotcha.** Reflection / proxies need hints; if you're targeting GraalVM, generate hints with the tracing agent and commit them — agents can't infer them.
- **Don't fight Spring with Spring.** If autoconfig is wrong, exclude the offending starter, don't write a competing bean. `@EnableAutoConfiguration(exclude=...)` is your escape.

## AI-agent gotchas
- **Wrong Java version assumption.** Agents default to Java 17/Boot 2.x APIs; current is Java 21+ Boot 3.x with `jakarta.*` packages, not `javax.*`. Pin in the system prompt.
- **`javax` vs `jakarta`.** Snippets generated with `javax.persistence.*` will not compile against Boot 3. Lint imports.
- **Field injection + Lombok mix.** Agents combine `@Autowired` field with `@RequiredArgsConstructor` and end up with two injection paths. Reject on review.
- **Skipped transactional rollback test.** Agents test happy paths; force one negative test that triggers `RuntimeException` mid-method to confirm rollback.
- **Hallucinated Spring Data methods.** Agents invent `findByEmailIgnoreCaseAndActiveTrue` without verifying it parses; pin to derived-query naming or use `@Query` JPQL with explicit checks.
- **Open-session-in-view debugging.** When a test passes and prod fails, agents won't suspect OSIV. Add to the autoconfig delta doc once and reference it.
- **Excess starters.** Agents add `spring-boot-starter-data-jpa`, `-data-redis`, `-data-mongodb`, `-amqp`, `-security`, `-mail` when only JPA is needed. Cap at the starters listed in the design doc.
- **Mapper drift.** Agents create a new mapper per endpoint instead of extending the existing one — review for duplicate `toResponse`/`toEntity`.
- **Test slice misuse.** `@SpringBootTest` everywhere; agents don't know about slices unless prompted. Reference `@WebMvcTest` and `@DataJpaTest` explicitly.
- **Human-in-loop on schema.** Auto-generated Flyway/Liquibase migrations from JPA model are dangerous. Always review the SQL diff before merge.

## References
- Spring Boot Reference. https://docs.spring.io/spring-boot/reference/
- Spring Framework Reference (transactions, AOP). https://docs.spring.io/spring-framework/reference/
- Spring Initializr. https://start.spring.io
- Walls, C. "Spring in Action," 6th ed. Manning, 2022.
- Long, J. "Reactive Spring." 2nd ed.
- Vlad Mihalcea — JPA / Hibernate posts (N+1, fetch joins, OSIV). https://vladmihalcea.com
- Baeldung — Spring catalogue. https://www.baeldung.com/spring-tutorial
- Sibling methodologies in this repo: `pro/dev/software-developer/clean-architecture/`, `pro/dev/software-developer/microservices-design/`, `pro/dev/code-quality/domain-driven-design/`.
