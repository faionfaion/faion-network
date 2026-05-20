---
slug: cloudflare-pages-github
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Connect a GitHub repository to Cloudflare Pages so every push to the production branch publishes to the global CDN and every pull request gets its own preview URL.
content_id: "ea301b0e8ef20ac9"
tags: [cloudflare, pages, static-site, github, cdn, wrangler, preview-deploys]
---
# Cloudflare Pages from a GitHub Repo

## Summary

**One-sentence:** Connect a GitHub repository to Cloudflare Pages so every push to the production branch publishes to the global CDN and every pull request gets its own preview URL.

**One-paragraph:** Connect a GitHub repository to Cloudflare Pages so every push to the production branch publishes to the global CDN and every pull request gets its own preview URL. Configure framework preset, build command, output directory, environment variables (split production vs preview), custom domain with SSL Full Strict, `_headers` and `_redirects` files, optional Pages Functions for edge logic, and Wrangler CLI for local parity.

## Applies If (ALL must hold)

- Astro / Next.js (static export) / Gatsby / Hugo / Vite SPA / SvelteKit static repo on GitHub.
- You want a global CDN with a generous free tier (unlimited bandwidth, 500 builds/month).
- You want automatic preview-per-PR with a unique URL on `*.pages.dev`.
- You need edge handlers for redirects, A/B tests, geo-routing, or lightweight APIs (Pages Functions).
- You serve a custom domain with managed SSL and want CF-Cache-Status on every response.

## Skip If (ANY kills it)

- Heavy server-side runtime that needs a custom Node version not on the Pages-supported matrix — use a regular VPS or Workers.
- Monorepo where the build takes longer than 20 minutes — Pages caps build time; switch to GitHub Actions + Wrangler direct deploy.
- Traffic that exceeds the free tier without a billing plan — switch to paid plan or migrate to Workers + R2.
- Server-rendered Next.js without the `@cloudflare/next-on-pages` adapter — runtime errors at the edge.
- Apps that need long-running background jobs — Functions hit the 30-second CPU limit; use Workers Queues / Cron Triggers.

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

- parent skill: `solo/infra/server-craft/`
