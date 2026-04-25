# Agent Integration — SEO for SPAs

## When to use
- Migrating a CSR-only React/Vue/Angular app to SSR/SSG (Next.js, Nuxt, Remix, Angular Universal) for indexable content.
- Adding per-route meta + Open Graph + Twitter Card + canonical tags via Next `<Head>` / Metadata API or `react-helmet-async`.
- Implementing JSON-LD structured data for Product, Article, FAQ, BreadcrumbList, Organization.
- Generating `sitemap.xml` and `robots.txt` from data, plus hreflang for multi-locale apps.
- Auditing Core Web Vitals (LCP, INP, CLS) — the ranking-relevant subset of Lighthouse.

## When NOT to use
- Internal app behind auth — search engines can't reach it; SEO budget is wasted.
- Pure marketing-static site already on Astro / Gatsby / 11ty — those generate static HTML by default and most "SEO for SPA" patterns don't apply.
- The site is on Cloudflare Pages with full prerendering already configured — additional SSR plumbing is duplicate work.

## Where it fails / limitations
- Next.js App Router replaced `<Head>` with the `metadata` export. Agents copy Pages Router examples and ship duplicate `<head>` tags.
- Dynamic OG images: building one per request from `@vercel/og` is fine on Vercel/Edge; on a self-hosted Node server it eats CPU. Cache with `Cache-Control: public, max-age=31536000, immutable`.
- Googlebot now renders JS, but rendering is delayed and rate-limited. Critical content must be in the SSR HTML, not lazy-mounted.
- Canonical wars: `canonical` pointing to a URL that 301s to another canonical creates an indexing loop — easy to introduce via locale prefixes.
- `react-helmet` (legacy) is no longer maintained and has SSR memory leaks; use `react-helmet-async`.

## Agentic workflow
Treat SEO as a per-route task. Subagent reads the route, identifies the content type (Product, Article, etc.), and emits: (1) meta tags, (2) JSON-LD, (3) canonical, (4) sitemap entry, (5) Open Graph image source. Use Lighthouse (mobile preset), `linkinator` for broken links, and Google's Rich Results Test API as oracles. Keep humans in the loop for keyword strategy and copy — those are content decisions, not engineering.

### Recommended subagents
- `faion-feature-executor` — per-route SEO retrofits with Lighthouse + structured-data validation gates.
- `faion-sdd-executor-agent` — full-site SEO migrations (CSR → SSR) span spec, design (URL structure, sitemap), implementation, and tests.

### Prompt pattern
- "For `/products/[slug]`, generate the Next.js App Router `generateMetadata` export and a Product JSON-LD `<script>`. Pull data via `getProduct(slug)`. Include canonical, OG, Twitter, hreflang for `en` and `uk`."
- "Audit Lighthouse SEO + Best Practices on `https://staging.example.com/products/widget`. List failing audits with file paths and proposed fixes; do not edit yet."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx lighthouse <url> --preset=desktop --only-categories=seo,performance` | SEO + CWV audit | https://developer.chrome.com/docs/lighthouse/ |
| `pnpm dlx @lhci/cli autorun` | Lighthouse CI per PR | https://github.com/GoogleChrome/lighthouse-ci |
| `npx linkinator https://example.com --recurse` | Broken-link crawler for sitemap validation | https://github.com/JustinBeckwith/linkinator |
| `pnpm add -D next-sitemap` | Generate `sitemap.xml` + `robots.txt` from Next routes | https://github.com/iamvishnusankar/next-sitemap |
| `npx schema-dts-gen` | Type-safe JSON-LD via TypeScript | https://github.com/google/schema-dts |
| `pnpm dlx @vercel/og` | Programmatic OG image generation | https://vercel.com/docs/functions/og-image-generation |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Search Console | SaaS | Partial (REST API) | Coverage, Core Web Vitals, sitemap submit; agents can pull index status. |
| Google Rich Results Test | SaaS | Yes (web + URL inspection API) | Validate JSON-LD; treat as CI oracle for structured data. |
| Bing Webmaster Tools | SaaS | Yes (REST API) | Often forgotten; lower traffic but indexes faster for small sites. |
| Ahrefs / Semrush | SaaS | Partial (REST API, paid) | Backlinks + keyword data; out of scope for code agents. |
| Schema.org validator | OSS | Yes | https://validator.schema.org/ — wrap with curl. |
| WebPageTest | SaaS + OSS | Yes (REST) | CWV testing under throttled networks. |

## Templates & scripts
See `templates.md` for `getStaticProps`, `<Head>` boilerplate, JSON-LD examples. Minimal sitemap script for static export:

```ts
// scripts/build-sitemap.ts
import { writeFileSync } from 'node:fs';
const SITE = 'https://example.com';
const routes = ['/', '/about', '/products', ...await getProductSlugs()];
const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${routes.map(r => `  <url><loc>${SITE}${r}</loc><changefreq>weekly</changefreq></url>`).join('\n')}
</urlset>`;
writeFileSync('public/sitemap.xml', xml);
```

## Best practices
- Critical content must be in the SSR HTML, not appended via `useEffect`. Test with `curl <url> | grep <expected-text>`.
- One canonical per page. If you serve trailing-slash and non-trailing-slash variants, redirect 301 to the canonical form.
- JSON-LD goes in `<head>` (or just before `</body>`); place exactly one block per type per page. Multiple Product blocks confuse Googlebot.
- Keep meta description under 160 chars and unique per page; avoid templated "Welcome to X" descriptions.
- Set `Cache-Control` on OG images aggressively — they get crawled from Slack/Twitter/Facebook bots, all of which hit the URL hard.
- For multi-locale, pair `hreflang` tags with `<link rel="alternate">` and a sitemap `<xhtml:link>` block; tag mismatches are the #1 indexing bug.

## AI-agent gotchas
- Agents add `<title>` both via `metadata` export and a manual `<head>` element in a layout — Next dedupes inconsistently and one wins per route.
- Generated JSON-LD often hard-codes `@id` to a placeholder URL; Search Console flags as "missing `@id`" or duplicate.
- LLMs use `next/image` then forget the explicit `width`/`height`, causing CLS regressions that tank the SEO score.
- For dynamic OG images, agents fetch fonts inside the handler on every request; use the prebuilt edge runtime + `fetch` with cache headers.
- `robots.txt` regenerated by an agent often blocks `/api/` and accidentally `/api/og/*` — OG images stop appearing on social.
- Generated `sitemap.xml` includes draft / private routes when the route function returns all DB rows; filter by published flag.

## References
- Google Search Central, "Core Web Vitals" — https://developers.google.com/search/docs/appearance/core-web-vitals
- Schema.org — https://schema.org/docs/full.html
- Next.js Metadata API — https://nextjs.org/docs/app/api-reference/functions/generate-metadata
- `next-sitemap` — https://github.com/iamvishnusankar/next-sitemap
- Google Rich Results Test — https://search.google.com/test/rich-results
- web.dev "Learn SEO" — https://web.dev/learn/seo/
