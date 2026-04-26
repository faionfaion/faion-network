# Agent Integration — Node.js Fastify

## When to use
- Greenfield Node.js HTTP API where TypeScript-first ergonomics, JSON Schema validation, and high RPS matter.
- Migrating Express 4/5 services that have outgrown ad-hoc validation and need typed routes via TypeBox.
- Microservices in TS monorepos — Fastify's plugin model maps cleanly to per-domain modules.
- API gateways where serialization speed (Fastify's `fast-json-stringify`) and schema-driven docs (Swagger UI) are required.
- Building secure-by-default services: helmet, rate limiting, JWT, CORS as first-class plugins.

## When NOT to use
- Edge-runtime targets (Cloudflare Workers, Vercel Edge) — use Hono/Itty Router instead; Fastify is Node-native.
- Static-site or thin SSR layers — frameworks (Next.js, SvelteKit) own the HTTP layer.
- WebSocket-heavy realtime — Fastify supports it via `@fastify/websocket`, but Socket.IO / uWebSockets.js may suit better.
- Trivial scripts and CLIs — boot weight isn't worth it.
- Bun-only services — `Bun.serve` + Hono is lighter; only use Fastify on Bun if you need a specific plugin.

## Where it fails / limitations
- TypeBox vs Zod: README chooses TypeBox for native JSON-Schema fit. Teams standardized on Zod must use `fastify-type-provider-zod` and accept extra serialization cost.
- Plugin encapsulation rules surprise: a plugin must use `fp` (fastify-plugin) to escape its scope — agents forget this and decorators "disappear".
- Default logger (Pino) is fast but JSON-only; humans need `pino-pretty` in dev. Forgetting `transport` config in dev is a common DX papercut.
- Schema-driven serialization silently drops fields not in the response schema — feature, but agents debugging "missing field" responses miss this for hours.
- `@fastify/jwt` does not handle key rotation or JWKS by default — pair with `@fastify/oauth2` or custom verifier for OIDC.

## Agentic workflow
Plan-then-build. Planner subagent produces module map: routes (path → method → request schema → response schema → handler signature) + plugins (auth, rate-limit, cors, redis, db). Implementer subagent writes one route file per domain with `FastifyPluginAsync` + TypeBox schemas + handler. Reviewer subagent verifies: every route has request/response schemas, every async handler awaits, every plugin needing decorators uses `fastify-plugin`, error handler returns Problem-Details JSON.

### Recommended subagents
- `faion-feature-executor` — sequential route additions; gate is `tsc --noEmit` + `vitest run` + a smoke `curl` via supertest.
- `faion-sdd-execution` — pattern memory for canonical schemas (pagination, errors, timestamps), reuses across routes.
- `faion-improver` — periodic audit: missing response schema, unscoped decorators, plugins not using `fp`, missing graceful shutdown.

### Prompt pattern
```
Apply nodejs-fastify README. For <domain>, design a routes plugin:
table of (METHOD, path, params, query, body schema, response schema, auth?,
rate-limit?). Reference existing schemas from src/schemas/. Stop.
```
```
Implement <routes plugin>. Use FastifyPluginAsync + TypeBoxTypeProvider.
Every route MUST have request and response schemas. Handler is async,
returns the typed payload (no `reply.send` unless setting status). Wire
into createApp(). Add a vitest using `app.inject()` for one happy + one
validation-error path.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `fastify-cli` | Scaffold + run apps via `start.js` convention | `npm i -D fastify-cli` |
| `tsx` / `tsdown` | Dev/build for TS Fastify apps | tsx.is |
| `pino-pretty` | Pretty dev logs | `npm i -D pino-pretty` |
| `@fastify/swagger` + `swagger-ui` | Auto OpenAPI from JSON-Schema | github.com/fastify/fastify-swagger |
| `autocannon` | Load testing (HTTP benchmarking) | `npx autocannon` |
| `clinic.js` | Production diag (doctor, flame, bubbleprof) | clinicjs.org |
| `@types/node` + `typescript` | TS toolchain | npm |
| `vitest` + `light-my-request` (`app.inject`) | Unit tests without a port | vitest.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| `@fastify/postgres` / `@fastify/mongodb` / `@fastify/redis` | OSS plugins | Yes | Decorators wired in via `fp`; agents follow plugin recipe |
| Drizzle ORM | OSS | Yes | TS-native, plays well with TypeBox types |
| Prisma | OSS | Partial | Works on Node; serverless/edge needs adapter; engine size is a tax |
| `@fastify/swagger-ui` | OSS | Yes | Auto-doc from schemas — first-class agent integration |
| Sentry | SaaS | Yes | `@sentry/node` integrates as plugin via `fp` |
| OpenTelemetry | OSS | Yes | `@opentelemetry/instrumentation-fastify` for traces |
| pm2 / systemd | OSS | Yes | Process supervision; pair with Fastify's `closeListener` for graceful shutdown |

## Templates & scripts
See `templates.md` for `app.ts`, route plugin, error handler, and JWT auth plugin patterns. Inline graceful-shutdown wiring (often missed):

```ts
// server.ts (graceful shutdown excerpt)
import closeWithGrace from 'close-with-grace';
import { createApp } from './app';

const app = await createApp();
await app.listen({ port: Number(process.env.PORT ?? 3000), host: '0.0.0.0' });

closeWithGrace({ delay: 10_000 }, async ({ signal, err }) => {
  if (err) app.log.error({ err }, 'shutdown error');
  app.log.info({ signal }, 'shutting down');
  await app.close();
});
```

Inject-style smoke test (no port required):

```ts
import { test, expect } from 'vitest';
import { createApp } from '../src/app';
test('GET /health', async () => {
  const app = await createApp();
  const res = await app.inject({ method: 'GET', url: '/health' });
  expect(res.statusCode).toBe(200);
  expect(res.json()).toMatchObject({ status: 'ok' });
  await app.close();
});
```

## Best practices
- Always set both request AND response schemas on every route. Response schema doubles as serializer (faster) and as OpenAPI source.
- Plugins that decorate `app` must be wrapped in `fastify-plugin` (`fp`) to break encapsulation; otherwise decorators are scoped and disappear at the parent scope.
- Use `await app.register(...)` — forgetting `await` causes async plugins to half-load; race conditions follow.
- Error handler returns RFC 7807 Problem Details (`type`, `title`, `status`, `detail`, `instance`) — pairs well with API consumers and OpenAPI.
- For auth: prefer `@fastify/jwt` + a verify hook on protected route prefixes; never decode JWT manually in handlers.
- Log everything with the request-bound `request.log` / `reply.log` — never `console.log` (T20 equivalent).
- Use `app.inject()` for tests over starting a real port — fast, deterministic, parallel-safe.

## AI-agent gotchas
- LLMs forget `fastify-plugin` (`fp`) wrapper, then `app.db` decorator is missing in routes — silent runtime failure. Reviewer must grep `fp(` against every plugin that calls `decorate*`.
- Agents place schemas inline as plain objects without `as const` or TypeBox; TS infers loose types and handler typing breaks. Use TypeBox `Type.Object` or `as const`.
- Default 200 response often returns extra fields not in schema; agents are confused why fields disappear — the response serializer strips them. Either expand schema or use `additionalProperties: true`.
- Mixing `reply.send(...)` and `return ...` from a handler causes double-response errors. Pick one (return) and keep `reply.code(...)` for status only.
- Adding `@fastify/cors` in dev but not in prod (or vice versa) is a common drift — keep CORS config in env-driven `config.ts`.
- Human-in-loop checkpoint: when wiring auth/JWT plugins, when introducing global hooks (preHandler/onRequest), and before changing the error-handler shape (consumer impact).

## References
- Fastify docs — https://fastify.dev/docs/latest/
- Fastify plugins guide — https://fastify.dev/docs/latest/Reference/Plugins/
- TypeBox — https://github.com/sinclairzx81/typebox
- `@fastify/swagger` — https://github.com/fastify/fastify-swagger
- close-with-grace — https://github.com/mcollina/close-with-grace
- autocannon — https://github.com/mcollina/autocannon
- Pino logger — https://getpino.io/
