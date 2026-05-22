---
slug: seo-for-spas
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for making JavaScript-heavy applications indexable.
content_id: "9e1fb98853ad1f54"
tags: [seo, spa, meta-tags, ssr, structured-data]
---
# SEO for SPAs

## Summary

**One-sentence:** A methodology for making JavaScript-heavy applications indexable.

**One-paragraph:** A methodology for making JavaScript-heavy applications indexable. Every public route must deliver title, meta[name=description], link[rel=canonical], og:image, and valid JSON-LD in the server-rendered HTML — not just the post-hydration DOM. Verify with curl -A "Googlebot/2.1", not Playwright. Treat SEO as a build-time contract verified by Lighthouse CI on every PR.

## Applies If (ALL must hold)

- Migrating CSR React/Vue/Angular app to SSR/SSG/ISR for indexable pages
- Auditing meta tags and OG/Twitter cards across dynamic routes
- Generating sitemap.xml + robots.txt from CMS or DB content at build time
- Wiring JSON-LD structured data (Product, Article, Breadcrumb, Organization)
- Fixing Core Web Vitals regressions surfaced by PageSpeed Insights
- Building OG image generation routes for share previews

## Skip If (ANY kills it)

- Authenticated dashboards or SaaS app shells — no SEO value, ship as CSR
- Internal tools or extranets behind login walls
- Sites where social share previews and search ranking are not goals

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
