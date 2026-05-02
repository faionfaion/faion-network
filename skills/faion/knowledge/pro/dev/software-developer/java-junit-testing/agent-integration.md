# Agent Integration — JUnit Testing (Spring Boot)

## When to use
- Adding a JUnit 5 + Spring Test layer to an existing Spring Boot 2.7 / 3.x service that has shipped without controller, repository, or service tests.
- Backfilling tests during a CRUD-to-CQRS or REST-to-GraphQL migration where contracts must be locked down before refactor.
- Generating `@WebMvcTest`, `@DataJpaTest`, `@SpringBootTest` skeletons for new endpoints as part of an SDD task.
- Driving Testcontainers-backed integration tests where the in-memory `H2` shortcut has been hiding bugs vs. real Postgres / MySQL.
- Establishing coverage gates (JaCoCo) and converting them into pre-commit / CI policy.
- Standardizing assertion style across a codebase (AssertJ over Hamcrest over JUnit's built-ins).

## When NOT to use
- Pure Java SE library code with no Spring context — drop the `@SpringBootTest` ceremony, use plain JUnit 5.
- Reactive WebFlux services — `@WebMvcTest` is wrong; use `@WebFluxTest` + `WebTestClient`. Agents will mis-pick the slice.
- Kotlin Spring projects where Kotest + MockK is the team's standard — don't impose JUnit by default.
- Throwaway prototypes / spike branches where coverage gates impede learning.
- Microservices using contract testing (Pact / Spring Cloud Contract) as the primary test strategy — `@WebMvcTest` duplicates coverage that the contract already enforces.

## Where it fails / limitations
- **`@WebMvcTest` only loads MVC layer.** Filters, security, and config beans are partially loaded. Agents miss-diagnose 401/403 in tests because `SecurityFilterChain` isn't in the slice; need `@AutoConfigureMockMvc` + explicit `@Import` of security config or `@SpringBootTest`.
- **`@MockBean` is deprecated as of Spring Boot 3.4.** New code should use `@MockitoBean`. README still uses `@MockBean`. Agents trained pre-2024 will keep emitting deprecated annotations.
- **`@DataJpaTest` defaults to H2.** Most JPA bugs are dialect-specific (SQL functions, `JSONB`, `RETURNING`, sequences). Tests pass, prod fails. Force `@AutoConfigureTestDatabase(replace = NONE)` + Testcontainers.
- **`MockMvc` doesn't run servlet container.** Filters that depend on container behavior (async dispatch, error pages) silently no-op. Use `@SpringBootTest(webEnvironment = RANDOM_PORT)` + `TestRestTemplate` / `WebTestClient` to catch these.
- **Test context caching pitfalls.** Each unique `@SpringBootTest` configuration spins a new context. Agents add `@TestPropertySource` per test method and balloon CI from 2 min to 30 min.
- **`@Transactional` on tests hides bugs.** Rolls back commits, hiding triggers, constraints, and CDC behavior. Required for some, harmful for others — agents apply blanket.
- **JaCoCo line coverage ≠ behavior coverage.** Agents target percentage and write tautological tests; mutation testing (PIT) is what catches no-op tests.

## Agentic workflow
Drive JUnit test scaffolding as a four-stage pipeline: (1) a slice-picker agent reads the controller / service / repository under test and selects the right Spring slice (`@WebMvcTest`, `@DataJpaTest`, `@SpringBootTest`); (2) a test-gen agent emits given/when/then-named tests using AssertJ + MockMvc + Mockito with one assertion focus per test; (3) a flake-hunter agent enables `@RepeatedTest(20)` for new tests on CI to surface order/clock/random flakes; (4) a coverage-review agent runs JaCoCo + PIT and flags low-mutation-score classes. Use `faion-sdd-executor-agent` to bind one test class per SDD task; tests must run green before the task closes.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — opus model fits because slice selection (when to use `@WebMvcTest` vs. `@SpringBootTest`) is decision-heavy.
- `feature-executor` skill — sequential mode is correct: write controller test → service test → repository test → integration test, each gating on green.
- A purpose-built **junit-style-lint agent** (worth adding under `agents/`): grep-based linter for the common drift (`assertEquals` instead of AssertJ, `@MockBean` instead of `@MockitoBean` on Spring Boot ≥3.4, missing `@DisplayName`, H2 in `@DataJpaTest`).
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — run before committing test fixtures; agents copy real-looking emails / tokens into `@Sql` seed scripts.
- For Testcontainers workflows, pair with sibling `pro/infra/devops-engineer/docker-*` methodologies; the agent should know how to start `PostgreSQLContainer` once per JVM.

### Prompt pattern
Slice selection + test generation:
```
You are writing JUnit 5 tests for a Spring Boot 3.4 application.
Given the class under test:
  - If it is a @RestController, use @WebMvcTest(<Controller>.class)
    + @MockitoBean for collaborators + MockMvc + AssertJ.
  - If it is a @Service with no web/JPA, use plain JUnit + Mockito
    @ExtendWith(MockitoExtension.class). NO @SpringBootTest.
  - If it is a @Repository (JpaRepository), use @DataJpaTest +
    @AutoConfigureTestDatabase(replace = NONE) + Testcontainers
    PostgreSQLContainer. NEVER fall back to H2.
  - If integration across layers is required, use
    @SpringBootTest(webEnvironment = RANDOM_PORT) + TestRestTemplate.
Each test method named <method>_When<Condition>_Then<Outcome>. Use
@DisplayName for human-readable description. AssertJ for all asserts.
```

Anti-pattern review:
```
You are reviewing a PR adding JUnit tests. Flag any of:
(1) @MockBean used on Spring Boot >= 3.4 (use @MockitoBean),
(2) @DataJpaTest without @AutoConfigureTestDatabase(replace = NONE),
(3) assertEquals / assertTrue from JUnit instead of AssertJ,
(4) @Transactional on a test that hits async / scheduled / @EventListener
   code (rollback hides bugs),
(5) test class extending another test class to share fixtures
   (use composition / @TestConfiguration),
(6) missing @DisplayName on tests with non-self-explanatory names.
Cite file:line. Do not propose fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mvn` / `gradle` | Run tests, JaCoCo, fail builds | https://maven.apache.org , https://gradle.org |
| Spring Boot CLI | `spring init` + scaffolding | https://docs.spring.io/spring-boot/docs/current/reference/html/getting-started.html#getting-started.installing.cli |
| JUnit Platform Console Launcher | Run JUnit outside Maven/Gradle | `--scan-classpath` ; https://junit.org/junit5 |
| JaCoCo CLI | Coverage report from `.exec` files | https://www.jacoco.org/jacoco |
| PIT mutation testing | Mutation-score gate on the suite | `mvn org.pitest:pitest-maven:mutationCoverage` ; https://pitest.org |
| Testcontainers Desktop | Local Docker / Cloud runners for IT | https://testcontainers.com/desktop |
| AssertJ Assertions Generator | Generate fluent custom assertions | https://joel-costigliola.github.io/assertj/assertj-assertions-generator.html |
| WireMock CLI | Stub external HTTP for `@SpringBootTest` runs | https://wiremock.org |
| Spring REST Docs / OpenAPI generator | Doc generation from MockMvc tests | https://docs.spring.io/spring-restdocs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Testcontainers (Docker) | OSS | yes | Real DB / Kafka / Redis for IT; default for `@DataJpaTest`. |
| WireMock / WireMock Cloud | OSS / SaaS | yes | HTTP stubs for downstream services in `@SpringBootTest`. |
| Pact / PactFlow | OSS / SaaS | yes | Contract testing — replaces some `@WebMvcTest` coverage. |
| LocalStack | OSS | yes | AWS-API-faithful container for IT against S3/SQS/SNS/DDB. |
| GitHub Actions / GitLab CI / CircleCI | SaaS | yes | All run JUnit + JaCoCo reports natively. |
| Codecov / Coveralls | SaaS | yes | Coverage reporting + PR comments. |
| SonarQube / SonarCloud | OSS / SaaS | yes | Adds mutation, quality gates beyond JaCoCo. |
| Allure Report | OSS | yes | Rich HTML reports from JUnit; agents can read failures faster. |
| Arquillian | OSS | partially | Old-school Java EE container test; mostly replaced by `@SpringBootTest`. |
| MockServer | OSS | yes | Alternative to WireMock; HTTPS + proxy modes. |
| Spring Cloud Contract | OSS | yes | Generates JUnit + WireMock from contracts. |

## Templates & scripts

The methodology already ships `@WebMvcTest`, service, and repository templates in `README.md` / `templates.md`. Gap: a script that audits the suite for the common drift the README's examples were written before (e.g., `@MockBean` deprecation in Boot 3.4). Inline drop-in (≤50 lines) — `scripts/junit-suite-audit.sh`:

```bash
#!/usr/bin/env bash
# junit-suite-audit.sh — detect deprecated annotations and slice misuse.
# Usage: junit-suite-audit.sh <project-root>
set -euo pipefail
root="${1:?usage: junit-suite-audit.sh PROJECT_ROOT}"
fail=0
echo "# JUnit suite audit ($root)"

echo "## Deprecated @MockBean usage (Spring Boot >= 3.4)"
grep -rEn '@MockBean' "$root/src/test" --include='*.java' \
  | tee /tmp/junit.mockbean || true
[[ -s /tmp/junit.mockbean ]] && fail=1

echo "## H2 fallback in @DataJpaTest (must use Testcontainers)"
grep -rlE '@DataJpaTest' "$root/src/test" --include='*.java' \
  | xargs -I{} grep -L 'AutoConfigureTestDatabase(replace = .*NONE\|Testcontainers\|@Container' {} \
  | tee /tmp/junit.h2 || true
[[ -s /tmp/junit.h2 ]] && fail=1

echo "## JUnit assertions instead of AssertJ"
grep -rEn '\bassertEquals\(|\bassertTrue\(|\bassertFalse\(|\bassertNotNull\(' \
  "$root/src/test" --include='*.java' \
  | tee /tmp/junit.junit-asserts || true
[[ -s /tmp/junit.junit-asserts ]] && fail=1

echo "## @SpringBootTest leaking into unit tests (>1s startup tax)"
grep -rEn '@SpringBootTest' "$root/src/test" --include='*Service*Test.java' \
  | tee /tmp/junit.heavy || true
[[ -s /tmp/junit.heavy ]] && fail=1

echo "## Tests missing @DisplayName"
grep -rEn '@Test' "$root/src/test" --include='*.java' -A 2 \
  | grep -B 2 'void test' | grep -v '@DisplayName' \
  | tee /tmp/junit.no-name || true

exit "$fail"
```

Wire into `mvn verify` via the `exec-maven-plugin` or as a pre-commit hook for the test directory.

## Best practices
- **One slice per test class.** `@WebMvcTest` for controllers, plain JUnit + Mockito for services, `@DataJpaTest` for repositories. Mixing slices in one test class blows context cache and slows CI.
- **AssertJ everywhere.** `assertThat(result).extracting(User::getEmail).contains("john@example.com")` is grep-able and self-documenting. Banned: `assertEquals`, `assertTrue`, raw `Hamcrest`.
- **`@MockitoBean` over `@MockBean` on Spring Boot ≥3.4.** Old README needs migration. Lint catches it.
- **Testcontainers with shared static container.** `@Container static PostgreSQLContainer postgres = new PostgreSQLContainer("postgres:16")` lives in a base class with `@Testcontainers` so it starts once per JVM, not per test.
- **`@DynamicPropertySource` for container ports.** Don't hard-code 5432; let Testcontainers assign and inject via `registry.add("spring.datasource.url", postgres::getJdbcUrl)`.
- **Naming: `methodUnderTest_givenCondition_thenOutcome`.** Or use `@DisplayName` for human-readable. Don't ship "test1, test2".
- **One assertion focus per test.** Multiple soft asserts via `SoftAssertions.assertSoftly(...)` if needed; never two unrelated `assertThat` calls testing different behaviors.
- **No `@SpringBootTest` for service unit tests.** It's a 1–5 second tax per class. Use plain JUnit + Mockito for services with no web/JPA dependencies.
- **Mutation score over line coverage.** Add PIT to CI and gate on a ratchet (e.g., never below 65%); raise floor over time.
- **Faker over hard-coded strings.** `Instancio` / `EasyRandom` / Java Faker for fixtures; reduces fixture drift across tests.
- **Test data builders, not setters.** `aUser().withRole(ADMIN).build()` — agents extend builders coherently; setter chains drift.

## AI-agent gotchas
- **Deprecated annotation reflex.** Agents emit `@MockBean`, `@RunWith(SpringRunner.class)`, `@Before` (JUnit 4 style). Pin Spring Boot version + JUnit version in the prompt and reject pre-Jupiter style.
- **Agents over-use `@SpringBootTest`.** It's the easiest to scaffold but the slowest. Force the agent to justify any `@SpringBootTest` over a slice annotation.
- **Mocking what you don't own.** Agents mock `RestTemplate` / `WebClient` directly; better to mock the typed gateway interface that wraps them. Otherwise tests bind to library API surface.
- **Asserting log messages.** Agents add `assertThat(output.getOut()).contains("user created")` — fragile, ties tests to log strings. Reject.
- **Hidden test ordering dependence.** Agents share state via static fields between tests. JUnit 5 `@TestMethodOrder` rescues none of it. Force `@TestInstance(Lifecycle.PER_METHOD)` + `@DirtiesContext` where state actually leaks.
- **Hard-coded random.** `Math.random()` / `LocalDateTime.now()` in tests. Force `Clock` injection and a `Random` with fixed seed; otherwise CI is non-deterministic.
- **`Thread.sleep` in async tests.** Replace with `Awaitility.await().atMost(Duration.ofSeconds(2)).until(...)`.
- **Fixture explosion.** Agents copy-paste full JSON request bodies into every test. Prefer `@Sql` scripts + builders; one fixture file per aggregate.
- **`@MockBean` invalidates context cache.** Each unique combination of mocked beans = a new ApplicationContext. Agents add `@MockBean` liberally and CI time triples. Justify each one.
- **Tests pass on H2, fail on Postgres.** Agents accept `@DataJpaTest` defaults. Force Testcontainers via base class or explicit `@AutoConfigureTestDatabase(replace = NONE)` + assert.
- **Coverage chasing.** Asked to "raise coverage to 90%", agents write tests that call methods and assert nothing. Add PIT mutation score as the gate, not lines.
- **Human-in-the-loop on flaky tests.** Agents `@Disabled` flaky tests to make CI green. Disabled tests must be reviewed by a human within 24h or removed.

## References
- Spring Boot Testing — https://docs.spring.io/spring-boot/reference/testing/index.html
- JUnit 5 User Guide — https://junit.org/junit5/docs/current/user-guide/
- AssertJ Core — https://assertj.github.io/doc/
- Testcontainers Java — https://java.testcontainers.org/
- Mockito — https://site.mockito.org/
- PIT Mutation Testing — https://pitest.org/
- WireMock — https://wiremock.org/docs/
- Spring REST Docs — https://docs.spring.io/spring-restdocs/docs/current/reference/html5/
- Pact JVM — https://docs.pact.io/implementation_guides/jvm
- Sibling methodologies: `pro/dev/software-developer/java-spring-boot/`, `java-spring-async/`, `java-spring-boot-patterns/`, `java-jpa-hibernate/`, `csharp-xunit-testing/`, `php-phpunit-testing/`, `ruby-rspec-testing/`.
