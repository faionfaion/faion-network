# Bun Runtime (Simple)

## Summary

**One-sentence:** Generates a minimal but production-shaped Bun + TypeScript + Hono service skeleton using only Bun stdlib (no external Express, no bcrypt, no dotenv).

**One-paragraph:** Bun consolidates runtime + bundler + test runner + package manager + transpiler; using Bun while still pulling express + bcrypt + dotenv wastes half its value. This methodology scaffolds a Bun service that uses Hono for routing, Bun.password for hashing, Bun.file for I/O, native `.env` loading, and `bun:test` for tests. Output is a runnable repo skeleton plus a 'why Bun primitives over npm equivalents' rationale per choice.

**Ефективно для:**

- Стартові projects, що хочуть Bun-perf без npm-tax.
- Microservices that pin Bun as their only runtime (no Node fallback).
- Demo / tutorial code: смужка коду 50 рядків замість 200 з Express.
- Edge / serverless deploys where startup time matters (Bun cold-start &lt; Node).

## Applies If (ALL must hold)

- Target runtime is Bun (≥1.1 with stable Bun.password API).
- Service is greenfield (legacy Express migration is a different exercise).
- Team accepts dropping Node-only deps (express, bcrypt, dotenv).

## Skip If (ANY kills it)

- Production already on Node + needs incremental migration.
- Dep tree requires native-compiled packages incompatible with Bun.
- Hosting platform doesn't support Bun (locked to Node runtime).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Bun version | string | bun --version |
| Service name | string | owner decision |
| Target routes | list | API spec or sketch |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: bun-primitives-first, hono-for-routing, bun-test-not-jest, bun-file-not-fs, bun-password-not-bcrypt | 1000 |
| `content/02-output-contract.xml` | essential | Schema for generated service spec | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: express-pulled-in, dotenv-imported, bcrypt-imported | 700 |
| `content/04-procedure.xml` | essential | 5-step scaffold procedure | 700 |
| `content/05-examples.xml` | reference | Worked Hono + Bun.password example | 500 |
| `content/06-decision-tree.xml` | essential | Route shape + auth shape tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold` | haiku | Deterministic file emission. |
| `draft_routes` | sonnet | Per-route TS code. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bun-service-skeleton.ts` | Hello-world Bun + Hono entry |
| `templates/bun-test-skeleton.ts` | bun:test skeleton |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bun-runtime-simple.py` | Validate the service-spec artefact + Bun version | After scaffold, before commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- - [[javascript-modern]] — TS-first principles still apply.
- - [[javascript-testing]] — bun:test is Jest-compatible; same patterns transfer.

## Decision tree

See `content/06-decision-tree.xml`. Branches: route count (≤5 simple / &gt;5 needs grouping) → Hono with or without grouping. Auth shape (none / token / session) → Bun.password and which primitive to use.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/bun-service-skeleton.ts`

```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/health', (c) => c.json({ ok: true }))

app.post('/register', async (c) => {
  const { email, password } = await c.req.json<{ email: string; password: string }>()
  const hash = await Bun.password.hash(password)
  return c.json({ ok: true, email, hash_prefix: hash.slice(0, 8) })
})

export default {
  port: Number(Bun.env.PORT ?? 3000),
  fetch: app.fetch,
}
```

### `templates/bun-test-skeleton.ts`

```typescript
import { test, expect } from 'bun:test'
import app from './bun-service-skeleton'

test('health returns ok', async () => {
  const res = await app.fetch(new Request('http://localhost/health'))
  expect(res.status).toBe(200)
  expect(await res.json()).toEqual({ ok: true })
})

test('register hashes password', async () => {
  const res = await app.fetch(new Request('http://localhost/register', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: 'a@b.c', password: 'hunter2' }),
  }))
  expect(res.status).toBe(200)
  const body = await res.json()
  expect(body.ok).toBe(true)
})
```
