# Node.js Service Layer Implementation

## Summary

Practical TypeScript implementation of the Controller-Service-Repository pattern for Express APIs: controllers handle HTTP only, services own business logic, repositories own all database access. The core rule: hash passwords in the service layer, never in the controller or repository; Prisma stays inside repositories only.

## Why

Without layer boundaries, business logic accumulates in controllers (fat controllers), making it untestable without spinning up HTTP infrastructure. The repository interface abstraction (`IUserRepository`) enables Jest mocks that replace real database calls in unit tests, allowing service business rules to be tested in isolation at millisecond speed.

## When To Use

- Scaffolding Controller-Service-Repository layers for a new Express/Fastify REST API
- Generating typed DTO interfaces and Zod validation schemas for a route handler
- Converting fat controller functions that mix HTTP and business logic into the 3-layer pattern
- Writing unit tests for service classes with injected repository mocks

## When NOT To Use

- Simple one-file scripts or CLI tools without persistent state
- Lambda functions where request → DB → response fits inline with no shared business logic
- Read-only proxy services that forward requests to another API without transformation

## Content

| File | What's inside |
|------|---------------|
| `content/01-repository.xml` | IUserRepository interface, UserRepository implementation with Prisma, paginated findAll |
| `content/02-service.xml` | IUserService interface, UserService with business rules, NotFoundError/ConflictError usage |
| `content/03-controller.xml` | UserController with Express, Zod validation, error delegation to next() |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-repository.ts` | Full IUserRepository interface + UserRepository class (Prisma) |
| `templates/user-service.ts` | Full IUserService interface + UserService class with business rules |
| `templates/user-controller.ts` | Full UserController class (Express, Zod schemas) |
| `templates/errors.ts` | AppError hierarchy: NotFoundError, ConflictError, UnauthorizedError, ValidationError |
| `templates/container.ts` | Manual DI wiring: Prisma → Repository → Service → Controller |
