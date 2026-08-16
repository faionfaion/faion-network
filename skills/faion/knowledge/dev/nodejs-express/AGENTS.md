# Node.js Express

## Summary

**One-sentence:** Emits an Express service skeleton with the canonical middleware stack, centralised error handler, and graceful shutdown on SIGINT/SIGTERM.

**One-paragraph:** Express stays the default Node REST framework because of ecosystem inertia. A production-shape Express service needs: helmet (security headers), cors (origin policy), compression (response gzip), pino-http (structured logs), express-rate-limit (DDoS/brute floor), centralised error middleware, and a graceful-shutdown handler that closes the server + drains in-flight before exit. This methodology emits the skeleton + decision-record for each choice (e.g. why not morgan, why not winston). Output is a runnable repo skeleton plus a 'middleware order matters' note.

**Ефективно для:**

- Net-new Express service: 'one shot' production skeleton.
- Audit існуючого Express: чи присутні helmet / rate-limit / graceful-shutdown.
- Onboarding: новачок розуміє WHY кожен middleware, не просто скопіювати.
- Migration з Express 4 → Express 5: pin сumber, pin async-error handling.

## Applies If (ALL must hold)

- Runtime is Node ≥20 (LTS).
- Framework is Express (≥ 4.18) — Fastify lives in a separate methodology.
- Service exposes HTTP / REST (not WebSocket / GraphQL only).

## Skip If (ANY kills it)

- Runtime is Bun — use bun-runtime-simple + Hono.
- Framework is Fastify — see nodejs-fastify.
- Service is GraphQL-only — different middleware stack.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Node version | string | node --version |
| Service name + routes | list | API spec |
| Auth shape | enum | owner decision |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: helmet-first, rate-limit-floor, central-error-handler, graceful-shutdown, pino-not-morgan | 1000 |
| `content/02-output-contract.xml` | essential | Schema for Express service spec | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: callback-error-leak, no-graceful-shutdown, helmet-missing | 700 |
| `content/04-procedure.xml` | essential | 5-step scaffold procedure | 700 |
| `content/05-examples.xml` | reference | Worked middleware-order example | 500 |
| `content/06-decision-tree.xml` | essential | Auth + scale tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold` | haiku | File generation. |
| `draft_routes` | sonnet | Per-route TS code. |
| `draft_error_handler` | sonnet | Per-error-kind branching. |

## Templates

| File | Purpose |
|------|---------|
| `templates/express-app.ts` | Hello-world Express app with middleware stack |
| `templates/error-middleware.ts` | Centralised error handler skeleton |
| `templates/graceful-shutdown.ts` | SIGINT/SIGTERM shutdown helper |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nodejs-express.py` | Validate Express service spec + middleware order | After scaffold, before commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[nodejs-fastify]] — higher-perf alternative; pick if &gt;5k rps target.
- [[javascript-modern]] — TS strict + named exports apply.

## Decision tree

See `content/06-decision-tree.xml`. Branches: auth (none / token / session) → middleware. Expected scale (low &lt;1k rps / medium / high) → consider Fastify above 5k rps. Multi-tenant? → context propagation via AsyncLocalStorage.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/express-app.ts`

```typescript
import express, { type NextFunction, type Request, type Response } from 'express'
import helmet from 'helmet'
import cors from 'cors'
import compression from 'compression'
import pinoHttp from 'pino-http'
import rateLimit from 'express-rate-limit'

export function createApp() {
  const app = express()
  app.use(helmet())
  app.use(cors())
  app.use(compression())
  app.use(pinoHttp())
  app.use(rateLimit({ windowMs: 60_000, max: 120 }))
  app.use(express.json({ limit: '1mb' }))

  app.get('/health', (_req, res) => res.json({ ok: true }))

  // routes go here

  // Central error handler MUST be last:
  app.use((err: any, _req: Request, res: Response, _next: NextFunction) => {
    res.status(err?.status ?? 500).json({ error: err?.code ?? 'internal' })
  })

  return app
}
```

### `templates/error-middleware.ts`

```typescript
import type { ErrorRequestHandler } from 'express'

const STATUS_MAP: Record<string, number> = {
  ValidationError: 400,
  AuthError: 401,
  ForbiddenError: 403,
  NotFoundError: 404,
  ConflictError: 409,
  RateLimitError: 429,
}

export const errorMiddleware: ErrorRequestHandler = (err, req, res, _next) => {
  const status = STATUS_MAP[err?.name] ?? err?.status ?? 500
  const code = err?.code ?? err?.name ?? 'internal'
  req.log?.error({ err, status, code }, 'request failed')
  res.status(status).json({ error: code, message: status >= 500 ? 'internal' : err?.message })
}
```

### `templates/graceful-shutdown.ts`

```typescript
import type { Server } from 'node:http'

export function wireGracefulShutdown(server: Server, opts: {
  dbClose?: () => Promise<void>
  drainTimeoutMs?: number
} = {}) {
  const drainTimeoutMs = opts.drainTimeoutMs ?? 30_000
  let shuttingDown = false

  async function shutdown(signal: string) {
    if (shuttingDown) return
    shuttingDown = true
    console.log(`[shutdown] ${signal} received; draining`)
    const t = setTimeout(() => {
      console.error('[shutdown] drain timeout exceeded; force exit')
      process.exit(1)
    }, drainTimeoutMs)
    server.close(async () => {
      try { await opts.dbClose?.() } catch (e) { console.error(e) }
      clearTimeout(t)
      process.exit(0)
    })
  }

  process.on('SIGINT', () => shutdown('SIGINT'))
  process.on('SIGTERM', () => shutdown('SIGTERM'))
}
```
