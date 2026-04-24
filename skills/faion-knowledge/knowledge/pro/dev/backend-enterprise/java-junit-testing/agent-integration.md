# Agent Integration — JUnit Testing (Spring Boot)

## When to use
- Spring Boot apps where you want layered tests: `@WebMvcTest` for controllers, plain Mockito for services, `@DataJpaTest` for repositories, `@SpringBootTest` for full integration.
- Codebases adopting test-first / TDD with LLM agents — pattern's clear slice boundaries match agent prompts well.
- Teams enforcing a coverage gate (≥70% line, ≥60% branch) — the slice tests + service Mockito tests reach coverage cheaply.
- Apps with REST contracts to maintain — controller tests double as living documentation.
- Refactor projects where you need a safety net before agents touch the service layer.

## When NOT to use
- Reactive Spring (WebFlux) — `@WebMvcTest` does not apply; use `WebTestClient` + `StepVerifier`. Different ergonomics.
- Pure library projects with no Spring context — Spring test slices add no value; plain JUnit 5 + Mockito is enough.
- Projects targeting Spring Boot < 2.4 — `@MockBean` works but the test infrastructure here assumes JUnit 5 + AssertJ + recent versions.
- Domain-heavy DDD codebases where the bulk of behavior is in plain POJOs — favor pure unit tests; reserve Spring slices for I/O boundaries.
- Performance-critical paths where you want JMH benchmarks, not example-based tests.

## Where it fails / limitations
- **Slice cache thrash.** Each `@WebMvcTest(UserController.class)` boots a new context; CI build time balloons. Mixing slice + `@SpringBootTest` defeats Spring's context cache.
- **`@MockBean` cache invalidation.** Adding a `@MockBean` to one slice rebuilds the context; agents adding mocks ad-hoc cripple performance.
- **Mockito + final classes/methods** — needs `mockito-inline`; agents wonder why `mock(KotlinService::class.java)` returns null.
- **Argument matchers + nullability.** `any(User.class)` returns `null`; with Kotlin or `@NonNull` services, NPE inside the SUT.
- **Verification on void calls.** `verify(svc).delete(1L)` after the action ran — but agents sometimes verify before invocation; silent pass.
- **Database state across tests.** `@DataJpaTest` rolls back; `@SpringBootTest` doesn't unless `@Transactional`. Agents mix and pollution leaks.
- **Test-only `application-test.yml` drift.** Properties differ from prod; tests pass, prod fails on missing `spring.flyway.enabled`.
- **Hamcrest vs AssertJ vs JUnit assertions** — codebase ends up with three idioms; LLMs copy the closest one.

## Agentic workflow
Drive JUnit work as: (1) a planner subagent identifies the SUT (controller / service / repo) and emits the slice + dependency mocks; (2) a code-writer subagent generates a test class with Arrange/Act/Assert sections per scenario; (3) a coverage subagent runs `mvn test jacoco:report` and reports per-class line coverage with red/green diff vs threshold; (4) a context-cache subagent flags any `@MockBean`/`@SpyBean` addition that would invalidate the shared context. Persist tests in `src/test/java/.../<SUTName>Test.java`; agents must use the same package as the SUT for package-private access.

### Recommended subagents
- `faion-backend-agent` (referenced in README frontmatter) — implementer for test classes.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs `mvn verify` (compile + test + jacoco threshold) before task close.
- A purpose-built **junit-coverage-agent** (worth creating): wraps Jacoco, parses `target/site/jacoco/jacoco.xml`, returns per-class missed lines + fix proposal mapped to behaviors.
- A **mutation-test-agent** (worth creating): runs `mvn org.pitest:pitest-maven:mutationCoverage` on changed files; flags mutations that survive (tests pass when they shouldn't).
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub `application-test.yml` and seed fixtures (DB URLs, JWT secrets) before commit.

### Prompt pattern
Controller test scaffold:
```
You are a Spring Boot 3.x engineer using JUnit 5 + Mockito +
AssertJ. Generate UserControllerTest covering POST /api/v1/users:
1. Valid body → 201 + JSON shape
2. Invalid email → 400 + errors.email field
3. Existing email → 409 + ConflictResponse
Use @WebMvcTest(UserController.class), @MockBean UserService.
ObjectMapper from autowire. Use jsonPath for body assertions.
Run: ./mvnw test -Dtest=UserControllerTest.
```

Coverage triage:
```
Read target/site/jacoco/jacoco.xml. For each Java class with line
coverage <70%, output: class FQN, missed lines (with source
context), and propose ONE specific test (name + 3-line outline).
Skip generated code (lombok, MapStruct, DTO records).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mvn test` / `gradle test` | Run JUnit | bundled |
| `mvn verify` | Run tests + integration tests + jacoco threshold | bundled |
| Jacoco | Coverage; XML for CI parsing | https://www.jacoco.org |
| PIT (Pitest) | Mutation testing — finds tests that pass when code is broken | `org.pitest:pitest-maven` |
| Surefire / Failsafe | Test report XML for CI | bundled |
| `spring-boot-testcontainers` | Real DB / Kafka / Redis in tests | https://www.testcontainers.org |
| ArchUnit | Layer fitness in tests | `com.tngtech.archunit:archunit-junit5` |
| WireMock | HTTP stubbing in integration tests | `wiremock-jre8` |
| AssertJ | Fluent assertions; agents handle DSL well | bundled with Spring Boot starter test |
| JsonUnit / JSONassert | Strict JSON assertions in controller tests | `net.javacrumbs.json-unit:json-unit-assertj` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions / GitLab CI / Jenkins | CI | yes | Run `mvn verify` + jacoco + Pitest as gates. |
| Codecov / Coveralls | SaaS coverage | API yes | Per-PR coverage diff; agent-readable. |
| SonarCloud / SonarQube | SaaS quality | API yes | Code smells, security, coverage; integrates with PRs. |
| Testcontainers Cloud | SaaS | yes | Remote test container infra; faster local + CI. |
| Spring Initializr | Web | yes | Bootstrap projects with starter-test pre-configured. |
| Snyk / Dependabot | SaaS | yes | Test-scope CVE alerts (e.g., Mockito vulns). |
| LogRocket / Datadog | SaaS APM | yes | Tag releases; correlate test runs with prod errors. |

## Templates & scripts
See `templates.md` for controller/service/repo test skeletons. Add a CI threshold script (≤50 lines):

```bash
#!/usr/bin/env bash
# jacoco-gate.sh — fail if coverage drops below thresholds.
# Usage: jacoco-gate.sh path/to/jacoco.xml LINE BRANCH
set -euo pipefail
XML="${1:?usage: jacoco-gate.sh JACOCO_XML LINE BRANCH}"
LINE="${2:-70}"
BRANCH="${3:-60}"
python3 - "$XML" "$LINE" "$BRANCH" <<'PY'
import sys, xml.etree.ElementTree as ET
xml, line_t, branch_t = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
tree = ET.parse(xml).getroot()
def pct(counter, kind):
    miss = int(counter.attrib.get("missed", 0))
    cov = int(counter.attrib.get("covered", 0))
    total = miss + cov
    return (cov / total * 100) if total else 100.0
line_cov = next((pct(c,"LINE") for c in tree.findall("counter")
                 if c.attrib["type"] == "LINE"), 100.0)
branch_cov = next((pct(c,"BRANCH") for c in tree.findall("counter")
                   if c.attrib["type"] == "BRANCH"), 100.0)
print(f"line={line_cov:.1f}% branch={branch_cov:.1f}%")
fails = []
if line_cov < line_t:   fails.append(f"line {line_cov:.1f} < {line_t}")
if branch_cov < branch_t: fails.append(f"branch {branch_cov:.1f} < {branch_t}")
if fails: print("FAIL:", "; ".join(fails)); sys.exit(1)
print("OK")
PY
```

Wire into `.github/workflows/ci.yml` after `mvn verify`.

## Best practices
- **One test class per SUT.** `UserService` → `UserServiceTest`. Agents finding tests for `UserManager` named `UserManagerTests` waste cycles.
- **Arrange / Act / Assert visible in every test.** Use blank lines or comments — agents emit clean tests when prompted with structure.
- **Test names: `methodUnderTest_state_expectedBehavior`.** `findById_whenUserNotExists_throwsException`. Self-documenting in failure output.
- **AssertJ for non-trivial assertions.** `assertThat(list).extracting(User::getEmail).containsExactly(...)` beats hand-rolled loops.
- **Reuse a single `@SpringBootTest` for full-stack** + many slice tests for layers. Don't sprinkle `@SpringBootTest` everywhere.
- **`@DynamicPropertySource` with Testcontainers** for real DB tests. Avoid H2 — behavior diverges from Postgres.
- **Verify exactly what's needed.** `verify(svc, times(1)).save(any())` over `verify(svc, atLeastOnce())` — flaky.
- **No `Thread.sleep`.** Awaitility (`org.awaitility:awaitility`) for async assertions.
- **Test data via factories** (`given_user_with_role(...)` builders) not via `new User(...)` repeated.
- **Run mutation tests on critical paths** (payment, auth) — coverage alone hides assertion-free tests.
- **Pin Mockito version** that matches Java/Kotlin combo to avoid `final` mocking surprises.

## AI-agent gotchas
- **Mocking the wrong layer.** Agent mocks `UserRepository` in a controller test where Service is also mocked — making the entire flow stubbed and testing nothing. Force the prompt to name what's mocked vs real.
- **Mockito stub mismatch.** `when(svc.findById(1L))...` then SUT calls `findById(1)` (int autoboxing); returns null. Use `anyLong()` or specify type explicitly.
- **Argument matcher mixing.** `verify(svc).save(eq(user), any(Boolean.class))` works; `verify(svc).save(user, any())` throws InvalidUseOfMatchersException. LLMs forget the rule.
- **Static mocking via `mockStatic`.** Agents reach for it for `LocalDateTime.now()`; forgetting `try-with-resources` leaves the static stubbed across tests → flaky.
- **`@MockBean` of a non-bean.** Agent annotates a class that isn't in the context; bean does not exist; test fails cryptically. Use `@Mock` for non-Spring deps.
- **`@WebMvcTest` not loading filters.** Agent expects the security filter; `@WebMvcTest` excludes most autoconfigure. Need `@AutoConfigureMockMvc` + explicit `@Import(SecurityConfig.class)`.
- **Snapshot test instability.** Agents emit `assertEquals(expectedJson, actualJson)` with hard-coded strings; minor JSON ordering breaks. Use `JSONAssert.assertEquals(..., LENIENT)` or JsonUnit.
- **DB-dependent test missing `@Sql`/`@Transactional`.** Agent inserts seed inside the test; next test fails on duplicate key. Use `@Sql(scripts = "classpath:cleanup.sql", executionPhase = AFTER_TEST_METHOD)` or rely on `@Transactional`.
- **Coverage but no assertions.** Agent calls `service.foo()` with `verifyNoMoreInteractions(...)` and no `assertThat` on the return. Test passes regardless. Mutation testing catches.
- **Time-dependent tests.** `assertThat(user.getCreatedAt()).isCloseTo(now(), within(1, SECONDS))` flakes under load. Inject a `Clock` bean and assert exact equality.
- **Test order dependence.** JUnit 5 default is deterministic but not ordered; agents write tests assuming order. Make every test independent or use `@TestMethodOrder`.
- **Reflection on private fields.** Agents use `ReflectionTestUtils` to set private fields instead of constructor injection; couples test to internals. Refactor the SUT instead.
- **Testcontainers on Mac M1/M2.** Agent uses `mysql:5.7` image; arm64 host pulls amd64 image; tests are 4x slower. Pin platform or use `mariadb`/`mysql:8` arm64-native.
- **Forgetting `await` for async controller methods.** Agents test reactive endpoints with MockMvc; need WebTestClient. Hard fail on reactive controllers in `@WebMvcTest`.

## References
- Spring Framework — Testing reference. https://docs.spring.io/spring-framework/reference/testing.html
- Spring Boot — Testing the web layer. https://spring.io/guides/gs/testing-web/
- JUnit 5 User Guide. https://junit.org/junit5/docs/current/user-guide/
- Mockito reference. https://site.mockito.org
- AssertJ docs. https://assertj.github.io/doc/
- Testcontainers docs. https://www.testcontainers.org
- Pitest (mutation testing). https://pitest.org
- Phil Webb — "Spring Boot Testing Best Practices." https://spring.io/blog
- Sibling methodologies in this repo: `pro/dev/backend-enterprise/java-spring-boot/`, `pro/dev/backend-enterprise/java-spring-boot-patterns/`, `pro/dev/backend-enterprise/java-jpa-hibernate/`, `pro/dev/backend-enterprise/csharp-xunit-testing/`, `pro/dev/backend-enterprise/ruby-rspec-testing/`.
