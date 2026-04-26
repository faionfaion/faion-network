# SEO for SPAs

## Summary

A methodology for making JavaScript Single Page Applications indexable by search engines. Covers server-side rendering for first paint, per-page meta tag management, JSON-LD structured data, crawlable link patterns, sitemap generation, and Core Web Vitals performance.

## Why

Search engines historically struggled with client-rendered SPAs because crawlers see an empty HTML shell until JS executes. SSR ensures critical content appears in the initial HTML response; without it, Google may index blank pages or rank content poorly. Core Web Vitals (LCP, CLS, FID) are ranking signals — a SPA that loads slowly loses rank even if content is present.

## When To Use

- Building React, Vue, or Angular apps for public web with search visibility requirements
- Content-heavy sites: blogs, e-commerce, marketing pages
- When pages need unique Open Graph previews for social sharing
- When crawlability audit reveals missing meta tags or JavaScript-gated content

## When NOT To Use

- Internal dashboards or authenticated apps with no public search requirement — SSR overhead is not justified
- Prototypes or MVPs where SEO is explicitly out of scope
- Apps using a separate static marketing site for SEO (e.g. Gatsby landing + React app)

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | SSR, meta tags, canonical URL, crawlable links — concrete rules with rationale |
| `content/02-structured-data.xml` | JSON-LD patterns for Product, Article, Breadcrumb with code examples |
| `content/03-performance.xml` | Core Web Vitals rules, Next.js image/lazy-load optimizations, sitemap generation |

## Templates

| File | Purpose |
|------|---------|
| `templates/seo-component.tsx` | Reusable SEO head component for React Helmet or Next.js Head |
| `templates/structured-data.tsx` | StructuredData component + Product/Article/Breadcrumb schemas |
| `templates/generate-sitemap.ts` | Sitemap + robots.txt generation script |
