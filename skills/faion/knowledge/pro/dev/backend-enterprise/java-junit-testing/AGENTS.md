# JUnit Testing (Spring Boot)

## Summary

Layered testing strategy for Spring Boot applications using JUnit 5 + Mockito + AssertJ. Uses Spring test slices (`@WebMvcTest` for controllers, plain Mockito for services, `@DataJpaTest` for repositories, `@SpringBootTest` for full integration) to isolate each layer, keeping tests fast and failure messages diagnostic.

## Why

Spring test slices boot only the relevant application context slice, cutting build time vs full `@SpringBootTest` on every test. Layer isolation (real controller, mocked service) catches HTTP contract bugs without a database. Naming convention `methodUnderTest_state_expectedBehavior` makes CI failure output self-documenting. Coverage + mutation testing together catch assertion-free tests that pass regardless of behavior.

## When To Use

- Spring Boot app with REST controllers that need HTTP contract tests.
- Service-layer unit tests requiring Mockito mocks for repository, password encoder, or mapper.
- Repository-layer tests with real SQL via `@DataJpaTest` + Testcontainers.
- Teams enforcing coverage gates (line >=70%, branch >=60%) via Jacoco.
- Refactor projects that need a safety net before agents modify the service layer.

## When NOT To Use

- Reactive Spring (WebFlux) — `@WebMvcTest` does not apply; use `WebTestClient` + `StepVerifier`.
- Pure library projects with no Spring context — Spring test slices add no value; plain JUnit 5 + Mockito is enough.
- Spring Boot < 2.4 targets — test infrastructure here assumes JUnit 5 + AssertJ + recent Boot versions.
- Domain-heavy DDD codebases where behavior lives in plain POJOs — favor pure unit tests; reserve Spring slices for I/O boundaries.
- Performance benchmarks — use JMH, not example-based tests.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Naming, Arrange/Act/Assert structure, layer assignment, coverage thresholds. |
| `content/02-examples.xml` | Controller slice test, service Mockito test, async assertion with Awaitility. |
| `content/03-antipatterns.xml` | Common agent mistakes: self-invocation mock, `@MockBean` cache thrash, missing `@Transactional`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/controller-test.java` | `@WebMvcTest` skeleton with MockMvc, ObjectMapper, `@MockBean`. |
| `templates/service-test.java` | `@ExtendWith(MockitoExtension.class)` skeleton with `@InjectMocks`. |
| `templates/jacoco-gate.sh` | CI script: parse `jacoco.xml`, fail if line/branch coverage below threshold. |
