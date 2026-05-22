---
slug: nodejs-express
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Scaffolds a production REST API on Express with layered middleware (helmet, cors, compression, pinoHttp, rate-limit), centralised error handling, and graceful shutdown.
content_id: "856ced48c3c11a15"
complexity: medium
produces: code
est_tokens: 3700
tags: [express, nodejs, rest-api, middleware, security]
---
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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nodejs-express.py` | Validate Express service spec + middleware order | After scaffold, before commit |

## Related

- [[nodejs-fastify]] — higher-perf alternative; pick if &gt;5k rps target.
- [[javascript-modern]] — TS strict + named exports apply.

## Decision tree

See `content/06-decision-tree.xml`. Branches: auth (none / token / session) → middleware. Expected scale (low &lt;1k rps / medium / high) → consider Fastify above 5k rps. Multi-tenant? → context propagation via AsyncLocalStorage.
