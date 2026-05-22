---
slug: nodejs-express-fastify
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for building production Node.
content_id: "98e4f4321c71df5c"
tags: [nodejs, express, fastify, http-api, typescript]
---
# Express / Fastify Patterns

## Summary

**One-sentence:** A methodology for building production Node.

**One-paragraph:** A methodology for building production Node.js HTTP APIs with Express or Fastify: structured middleware stack (helmet, cors, rate-limit, pino), centralized error handler, schema-validated routes (Zod for Express, TypeBox for Fastify), JWT auth decorator, and graceful shutdown on SIGTERM/SIGINT. Choose Express for ecosystem breadth; Fastify for high-throughput TypeScript-first JSON APIs.

## Applies If (ALL must hold)

- Bootstrapping a Node.js HTTP API needing a known-good middleware stack.
- Choosing between Express (ecosystem) and Fastify (performance, schema, TS-first).
- Migrating an Express app to TypeScript-strict + Zod or Fastify + TypeBox.
- Greenfield service with fewer than 10 routes where full Nest/Adonis is overkill.
- Designing route, error-handler, and auth boundaries an agent can extend safely.

## Skip If (ANY kills it)

- Heavy realtime / streaming workloads — uWebSockets or Go service is cheaper.
- Edge-runtime targets (Cloudflare Workers, Vercel Edge) — use Hono or itty-router.
- Frontend-only / full-stack frameworks (Next.js Route Handlers, Remix, SvelteKit).
- Codebases already standardized on Nest or tRPC — mixing is double-tooling.
- Python or Go shops without Node expertise — unnecessary runtime to operate.

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

- parent skill: `free/dev/software-developer/`
