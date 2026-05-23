# JUnit Testing (Spring Boot)

## Summary

**One-sentence:** Layered Spring Boot testing with JUnit 5 + Mockito + AssertJ — @WebMvcTest controllers, plain Mockito services, @DataJpaTest repositories with Testcontainers, Jacoco coverage gate in CI.

**One-paragraph:** Layered testing strategy for Spring Boot 3 applications using JUnit 5 + Mockito + AssertJ. Tests use Spring slices to isolate concerns: `@WebMvcTest(Controller.class)` for HTTP contract, plain `@ExtendWith(MockitoExtension.class)` for service logic, `@DataJpaTest` with Testcontainers Postgres for repositories, `@SpringBootTest` once per module for cross-layer integration. Tests follow `methodUnderTest_state_expectedBehaviour`; assertions use AssertJ on collections; async waits use Awaitility, never `Thread.sleep`. Jacoco enforces line ≥ 70 % / branch ≥ 60 % in CI; mutation testing (Pitest) covers payment / auth / billing paths.

**Ефективно для:**

- Spring Boot apps with REST controllers needing HTTP contract tests.
- Service-layer unit tests requiring Mockito mocks for repository / password encoder / mapper.
- Repository-layer tests with real SQL via `@DataJpaTest` + Testcontainers.
- Teams enforcing coverage gates (line ≥ 70 %, branch ≥ 60 %) via Jacoco.
- Refactor projects that need a safety net before agents modify the service layer.

## Applies If (ALL must hold)

- Spring Boot 3 service standardised on JUnit 5 + Mockito + AssertJ.
- Codebase has separable controller, service, repository layers.
- CI infrastructure can run Docker (for Testcontainers).

## Skip If (ANY kills it)

- Reactive Spring (WebFlux) — `@WebMvcTest` does not apply; use `WebTestClient` + `StepVerifier`.
- Pure library projects with no Spring context — plain JUnit 5 + Mockito suffices.
- Spring Boot < 2.4 targets — test infrastructure here assumes JUnit 5 + AssertJ + recent Boot versions.
- Performance benchmarks — use JMH, not example-based tests.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| SUT class list | Java classpath | dev |
| Coverage thresholds | YAML | platform team |
| Container runtime | Docker on dev/CI hosts | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Umbrella for service layering. |
| [[java-jpa-hibernate]] | Drives `@DataJpaTest` configuration for repositories. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: naming-convention, layer-slice-assignment, assertj-over-junit-assert, awaitility-not-thread-sleep, testcontainers-not-h2, jacoco-gate-in-ci | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the test-plan manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: mocking-wrong-layer, argument-matcher-mixing, mockbean-on-non-bean, springboottest-everywhere, mockedstatic-leak, missing-rollback | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: assign-layer-slice → controller tests → service tests → repository tests → coverage gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-controller-test` | sonnet | MockMvc + jsonPath assertion synthesis. |
| `generate-service-test` | sonnet | Per-branch Mockito stubbing. |
| `audit-springboottest-usage` | haiku | Mechanical scan for `@SpringBootTest` on slice tests. |

## Templates

| File | Purpose |
|------|---------|
| `templates/controller-test.java` | @WebMvcTest skeleton with MockMvc + jsonPath assertions. |
| `templates/service-test.java` | Mockito-only unit test skeleton with AssertJ. |
| `templates/jacoco-gate.sh` | CI wrapper enforcing line/branch thresholds against `jacoco.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-junit-testing.py` | Validate the test-plan manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[java-spring-boot]]
- [[java-jpa-hibernate]]
- [[java-spring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (layer under test, persistence dependency, mock target) to a rule from `01-core-rules.xml`. Use it before authoring or refactoring a Spring Boot test.
