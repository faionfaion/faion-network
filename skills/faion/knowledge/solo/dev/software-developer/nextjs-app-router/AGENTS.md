---
slug: nextjs-app-router
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Modern Next.
content_id: "307eeb4aa296acea"
tags: [nextjs, react, server-components, routing, app-router]
---
# Next.js App Router

## Summary

**One-sentence:** Modern Next.

**One-paragraph:** Modern Next.js (13+) routing using React Server Components as the default, with client components only at the leaves. Covers segment structure (page.tsx, loading.tsx, error.tsx), Server Actions for mutations, Route Handlers for API endpoints, and middleware for auth.

## Applies If (ALL must hold)

- New Next.js 13+ projects (App Router is the default; Pages Router is legacy).
- SSR/SSG/ISR products where SEO and first-paint matter.
- Apps with deep nested layouts and per-segment loading/error UI.
- Server-first stacks calling the DB directly from RSCs without an internal API.
- Form-heavy products using Server Actions with progressive enhancement.

## Skip If (ANY kills it)

- Migrating a working Pages Router app with no concrete pain — rewrite cost rarely pays off.
- Static portfolio/brochure sites — Astro/Gatsby/11ty are simpler and cheaper.
- Heavy realtime/dashboard SPAs — Vite + React Router is lighter; RSC adds little.
- Apps that must run on serverless without a Node-compatible runtime (some Workers, Lambda@Edge) — Server Components are a tight fit only on Vercel and Node-compatible hosts.
- Teams with no Server Components experience and no time to learn — bugs in client/server boundary are subtle and frequent.

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

- parent skill: `solo/dev/software-developer/`
