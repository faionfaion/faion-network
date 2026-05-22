---
slug: java-junit-testing
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: JUnit 5 (Jupiter) is the standard test framework for modern Spring Boot applications.
content_id: "e1f6c1c935629bbe"
tags: [java, junit5, mockito, testing, spring-boot]
---
# JUnit Testing for Spring Boot

## Summary

**One-sentence:** JUnit 5 (Jupiter) is the standard test framework for modern Spring Boot applications.

**One-paragraph:** JUnit 5 (Jupiter) is the standard test framework for modern Spring Boot applications. Write controller tests via MockMvc or WebTestClient, service unit tests using Mockito annotations (@Mock, @InjectMocks), and repository slice tests via @DataJpaTest. Parameterize tests with @ParameterizedTest and @ValueSource, enforce test isolation through @ExtendWith(MockitoExtension.class), and use Testcontainers for integration tests with real PostgreSQL or MySQL instances. Measure coverage via JaCoCo and enforce thresholds in CI.

## Applies If (ALL must hold)

- Spring Boot applications with controller, service, and repository layers.
- Unit tests for service logic, domain logic, and utility classes using Mockito.
- Slice tests for repositories via @DataJpaTest, catching lazy-loading and query bugs in isolation.
- Integration tests that need a real database (PostgreSQL, MySQL) via Testcontainers.
- Controller tests via MockMvc to verify HTTP endpoints without a full application context.
- CI gates with JaCoCo coverage thresholds.

## Skip If (ANY kills it)

- BDD-flavored prose specs where Cucumber or Gherkin readability is non-negotiable — JUnit 5 is orthogonal to BDD.
- Browser-based end-to-end tests — use Selenium or Playwright with a different harness.
- Microservice contract tests where Pact or Spring Cloud Contract is mandated by a central team.
- Legacy JUnit 4 code where the cost of upgrading exceeds the value — backport patterns carefully if needed.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/dev/software-developer/`
