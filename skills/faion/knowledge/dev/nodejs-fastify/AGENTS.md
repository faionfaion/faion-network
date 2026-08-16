# Node.js Fastify

## Summary

**One-sentence:** Generates a Fastify service skeleton (TypeScript-first, JSON-Schema route validators, @fastify/helmet, @fastify/rate-limit, plugin registration).

**One-paragraph:** Fastify is the high-perf Node alternative to Express: TypeScript-first, plugin architecture, JSON-Schema validation built-in, faster JSON serialization. This methodology scaffolds: app entry that wires @fastify/helmet, @fastify/cors, @fastify/compress, @fastify/rate-limit, route schemas validating request + response, error handler via setErrorHandler, and a graceful close hook. Output is a runnable repo skeleton plus 'plugin order matters' note (plugins registered before routes).

**Ефективно для:**

- Services з high-rps (&gt;5k rps) target: Fastify виграє у Express на bench-тестах ~2x.
- TypeScript-first проекти: route schemas автогенерують типи через @sinclair/typebox.
- Plugin-композиція: модулярний скейлінг по фічах.
- Микросервіси з суворою JSON-валидацією: schemas замість ручного парсінгу.

## Applies If (ALL must hold)

- Runtime is Node ≥20.
- Service expects ≥1k rps OR is TypeScript-first.
- Plugin architecture matches the team's mental model.

## Skip If (ANY kills it)

- Team has deep Express expertise + low scale — Express simpler to maintain.
- Runtime is Bun — use Hono via bun-runtime-simple.
- Service is GraphQL-only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Node version | string | node --version |
| Routes + schemas | list | API spec |
| Plugin list | list | owner decision |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: typescript-first, schema-required, plugins-before-routes, set-error-handler, graceful-close | 1000 |
| `content/02-output-contract.xml` | essential | Schema for Fastify service spec | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: no-route-schema, plugin-after-route, custom-error-formatter-leak | 700 |
| `content/04-procedure.xml` | essential | 5-step scaffold | 700 |
| `content/05-examples.xml` | reference | Worked TypeBox route | 500 |
| `content/06-decision-tree.xml` | essential | Surface + plugin tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold` | haiku | File generation. |
| `draft_schemas` | sonnet | Per-route TypeBox / JSON Schema. |
| `draft_plugin_order` | haiku | Deterministic — fixed plugin order. |

## Templates

| File | Purpose |
|------|---------|
| `templates/fastify-app.ts` | Fastify entry with plugin registration |
| `templates/route-with-schema.ts` | Route + TypeBox schema example |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nodejs-fastify.py` | Validate Fastify service spec + plugin order | After scaffold |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[nodejs-express]] — lower-perf alternative; pick if team already on Express.
- [[javascript-modern]] — TS strict + named exports.

## Decision tree

See `content/06-decision-tree.xml`. Branches: surface (REST / WebSocket / GraphQL) → plugin choice. TypeBox vs Ajv schemas → pick TypeBox for TS-first.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/fastify-app.ts`

```typescript
import Fastify from 'fastify'
import helmet from '@fastify/helmet'
import cors from '@fastify/cors'
import compress from '@fastify/compress'
import rateLimit from '@fastify/rate-limit'

export async function buildApp() {
  const app = Fastify({ logger: true })

  // Plugins BEFORE routes
  await app.register(helmet)
  await app.register(cors)
  await app.register(compress)
  await app.register(rateLimit, { max: 120, timeWindow: '1 minute' })

  app.setErrorHandler((err, _req, reply) => {
    const status = err.statusCode ?? 500
    reply.status(status).send({ error: err.code ?? 'internal', message: status >= 500 ? 'internal' : err.message })
  })

  app.get('/health', { schema: { response: { 200: { type: 'object', properties: { ok: { const: true } } } } } }, async () => ({ ok: true as const }))

  // route plugins go here

  return app
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const app = await buildApp()
  await app.listen({ port: Number(process.env.PORT ?? 3000), host: '0.0.0.0' })
  const close = async () => { await app.close(); process.exit(0) }
  process.on('SIGINT', close); process.on('SIGTERM', close)
}
```

### `templates/route-with-schema.ts`

```typescript
import { Type, type Static } from '@sinclair/typebox'
import type { FastifyInstance } from 'fastify'

const Body = Type.Object({
  amount_cents: Type.Integer({ minimum: 1 }),
  currency: Type.String({ pattern: '^[A-Z]{3}$' }),
})

const Reply = Type.Object({ id: Type.String() })

export default async function invoiceRoutes(f: FastifyInstance) {
  f.post<{ Body: Static<typeof Body>; Reply: Static<typeof Reply> }>(
    '/invoices',
    { schema: { body: Body, response: { 200: Reply } } },
    async (req) => ({ id: `inv-${req.id}` }),
  )
}
```
