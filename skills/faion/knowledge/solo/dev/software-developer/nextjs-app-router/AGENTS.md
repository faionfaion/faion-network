---
slug: nextjs-app-router
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Build with Next.js 14+ App Router using server components by default, server actions for mutations, and explicit `'use client'` boundaries.
content_id: "fdc9b008dcb7413c"
complexity: medium
produces: code
est_tokens: 4200
tags: [nextjs, react, server-components, routing, app-router]
---
# Next.js App Router

## Summary

**One-sentence:** Build with Next.js 14+ App Router using server components by default, server actions for mutations, and explicit `'use client'` boundaries.

**One-paragraph:** Modern Next.js apps default to React Server Components in app/; client interactivity lives only behind explicit `'use client'` boundaries. Mutations use server actions (no API routes for form submits). Loading + error states use the conventions (loading.tsx, error.tsx) per segment. Data fetching is colocated with the component. Output is the routing tree + server/client boundaries + server action set.

**Ефективно для:**

- Greenfield Next.js >=14 apps.
- Migrating Pages Router projects to App Router.
- Replacing client-fetch + spinner patterns with server-rendered + suspense.
- Producing SEO-friendly + fast-paint marketing or product surfaces.

## Applies If (ALL must hold)

- Next.js >=14 (App Router stable).
- Stack supports server runtime (Node or Edge) — not static export only.
- Project owns the routing layer (not embedded into another framework).
- Team is comfortable with React Server Components mental model.

## Skip If (ANY kills it)

- Project locked on Pages Router for legacy reasons.
- Static export only (server components and actions don't apply).
- App is wrapped in a different routing framework (Remix, TanStack Router).
- Tiny prototype where the App Router overhead exceeds payoff.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Next.js version + Node version pinned | config | platform |
| Auth strategy (Next-Auth, Clerk, custom JWT) | ADR | tech-lead |
| Data layer (Postgres + Drizzle/Prisma, REST API, GraphQL) | ADR | tech-lead |
| Caching strategy (revalidatePath / revalidateTag / static) | ADR | tech-lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[frontend-design]] | Design tokens + component library follow separately. |
| [[api-error-handling]] | Server actions surface domain errors consistently. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (server-components by default, explicit use-client, server actions for mutations, loading+error conventions, no fetch in client components, revalidate explicit) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for App Router spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: route map → server components → client boundaries → server actions → caching | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `route_tree_design` | sonnet | Mechanical: layout/page/loading/error per segment. |
| `server_action_authoring` | opus | Form + revalidation patterns need synthesis. |
| `caching_strategy` | opus | revalidatePath vs revalidateTag vs static decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/next.config.ts` | Next.js config with experimental flags + image domains |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nextjs-app-router.py` | Validate App Router spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[react-component-architecture]]
- [[frontend-design]]
- [[monorepo-turborepo]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps Next.js version, routing scope, and team familiarity to a rule from `01-core-rules.xml`, telling the agent whether to apply App Router patterns or skip for Pages Router / static-only. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
