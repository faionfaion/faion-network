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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bun-runtime-simple.py` | Validate the service-spec artefact + Bun version | After scaffold, before commit |

## Related

- - [[javascript-modern]] — TS-first principles still apply.
- - [[javascript-testing]] — bun:test is Jest-compatible; same patterns transfer.

## Decision tree

See `content/06-decision-tree.xml`. Branches: route count (≤5 simple / &gt;5 needs grouping) → Hono with or without grouping. Auth shape (none / token / session) → Bun.password and which primitive to use.
