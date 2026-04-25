# Agent Integration — Next.js App Router

## When to use
- Bootstrapping a new Next.js 13+ project and deciding file-based routing structure before writing pages
- Converting Pages Router routes to App Router equivalents (layout nesting, loading.tsx, error.tsx)
- Generating Server Actions for form submissions that currently use client-side fetch + API routes
- Setting up route groups, parallel routes, or intercepted routes for modal patterns

## When NOT to use
- Projects already on Pages Router with no planned migration — mixing routers in one app is supported but creates cognitive overhead
- Applications with heavy client-side state that re-renders on every user action (e.g. complex canvas editors) — Server Components add serialization overhead with no render benefit
- REST API backends that happen to use Next.js only for API routes — a dedicated Express/Fastify service is simpler

## Where it fails / limitations
- Server Components cannot use React hooks, event handlers, or browser APIs; agents frequently add `useState` inside a Server Component without the `'use client'` directive
- Data fetching inside Server Components is not automatically deduplicated across a request unless using `React.cache()`; duplicate DB calls are invisible to the developer
- Server Actions have a 1MB payload limit by default; file uploads require a different approach (presigned URLs + direct-to-storage)
- Middleware runs on the Edge runtime (limited Node.js API surface) — agents importing Node.js-only modules in middleware cause silent build failures
- `generateStaticParams` must return all possible param values at build time; dynamic data sources (database) require a build-time DB connection

## Agentic workflow
An agent scaffolds a new page by reading the root `app/layout.tsx` to understand existing providers and font setup, then generating the page file, a loading skeleton, and an error boundary in the correct directory. For data-fetching pages, the agent determines whether to use a Server Component with direct DB access or a client component with React Query based on interactivity requirements. Server Actions are generated as separate `actions.ts` files colocated with the route, not inlined in the page.

### Recommended subagents
- `faion-sdd-executor-agent` — executes multi-step page scaffolding tasks (layout → page → loading → error → action) with type-check gates

### Prompt pattern
```
Generate a Next.js App Router page for route /<route-path>.
Requirements:
- Server Component (no 'use client' unless interactive)
- Auth check using getServerSession, redirect to /login if no session
- Suspense boundaries with skeleton loading states
- generateMetadata export with page title: "<Title>"
- Data fetching: read from <data source> directly (no API route needed)
Output files: app/<route>/page.tsx, app/<route>/loading.tsx, app/<route>/error.tsx
```

```
Convert this form from client-side fetch to a Next.js Server Action.
Current: POST /api/<endpoint> with JSON body.
Target: app/actions.ts with 'use server', Zod validation, revalidatePath, redirect on success.
Return { error } object on validation failure so the client can show field errors.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `next dev` | Development server with HMR and error overlay | Built into Next.js |
| `next build` | Production build with static analysis | Built into Next.js |
| `@next/bundle-analyzer` | Visualize JS bundle sizes | `npm i @next/bundle-analyzer` / https://github.com/vercel/next.js/tree/canary/packages/next-bundle-analyzer |
| `next-auth` / `Auth.js` | Authentication with server session support | `npm i next-auth` / https://authjs.dev |
| `next-intl` | i18n for App Router with server component support | `npm i next-intl` / https://next-intl-docs.vercel.app |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Vercel | SaaS | Yes | Native Next.js deployment; agent can generate `vercel.json` config and review build logs |
| Prisma | OSS | Yes | Direct DB access in Server Components; agent must ensure Prisma client is not instantiated per-request |
| React Query (TanStack Query) | OSS | Partial | Needed for client-side mutations with optimistic updates; agent must mark consuming components `'use client'` |
| Uploadthing | SaaS | Yes | File upload for App Router with presigned URLs; avoids Server Action payload limits |
| Vercel Analytics | SaaS | Yes | Zero-config analytics for Next.js; agent adds `<Analytics />` to root layout |

## Templates & scripts
See `templates.md` for root layout, dynamic page, API route, and middleware templates.

Prisma singleton for App Router (prevents connection pool exhaustion in dev):
```typescript
// lib/db.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const db =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error'] : ['error'],
  });

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = db;
}
```

## Best practices
- Use `React.cache()` to deduplicate identical DB calls made in multiple Server Components during the same request — agents must wrap fetch/DB helper functions with it
- Colocate `loading.tsx` and `error.tsx` with every page that fetches data asynchronously; missing `loading.tsx` causes the entire layout to block during navigation
- Route groups `(group-name)` allow multiple layouts without URL nesting; use them to avoid duplicating providers across auth and non-auth sections
- API routes (`route.ts`) should only be created for webhook endpoints or third-party integrations; all internal data access goes through Server Components or Server Actions
- Middleware matcher pattern must be explicit — avoid `matcher: '/'` patterns that catch static assets and API routes unnecessarily

## AI-agent gotchas
- Agents add `'use client'` to pages that only need interactivity in a child component — the directive should move to the child, keeping the page as a Server Component
- `params` in dynamic segments is a `Promise<{ id: string }>` in Next.js 15 (requires `await params`), but agents trained on Next.js 13/14 patterns generate synchronous `params.id` access
- `redirect()` and `notFound()` inside Server Components throw internally and must NOT be wrapped in try/catch; agents frequently wrap them, swallowing the redirect
- Server Actions are only available in forms or client event handlers — calling a `'use server'` function from a Server Component directly is just a regular async function call with no RPC overhead; agents may add unnecessary `'use server'` at file level
- Human checkpoint needed before adding middleware matchers that protect auth routes, to verify session token handling is correct and logout flow does not create redirect loops

## References
- https://nextjs.org/docs/app
- https://nextjs.org/docs/app/building-your-application/rendering/server-components
- https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
- https://nextjs.org/learn
- https://vercel.com/docs/frameworks/nextjs
