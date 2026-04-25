# Agent Integration — Next.js App Router

## When to use
- Greenfield Next.js 13+ projects (treat App Router as the default; Pages Router is legacy).
- SSR / SSG / ISR products where SEO + first-paint matter (marketing site, blog, e-commerce, docs).
- Apps with deep nested layouts and per-segment loading/error UI.
- Server-first stacks where you want to call the DB directly from RSCs and skip an internal API tier.
- Form-heavy products that benefit from Server Actions + progressive enhancement.

## When NOT to use
- Migrating a working Pages Router app with no concrete pain — App Router is a big change for marginal wins.
- Static portfolio / brochure sites — Astro / Gatsby / 11ty are simpler and cheaper.
- Heavy realtime / dashboard SPAs — Vite + React Router or TanStack Router is lighter; RSC adds little.
- Apps that must run on serverless without a Node-compatible runtime (some Workers, Lambda@Edge) — Server Components are a tight fit only on Vercel and Node-compatible hosts.
- Teams with no Server Components experience and no time to learn — bugs in client/server boundary are subtle and frequent.

## Where it fails / limitations
- Caching model is opaque; `fetch` cache, `unstable_cache`, route segment config, and Route Handler caching interact in non-obvious ways.
- `'use client'` is viral: importing a client component into a server component is fine, but the inverse is not — and one stray `useState` poisons the whole tree above.
- Server Actions require careful CSRF + size limits; the default 1 MB body limit catches teams off guard.
- Streaming with `Suspense` + `loading.tsx` interacts oddly with `<head>` metadata in some browsers (FOUC, late-arriving title).
- ISR + on-demand revalidation works on Vercel; self-hosting it (Node, Docker) needs manual cache adapter setup.
- `cookies()` / `headers()` / `searchParams` are dynamic APIs — touching them in a layout opts the whole route into dynamic rendering.
- Middleware runs on the Edge runtime by default — `node:` imports break silently.
- Parallel routes (`@modal`) and intercepting routes (`(.)photo`) are powerful but rarely understood; LLMs misuse them.
- Build-time `generateStaticParams` calls real APIs; without rate-limit awareness, builds can DoS your own backend.

## Agentic workflow
A planner subagent decides per route: server vs client, static vs dynamic, ISR window, where to put `Suspense`. An implementer subagent scaffolds the segment (`page.tsx`, `loading.tsx`, `error.tsx`, `layout.tsx` if needed) and emits Server Actions or Route Handlers as appropriate. A boundary-auditor subagent walks the import graph and flags accidental client-component leaks (`useState` reaching into a server component). A perf subagent runs Lighthouse CI on key routes and inspects `next build` output for unexpected dynamic rendering.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → segment → tests → review.
- A user-defined `rsc-boundary-auditor` (model: sonnet) — checks every `'use client'` placement; flags client-only hooks reaching into server tree.
- A user-defined `nextbuild-analyzer` (model: haiku) — parses `next build` output, surfaces unexpected `λ` dynamic routes that should be `○` static or `ƒ` ISR.
- `password-scrubber-agent` — sweep server actions and route handlers before commit.

### Prompt pattern
- "Read `nextjs-app-router/README.md`. Add segment `app/(app)/projects/[id]/`. Decide: server or client? static or dynamic? Output a 5-bullet plan, then emit `page.tsx`, `loading.tsx`, `error.tsx`. Server Component by default — only add `'use client'` for the comments box. Use `notFound()` for missing project. Add `generateMetadata` reading from `getProject(id)`."
- "Walk all `app/**/*.tsx`. For each file with `'use client'`, list which props it accepts and whether they cross the server/client boundary as serializable JSON. Flag any prop typed as `() => void` or `Date` (non-serializable). Output a markdown table."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `next` CLI | dev / build / start / lint | bundled |
| `next-bundle-analyzer` | Inspect server/client bundle splits | `npm i -D @next/bundle-analyzer` |
| `next-on-pages` / `next-on-cf` | Deploy to Cloudflare Workers | https://github.com/cloudflare/next-on-pages |
| `vercel` CLI | Deploy + env mgmt | `npm i -g vercel` |
| `eslint-config-next` | Built-in lint rules incl. `react-server-components` checks | included |
| `lighthouse-ci` | Perf / SEO budgets in CI | `npm i -D @lhci/cli` |
| `playwright` | E2E + a11y on real Next builds | `npm init playwright@latest` |
| `next-test-api-route-handler` | Unit-test Route Handlers | `npm i -D next-test-api-route-handler` |
| `taintObjectReference` (React 19) | Server-only data tainting | built-in |
| `serverpod`/`drizzle-kit`/`prisma` | DB schema management used inside RSCs | per ORM |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Vercel | SaaS | Yes (CLI + REST) | First-party host; ISR + Edge cache built in. |
| Cloudflare Pages | SaaS | Yes | Use `next-on-pages`; some Node APIs missing. |
| Netlify | SaaS | Yes | Adapter exists; ISR supported. |
| Self-host (Node / Docker) | OSS | Yes | Bring-your-own cache adapter for ISR; works fine. |
| Sanity / Contentful / Sanity / Hygraph / Storyblok | SaaS | Yes | CMS targets; pair with `generateStaticParams` + ISR. |
| Clerk / NextAuth / Auth.js / Supabase Auth | SaaS / OSS | Yes | Auth providers with App Router-native middleware + `getServerSession`. |
| Stripe | SaaS | Yes | Server Actions + webhook Route Handlers fit cleanly. |
| Sentry | SaaS | Yes | Has a Next adapter that handles RSC + Server Actions. |

## Templates & scripts
See `templates.md`. Minimal `next.config.ts` + bundle-analyzer wiring an agent should set up early:

```ts
// next.config.ts
import type { NextConfig } from 'next';
import bundleAnalyzer from '@next/bundle-analyzer';

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
});

const config: NextConfig = {
  experimental: {
    typedRoutes: true,
    serverActions: { bodySizeLimit: '2mb' },
  },
  images: {
    remotePatterns: [{ protocol: 'https', hostname: 'cdn.example.com' }],
  },
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=()' },
        ],
      },
    ];
  },
};

export default withBundleAnalyzer(config);
```

## Best practices
- Default every component to Server Component; promote to Client only when you need state, effects, browser APIs, or event handlers.
- Keep `'use client'` at the **leaves**; never put it at a layout level if you can avoid it.
- Pass only **serializable** props across the boundary (no functions, Dates, Maps); use a server-side `<form action>` instead of click handlers when possible.
- Co-locate data fetching with the component that uses it (RSC + `await`), not in a parent layout.
- Wrap slow data fetches in `<Suspense>` with a meaningful skeleton, not generic spinners.
- For dynamic routes, choose: full SSG (`generateStaticParams` returns full set), partial PPR (Next 14+), or pure ISR (`revalidate: 60`). Document the choice per route.
- Use Server Actions for mutations + `revalidatePath` / `revalidateTag` to refresh exactly what changed.
- Cache Route Handlers explicitly with `export const dynamic = 'force-static' | 'auto' | 'force-dynamic'`.
- Always set `Cache-Control` headers on Route Handlers serving public data; default is `no-store` in dev.
- Validate Server Action inputs with `zod`; never trust `formData` directly.
- Use `next/image` for every image with explicit width/height; configure `remotePatterns` for external CDNs.
- Add `metadataBase`, `default` title template, and per-page `generateMetadata` for proper SEO.
- Set `experimental.typedRoutes: true` so `<Link href>` is type-checked.
- Audit `next build` output for unexpected dynamic routes (`λ`); each is a missed cache opportunity.
- For self-hosting, configure a `cacheHandler` (Redis-backed) in `next.config.ts`.

## AI-agent gotchas
- LLMs default to `'use client'` at the top of every component because the training data is full of pre-RSC code. Strip it whenever it's not needed.
- Agents pass non-serializable props (functions, Dates, class instances) from server to client — silent runtime errors. The boundary auditor catches these.
- `cookies()` / `headers()` is async in the new Next; LLMs forget to `await` and pass a Promise around.
- Agents write `useEffect(() => fetch('/api/x'))` inside a client component when they should fetch in the parent server component and pass data down.
- LLMs misuse parallel/intercepting routes; if not specifically asked, avoid them — they almost always over-engineer the route tree.
- Server Actions: agents forget `'use server'` directive (top of file or function), and the action silently becomes a client function.
- `revalidatePath` and `revalidateTag` are easy to mix up; agents over-invalidate (`'/'`) and tank the cache hit rate.
- Middleware: agents add Node-only imports (`crypto`, `fs`) to `middleware.ts` — Edge runtime breaks.
- `generateStaticParams` returning thousands of slugs without batching = build OOM or backend DoS. Force pagination + warmup logic.
- Hydration mismatches: agents emit `Date.now()` / `Math.random()` in server components and trip "text content did not match" errors. Pin or move to client.
- Human-in-loop checkpoint: cache-related changes (`revalidate`, `dynamic`, `cacheHandler`, ISR) must be reviewed; subtle config drift can serve stale data for hours.
- Don't let an agent silently delete `loading.tsx` / `error.tsx` — those are required for graceful UX and SEO.

## References
- App Router docs — https://nextjs.org/docs/app
- Server Components — https://nextjs.org/docs/app/building-your-application/rendering/server-components
- Server Actions — https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
- Caching reference — https://nextjs.org/docs/app/building-your-application/caching
- Middleware — https://nextjs.org/docs/app/building-your-application/routing/middleware
- React server components RFC — https://github.com/reactjs/rfcs/pull/188
- `next-on-pages` — https://github.com/cloudflare/next-on-pages
- Vercel docs — https://vercel.com/docs/frameworks/nextjs
