---
slug: java-spring
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Canonical layered architecture for Spring Boot 3.
content_id: "8a0a8ae87e66df63"
tags: [spring-boot, architecture, layered-pattern, jpa, crud]
---
# Java Spring Boot Backend

## Summary

**One-sentence:** Canonical layered architecture for Spring Boot 3.

**One-paragraph:** Canonical layered architecture for Spring Boot 3.x: `@RestController` → `@Service` → `JpaRepository`. Covers CRUD endpoints with Bean Validation, MapStruct DTO mapping, `@Transactional` write methods, and `Pageable` list endpoints. This is the starter Spring Boot pattern; for richer search, Specifications, and ProblemDetail see related methodologies.

## Applies If (ALL must hold)

- New Spring Boot 3.x service with standard CRUD endpoints.
- Adding endpoints with Bean Validation, MapStruct DTO mapping, and paginated list queries.
- Refactoring code that mixes controller/service/repository concerns or returns entity types to clients.
- Wiring BCrypt `PasswordEncoder` and paginated `Pageable` defaults in the service layer.

## Skip If (ANY kills it)

- WebFlux/reactive stack — blocking JPA, `@Transactional`, and `ResponseEntity` semantics differ.
- Hexagonal/Clean Architecture with explicit ports/adapters — layering on top doubles up indirection.
- CQRS or event-sourced systems — service+JPA hides the command/query split.
- Quarkus, Micronaut, or serverless — annotations differ; pattern translates conceptually but not literally.

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
