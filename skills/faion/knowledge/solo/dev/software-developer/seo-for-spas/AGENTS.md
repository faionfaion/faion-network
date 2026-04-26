# SEO for SPAs

## Summary

A methodology for making JavaScript-heavy applications indexable. Every public route must deliver `<title>`, `meta[name=description]`, `link[rel=canonical]`, `og:image`, and valid JSON-LD in the server-rendered HTML — not just the post-hydration DOM. Verify with `curl -A "Googlebot/2.1"`, not Playwright. Treat SEO as a build-time contract verified by Lighthouse CI on every PR.

## Why

Googlebot renders JS but Bing, Yandex, and social crawlers often do not. SSR/SSG/ISR ensures the first HTML response carries discoverable content. Dynamic meta tags drive social sharing (Open Graph, Twitter Card). JSON-LD structured data enables rich results. Core Web Vitals (LCP, CLS, INP) directly affect search ranking. Without CI verification, meta tags silently regress across route changes.

## When To Use

- Migrating CSR React/Vue/Angular app to SSR/SSG/ISR for indexable pages
- Auditing meta tags and OG/Twitter cards across dynamic routes
- Generating `sitemap.xml` + `robots.txt` from CMS or DB content at build time
- Wiring JSON-LD structured data (Product, Article, Breadcrumb, Organization)
- Fixing Core Web Vitals regressions surfaced by PageSpeed Insights
- Building OG image generation routes for share previews

## When NOT To Use

- Authenticated dashboards or SaaS app shells — no SEO value, ship as CSR
- Internal tools or extranets behind login walls
- Sites where social share previews and search ranking are not goals

## Content

| File | What's inside |
|------|---------------|
| `content/01-ssr-and-meta.xml` | SSR rules, meta tag requirements per route, canonical URL, OG/Twitter card fields |
| `content/02-structured-data-and-sitemap.xml` | JSON-LD product/article/breadcrumb schemas, sitemap generation, robots.txt rules |
| `content/03-antipatterns.xml` | Client-only content, JavaScript-only navigation, ISR stale meta, og:image escaping bug |

## Templates

| File | Purpose |
|------|---------|
| `templates/seo-component.tsx` | React SEO component (Next.js Head + react-helmet-async) with all required fields |
| `templates/verify-seo.sh` | Build-time bash script that curl-fetches each route and asserts meta presence |
