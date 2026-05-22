---
slug: seo-for-spas
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for making JavaScript Single Page Applications indexable by search engines.
content_id: "9e1fb98853ad1f54"
tags: [seo, spa, ssr, structured-data, core-web-vitals, sitemap]
---
# SEO for SPAs

## Summary

**One-sentence:** A methodology for making JavaScript Single Page Applications indexable by search engines.

**One-paragraph:** A methodology for making JavaScript Single Page Applications indexable by search engines. Covers server-side rendering for first paint, per-page meta tag management, JSON-LD structured data, crawlable link patterns, sitemap generation, and Core Web Vitals performance.

## Applies If (ALL must hold)

- Migrating a CSR-only React/Vue/Angular app to SSR/SSG (Next.js, Nuxt, Remix, Angular Universal) for indexable content.
- Adding per-route meta + Open Graph + Twitter Card + canonical tags via Next `<Head>` / Metadata API or `react-helmet-async`.
- Implementing JSON-LD structured data for Product, Article, FAQ, BreadcrumbList, Organization.
- Generating `sitemap.xml` and `robots.txt` from data, plus hreflang for multi-locale apps.
- Auditing Core Web Vitals (LCP, INP, CLS) — the ranking-relevant subset of Lighthouse.

## Skip If (ANY kills it)

- Internal app behind auth — search engines can't reach it; SEO budget is wasted.
- Pure marketing-static site already on Astro / Gatsby / 11ty — those generate static HTML by default and most "SEO for SPA" patterns don't apply.
- The site is on Cloudflare Pages with full prerendering already configured — additional SSR plumbing is duplicate work.

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

- parent skill: `solo/dev/frontend-developer/`
