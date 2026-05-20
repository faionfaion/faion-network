---
slug: nextjs-app-router
tier: solo
group: dev
domain: javascript-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The App Router is the file-system routing model introduced in Next.
content_id: "307eeb4aa296acea"
tags: [nextjs, react, server-components, routing, app-router]
---
# Next.js App Router

## Summary

**One-sentence:** The App Router is the file-system routing model introduced in Next.

**One-paragraph:** The App Router is the file-system routing model introduced in Next.js 13, built on React Server Components. Every file under app/ is a Server Component by default; client interactivity requires an explicit 'use client' directive. Pages, layouts, loading skeletons, and error boundaries are separate colocated files (page.tsx, layout.tsx, loading.tsx, error.tsx). Data fetching happens directly in Server Components via async/await.

## Applies If (ALL must hold)

- Starting a new Next.js 13+ project from scratch
- Converting Pages Router routes to App Router (layout nesting, loading.tsx, error.tsx)
- Generating Server Actions for forms that currently use client-side fetch + API routes
- Setting up route groups (group), parallel routes @slot, or intercepted routes for modal patterns
- Adding per-page streaming with Suspense and skeleton loading states

## Skip If (ANY kills it)

- Projects already on Pages Router with no planned migration — mixing routers in one app is supported but creates cognitive overhead
- Applications with heavy client-side state that re-renders on every user action (complex canvas editors) — Server Components add serialization overhead with no render benefit
- REST API backends that use Next.js only for API routes — a dedicated Express/Fastify service is simpler
- Middleware that needs full Node.js API surface — middleware runs on Edge runtime, not Node.js

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

- parent skill: `solo/dev/javascript-developer/`
