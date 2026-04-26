# Agent Integration — Express / Fastify Patterns

## When to use
- Bootstrapping a Node.js HTTP API where the team needs a known-good middleware stack (helmet, cors, compression, rate-limit, pino, graceful shutdown).
- Picking a framework: Express for ecosystem breadth and legacy/middleware reuse; Fastify for high-throughput JSON APIs, schema validation, and TypeScript-first plugin architecture.
- Migrating an old Express app to TypeScript-strict + Zod or Fastify + TypeBox.
- Designing route, error-handler, and auth boundaries that an LLM can extend safely without breaking the request lifecycle.
- Greenfield service with <10 routes where a full Nest/Adonis framework is overkill.

## When NOT to use
- Heavy realtime / streaming workloads where Bun + native HTTP, uWebSockets, or a Go service would be 5-10× cheaper.
- Edge-runtime targets (Cloudflare Workers, Vercel Edge): Express won't run there; Fastify partially. Use Hono or itty-router instead.
- Frontend-only or full-stack frameworks (Next.js Route Handlers, Remix, SvelteKit) where the framework already owns the server.
- Strict-typed contract APIs that already use Nest or tRPC; mixing pulls the team into double-tooling.
- Python or Go shops without Node expertise — adopting Express just for "easy" APIs introduces a new runtime to operate.

## Where it fails / limitations
- **Express's middleware order is implicit.** Reorder one `app.use` and 4xx/5xx behavior changes silently. Newer engineers (and LLMs) misplace `errorHandler` ahead of routes.
- **No built-in validation in Express.** Without zod / joi the API ships unvalidated bodies; error shape becomes a per-route snowflake.
- **Async error swallowing.** Forgetting `next(err)` in an async Express handler hangs the response. Express 5 fixes most cases; Express 4 still bites.
- **Fastify schema lock-in.** TypeBox / Ajv schemas double as runtime validators *and* TS types — great until you need a dynamic schema; serialization shortcuts can also drop fields silently if the response schema omits them.
- **Plugin scoping in Fastify.** `app.register` creates encapsulation contexts; decorators leak in non-obvious ways. LLMs frequently forget `fastify-plugin` wrappers.
- **Performance ceiling.** Both frameworks plateau around 30-80k req/s on a single core; CPU-heavy work (JSON parsing, JWT verify) dominates. Don't expect a framework swap to fix architectural bottlenecks.
- **Ecosystem rot.** Express middlewares often unmaintained (`body-parser`, `morgan`, custom CSRF). Audit before adopting; many have CVEs or have been superseded.

## Agentic workflow
Drive Node API work as a 4-stage pipeline. (1) An **architect agent** reads the README + the team's existing repo and decides Express vs Fastify, validation lib (Zod vs TypeBox), and folder layout. (2) A **scaffolder agent** (haiku-class is sufficient) emits `app.ts`, `server.ts`, `routes/`, `middleware/`, and a Dockerfile from the README templates. (3) A **route-builder agent** generates handlers, schemas, and tests one resource at a time, gated by a contract spec (OpenAPI or TypeBox source-of-truth). (4) A **reviewer / SDD agent** verifies error handling, logging context, auth scoping, and graceful shutdown before merge. Persist decisions to `.aidocs/decisions/` so subsequent agents stay consistent.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — runs the contract → handler → test cycle as SDD tasks; rejects PRs missing route schemas or rate-limit/auth on protected paths.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrubs `.env.example`, logs, and route examples before publishing; this stack leaks JWT secrets and DB URLs constantly.
- A purpose-built **node-api-reviewer agent** (worth creating): checks middleware order, handler async patterns, Fastify plugin encapsulation, and graceful-shutdown signals.
- `nero-sdd-executor-agent` — for NERO-internal services on `nero-prod`, drives systemd unit + nginx reverse-proxy alignment alongside the Node code.

### Prompt pattern
Scaffold pass:
```
Generate a Fastify v5 + TypeBox + Pino service with:
- Routes prefix /api/v1
- Resources: <list>
- Auth: JWT via @fastify/jwt, decorator `app.authenticate`
- Plugins: @fastify/cors, @fastify/helmet, @fastify/rate-limit
- Graceful shutdown on SIGINT/SIGTERM
Output: app.ts, server.ts, routes/<resource>.routes.ts, plugins/auth.ts,
package.json (pinned versions), tsconfig.json (strict), Dockerfile.
```

Route pass:
```
For resource <X>, given the TypeBox schemas in schemas/<X>.ts, produce:
- routes/<x>.routes.ts with GET list, GET by id, POST, PATCH, DELETE.
- All routes typed via Static<typeof Schema>.
- 401 on missing auth, 404 on missing resource, 422 on validation,
  centralized errorHandler. Include unit tests (vitest) and an
  integration test using fastify.inject.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pnpm` / `npm` / `bun` | Package management; `pnpm` recommended for monorepos | https://pnpm.io |
| `tsx` | Run TypeScript without compile step (dev/watch) | `pnpm add -D tsx` ; https://github.com/privatenumber/tsx |
| `tsup` / `esbuild` | Production bundle to single ESM file | `pnpm add -D tsup` ; https://tsup.egoist.dev |
| `pino-pretty` | Local log formatter for `pino` JSON logs | `pnpm add -D pino-pretty` |
| `vitest` | Test runner; works with both frameworks; supports `fastify.inject` and `supertest` | https://vitest.dev |
| `supertest` / `@fastify/inject` | HTTP integration testing | https://github.com/ladjs/supertest |
| `autocannon` | Built-in benchmarking (Fastify devs maintain it) | `pnpm add -D autocannon` ; https://github.com/mcollina/autocannon |
| `clinic.js` | Node.js performance profiling (flame, doctor, bubbleprof) | `pnpm add -g clinic` ; https://clinicjs.org |
| `eslint --fix` + `@typescript-eslint` | Static analysis; pair with `eslint-plugin-security` and `eslint-plugin-node` | https://typescript-eslint.io |
| `npm-check-updates` (`ncu`) | Detect outdated middleware / plugin versions | `pnpm add -g npm-check-updates` |
| `swagger-cli` / `redocly` | Validate / preview the generated OpenAPI from `@fastify/swagger` | https://redocly.com/docs/cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| `@fastify/swagger` + `@fastify/swagger-ui` | OSS plugin | yes | Auto-generates OpenAPI from TypeBox schemas — excellent agent input/output contract. |
| Stoplight / Redocly | SaaS / OSS | yes | Render OpenAPI as docs portal; CLI-driven. |
| Sentry / Highlight | SaaS APM | yes (SDK) | Both frameworks have first-class SDKs; agents can wire `@sentry/node` in <10 lines. |
| Datadog APM / OpenTelemetry SDK | SaaS / OSS | yes | OTel auto-instruments Express + Fastify; preferred for vendor-neutral telemetry. |
| Better Stack / Logtail | SaaS log + uptime | yes (HTTP) | Pino transport ships JSON logs directly. |
| Render / Railway / Fly.io / Hetzner | PaaS / IaaS | yes (CLI) | All deploy a Node Dockerfile in one command — match to budget. |
| Cloudflare Workers / Vercel Edge | Serverless | no for Express | Use Hono instead; Fastify v5 has partial Edge support but not recommended. |
| AWS Lambda + `@fastify/aws-lambda` / `serverless-http` | SaaS | partial | Cold-start tax; only worth it for spiky traffic. |
| PM2 | OSS process manager | yes | Cluster mode + zero-downtime reload; less needed if you're already in Docker/K8s. |
| Auth0 / Clerk / Supabase Auth | SaaS auth | yes (SDK) | Drop-in JWT issuer; pair with the Fastify decorator pattern in README. |

## Templates & scripts

The README ships solid app/server templates. The gap for agents is a **route audit script** that flags missing pieces. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# audit-routes.sh — flag handlers missing validation, auth, or error wiring.
# Usage: audit-routes.sh src/routes
set -euo pipefail
dir="${1:-src/routes}"
fail=0
node - <<'JS' "$dir"
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
const root = process.argv[1];
const issues = [];
const walk = (d) => readdirSync(d).flatMap(f => {
  const p = join(d, f);
  return statSync(p).isDirectory() ? walk(p) : [p];
});
for (const file of walk(root).filter(f => /\.routes?\.ts$/.test(f))) {
  const src = readFileSync(file, 'utf8');
  const verbs = [...src.matchAll(/\.(get|post|put|patch|delete)\(/g)];
  for (const m of verbs) {
    const idx = m.index;
    const window = src.slice(idx, idx + 600);
    if (!/schema\s*:/i.test(window)) issues.push(`${file}: ${m[1].toUpperCase()} missing schema near offset ${idx}`);
    if (m[1] !== 'get' && !/(authenticate|preHandler)/.test(window)) issues.push(`${file}: ${m[1].toUpperCase()} missing auth/preHandler near offset ${idx}`);
  }
  if (!/setErrorHandler|errorHandler|next\(/.test(src)) issues.push(`${file}: no error wiring detected`);
}
if (issues.length) { for (const i of issues) console.error('-', i); process.exit(1); }
console.log('routes audit OK');
JS
```

Wire into `pre-commit` to block PRs that add unprotected mutating routes or routes without schemas.

## Best practices
- **Pin versions exactly** (`package.json` no carets) for the Fastify ecosystem; minor releases of `@fastify/*` plugins occasionally rename hooks.
- **Use `fastify-plugin` (`fp`) for any decorator that must escape encapsulation** — forgetting this is the #1 Fastify bug agents introduce.
- **Centralize error class hierarchy** (`AppError → ValidationError, NotFoundError, UnauthorizedError`) and map them in one error handler. Don't `res.status(...).json(...)` in handlers.
- **Validate at the edge with the same schema you use for types.** Zod (Express) or TypeBox (Fastify) gives one source of truth; never hand-write a TypeScript interface for a payload.
- **Log a request ID + user ID with every line** via `pino-http` `genReqId` or Fastify's `requestIdHeader`; without it, prod debugging is impossible.
- **Graceful shutdown is non-negotiable.** Listen for `SIGTERM`, stop accepting new connections, drain in-flight, close DB pools, then exit. Container orchestrators give you 10-30s — use them.
- **Set `app.set('trust proxy', 1)` in Express behind a single proxy** (Nginx, ALB); without it `req.ip` and rate-limit see the proxy IP only.
- **Guard secrets at boundary.** Never log `req.body` or `req.headers` raw; redact `authorization`, `cookie`, `password` via Pino's `redact` option.
- **Use `@fastify/sensible` for `httpErrors`** rather than throwing raw `Error`; status codes stay consistent without per-route boilerplate.
- **Compile schemas once.** In Fastify, define schemas at module scope; redefining inside the handler tanks throughput.

## AI-agent gotchas
- **LLMs love deprecated Express middleware.** Models still emit `body-parser`, `morgan`, `cookie-parser` separately even though `express.json()` and structured pino replace them. Pin the prompt to "Express ≥4.18, no `body-parser` import."
- **Async error handlers in Express 4.** Agents forget `next(err)` in async functions; use `express-async-errors` or wrap with `asyncHandler`. Express 5 mostly fixes this — confirm the version.
- **Fastify plugin encapsulation.** Agents place auth decorators in a normal plugin (encapsulated) and then can't use them in sibling routes. Force-prompt: "wrap with fastify-plugin if it must be visible outside this scope."
- **Schema-less agent code.** Without explicit schemas, generated routes pass any body. Reject any handler PR without `schema` (Fastify) or `validate(...)` middleware (Express + Zod).
- **Hardcoded ports / origins.** Agents inline `3000` and `http://localhost:3000`; force config via `process.env` and reject string literals in route or app code.
- **CORS wildcard.** Default LLM output is `cors({ origin: '*' })` with `credentials: true` — that's a runtime error in modern browsers. Specify origins explicitly.
- **JWT secret length.** Agents pick weak HS256 secrets in examples; reject anything <32 chars in `JWT_SECRET` or push to RS256 with KMS-backed keys.
- **Logging the request body.** Pino's default with `pino-http` may include `req.body`; agents forget to enable redaction. Mandate the redact list.
- **Graceful shutdown swallowed.** Agents register `SIGTERM` but don't wait for `server.close()`'s callback; container kills mid-request. Verify the close→exit chain in review.
- **Test-only auth bypass leaking.** Agents add `if (process.env.NODE_ENV === 'test') skip auth` and forget the env check on prod; treat as a security gate, not a convenience.
- **Streaming responses break Fastify schema serialization.** Agents wire `response: { 200: SomeSchema }` then return a stream — Fastify drops the body. Disable response schema for streamed routes.

## References
- Express.js Guide. https://expressjs.com/en/guide/
- Fastify Documentation. https://fastify.dev/docs/latest/
- Goldberg, Y. — Node.js Best Practices. https://github.com/goldbergyoni/nodebestpractices
- TypeBox. https://github.com/sinclairzx81/typebox
- Zod. https://zod.dev
- Pino logger. https://getpino.io
- Fastify plugin guide (encapsulation). https://fastify.dev/docs/latest/Reference/Plugins/
- OWASP Node.js Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html
- Sibling methodologies in this repo: `free/dev/software-developer/error-handling/`, `solo/dev/api-developer/`.
