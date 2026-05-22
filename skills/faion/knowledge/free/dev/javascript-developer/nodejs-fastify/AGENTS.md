---
slug: nodejs-fastify
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Scaffolds a high-perf TypeScript-first Fastify service with JSON-Schema validation, plugin architecture, and built-in security + rate-limiting.
content_id: "84e81fabe60bc913"
complexity: medium
produces: code
est_tokens: 3700
tags: [fastify, nodejs, rest-api, json-schema, plugins]
---
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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nodejs-fastify.py` | Validate Fastify service spec + plugin order | After scaffold |

## Related

- [[nodejs-express]] — lower-perf alternative; pick if team already on Express.
- [[javascript-modern]] — TS strict + named exports.

## Decision tree

See `content/06-decision-tree.xml`. Branches: surface (REST / WebSocket / GraphQL) → plugin choice. TypeBox vs Ajv schemas → pick TypeBox for TS-first.
