# Agent Integration — Node.js Service Layer Architecture

## When to use
- Designing the folder structure and layer boundaries for a new Node.js REST API before writing any code
- Establishing dependency injection patterns and container wiring strategy for a team codebase
- Auditing an existing Express app for layer violations (business logic in controllers, Prisma calls in services)
- Defining error taxonomy and error handler middleware as a shared foundation before feature work begins

## When NOT to use
- Prototypes and throwaway scripts where architectural purity adds no return
- Serverless functions (Lambda/Edge) where a cold start DI container is overhead and the function is a single responsibility by design
- GraphQL APIs with resolver-based patterns where the resolver layer replaces controllers and repository-per-field is the norm

## Where it fails / limitations
- Hand-wired DI containers (`container.ts`) become maintenance burdens past 15-20 services — consider tsyringe or InversifyJS at that scale
- The architecture assumes a single database per service; multi-database or event-sourced persistence requires a different repository abstraction
- Service-to-service calls within the same process (e.g. OrderService calling UserService) can introduce hidden coupling; prefer passing resolved data as parameters instead
- TypeScript interfaces for repositories must be kept in sync with Prisma schema changes manually — schema drift is silent until runtime

## Agentic workflow
An agent bootstraps the architecture by first generating the `src/` folder tree (controllers/, services/, repositories/, middleware/, routes/, utils/), then creating the shared error taxonomy in `utils/errors.ts`, then wiring the `container.ts` file. Feature-specific layers (controller, service, repository per entity) are generated separately per entity. An audit agent can scan all controller files for direct Prisma or business-logic calls and report violations.

### Recommended subagents
- `faion-sdd-executor-agent` — sequences architecture setup tasks (error utils → container → entity layers) with type-check gates between steps

### Prompt pattern
```
Generate the Node.js service layer architecture scaffold for a REST API with entities: <EntityA>, <EntityB>.
Stack: Express, TypeScript strict, Prisma ORM.
Output:
1. src/ directory tree (no code, just structure)
2. utils/errors.ts with AppError, NotFoundError, ConflictError, UnauthorizedError, ValidationError
3. middleware/errorHandler.ts that handles ZodError and AppError
4. container.ts with manual DI wiring for all entities
5. routes/index.ts mounting all entity routers
```

```
Audit the controllers/ directory. Flag any function that:
- Uses PrismaClient directly
- Contains if/else business logic beyond input parsing
- Catches errors and builds error responses (instead of calling next(error))
Report violations as a list with file path and line number.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tsx` | Run TypeScript entry point without compile step | `npm i -D tsx` / https://github.com/privatenumber/tsx |
| `tsc --noEmit` | Full type-check without output | Built into TypeScript |
| `tsyringe` | Lightweight decorator-based DI container | `npm i tsyringe reflect-metadata` / https://github.com/microsoft/tsyringe |
| `zod` | Runtime validation + static type inference | `npm i zod` / https://zod.dev |
| `pino` / `winston` | Structured logging for error handler and request logging | `npm i pino` or `npm i winston` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| tsyringe | OSS | Yes | Replaces manual container.ts; agent generates `@injectable()` decorators automatically |
| InversifyJS | OSS | Yes | Full DI container with interface tokens; more verbose but supports async factory providers |
| Prisma | OSS | Yes | Agent reads `schema.prisma` to derive repository method signatures |
| Supertest | OSS | Yes | Integration testing HTTP layer without spinning up a real server; pairs with Jest |
| Hono | OSS | Yes | Lightweight alternative to Express with built-in TypeScript types; same layered pattern applies |

## Templates & scripts
See `templates.md` for full directory scaffold and typed DI container template.

Layer violation check (grep-based, runs in project root):
```bash
#!/bin/bash
echo "=== Prisma in services (should be in repositories only) ==="
grep -rn "PrismaClient\|prisma\." src/services/ || echo "None found"

echo "=== Direct DB calls in controllers ==="
grep -rn "prisma\.\|findUnique\|findMany\|create\|update\|delete" src/controllers/ || echo "None found"

echo "=== res.status in services (should only be in controllers) ==="
grep -rn "res\.status\|res\.json" src/services/ || echo "None found"
```

## Best practices
- Define the error hierarchy in `utils/errors.ts` as the very first file; all subsequent code depends on it and agents need a stable import target
- The error handler middleware must be registered last in `app.ts` after all routes — agents frequently add it before routes, breaking the Express middleware chain
- Keep `container.ts` as a single point of truth for DI wiring; feature agents must read it before adding new constructor injections
- Use `process.env` only in `config/index.ts` — nowhere else; agents tend to scatter `process.env.XYZ` calls across the codebase
- Router files should only import from `container.ts` and middleware — never import services directly
- Integration tests should use a real (test) database rather than mocking repositories, to catch SQL-level bugs invisible to unit tests

## AI-agent gotchas
- Agents generating multiple entity layers in one pass often produce inconsistent naming (UserRepository vs UsersRepository) — enforce a naming convention in the prompt
- The `errorHandler` middleware signature must have 4 parameters (`err, req, res, next`) including the unused `_next`; agents often emit 3-parameter versions that Express does not recognize as error handlers
- Agents writing `container.ts` may instantiate `PrismaClient` inside a function rather than as a module-level singleton, causing a new connection pool per request
- When using `async/await` in route handlers, unhandled promise rejections bypass the error handler unless the controller passes errors to `next()`; agents must wrap every async controller in `try/catch ... next(error)`
- Human checkpoint needed before adding a new service that introduces a circular dependency in container.ts

## References
- https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- https://github.com/goldbergyoni/nodebestpractices
- https://khalilstemmler.com/articles/software-design-architecture/dependency-injection/
- https://martinfowler.com/eaaCatalog/serviceLayer.html
- https://www.prisma.io/docs
