# Agent Integration — Node.js Service Layer

## When to use
- Building Express, Fastify, NestJS, or Hono services where business logic should be decoupled from HTTP framework specifics.
- Multi-team backends where services are reused across HTTP, gRPC, queues, and CLI entry points.
- Apps with non-trivial domain logic (payments, billing, scheduling) that benefit from unit-tested pure services.
- Codebases that target high test coverage; controller-heavy code resists unit testing.
- LLM-driven implementation: the controller / service / repository pattern gives agents three specific shapes to fill — fewer free decisions, fewer bugs.

## When NOT to use
- Toy CRUD apps where every endpoint is `db.find().lean()` — extra layers add ceremony with no payoff.
- Edge functions / serverless with strict cold-start budgets — extra DI containers and class instantiation slow boot.
- Pure proxies / BFFs that compose other services and have no domain logic — `route → fetch → respond` is enough.
- Realtime-heavy apps (WebSocket gaming, MQTT) where event handlers don't fit a request-response service shape.
- Tiny CLIs / scripts — overkill.

## Where it fails / limitations
- Anaemic services: every method is `repo.findById`-and-return; the layer adds cost without value. A symptom, not the pattern's fault.
- Manual DI bowls of spaghetti: hand-wired constructors get unmanageable past ~30 services; tools like `tsyringe`, `awilix`, or NestJS DI become necessary.
- Repository over-abstraction: hiding ORM features (eager loading, query builders, transactions) behind generic `find(filter)` cripples performance and forces leaky workarounds.
- Cross-service transactions: two services calling two repos can't rely on a request-scoped DB transaction unless explicitly threaded; bugs manifest as partial writes.
- TypeScript boundaries: agents widen DTOs to `any` to "make it compile"; runtime payloads diverge from types.
- Error-mapping leaks: domain errors end up as 500s because controllers don't translate them to HTTP — kills observability.
- Test fixtures explode: every service test mocks 3 repos; brittle and slow. Symptom of poor seam design.
- "Service" becomes "the place I dump utility functions" — naming rot.

## Agentic workflow
A four-stage flow per feature. (1) **Spec → DTOs**: an agent generates Zod / TypeBox schemas for request, response, and domain entities; controllers and services derive types from the schemas. (2) **Service skeleton**: agent creates `<feature>.service.ts` with constructor injection of repository + clients, returns domain types only. (3) **Controller**: thin handler validates with the schema, calls the service, maps domain errors to HTTP via a central error mapper. (4) **Tests**: unit tests for the service with mocked repo, integration tests for the controller using `supertest` or `light-my-request` (Fastify). `faion-sdd-executor-agent` enforces "controller has no business logic; service has no req/res" as a structural rule.

### Recommended subagents
- `faion-sdd-executor-agent` — gates: controllers don't import repos, services don't import `Request`/`Response`, every public service method has unit tests with ≥1 happy + ≥1 error path.
- A **layer-linter** subagent (worth creating): walks the dependency graph and fails when controller→repo or service→framework imports appear. Cheap to run with `dependency-cruiser` / `eslint-plugin-boundaries`.
- A **DTO-from-schema** subagent: given Zod / TypeBox schemas, generates request/response types and OpenAPI fragments.
- `feature-executor` (skill) — sequence schema → service → repo → controller → tests as ordered SDD tasks.
- `password-scrubber-agent` — scrub fixture data and example logs before publishing.

### Prompt pattern
Service skeleton:
```
You are a TypeScript backend engineer. Generate <Feature>Service:
- Class with constructor injection of <Repo>, <Logger>, <ExternalClient>.
- Public methods named after use cases (createOrder, cancelOrder), not
  CRUD verbs. Inputs/outputs are domain types from <feature>.types.ts;
  no Express/Fastify imports allowed.
- Throw domain errors (OrderNotFoundError, PaymentDeclinedError) — never
  raw Error.
- Output: service file + a sibling .test.ts with mocked repo covering
  happy + 2 error paths.
```

Controller pass:
```
Generate the controller for <Feature>Service: validate body/query/
params with the Zod schema in <feature>.schema.ts, call the service,
return the response. NO business logic in the handler. Map domain
errors to HTTP via the central ErrorMapper. Use req.id for log context.
Reject the change if the handler has more than 15 lines after format.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tsx` / `ts-node` | TS execution for dev / scripts | `npm i -D tsx` |
| `tsc` | Type-check (run separately from bundler) | bundled with TS |
| `eslint-plugin-boundaries` | Enforce layer boundaries | `npm i -D eslint-plugin-boundaries` |
| `dependency-cruiser` | Visualize / forbid dependency graphs | `npm i -D dependency-cruiser` |
| `madge` | Detect circular dependencies | `npm i -D madge` |
| `vitest` / `jest` | Unit tests | `npm i -D vitest` |
| `supertest` / `light-my-request` | HTTP integration tests | `npm i -D supertest` |
| `pino` | Fast structured logger | `npm i pino` |
| `opentelemetry/api` + auto-instrumentations | Tracing | `npm i @opentelemetry/api` |
| `tsyringe` / `awilix` / `inversify` | DI containers | `npm i awilix` |
| `zod` / `@sinclair/typebox` / `valibot` | Runtime schemas + types | `npm i zod` |
| `prisma` / `drizzle-orm` / `kysely` | Type-safe data access | `npm i drizzle-orm` |
| `nestjs/cli` | Scaffold layered apps | `npm i -g @nestjs/cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Fastify | OSS | Yes | Lightweight, schema-first, ergonomic for layered code. |
| NestJS | OSS | Yes — CLI | Built-in DI + module system; high agent productivity, more boilerplate. |
| Express | OSS | Yes | Default; pair with custom DI to avoid layer leaks. |
| Hono | OSS | Yes | Edge-friendly; layered patterns still fit. |
| Sentry | SaaS | Yes — SDK | Per-layer breadcrumbs; trace ids propagate. |
| Datadog APM | SaaS | Yes — SDK | Auto-instrumentation across Express/Fastify/Nest. |
| OpenTelemetry Node | OSS | Yes — CLI | Vendor-neutral tracing. |
| Prisma Studio / Drizzle Studio | OSS | Partial | Inspect repository layer at dev time. |
| Postman / Bruno | SaaS / OSS | Yes — CLI | Run controller integration tests in CI. |

## Templates & scripts
See `templates.md` for full Controller / Service / Repository scaffolds. Inline boundary check (≤50 lines):

```bash
#!/usr/bin/env bash
# layer-check.sh — fail if controllers depend on repos, or services on framework.
set -euo pipefail
ROOT="${1:-src}"

# 1. ESLint with eslint-plugin-boundaries (assumes config in repo).
npx --yes eslint "$ROOT/**/*.ts" --max-warnings=0

# 2. dependency-cruiser custom rule.
cat > /tmp/dc.json <<'JSON'
{
  "forbidden": [
    { "name": "ctrl-no-repo",
      "from": { "path": "controllers" },
      "to":   { "path": "repositories" },
      "comment": "Controllers must call services, not repositories." },
    { "name": "svc-no-framework",
      "from": { "path": "services" },
      "to":   { "path": "node_modules/(express|fastify|@nestjs/core)" },
      "comment": "Services are framework-agnostic." },
    { "name": "no-circular",
      "severity": "error",
      "from": {}, "to": { "circular": true } }
  ]
}
JSON
npx --yes dependency-cruiser --config /tmp/dc.json --output-type err "$ROOT"

# 3. Quick madge sanity check.
npx --yes madge --circular --extensions ts "$ROOT"
```

Wire into pre-commit and CI; failures block merge.

## Best practices
- Controllers do four things: validate input (Zod/TypeBox), call one service method, map errors via a central mapper, return DTO. Anything else is a smell.
- Services own business logic, accept and return domain types, throw domain errors. They never know about `Request`, `Response`, or HTTP status codes.
- Repositories own SQL / ORM specifics. Expose intention-revealing methods (`findActiveByUserId`) over generic `find(filter)` to keep performance in your hands.
- Use a DI container (`awilix`, `tsyringe`, NestJS) once you exceed ~10 services; manual wiring becomes a tax.
- Validate at the edges: Zod / TypeBox at controllers, infer types throughout. No `any`, no `as unknown as T`.
- Log with `pino` and a request-scoped child logger (`req.log`); propagate trace IDs into services so logs join up.
- Use a central `ErrorMapper` translating domain errors to HTTP. Every new domain error gets a registered mapping or a CI lint failure.
- Transactions: thread an `unitOfWork` (Drizzle / Prisma `$transaction` callback) through service methods that span repos.
- Test pyramids: heavy on service unit tests with mocked repos, plus integration tests using a real DB (Testcontainers) for repos and route-level tests for controllers.
- Don't reach for NestJS unless you'll use modules, guards, interceptors, and pipes; otherwise its DI and decorators are pure overhead.

## AI-agent gotchas
- Agents move HTTP concerns into services (`res.status(404).json(...)`) because that's the dominant pattern in the training set. Reject and require domain errors.
- LLMs invent generic `findAll(filter)` repository methods, encouraging callers to compose unindexed filters at runtime. Force intention-revealing names.
- Agents skip dependency injection and `import` repositories directly inside services, defeating testability. The boundary check above catches this.
- DTO drift: agents update Zod schemas without regenerating types or vice versa. Use `z.infer<typeof schema>` and lint for divergence.
- `as any` / `@ts-ignore` proliferation. Add `eslint-rule-ban-ts-comment` and `no-explicit-any` and treat them as errors.
- Async error swallowing: agents wrap service calls in `try { ... } catch { res.status(500) }` and lose stack + context. Centralize via the error mapper, never per-handler.
- Agents over-mock in service tests, ending up testing the mocks. Require ≥1 integration test per public service method using a real DB.
- DI container misuse: agents register everything as singleton; request-scoped state (auth, tenant) leaks across requests. Pin lifetimes in the container.
- Agents introduce cyclic deps when a service imports another service that imports the first. `madge --circular` in CI prevents.
- Human-in-loop checkpoint: any change to the central error mapper or the DI container registration must be human-approved — both have system-wide impact.

## References
- Vaughn Vernon — "Implementing Domain-Driven Design" (chapters on application services).
- Eric Evans — "Domain-Driven Design".
- Mark Seemann — "Dependency Injection Principles, Practices, and Patterns".
- "Pro TypeScript" — Steve Fenton (covers DI patterns in TS).
- NestJS docs — https://docs.nestjs.com
- Fastify docs (plugins / decorators) — https://fastify.dev
- "Clean Architecture" — Robert C. Martin.
- Awilix docs — https://github.com/jeffijoe/awilix
- Drizzle ORM docs — https://orm.drizzle.team
- Sibling methodologies in this repo: `nextjs-app-router/`, `nodejs-service-layer/`, `react-component-architecture/`, `api-rest-design/`, `api-contract-first/`, `monorepo-turborepo/`.
