---
slug: nodejs-service-layer
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Controller-Service-Repository pattern for Node.
content_id: "876064ba4999df8f"
tags: [nodejs, typescript, architecture, layered, service-layer]
---
# Node.js Service Layer

## Summary

**One-sentence:** Controller-Service-Repository pattern for Node.

**One-paragraph:** Controller-Service-Repository pattern for Node.js/TypeScript backends. Controllers validate input with Zod and map errors to HTTP; services own all business logic and throw typed domain errors; repositories encapsulate ORM/SQL. Each layer has a single responsibility and no cross-layer imports (controller never imports repository).

## Applies If (ALL must hold)

- Express, Fastify, NestJS, or Hono services with non-trivial domain logic.
- Multi-entry backends (HTTP + gRPC + queue consumers) reusing the same service.
- Projects targeting high unit-test coverage — controller-heavy code resists testing.
- LLM-driven implementation: three specific shapes (controller/service/repository) reduce free decisions and bugs.

## Skip If (ANY kills it)

- Toy CRUD apps where every handler is db.find().lean() — extra layers add ceremony with no payoff.
- Edge functions / serverless with strict cold-start budgets — DI containers slow boot.
- Pure proxies / BFFs with no domain logic — route → fetch → respond is enough.
- Realtime-heavy apps (WebSocket gaming, MQTT) where event handlers don't fit request-response shape.

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

- parent skill: `solo/dev/software-developer/`
