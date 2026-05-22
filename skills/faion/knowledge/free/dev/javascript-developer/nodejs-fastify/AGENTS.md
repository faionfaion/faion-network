---
slug: nodejs-fastify
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Fastify is a modern web framework for Node.
content_id: "057eb26df510dcdc"
tags: [nodejs, fastify, typescript, rest-api, http-framework]
---
# Fastify Framework Patterns

## Summary

**One-sentence:** Fastify is a modern web framework for Node.

**One-paragraph:** Fastify is a modern web framework for Node.js that prioritizes performance, TypeScript support, and comprehensive schema validation using JSON Schema and TypeBox. Features a plugin architecture, built-in security, rate limiting, CORS, graceful shutdown, and custom error handling.

## Applies If (ALL must hold)

- Performance-critical APIs where high RPS and fast serialization matter.
- TypeScript-first projects requiring strict type safety and schema validation.
- Greenfield HTTP APIs with JSON payloads and microservices architectures.
- Migrating Express 4/5 services that have outgrown ad-hoc validation.
- Building secure-by-default services where helmet, rate limiting, JWT, and CORS are required.

## Skip If (ANY kills it)

- Edge-runtime targets (Cloudflare Workers, Vercel Edge) — use Hono or Itty Router instead; Fastify is Node-native only.
- Static-site or thin SSR layers — use Next.js, SvelteKit, or similar frameworks that own the HTTP layer.
- WebSocket-heavy realtime applications — Socket.IO or uWebSockets.js may suit better despite Fastify's @fastify/websocket plugin.
- Trivial scripts and CLIs — Fastify boot weight exceeds value for minimal utilities.
- Bun-only services without specific Fastify plugins — use Bun.serve with Hono for lighter footprint.

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
