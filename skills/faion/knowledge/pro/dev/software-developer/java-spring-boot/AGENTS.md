---
slug: java-spring-boot
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structure Spring Boot applications with clean architecture.
content_id: "1dd8c718abed52c8"
tags: [spring-boot, java, rest-api, layered-architecture, clean-architecture]
---
# Spring Boot Patterns

## Summary

**One-sentence:** Structure Spring Boot applications with clean architecture.

**One-paragraph:** Structure Spring Boot applications with clean architecture. Build enterprise Java services with the standard layered Controller → Service → Repository stack using Spring Data JPA, Bean Validation, dependency injection, declarative transactions, and Actuator-based observability. The patterns prevent subtle runtime bugs like lazy-load exceptions, N+1 queries, and proxy-based annotation failures.

## Applies If (ALL must hold)

- Greenfield enterprise Java services where the team standardises on a layered Controller → Service → Repository stack with Spring Data JPA + Bean Validation.
- Migrating legacy Java EE / older Spring MVC apps onto Spring Boot 3.x (Jakarta EE 10, virtual threads, Native Image option).
- Building REST APIs that already commit to dependency injection, AOP, declarative transactions, and Actuator-based observability.
- Multi-module Gradle/Maven monorepos where you want a uniform skeleton (controller / service / mapper / dto / entity) generated per module.
- Teams that are JVM-bound (JDK licensing, existing Kafka/Cassandra/Oracle drivers, internal Spring Cloud config server).

## Skip If (ANY kills it)

- Sub-200ms cold-start serverless (Lambda, Cloud Run min-instances=0). Spring Boot startup is heavy; pick Quarkus or Micronaut, or compile to GraalVM native — but then most Spring "magic" silently breaks.
- Polyglot reactive pipelines where the dominant pattern is async streams; Spring WebFlux exists but most teams writing Boot apps default to blocking servlet stack which dilutes the win.
- Tiny solo projects / scripts. The annotation surface and starter explosion (spring-boot-starter-*) is overkill for a CRUD <5 entities.
- When the team has no Spring expertise — Boot's autoconfig debugging is a senior-Java skill (--debug + ConditionEvaluationReport reading).
- Anywhere tight, predictable memory matters (embedded, edge). JVM + Spring is not the right footprint.

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
