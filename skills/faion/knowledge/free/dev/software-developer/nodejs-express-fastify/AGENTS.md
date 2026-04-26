# Express / Fastify Patterns

## Summary

A methodology for building production Node.js HTTP APIs with Express or Fastify: structured middleware stack (helmet, cors, rate-limit, pino), centralized error handler, schema-validated routes (Zod for Express, TypeBox for Fastify), JWT auth decorator, and graceful shutdown on SIGTERM/SIGINT. Choose Express for ecosystem breadth; Fastify for high-throughput TypeScript-first JSON APIs.

## Why

Express's implicit middleware order and lack of built-in validation cause silent security gaps and inconsistent error shapes. Fastify's plugin encapsulation and schema-first design prevent these but introduce non-obvious scoping rules. Both frameworks require a deliberate middleware stack to be production-safe — missing any one piece (rate-limit, error handler, graceful shutdown) creates either reliability or security issues that only manifest under load or during deploys.

## When To Use

- Bootstrapping a Node.js HTTP API needing a known-good middleware stack.
- Choosing between Express (ecosystem) and Fastify (performance, schema, TS-first).
- Migrating an Express app to TypeScript-strict + Zod or Fastify + TypeBox.
- Greenfield service with fewer than 10 routes where full Nest/Adonis is overkill.
- Designing route, error-handler, and auth boundaries an agent can extend safely.

## When NOT To Use

- Heavy realtime / streaming workloads — uWebSockets or Go service is cheaper.
- Edge-runtime targets (Cloudflare Workers, Vercel Edge) — use Hono or itty-router.
- Frontend-only / full-stack frameworks (Next.js Route Handlers, Remix, SvelteKit).
- Codebases already standardized on Nest or tRPC — mixing is double-tooling.
- Python or Go shops without Node expertise — unnecessary runtime to operate.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Middleware order rules, validation requirement, error handler placement, graceful shutdown |
| `content/02-examples.xml` | Express app setup, Express router, Fastify setup, Fastify TypeBox routes, auth middleware |
| `content/03-antipatterns.xml` | Antipatterns: callback hell, missing next(err), no schema, CORS wildcard + credentials, hardcoded secrets |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-routes.sh` | Script: flag route handlers missing schema, auth, or error wiring |
