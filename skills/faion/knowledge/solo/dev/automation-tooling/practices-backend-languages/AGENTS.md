---
slug: practices-backend-languages
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reference patterns for six backend languages: Go (cmd/internal/pkg layout, wrapped errors, consumer-side interfaces, worker-pool concurrency), Ruby on Rails (service/form/query objects), PHP Laravel (service pattern), Java Spring Boot (constructor injection), C#.
content_id: "763560296b823227"
tags: [go, rust, backend, coding-standards, multi-language]
---
# Backend Languages Practices

## Summary

**One-sentence:** Reference patterns for six backend languages: Go (cmd/internal/pkg layout, wrapped errors, consumer-side interfaces, worker-pool concurrency), Ruby on Rails (service/form/query objects), PHP Laravel (service pattern), Java Spring Boot (constructor injection), C#.

**One-paragraph:** Reference patterns for six backend languages: Go (cmd/internal/pkg layout, wrapped errors, consumer-side interfaces, worker-pool concurrency), Ruby on Rails (service/form/query objects), PHP Laravel (service pattern), Java Spring Boot (constructor injection), C# .NET (async repository pattern), Rust (thiserror Result types, tokio async). One canonical snippet per pattern.

## Applies If (ALL must hold)

- Greenfield service scaffolding in any of the six languages — use as layout template.
- Cross-language onboarding: agent must produce equivalent shape in two stacks.
- Refactor passes aligning an existing module to the known-good shape.
- Code review gate — check Go interfaces are consumer-side, Spring uses constructor injection.

## Skip If (ANY kills it)

- Architecture decisions (microservices vs monolith) — see dev-methodologies-architecture.
- Testing patterns — see dev-methodologies-testing.
- Performance profiling or observability — out of scope.
- When the project already has a documented house style that diverges — agent will overwrite.

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

- parent skill: `solo/dev/automation-tooling/`
