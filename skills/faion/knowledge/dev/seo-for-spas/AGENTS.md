# SEO for SPAs

## Summary

**One-sentence:** SEO spec for SPAs: rendering mode (SSG / SSR / ISR / hybrid), per-page metadata + structured data, canonical URLs, sitemap, hreflang for i18n, Core Web Vitals targets.

**One-paragraph:** SPAs lose SEO when content depends on JS for the first paint, when meta tags are global instead of per-route, when canonical and hreflang are missing, and when LCP is dominated by client-side hydration. This methodology produces an SEO spec: rendering mode picked per route (SSG, SSR, ISR), per-page metadata (title, description, OG, structured data JSON-LD), canonical URL per route, hreflang for i18n, sitemap.xml + robots.txt, and Core Web Vitals targets (LCP<=2.5s, INP<=200ms, CLS<=0.1).

**Ефективно для:**

- Next.js / Nuxt / Remix app з search-driven traffic - вибрати rendering mode per route.
- Marketing pages ховаються від Google - hydration-only без SSR/SSG.
- Duplicate-content issues - відсутні canonical URL.
- Multi-language site - відсутні hreflang.
- LCP > 4s - перевести above-the-fold на SSR/SSG.

## Applies If (ALL must hold)

- Web property has search-driven traffic as a goal.
- Codebase is a SPA / framework with rendering options (Next, Nuxt, Remix, Astro, Gatsby).
- Team can ship per-route rendering mode changes.
- Analytics + Search Console access available to verify outcomes.

## Skip If (ANY kills it)

- Site is a logged-in dashboard with noindex policy.
- Web property is entirely brand promotion via paid social - no SEO budget.
- App lives behind auth wall with no public pages.
- Team has chosen a server-rendered framework already (plain Django / Rails) - SPA SEO is moot.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Route map | list of routes + traffic class (marketing / product / dashboard) | product |
| Locale list | supported languages + url pattern | i18n |
| Core Web Vitals baseline | current LCP / INP / CLS p75 | analytics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pwa-development]] | shared SPA shell concerns and offline behaviour. |
| [[performance-testing]] | Core Web Vitals interleave with perf SLOs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: rendering mode per route, per-page metadata, structured data, hreflang, sitemap+robots, CWV targets, no client-only above the fold | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: routes, metadata, structured data, sitemap+hreflang, CWV targets | ~900 |
| `content/05-examples.xml` | essential | Worked example for a multi-locale content site | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-routes` | sonnet | Per-route judgement on traffic + freshness. |
| `metadata-templates` | haiku | Boilerplate metadata API wiring. |
| `structured-data` | sonnet | Map template fields to schema.org type. |
| `cwv-budget` | opus | Stakes high; CWV is a ranking factor. |

## Templates

| File | Purpose |
|------|---------|
| `templates/metadata.ts` | Next.js app-router metadata + structured data per route. |
| `templates/sitemap.ts` | Sitemap generator stub for Next.js app router. |
| `templates/seo-component.tsx` | Reusable SEO head component with JSON-LD + canonical + OG tags. |
| `templates/verify-seo.sh` | Bash smoke-check: fetch route, assert title/og:image/canonical present. |
| `templates/_smoke-test.json` | Minimum viable SEO spec for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-seo-for-spas.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[pwa-development]]
- [[performance-testing]]
- [[react-component-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - rendering mode per route, metadata scope, locale presence, CWV baseline - onto a rule from `content/01-core-rules.xml`. Use it before launch: it catches csr-marketing and global-metadata upstream.
