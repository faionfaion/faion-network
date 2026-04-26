# Node.js Service Layer Architecture

## Summary

Architectural scaffold for layered Node.js REST APIs: folder structure, error taxonomy, DI wiring, and layer boundary rules. The core rule: `process.env` access only in `config/index.ts`, never scattered across the codebase; error handler middleware must be registered last in `app.ts` after all routes.

## Why

Without explicit layer boundaries, Node.js apps accumulate business logic in route handlers (fat controllers), Prisma calls leak into services, and error handling is inconsistent. Establishing the error hierarchy in `utils/errors.ts` as the first file and wiring dependencies in `container.ts` as a module-level singleton gives all subsequent feature code a stable foundation to depend on.

## When To Use

- Designing the folder structure and layer boundaries for a new Node.js REST API before writing code
- Establishing dependency injection patterns and container wiring strategy for a team codebase
- Auditing an existing Express app for layer violations (business logic in controllers, Prisma in services)
- Defining error taxonomy and error handler middleware as a shared foundation before feature work

## When NOT To Use

- Prototypes and throwaway scripts where architectural purity adds no return
- Serverless functions (Lambda/Edge) where a cold-start DI container is overhead
- GraphQL APIs with resolver-based patterns where resolvers replace controllers

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Canonical folder layout (controllers, services, repositories, middleware, routes, utils) |
| `content/02-di-and-errors.xml` | container.ts DI wiring pattern, error class hierarchy, errorHandler middleware |
| `content/03-antipatterns.xml` | Business logic in controllers, direct DB in services, PrismaClient singleton violations |

## Templates

| File | Purpose |
|------|---------|
| `templates/errors.ts` | Full AppError hierarchy with NotFoundError, ConflictError, UnauthorizedError, ValidationError |
| `templates/error-handler.ts` | Express error handler middleware (ZodError + AppError + fallback) |
| `templates/container.ts` | Manual DI container wiring Prisma → repositories → services → controllers |
| `templates/layer-violation-check.sh` | Grep script to detect Prisma in services, direct DB in controllers, res.status in services |
