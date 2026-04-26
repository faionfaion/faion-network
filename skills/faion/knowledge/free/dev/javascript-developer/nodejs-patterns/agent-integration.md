# Agent Integration — Node.js Patterns

## When to use
- Bootstrapping a new TypeScript Express API (controllers, services, middleware, errors, Pino logger).
- Refactoring an existing JS/TS Node service into a layered structure with central error handling.
- Asking an agent to add a new domain (resource) to an existing Express app and follow the project's module layout.
- Wiring request-scoped logging (request id, duration) into an existing Express server.

## When NOT to use
- Pure CLI/script Node code with no HTTP layer — the routing/controller scaffolding is overhead.
- Edge-runtime targets (Cloudflare Workers, Vercel Edge, Deno Deploy) — Express is incompatible; use Hono or Fastify-on-Node.
- High-throughput WebSocket-first services — Express middleware chain is slow; use uWebSockets.js or Fastify.
- Frontend-only React projects — no Node server is owned.

## Where it fails / limitations
- Node 22+ has native `--watch`, `node:test`, fetch — README implicitly assumes external watchers/Jest; agents may install redundant deps.
- `helmet` defaults break some inline-script SSR flows; agents that follow the snippet verbatim ship broken CSP for Next-on-Express.
- The error-handler swallows the original error in non-operational paths (only logs `err`) — production traces lose stack on retry from worker queues.
- Zod parse inside controllers (instead of a validate middleware) duplicates error mapping; agents writing many controllers diverge from the shared error path.
- `req.user` global declaration merges into all Express types in the workspace — multiple apps in a monorepo collide.

## Agentic workflow
Drive with a planning agent that reads `README.md`, decides which layers to scaffold (routes/controllers/services/middleware/errors/logger), then a coder agent that creates files in that order in a single PR. Validation agent runs `tsc --noEmit`, `eslint`, and a smoke `supertest` for `/health` and one resource endpoint. Keep the controller/service split — agents that flatten them lose testability. For middleware ordering issues, run a focused review agent against the `createApp` chain.

### Recommended subagents
- `faion-sdd-executor-agent` — sequential scaffold of layered files with quality gates.
- `faion-feature-executor` — adding a new resource (route + controller + service + schema + tests) end-to-end.
- `password-scrubber-agent` — final pass to ensure no JWT secrets / connection strings leak into logs or examples.
- A custom `nodejs-express-reviewer` (sonnet) — verifies middleware order, error handler is last, async wrappers exist on every route.

### Prompt pattern
```
Read skills/faion/knowledge/free/dev/javascript-developer/nodejs-patterns/README.md.
Add resource <name> following the controller/service/schema/route layout. Use Zod for input,
AppError subclasses for failures, async/await with next(err). Do not duplicate validation
inside controllers — use middleware/validate.ts.
```

```
Audit src/app.ts middleware order against README. Report deviations: helmet→cors→json→
compression→requestLogger→routes→errorHandler. Fail if errorHandler is not last.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tsx` | Run TS directly in dev | `npm i -D tsx` · https://tsx.is |
| `node --watch` | Native dev reload (Node 22+) | https://nodejs.org/api/cli.html#--watch |
| `pino-pretty` | Dev log pretty printing | `npm i -D pino-pretty` · https://github.com/pinojs/pino-pretty |
| `pino` | Production JSON logger | https://getpino.io |
| `supertest` | HTTP integration tests | `npm i -D supertest` · https://github.com/ladjs/supertest |
| `clinic.js` | Perf flamegraphs / event-loop lag | `npx clinic doctor -- node dist/server.js` |
| `0x` | Single-process flamegraph | `npx 0x dist/server.js` |
| `autocannon` | Load test endpoints | `npx autocannon http://localhost:3000/api/v1/...` |
| `nodemon` | Legacy watcher (pre-Node 22) | https://nodemon.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Pino transport (Loki, Datadog) | OSS/SaaS | Yes | `pino-loki`, `pino-datadog-transport`; agents wire via env vars. |
| OpenTelemetry Node SDK | OSS | Yes | Auto-instruments Express; one-line `@opentelemetry/auto-instrumentations-node`. |
| Sentry Node | SaaS | Yes | `Sentry.Handlers.errorHandler()` slots into the chain before the README's handler. |
| BullMQ | OSS (Redis) | Yes | Pairs with Express for background jobs; reuses the same Pino logger. |
| PM2 | OSS | Partial | Useful for cluster mode; agents must respect graceful-shutdown signals. |
| Render / Railway / Fly.io | SaaS | Yes | Deploy targets that respect SIGTERM (matches the patterns shown). |

## Templates & scripts
See `templates.md` for the per-layer file templates. Inline minimal async-handler wrapper that the README is missing — drop into `utils/asyncHandler.ts`:

```typescript
import type { RequestHandler } from 'express';

export const asyncHandler =
  <P, ResB, ReqB, ReqQ>(
    fn: (
      req: Parameters<RequestHandler<P, ResB, ReqB, ReqQ>>[0],
      res: Parameters<RequestHandler<P, ResB, ReqB, ReqQ>>[1],
      next: Parameters<RequestHandler<P, ResB, ReqB, ReqQ>>[2],
    ) => Promise<unknown>,
  ): RequestHandler<P, ResB, ReqB, ReqQ> =>
  (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
```

Use as `router.get('/', asyncHandler(getUsers))` to drop the manual `try/catch + next(error)` boilerplate the README shows.

## Best practices
- Keep `createApp()` pure — no `listen()`. Lets supertest mount it without binding a port.
- Set `app.set('trust proxy', 1)` only when behind a known proxy; otherwise rate-limit by `req.ip` is spoofable.
- `express.json({ limit: '10kb' })` is fine for APIs but block-by-default for file uploads — route uploads through `multer` with explicit size limits.
- Never import `process.env` deep in modules; resolve a frozen `config` object once in `config/env.ts` (parsed via Zod) and import that.
- `res.on('finish')` logging misses connection-aborted requests — also hook `res.on('close')` for accurate observability.
- Always call `Error.captureStackTrace` in custom error subclasses (the README does this — preserve it).
- Distinguish operational vs programmer errors. Crash on programmer errors (let PM2/k8s restart) — do not blanket-catch in `errorHandler`.

## AI-agent gotchas
- Agents love duplicating `try/catch` in every controller — enforce `asyncHandler` or `express-async-errors` patch via lint rule, otherwise PRs accumulate boilerplate.
- LLMs frequently put `errorHandler` before routes when generating from scratch — pin its position with a comment marker `// MUST BE LAST` and a test that hits a 500 and asserts JSON shape.
- Pino transports are loaded async; agents that call `logger.info()` then `process.exit(0)` lose logs. Require `await logger.flush?.()` in shutdown.
- `req.user` augmentation must live in a single `types/express.d.ts` — agents that re-declare it per middleware cause TS2717 merge conflicts.
- When agents add routes they often forget to register them in `routes/index.ts` — add a checklist test that scans for orphan `*.routes.ts` files.
- Human checkpoint: review of new `AppError` subclasses (status code, code string) before merge — agents tend to overload 500 for everything.
- For dependency upgrades (Express 4 → 5), let the agent open a separate PR; mixing with feature work hides breakage in error-handling semantics.

## References
- https://expressjs.com/en/guide/error-handling.html
- https://github.com/goldbergyoni/nodebestpractices
- https://getpino.io/#/docs/api
- https://nodejs.org/api/cli.html#--watch
- https://opentelemetry.io/docs/languages/js/getting-started/nodejs/
- https://docs.sentry.io/platforms/node/guides/express/
