# Next.js App Router

## Summary

Modern Next.js (13+) routing using React Server Components as the default, with client components only at the leaves. Covers segment structure (`page.tsx`, `loading.tsx`, `error.tsx`), Server Actions for mutations, Route Handlers for API endpoints, and middleware for auth.

## Why

Server Components render on the server and ship zero client JS by default, improving FCP and SEO. Keeping `'use client'` at the leaves rather than layout-level minimizes hydration cost. Server Actions with Zod validation remove the need for an internal API tier for mutations. Streaming via `Suspense` lets slow data fetches unblock fast ones.

## When To Use

- New Next.js 13+ projects (App Router is the default; Pages Router is legacy)
- SSR/SSG/ISR products where SEO and first-paint matter
- Apps with deep nested layouts and per-segment loading/error UI
- Server-first stacks calling the DB directly from RSCs without an internal API
- Form-heavy products using Server Actions with progressive enhancement

## When NOT To Use

- Migrating a working Pages Router app with no concrete pain — rewrite cost rarely pays off
- Static portfolio/brochure sites — Astro/Gatsby/11ty are simpler and cheaper
- Heavy realtime/dashboard SPAs — Vite + React Router is lighter; RSC adds little
- Teams with no Server Components experience and no capacity to learn the client/server boundary rules

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Core rules: server-first, 'use client' at leaves, serializable props, caching choices |
| `content/02-patterns.xml` | Segment structure, Server Actions, Route Handlers, middleware, anti-patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/next.config.ts` | Production-ready next.config.ts with bundle analyzer, typed routes, security headers |
