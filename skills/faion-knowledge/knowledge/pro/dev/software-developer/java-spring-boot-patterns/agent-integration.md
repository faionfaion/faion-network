# Agent Integration — Java Spring Boot Patterns

## When to use
- Scaffolding a new Spring Boot service (Boot 3.x, Java 17/21) from a feature spec.
- Generating entity / repository / service / controller / DTO / mapper layers from a domain model.
- Adding Spring Security (JWT, OAuth2 resource server, method security) to an existing app.
- Reviewing PRs for N+1 issues, transaction-boundary mistakes, anemic-domain anti-patterns.
- Migrating from Spring Boot 2.x → 3.x (Jakarta EE namespaces, Hibernate 6, Spring 6).
- Authoring integration tests (@SpringBootTest, Testcontainers, MockMvc/WebTestClient).

## When NOT to use
- Greenfield where the team has no Java experience — pick what they ship best.
- Tiny CLI tools or short-lived scripts — Spring overhead dwarfs the binary.
- Real-time low-latency engines (HFT, game servers) — JVM warmup + GC are issues.
- AOT-only constraints unless using Spring Native / GraalVM, and the agent must explicitly target it.

## Where it fails / limitations
- LLMs frequently mix `javax.*` (Boot 2) with `jakarta.*` (Boot 3) imports — pin Boot version and Java version in the prompt.
- Hibernate 6 schema validation differs from 5; agent emits queries that fail at runtime.
- Lombok usage assumed; in projects without Lombok, generated code won't compile.
- Reactive (WebFlux) vs imperative (Web MVC) often mixed in a single class — non-trivial to debug.
- `@Transactional` placement: agent puts on controller (wrong) or omits where lazy loading happens.
- Agents skip `@JsonIgnore` / `@JsonView` on entities → infinite recursion in JSON.

## Agentic workflow
A scaffolder subagent generates the package layout from the domain spec; a coder subagent fills in entity, repo, service, controller, DTO, mapper layers; a security-reviewer adds Spring Security config + method security and ensures secrets via `@ConfigurationProperties` + Vault/Config Server; a test-coder writes Testcontainers-backed tests. Reviewer pass enforces transaction boundaries, fetch strategies, validation, and exception handling. Use Sonnet for scaffolder/coder/test, Opus for tricky decisions (transaction propagation, JPA inheritance, security policy).

### Recommended subagents
- `springboot-scaffolder` (Haiku/Sonnet) — package structure, Maven/Gradle, application.yml profiles.
- `domain-coder` (Sonnet) — entities, repositories, specifications, mappers (MapStruct).
- `service-coder` (Sonnet) — service layer with `@Transactional`, validation, business rules.
- `web-coder` (Sonnet) — controllers, ProblemDetail handlers, OpenAPI annotations.
- `springsec-reviewer` (Sonnet) — SecurityFilterChain, JWT, RBAC, method security audit.
- `test-coder` (Sonnet) — Testcontainers, MockMvc, WebTestClient, slice tests.

### Prompt pattern
```
You are domain-coder. Boot 3.3, Java 21, Hibernate 6, Lombok yes, MapStruct yes.
Domain: <ERD>. For each aggregate: entity (BaseEntity superclass with UUID +
@Version + audit fields), repository (JpaRepository + JpaSpecificationExecutor),
specifications class. Force fetch=LAZY everywhere; include @Query JPQL for any
multi-step join. No setters on aggregate root; expose intent methods.
```

```
You are springsec-reviewer. Diff: <patch>. Reject if:
- WebSecurityConfigurerAdapter used (deprecated — use SecurityFilterChain bean),
- CSRF disabled without justification,
- in-memory user store in non-test profile,
- @Secured / @PreAuthorize missing on service-layer methods that mutate state,
- secrets read via @Value from plain properties.
Output minimal-diff fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `spring` (Spring Boot CLI) | `spring init`, run apps | https://docs.spring.io/spring-boot/cli/ |
| `mvn` / `mvnw` / `gradle` / `gradlew` | Build, test, package | maven.apache.org / gradle.org |
| `jbang` | Run Java scripts | jbang.dev |
| `flyway` / `liquibase` | DB migrations | flywaydb.org / liquibase.org |
| `httpie` / `grpcurl` | Probe endpoints | httpie.io / github.com/fullstorydev/grpcurl |
| `testcontainers` (lib) | Disposable Postgres/Kafka/Redis | testcontainers.com |
| `jacoco` (Maven plugin) | Coverage | jacoco.org |
| `spotless` | Format Java | github.com/diffplug/spotless |
| `errorprone` / `checkstyle` / `pmd` | Static analysis | errorprone.info / checkstyle.org / pmd.github.io |
| `springdoc-openapi` | OpenAPI from controllers | springdoc.org |
| `actuator` (built-in) | Metrics, health, env | docs.spring.io/spring-boot/docs/current/reference/html/actuator.html |
| `sdkman` | JDK + tooling versions | sdkman.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Spring Cloud Config / HashiCorp Vault / Consul | OSS + SaaS | Yes | Config + secrets; agent emits bootstrap config. |
| Spring Cloud Gateway | OSS | Yes | Reactive gateway; routes-as-config. |
| Eureka / Consul / K8s | OSS | Yes | Service discovery — prefer K8s in greenfield. |
| Resilience4j | OSS | Yes | Circuit breaker / retry / bulkhead beans. |
| Micrometer + Prometheus | OSS | Yes | Metrics; built into Actuator. |
| OpenTelemetry Java | OSS | Yes | Tracing; auto-instrumentation agent + manual spans. |
| Hibernate / Spring Data JPA | OSS | Yes | ORM; agent emits entities + specs reliably. |
| MapStruct | OSS | Yes | Compile-time mapping; agent integrates with Lombok. |
| Liquibase / Flyway | OSS + SaaS | Yes | Migration files; agent versions sequentially. |
| Kafka / RabbitMQ / AWS SQS | OSS + SaaS | Yes | Spring `KafkaTemplate`, `@RabbitListener`, etc. |
| Tanzu / Spring Cloud Kubernetes | SaaS + OSS | Yes | Cloud Foundry + K8s operators. |

## Templates & scripts
See `templates.md` for entity/service/controller/test snippets. Inline guard for every Spring Boot PR:

```bash
#!/usr/bin/env bash
# springboot-pr-gate.sh
set -euo pipefail
./mvnw -B -q -ntp verify -Dspotless.check.skip=false
./mvnw -B -q -ntp test jacoco:report
# fail if @Transactional sneaks into controllers
grep -RIn --include='*.java' 'org.springframework.transaction.annotation.Transactional' \
  src/main/java/**/controller/**/*.java && {
    echo "ERROR: @Transactional in controller layer"; exit 1; } || true
# enforce no eager fetching by default
grep -RIn --include='*.java' '@OneToMany\|@ManyToMany\|@OneToOne' src/main/java |
  while read -r line; do
    f=${line%%:*}
    grep -A1 "@OneToMany\|@ManyToMany\|@OneToOne" "$f" | grep -q 'fetch = FetchType.LAZY' || {
      echo "ERROR: eager fetch in $f"; exit 1; }
  done
# disallow System.out / printStackTrace in main code
grep -RIn --include='*.java' 'System\.out\|printStackTrace' src/main && {
  echo "ERROR: stdout/printStackTrace usage"; exit 1; } || true
echo "Spring Boot gate OK"
```

## Best practices
- Pin Spring Boot, Java, Hibernate versions in the prompt; otherwise the agent mixes Jakarta/Javax.
- Service-layer transactions only; controllers stay transaction-free; readOnly=true at class level, override at method.
- Aggregate roots own invariants — no public setters; methods like `promote()`, `markActive()`.
- Use Java 17+ records for DTOs and `@Validated` request records; reject mutable DTO classes.
- Use MapStruct for entity↔DTO; reject hand-rolled mappers without justification.
- Use `ProblemDetail` (RFC 7807) in `@RestControllerAdvice` — agent should never invent custom error envelopes.
- Always pair `@OneToMany` with `@JoinColumn` AND test fetch strategy; default eager is a foot-gun.
- Configure Actuator with security + masking sensitive values (`management.endpoint.env.show-values=NEVER`).

## AI-agent gotchas
- `WebSecurityConfigurerAdapter` is removed in Spring Security 6.x; agent still emits it from training data.
- `@RequestMapping` on class with `produces=MediaType.APPLICATION_JSON_VALUE` then method override drops the produces — re-add per method.
- Hibernate 6 dialect class names changed (`org.hibernate.dialect.PostgreSQLDialect` is fine; `PostgreSQL10Dialect` is gone).
- Agent emits `@Autowired` field injection; prefer constructor injection (Lombok `@RequiredArgsConstructor`).
- Bean validation (`jakarta.validation.constraints`) on records: must use `@Valid` on the controller arg.
- Human checkpoint REQUIRED before: changing `spring.jpa.hibernate.ddl-auto` in any non-dev profile, rotating JWT signing keys, modifying SecurityFilterChain order, enabling `spring.devtools.restart` in prod.
- LazyInitializationException at JSON serialization — agent forgets `@JsonIgnore` on lazy collections or open-in-view = false.
- `application.yml` placeholder fallback `${VAR:default}` mistakenly used for secrets — must read from Vault.

## References
- Spring Boot reference: https://docs.spring.io/spring-boot/.
- Spring Security 6: https://docs.spring.io/spring-security/reference/.
- Spring Data JPA: https://docs.spring.io/spring-data/jpa/reference/.
- Hibernate 6 migration guide: https://github.com/hibernate/hibernate-orm/wiki.
- Baeldung Spring tutorials: https://www.baeldung.com/spring-boot.
- "Spring in Action", Craig Walls (6th ed.).
- "Java Persistence with Spring Data and Hibernate", Catalin Tudose.
- Testcontainers for Java: https://java.testcontainers.org/.
