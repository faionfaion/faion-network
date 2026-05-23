# Spring Boot Patterns

## Summary

**One-sentence:** Idiomatic Spring Boot patterns for configuration binding, exception handling, conditional beans, and externalized properties.

**One-paragraph:** Apply Spring Boot's idiomatic patterns — @ConfigurationProperties for type-safe configuration, @ControllerAdvice + ProblemDetail for centralized exception translation, @Conditional bean wiring, and Profiles for environment isolation. The patterns make services portable across environments and surface configuration drift at startup, not at runtime.

**Ефективно для:**

- Сервіси з багатьма env-specific параметрами (dev/staging/prod) — type-safe @ConfigurationProperties.
- Уніфікована обробка помилок REST → ProblemDetail (RFC 7807) через @ControllerAdvice.
- Conditional bean wiring (@ConditionalOnProperty, @ConditionalOnClass) — feature-flag friendly.
- Externalized configuration через application-{profile}.yml + Spring Cloud Config / Vault.

## Applies If (ALL must hold)

- Spring Boot 3.x service with non-trivial configuration surface (>10 properties).
- REST API needs a single uniform error contract (ProblemDetail).
- Multiple deployment environments with different bean wirings.
- Need to expose configuration validation errors at startup (fail fast).

## Skip If (ANY kills it)

- Trivial single-purpose CLI — pattern overhead outweighs benefit.
- Legacy Boot 2.x services — ProblemDetail/binding APIs differ; use Boot 2.x methodology.
- Non-Spring stack (Quarkus, Micronaut) — patterns named differently.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Property surface | list of env vars / config keys | ops |
| Error catalogue | list of business exceptions → HTTP status | API design |
| Profile map | dev/staging/prod yml files | deployment |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Layered architecture is the substrate these patterns plug into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: configuration-properties-typed, controller-advice-problem-detail, conditional-on-property, validation-on-properties, no-system-getenv | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-properties-record` | sonnet | Templated record generation. |
| `design-error-catalogue` | opus | Mapping business exceptions ↔ HTTP status is decision-heavy. |
| `lint-system-getenv` | haiku | Mechanical grep audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/MailProperties.java` | Typed @ConfigurationProperties record with Jakarta Bean Validation |
| `templates/GlobalExceptionHandler.java` | @RestControllerAdvice translating business exceptions to ProblemDetail |
| `templates/application-prod.yml` | Profile-specific configuration overlay (prod) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring-boot-patterns.py` | Validate the Boot-patterns artefact against the schema | Pre-commit + CI |

## Related

- [[java-spring-boot]]
- [[java-spring-async]]
- [[clean-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
