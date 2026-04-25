# Agent Integration — Node.js Service Layer Implementation

## When to use
- Scaffolding Controller-Service-Repository layers for a new Express/Fastify REST API
- Generating typed DTO interfaces and Zod validation schemas for a route handler
- Converting fat controller functions that mix HTTP and business logic into the 3-layer pattern
- Writing unit tests for service classes with injected repository mocks

## When NOT to use
- Simple one-file scripts or CLI tools without persistent state
- Lambda functions where request → DB → response fits inline and there is no shared business logic
- Read-only proxy services that forward requests to another API without transformation

## Where it fails / limitations
- Dependency injection wired by hand (as in this methodology) breaks down at 30+ services; use a DI container (tsyringe, InversifyJS) instead
- Repository interfaces defined against Prisma-specific types leak ORM concerns into the contract; using ORM-neutral types requires extra mapping boilerplate
- Circular dependencies between services (e.g. UserService needs OrderService and vice versa) cause runtime issues with manual DI — requires restructuring or lazy injection
- Domain errors thrown in services must be caught consistently in all controller catch blocks; missing one causes 500 leaks

## Agentic workflow
An agent receives a feature spec (entity name + CRUD endpoints) and executes the implementation in three sequential steps: generate repository interface and implementation, generate service with business rules, then generate controller and route registration. Each step can be verified by running the TypeScript compiler before moving to the next. A separate test-writing step uses the service interfaces to generate Jest mocks without touching the database.

### Recommended subagents
- `faion-sdd-executor-agent` — executes task files sequentially, suitable for driving multi-step code generation with quality gates between layers

### Prompt pattern
```
Generate a Node.js service layer for entity "<EntityName>".
Requirements:
- Repository: IUserRepository interface + UserRepository class (Prisma)
- Service: IUserService interface + UserService class with business rules: <rules>
- Controller: UserController class (Express)
- Error types: NotFoundError, ConflictError from utils/errors.ts
- Output each file separately with path comments.
```

```
Write Jest unit tests for UserService. Mock IUserRepository using jest.Mocked<>.
Cover: happy path for each method, ConflictError on duplicate email, NotFoundError on missing id.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tsx` | Run TypeScript files directly without build step | `npm i -D tsx` / https://github.com/privatenumber/tsx |
| `tsc --noEmit` | Type-check without emitting JS | Built into TypeScript |
| `jest` | Unit test runner with mock support | `npm i -D jest @types/jest ts-jest` |
| `prisma generate` | Regenerate Prisma client after schema changes | `npx prisma generate` |
| `prisma migrate dev` | Apply migrations during development | https://www.prisma.io/docs/reference/api-reference/command-reference#migrate-dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Prisma ORM | OSS | Yes | Schema-first, generates typed client; agent can read schema to derive repository methods |
| tsyringe | OSS | Yes | Decorator-based DI container for TypeScript; alternative to manual wiring in container.ts |
| InversifyJS | OSS | Yes | More feature-rich DI container; requires `reflect-metadata` polyfill |
| Zod | OSS | Yes | Schema validation; agent can generate schemas from TypeScript interfaces deterministically |
| Vitest | OSS | Yes | Faster alternative to Jest, same API; works with Vite projects |

## Templates & scripts
See `templates.md` for full Controller/Service/Repository file templates.

Minimal DI container bootstrap (inline, 20 lines):
```typescript
// src/container.ts
import { PrismaClient } from '@prisma/client';
import { UserRepository } from './repositories/users.repository';
import { UserService } from './services/users.service';
import { UserController } from './controllers/users.controller';

const prisma = new PrismaClient();
const userRepository = new UserRepository(prisma);
const userService = new UserService(userRepository);
const userController = new UserController(userService);

export { prisma, userRepository, userService, userController };
```

## Best practices
- Define interfaces (`IUserRepository`, `IUserService`) before implementations; agents can then generate mocks from the interface without touching implementation files
- Use `async/await` everywhere and propagate errors via `next(error)` in controllers — never `res.status(500).send(error)` directly
- Keep Prisma inside repositories only; services receive domain types, not `PrismaClient` or Prisma-generated models
- Hash passwords in the service layer, never in the controller or repository
- Use `Promise.all` for parallel independent queries inside repositories (e.g. `findMany` + `count`) to avoid serial round-trips
- Export interfaces from `index.ts` barrel files so consumers import from the feature, not internal paths

## AI-agent gotchas
- Agents generating `container.ts` from scratch may duplicate instantiation if they regenerate the file rather than editing it — always read before writing
- TypeScript strict mode (`"strict": true`) is required for interface mismatch errors to surface; agents should verify `tsconfig.json` before assuming types match
- Prisma-generated `User` type includes all fields; agents may expose `hashedPassword` in API responses unless explicit field omission (`omit`) is applied — include a field-strip step in the prompt
- When an agent adds a new service dependency, it must also update `container.ts`; missing this causes runtime `undefined` errors that pass type-checking
- Human checkpoint needed before running `prisma migrate dev --name <name>` in any environment that has production data

## References
- https://martinfowler.com/eaaCatalog/serviceLayer.html
- https://martinfowler.com/eaaCatalog/repository.html
- https://www.prisma.io/docs
- https://github.com/goldbergyoni/javascript-testing-best-practices
- https://khalilstemmler.com/articles/software-design-architecture/dependency-injection/
