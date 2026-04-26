# Next.js App Router

## Summary

The App Router is the file-system routing model introduced in Next.js 13, built on React Server Components. Every file under `app/` is a Server Component by default; client interactivity requires an explicit `'use client'` directive at the top of the file. Pages, layouts, loading skeletons, and error boundaries are separate colocated files (`page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`). Data fetching happens directly in Server Components via async/await — no `useEffect`, no `fetch`-to-API-route for internal data.

## Why

Server Components eliminate unnecessary client JS: the component renders on the server, sends HTML, and ships zero React hydration cost unless the component needs interactivity. Colocation of `loading.tsx` and `error.tsx` enables per-segment streaming and error isolation without global state. Server Actions replace the POST API route pattern for form submissions, keeping validation and DB writes server-side with automatic revalidation.

## When To Use

- Starting a new Next.js 13+ project from scratch
- Converting Pages Router routes to App Router (layout nesting, `loading.tsx`, `error.tsx`)
- Generating Server Actions for forms that currently use client-side fetch + API routes
- Setting up route groups `(group)`, parallel routes `@slot`, or intercepted routes for modal patterns
- Adding per-page streaming with `<Suspense>` and skeleton loading states

## When NOT To Use

- Projects already on Pages Router with no planned migration — mixing routers in one app is supported but creates cognitive overhead
- Applications with heavy client-side state that re-renders on every user action (complex canvas editors) — Server Components add serialization overhead with no render benefit
- REST API backends that use Next.js only for API routes — a dedicated Express/Fastify service is simpler
- Middleware that needs full Node.js API surface — middleware runs on Edge runtime, not Node.js

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | File conventions (`page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`), route groups, dynamic segments, project layout tree |
| `content/02-components.xml` | Server vs client component rules, `'use client'` placement, `React.cache()` deduplication, data fetching patterns |
| `content/03-server-actions.xml` | Server Actions authoring, Zod validation pattern, `revalidatePath`/`redirect` usage, API route replacement decision |
| `content/04-antipatterns.xml` | Common agent mistakes: `'use client'` on pages, synchronous `params` in Next.js 15, wrapping `redirect()` in try/catch |

## Templates

| File | Purpose |
|------|---------|
| `templates/root-layout.tsx` | Root `app/layout.tsx` with metadata, font, and Providers wrapper |
| `templates/dynamic-page.tsx` | Dynamic `[id]` page with `generateStaticParams`, `generateMetadata`, `notFound()` |
| `templates/server-action.ts` | Server Action with `'use server'`, Zod validation, `revalidatePath`, `redirect` |
| `templates/api-route.ts` | `route.ts` handler (GET + POST) with auth check and Zod validation |
| `templates/middleware.ts` | Auth middleware with `getToken`, matcher config, callback URL |
| `templates/prisma-singleton.ts` | Prisma client singleton preventing connection pool exhaustion in dev |
| `templates/prompt-scaffold-page.txt` | Prompt for scaffolding a new App Router page (page + loading + error + action) |
| `templates/prompt-convert-action.txt` | Prompt for converting a client-side form to a Server Action |
