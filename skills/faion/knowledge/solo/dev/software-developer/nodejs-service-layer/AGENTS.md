# Node.js Service Layer

## Summary

Controller-Service-Repository pattern for Node.js/TypeScript backends. Controllers validate input with Zod and map errors to HTTP; services own all business logic and throw typed domain errors; repositories encapsulate ORM/SQL. Each layer has a single responsibility and no cross-layer imports (controller never imports repository).

## Why

Thin controllers and pure services are unit-testable without an HTTP server. Repository abstraction lets the service layer swap DB implementations. Domain errors — not HTTP codes — inside services mean the same logic can be invoked from HTTP, gRPC, queues, or CLIs. `eslint-plugin-boundaries` + `dependency-cruiser` enforce the layering automatically.

## When To Use

- Express, Fastify, NestJS, or Hono services with non-trivial domain logic.
- Multi-entry backends (HTTP + gRPC + queue consumers) reusing the same service.
- Projects targeting high unit-test coverage — controller-heavy code resists testing.
- LLM-driven implementation: three specific shapes (controller/service/repository) reduce free decisions and bugs.

## When Not To Use

- Toy CRUD apps where every handler is `db.find().lean()` — extra layers add ceremony with no payoff.
- Edge functions / serverless with strict cold-start budgets — DI containers slow boot.
- Pure proxies / BFFs with no domain logic — `route → fetch → respond` is enough.
- Realtime-heavy apps (WebSocket gaming, MQTT) where event handlers don't fit request-response shape.

## Content

| File | What's inside |
|------|---------------|
| `content/01-layers.xml` | Layer responsibilities, dependency direction rules, DI wiring pattern. |
| `content/02-error-handling.xml` | Domain error hierarchy, central ErrorMapper, controller error-translation rule. |
| `content/03-antipatterns.xml` | Business logic in controllers, direct DB access in services, DTO drift, async error swallowing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-repository.ts` | IUserRepository interface + Prisma implementation. |
| `templates/user-service.ts` | UserService with DI, domain errors, business logic. |
| `templates/user-controller.ts` | Thin Express controller — validate, call service, map errors. |
| `templates/errors.ts` | AppError hierarchy + central ErrorMapper. |
| `templates/layer-check.sh` | Bash script using dependency-cruiser to block cross-layer imports in CI. |
