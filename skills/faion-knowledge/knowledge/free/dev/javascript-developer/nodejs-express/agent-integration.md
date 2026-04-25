# Agent Integration — Node.js Express

## When to use
- Production REST API on Node 20/22 where you want a familiar, mature middleware ecosystem.
- Adding a new resource (router + controller + service + Zod schema + auth middleware) to an existing Express service.
- Hardening a hand-rolled Express server: add `helmet`, `cors`, `compression`, `pino-http`, `express-rate-limit`, graceful shutdown.
- Centralizing error handling with `AppError` + Zod-aware error middleware in a project that currently mixes `res.status(...).json(...)` everywhere.

## When NOT to use
- New projects targeting peak throughput — Fastify is ~2-3x faster on the same hardware; use the sibling `nodejs-fastify` methodology.
- Edge runtimes (Cloudflare Workers, Vercel Edge) — Express depends on Node-only APIs.
- Greenfield Bun-only services where `Bun.serve` removes the framework entirely.
- A microservice that only needs WebSockets — bare `ws` or `uWebSockets.js` beats Express middleware overhead.

## Where it fails / limitations
- Express 4 LTS does not auto-forward async errors (Express 5 does). Agents copying `app.get(..., async ...)` without `try/catch + next(err)` get unhandled rejections.
- `express-rate-limit` with `trust proxy` set incorrectly is a known foot-gun (CVE-style spoofing); blindly setting `app.set('trust proxy', 1)` in dev when there is no proxy lets attackers forge IPs.
- `helmet()` defaults can break `<script>` inline patterns from older SSR setups; CSP must be tuned per app.
- Graceful shutdown in the README closes the HTTP server but does not drain DB pools / queues — long-running workers leak on SIGTERM.
- `pino-http` `autoLogging: true` logs full URLs including tokens in query strings; PII leakage is silent.
- `validate(schema)` only validates `req.body`; agents copy the snippet and miss `params` / `query` validation. The included `validateAll` covers it but is rarely surfaced.

## Agentic workflow
Drive with a planner that produces a file list (`app.ts`, `server.ts`, `routes/*`, `controllers/*`, `services/*`, `middleware/*`, `schemas/*`, `utils/errors.ts`, `utils/logger.ts`), then a coder agent that creates each file. A reviewer agent checks middleware order (`helmet → cors → compression → json → pinoHttp → rateLimit → routes → notFound → errorHandler`) and that the error handler is registered last. A security agent runs `npm audit`, `eslint-plugin-security`, and a CSP/CORS sanity check.

### Recommended subagents
- `faion-sdd-executor-agent` — gated build of layered Express files with `tsc`, lint, and supertest at each step.
- `faion-feature-executor` — adding a complete resource (route + controller + service + schema + tests).
- `password-scrubber-agent` — final scan to ensure JWT secrets, DB strings, and bearer tokens never enter logs/examples.
- A custom `express-middleware-orderer` (sonnet) — verifies registration order matches README; refuses to merge if `errorHandler` is not last.

### Prompt pattern
```
Read skills/faion-knowledge/knowledge/free/dev/javascript-developer/nodejs-express/README.md.
Add resource <name>: routes/<name>.routes.ts, controllers/<name>.controller.ts,
services/<name>.service.ts, schemas/<name>.ts. Use validateAll({ body, params, query }).
Wrap each handler in asyncHandler. Add 200/400/404 supertests.
```

```
Audit src/app.ts. Verify: trust proxy ↔ deployment, helmet→cors→compression→json→pinoHttp→
rateLimit→routes→notFound→errorHandler. Fail if any out-of-order or missing.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tsx` | Run TypeScript in dev | `npm i -D tsx` · https://tsx.is |
| `node --watch` | Native dev reload (Node 22+) | https://nodejs.org/api/cli.html#--watch |
| `supertest` | HTTP integration tests | `npm i -D supertest @types/supertest` |
| `pino-pretty` | Pretty dev logs | `npm i -D pino-pretty` · https://github.com/pinojs/pino-pretty |
| `autocannon` | Load test endpoints | `npx autocannon http://localhost:3000/health` |
| `clinic doctor` | Event-loop / GC diagnosis | `npx clinic doctor -- node dist/server.js` |
| `npm audit` / `osv-scanner` | Vulnerability scan | https://google.github.io/osv-scanner/ |
| `eslint-plugin-security` | Lint for unsafe patterns | https://github.com/eslint-community/eslint-plugin-security |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry Node | SaaS | Yes | `Sentry.Handlers.errorHandler()` slots in before user error handler. |
| OpenTelemetry Express auto-instrumentation | OSS | Yes | One-line `@opentelemetry/instrumentation-express`. |
| Datadog APM / New Relic | SaaS | Yes | Tracer init must run before `express` import. |
| BullMQ | OSS (Redis) | Yes | Reuse Pino logger and config; mount admin UI behind authenticate. |
| Helmet.js | OSS | Yes | Defaults are agent-safe; CSP requires per-app tuning. |
| Render / Railway / Fly.io / Heroku | SaaS | Yes | Honor SIGTERM; the README's shutdown handler is correct. |
| AWS Lambda + serverless-http | SaaS | Partial | Wraps Express; agents should disable `compression` and use API Gateway features instead. |

## Templates & scripts
See `templates.md` for full per-layer templates. Inline async-handler wrapper to remove `try/catch` boilerplate (`utils/asyncHandler.ts`):

```typescript
import type { RequestHandler } from 'express';

export const asyncHandler =
  (fn: (...a: Parameters<RequestHandler>) => Promise<unknown>): RequestHandler =>
  (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
```

Use as `router.post('/', validate(Schema), asyncHandler(controller.create))`. On Express 5+, async errors auto-forward and the wrapper becomes optional.

## Best practices
- Register `errorHandler` last and `notFoundHandler` immediately before it. Pin position with a smoke test that asserts a 404 JSON shape.
- `app.set('trust proxy', N)` only when behind exactly N proxies (`1` for one nginx/load balancer). Wrong value enables IP spoofing for rate-limiter.
- Validate `req.body`, `req.params`, AND `req.query` — use the `validateAll` form, not the body-only `validate`.
- Strip secrets from `pino-http` with `redact: ['req.headers.authorization', 'req.query.token']`. Defaults log everything.
- Mount `/health` BEFORE rate-limiter and auth — load balancers will mark you down otherwise.
- Use `Router({ mergeParams: true })` only when nesting routers under `:param` paths. Default leaves `req.params` empty in nested routers.
- Don't call `process.exit()` in `errorHandler`. Throw operational errors, let infra restart on programmer errors.
- Drain DB / queue connections in the SIGTERM handler before `server.close` callback resolves.

## AI-agent gotchas
- LLMs love `app.use(cors())` (open CORS) — pin to `corsOrigins` from config and lint for the bare form.
- Agents wrap controllers in `try/catch` and forget `next(err)`, swallowing errors silently. Either enforce `asyncHandler` or migrate to Express 5.
- `Request` global augmentation for `req.user` must live in exactly one `types/express.d.ts`. Multiple files merge silently and produce incompatible typings.
- `req.id` is added by `pino-http` only when configured with `genReqId`; agents read `req.id` elsewhere and get `undefined` in tests.
- Rate-limiter in tests: agents copy production config and trip 429 in the test suite. Wrap in `if (process.env.NODE_ENV !== 'test')`.
- Human checkpoint: any new auth/authorization middleware should be reviewed before merge — silent role drift is the most common security regression.
- LLMs frequently downgrade Helmet to `helmet({ contentSecurityPolicy: false })` to "fix" a CSP error from one inline script. Require an explicit allowlisted CSP instead.
- Express version drift: 4 vs 5 differs in async handling, query parser, and route param syntax. Pin the major version in the project AGENTS.md so agents don't auto-upgrade.

## References
- https://expressjs.com/en/advanced/best-practice-production.html
- https://expressjs.com/en/guide/error-handling.html
- https://expressjs.com/en/guide/using-middleware.html
- https://github.com/goldbergyoni/nodebestpractices
- https://helmetjs.github.io/
- https://express-rate-limit.mintlify.app/guides/troubleshooting-proxy-issues
- https://github.com/pinojs/pino-http
- https://opentelemetry.io/docs/instrumentation/js/libraries/
