---
slug: nodejs-patterns
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Backend patterns for Express and modern Node.
content_id: "d03e2aafee5b52e1"
tags: [nodejs, express, backend, patterns, architecture]
---
# Node.js Patterns

## Summary

**One-sentence:** Backend patterns for Express and modern Node.

**One-paragraph:** Backend patterns for Express and modern Node.js, covering application structure, middleware ordering, controller/service layer separation, centralized error handling, and Pino request logging.

## Applies If (ALL must hold)

- Bootstrapping a new TypeScript Express API with controllers, services, middleware, errors, and Pino logger.
- Refactoring an existing JS/TS Node service into a layered structure with central error handling.
- Adding a new domain (resource) to an existing Express app while following the project's module layout.
- Wiring request-scoped logging (request ID, duration) into an existing Express server.
- Teams seeking a scalable, testable backend structure that resists feature bloat.

## Skip If (ANY kills it)

- Pure CLI/script Node code with no HTTP layer — routing/controller scaffolding is overhead.
- Edge-runtime targets (Cloudflare Workers, Vercel Edge, Deno Deploy) — Express is Node-only; use Hono instead.
- High-throughput WebSocket-first services — Express middleware chain is slow; use uWebSockets.js or Fastify.
- Frontend-only React projects — no Node server is owned.
- Single-file scripts where latency/startup matter more than modularity.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `free/dev/javascript-developer/`
