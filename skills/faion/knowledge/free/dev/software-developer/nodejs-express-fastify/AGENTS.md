---
slug: nodejs-express-fastify
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a production Node.js HTTP service (Express or Fastify) with helmet/cors/rate-limit middleware, schema-validated routes (Zod or TypeBox), centralized error handler, and SIGTERM/SIGINT graceful shutdown.
content_id: "nodejs-fb15"
complexity: medium
produces: code
est_tokens: 4000
tags: [nodejs, express, fastify, middleware, graceful-shutdown]
---
# Node.js HTTP: Express / Fastify

## Summary

**One-sentence:** Produces a production Node.js HTTP service (Express or Fastify) with helmet/cors/rate-limit middleware, schema-validated routes (Zod or TypeBox), centralized error handler, and SIGTERM/SIGINT graceful shutdown.

**One-paragraph:** Structured Node service with middleware in the exact order: security (helmet) → cors → body parsing → logging → rate-limit → routes → 404 → error handler (always last). Zod for Express routes; TypeBox for Fastify (compiled at module scope, not per request). Errors flow to a centralized error handler via `next(err)` (Express) or by throwing (Fastify). Async handlers wrapped with try/catch in Express 4 (Express 5 propagates automatically). Fastify plugins that decorate the instance use `fastify-plugin` when the decorator must be visible outside scope. Graceful shutdown: SIGTERM/SIGINT → stop accepting → server.close() → close DB pools → exit.

**Ефективно для:** new Node HTTP services, refactors merging mixed error shapes/handlers into one, services missing helmet+rate-limit, code reviews flagging middleware-order bugs.

## Applies If (ALL must hold)

- Building a Node.js HTTP service with Express ≥4.18 or Fastify ≥4.
- Team accepts one central error handler.
- Can install helmet, cors, express-rate-limit (or @fastify/rate-limit), pino.
- Service must drain on SIGTERM (containers, k8s).

## Skip If (ANY kills it)

- Serverless function — different shutdown model.
- Heavily-customised framework (hapi/koa with conventions diverging).
- Pure WebSocket/SSE server — error model is different.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Framework choice | express / fastify | tech stack ADR |
| Logger | pino (recommended) | observability ADR |
| Auth scheme | JWT/cookie | security ADR |
| Rate-limit budget | RPS per route | infra ADR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[javascript]]` | TS strict + named-exports apply. |
| `[[error-handling]]` | Cross-language RFC 7807 envelope this layer emits. |
| `[[pnpm-package-management]]` | Package manager pinning. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: middleware order, error-handler last, schema validation, schemas at module scope, next(err) only, Express 4 async wrapping, fastify-plugin, graceful shutdown | ~800 |
| `content/02-output-contract.xml` | essential | Required app shape + middleware ordering + shutdown wiring | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: error handler before routes, inline schema in handler, res.status(err) in handler, no SIGTERM listener | ~600 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Root: "Is this Node HTTP with long-lived lifecycle?" | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold app.ts | sonnet | Template-driven. |
| Author Zod/TypeBox schemas | sonnet | Schema generation. |
| Migrate inline error handling | opus | AST-level reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-routes.sh` | grep middleware order + error-handler position. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nodejs-express-fastify.py` | Verifies error handler comes after routes, schemas at module scope, SIGTERM listener present. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[error-handling]]` — RFC 7807 envelope this layer emits
- `[[javascript]]` — TS standards
- `[[pnpm-package-management]]` — pnpm pin

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: Node service yes/no, owns lifecycle yes/no, can install helmet+rate-limit yes/no.
