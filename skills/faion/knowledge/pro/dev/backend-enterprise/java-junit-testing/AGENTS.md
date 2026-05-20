---
slug: java-junit-testing
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Layered testing strategy for Spring Boot applications using JUnit 5 + Mockito + AssertJ.
content_id: "e1f6c1c935629bbe"
tags: [junit, testing, spring-boot, mockito, coverage]
---
# JUnit Testing (Spring Boot)

## Summary

**One-sentence:** Layered testing strategy for Spring Boot applications using JUnit 5 + Mockito + AssertJ.

**One-paragraph:** Layered testing strategy for Spring Boot applications using JUnit 5 + Mockito + AssertJ. Uses Spring test slices (`@WebMvcTest` for controllers, plain Mockito for services, `@DataJpaTest` for repositories, `@SpringBootTest` for full integration) to isolate each layer, keeping tests fast and failure messages diagnostic.

## Applies If (ALL must hold)

- Spring Boot app with REST controllers that need HTTP contract tests.
- Service-layer unit tests requiring Mockito mocks for repository, password encoder, or mapper.
- Repository-layer tests with real SQL via `@DataJpaTest` + Testcontainers.
- Teams enforcing coverage gates (line ≥70%, branch ≥60%) via Jacoco.
- Refactor projects that need a safety net before agents modify the service layer.

## Skip If (ANY kills it)

- Reactive Spring (WebFlux) — `@WebMvcTest` does not apply; use `WebTestClient` + `StepVerifier`.
- Pure library projects with no Spring context — Spring test slices add no value; plain JUnit 5 + Mockito is enough.
- Spring Boot < 2.4 targets — test infrastructure here assumes JUnit 5 + AssertJ + recent Boot versions.
- Domain-heavy DDD codebases where behavior lives in plain POJOs — favor pure unit tests; reserve Spring slices for I/O boundaries.
- Performance benchmarks — use JMH, not example-based tests.

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

- parent skill: `pro/dev/backend-enterprise/`
