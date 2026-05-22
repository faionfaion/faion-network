---
slug: java-spring-boot
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Spring Boot 3.
content_id: "1dd8c718abed52c8"
tags: [java, spring-boot, backend, rest-api, layered-architecture]
---
# Spring Boot Patterns

## Summary

**One-sentence:** Spring Boot 3.

**One-paragraph:** Spring Boot 3.x layered architecture with controller → service → repository pattern, DTOs separate from JPA entities, Lombok for immutability, MapStruct for mapping, Bean Validation for inputs, ProblemDetail for error responses, and @Transactional boundaries on service operations.

## Applies If (ALL must hold)

- Bootstrapping or extending a Spring Boot 3.x service with the canonical Controller → Service → Repository layering, DTOs separate from JPA entities, and @Transactional boundaries on the service layer.
- Generating new resource endpoints (REST or gRPC) that follow existing project conventions: Lombok, MapStruct, Bean Validation, ProblemDetail error handling.
- Refactoring legacy Spring MVC code toward constructor injection, immutable DTOs, and Pageable/Page<T> paging.
- Adding cross-cutting concerns via filters, interceptors, or @RestControllerAdvice rather than duplicating logic.

## Skip If (ANY kills it)

- The team chose Quarkus, Micronaut, or Helidon — Spring's reflection-heavy startup and AOT story differs; don't backport patterns.
- Pure event-driven workers without HTTP — use Spring Modulith or plain @KafkaListener/@RabbitListener services; the controller layer is dead weight.
- Reactive stack (spring-webflux) — most templates here assume blocking servlet stack; Mono/Flux plumbing is different.
- Native image (GraalVM) without explicit reachability config — Lombok + reflection-based Jackson causes hidden failures at runtime.

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
