---
slug: nodejs-express
tier: free
group: dev
domain: javascript-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-grade REST API framework for Node.
content_id: "4b1e6ba1d24c67f8"
tags: [nodejs, express, rest-api, typescript, middleware]
---
# Express Framework Patterns

## Summary

**One-sentence:** Production-grade REST API framework for Node.

**One-paragraph:** Production-grade REST API framework for Node.js. Set up Express with middleware in order (helmet → cors → compression → json → pinoHttp → rateLimit → routes → notFoundHandler → errorHandler). Use Zod schemas for input validation, centralized error handler for consistent responses, graceful shutdown (SIGTERM/SIGINT), and structured JSON logging with Pino.

## Applies If (ALL must hold)

- REST APIs and microservices on Node 20/22 where ecosystem compatibility is priority.
- Adding a new resource (router + controller + service + schema + tests) to an existing Express service.
- Hardening a hand-rolled Express server: add helmet, cors, compression, pino-http, express-rate-limit, graceful shutdown.
- Centralizing error handling with AppError + Zod-aware error middleware in a project that currently mixes res.status(...).json(...) everywhere.

## Skip If (ANY kills it)

- New projects targeting peak throughput — Fastify is 2-3x faster on the same hardware.
- Edge runtimes (Cloudflare Workers, Vercel Edge) — Express depends on Node-only APIs.
- Greenfield Bun-only services where Bun.serve removes the framework entirely.
- A microservice that only needs WebSockets — bare ws or uWebSockets.js beats Express middleware overhead.

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
