---
slug: java-junit-testing
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: JUnit 5 + Spring Boot test conventions — @WebMvcTest for controllers, @ExtendWith(MockitoExtension) for services, @DataJpaTest for slices, Testcontainers for integration.
content_id: "c5e3f95d3ba72010"
complexity: medium
produces: code
est_tokens: 4200
tags: [java, junit5, mockito, testing, spring-boot]
---
# JUnit Testing for Spring Boot

## Summary

**One-sentence:** JUnit 5 + Spring Boot test conventions — @WebMvcTest for controllers, @ExtendWith(MockitoExtension) for services, @DataJpaTest for slices, Testcontainers for integration.

**One-paragraph:** Spring Boot test misuse — `@SpringBootTest` everywhere, H2 instead of real DB, manual collaborator construction, no `@ParameterizedTest` — produces slow, flaky CI. This methodology pins five rules: controller tests use `@WebMvcTest` + mock service, service unit tests use `@ExtendWith(MockitoExtension.class)`, repository tests use `@DataJpaTest`, integration tests use `@SpringBootTest(webEnvironment=RANDOM_PORT) + @Testcontainers` with real DB, parametric tests use `@ParameterizedTest`. Output: test-class spec conforming to `02-output-contract.xml`.

**Ефективно для:**

- Layered Spring Boot test suite with right-sized slices.
- Repository tests that catch N+1 + lazy bugs.
- Integration tests that use the actual production DB engine.
- Parametric boundary tests via `@CsvSource`/`@ValueSource`.
- Coverage thresholds enforced in CI via JaCoCo.

## Applies If (ALL must hold)

- Spring Boot 3.x with JUnit Jupiter.
- Mockito 5+, AssertJ, Testcontainers available.
- Postgres (or other real engine) is the production DB.
- CI can run docker (for Testcontainers).

## Skip If (ANY kills it)

- Reactive stack — `@WebFluxTest` patterns differ.
- Plain Java SE without Spring Boot — apply the relevant framework's methodology.
- DB-less microservice — repository slice + Testcontainers irrelevant.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Unit-under-test | Java source | repo |
| Test plan | Markdown | spec |
| Testcontainers + Docker | infra | CI config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring]] | Controller/service layout being tested. |
| [[java-jpa-hibernate]] | Repository slice tests target these patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: webmvctest-for-controllers, mockitoextension-for-services, datajpatest-for-repo-slices, testcontainers-for-integration, parameterizedtest-for-boundaries | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for test-class spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: springboottest-for-everything, h2-for-relational, manual-collaborator-construction, void-async-test | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on test target → rule | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-test-scope` | sonnet | Unit / slice / integration judgment. |
| `write-test-class` | haiku | Mechanical scaffolding once scope chosen. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ControllerTests.java` | @WebMvcTest skeleton |
| `templates/ServiceTests.java` | Mockito service test skeleton |
| `templates/RepositoryTests.java` | @DataJpaTest skeleton |
| `templates/IntegrationTests.java` | @SpringBootTest + Testcontainers skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-junit-testing.py` | Validate test-class spec | Pre-commit on spec artefact |

## Related

- [[java-spring]]
- [[java-jpa-hibernate]]
- [[csharp-xunit-testing]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps target (controller/service/repository/integration) to a rule from `01-core-rules.xml`. Use it whenever picking the right Spring Boot test annotation set.
