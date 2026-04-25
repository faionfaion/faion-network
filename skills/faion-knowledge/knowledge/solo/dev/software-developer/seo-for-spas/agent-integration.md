# Agent Integration — SEO for SPAs

## When to use
- Migrating CSR React/Vue/Angular app to SSR/SSG/ISR for indexable pages
- Auditing meta tags, canonical URLs, OG/Twitter cards across hundreds of dynamic routes
- Generating `sitemap.xml` + `robots.txt` from CMS or DB content at build time
- Wiring JSON-LD structured data (Product, Article, Breadcrumb, Organization)
- Fixing Core Web Vitals (LCP, CLS, INP) regressions surfaced by PageSpeed Insights
- Building OG image generation routes (`@vercel/og`, Satori) for share previews

## When NOT to use
- Authenticated dashboards / SaaS app shells — no SEO value, ship as CSR
- Internal tools / extranets behind login walls
- Native mobile or desktop Electron apps (no crawler concerns)
- Sites where social share previews + search ranking are explicitly not goals

## Where it fails / limitations
- Soft-404s: SPA returning 200 with empty body for missing slugs — Search Console flags, not the framework
- Hydration mismatches break SSR HTML before crawlers parse it; agents must read SSR output, not browser DOM
- Googlebot renders JS but Bing/Yandex/social crawlers do not always — test with `curl -A` per crawler
- ISR `revalidate` windows leak stale meta after content edits; `on-demand revalidation` required for editorial sites
- `next/image` blocks build when remote `domains` not configured; agents often miss this on new image sources
- Structured data validators (schema.org parser) reject objects with `undefined` values — JSON.stringify drops them but typed nesting can break

## Agentic workflow
Treat SEO as a verifiable build-time contract: agent generates pages + meta, then a second pass fetches the rendered HTML (not the SPA shell) and parses meta/JSON-LD with cheerio or `linkedom`. Pair with a Lighthouse CI run for Core Web Vitals; agent only ships when both gates pass. Long-tail content edits route through a humans-in-loop review for canonical decisions and duplicate-content collapses.

### Recommended subagents
- General-purpose subagent — implement SSR/ISR routes, meta components, sitemap generators
- `faion-feature-executor` — sequence: scaffold pages → wire meta → generate sitemap → run Lighthouse → fix
- `faion-sdd-execution` — quality gate that asserts every public route has `<title>`, `description`, canonical, OG image
- Browser-automation subagent (Playwright) — fetch SSR HTML and assert meta presence per route

### Prompt pattern
```
For each route in routes.json: render SSR HTML via `next build && next start`,
fetch with curl -A "Googlebot/2.1", parse with cheerio, assert:
- <title> present, length 30-65
- meta[name=description] present, length 120-160
- link[rel=canonical] absolute URL
- script[type=application/ld+json] valid against schema.org Product/Article
Fail the run on first miss; emit a JSON report keyed by route.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `lighthouse` / `lhci` | Core Web Vitals + SEO audit | `npm i -g @lhci/cli` |
| `next build` / `nuxt build` / `gatsby build` | SSR/SSG output | framework docs |
| `next-sitemap` | Sitemap + robots.txt for Next.js | `npm i next-sitemap` |
| `sitemap` (npm) | Programmatic sitemap | `npm i sitemap` |
| `schema-dts` | Typed schema.org JSON-LD | `npm i schema-dts` |
| `react-helmet-async` | Dynamic head for non-Next React | `npm i react-helmet-async` |
| `unlighthouse` | Crawl-the-whole-site Lighthouse | `npx unlighthouse --site` |
| `pa11y` | Accessibility (impacts SEO ranking) | `npm i -g pa11y` |
| Google Rich Results Test | Validate JSON-LD | `https://search.google.com/test/rich-results` |
| Bing/Google URL inspection API | Programmatic re-index | requires verified property |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Search Console | SaaS | Yes (API v1) | Crawl status, sitemap submit, Core Web Vitals report |
| Bing Webmaster Tools | SaaS | Yes (REST API) | URL submission API allows programmatic indexing |
| Cloudflare Pages / Vercel / Netlify | SaaS | Yes | Edge SSR, ISR, image optimization, OG image runtime |
| Ahrefs / Semrush | SaaS | Partial | Rank tracking, backlink audits via API; expensive |
| Screaming Frog SEO Spider | OSS desktop | CLI mode | Headless crawl with `--crawl` flag, exports CSV |
| `@vercel/og` | OSS | Yes | Edge OG image generation from JSX |
| Sanity / Contentful / Strapi | SaaS / OSS | Yes (webhooks) | Trigger ISR revalidation on publish |

## Templates & scripts
See `templates.md` for SSR meta component, sitemap generator, and JSON-LD helpers. Inline check script:

```bash
#!/usr/bin/env bash
# verify-seo.sh — fail the build if any route lacks SEO essentials
set -euo pipefail
BASE="${1:-http://localhost:3000}"
ROUTES_FILE="${2:-routes.txt}"
fail=0
while IFS= read -r path; do
  html=$(curl -fsSL -A "Googlebot/2.1" "$BASE$path")
  for sel in '<title>' 'name="description"' 'rel="canonical"' 'property="og:image"'; do
    grep -q "$sel" <<<"$html" || { echo "MISS $sel @ $path"; fail=1; }
  done
done < "$ROUTES_FILE"
exit $fail
```

## Best practices
- Hardcode the canonical host (`https://example.com`) in env, never read from `window.location.host` — preview deploys leak as canonical otherwise
- Generate OG images at edge with text-only fonts; avoid bundling display fonts >100KB into the image function
- Set `next/image` `priority` on the LCP image only; everywhere else it triggers preload spam that tanks performance
- Use `next-sitemap` `transform` to emit `<lastmod>` from CMS `updatedAt`, not build time — crawlers ignore "everything changed today"
- Split sitemaps at 50k URLs / 50MB; auto-emit a sitemap index file
- Robots: disallow `/api/`, preview deploys (`?preview=`), and search-result pages with infinite facet combos
- For pagination, prefer `rel=canonical` to page 1 and `rel=next/prev` (still respected by Bing) over `noindex` deep pages
- Validate JSON-LD against Google's Rich Results Test in CI, not just locally — Schema.org drift breaks rich snippets quietly

## AI-agent gotchas
- Agents reading the SPA via Playwright get the post-hydration DOM; Googlebot may timeout earlier — always also fetch raw SSR HTML via `curl` for ground truth
- LLMs hallucinate meta tag formats: `og:price:amount` vs `product:price:amount` (the latter is correct for Facebook product schema). Cross-check against ogp.me before shipping
- `dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}` — agents often forget to escape `</script>` inside JSON, breaking the page. Use `JSON.stringify(data).replace(/</g, '\\u003c')`
- Human-in-loop checkpoint required when: changing canonical strategy, adding `noindex`, restructuring URLs (301 plan), submitting reindex requests
- Token waste: do not feed the full Lighthouse JSON (often >2MB) into context; pre-extract only `audits` with score < 1
- Agents over-pack JSON-LD with optional fields and trip schema validation; keep to required + recommended properties only
- ISR + agent-driven content updates: agent must call the on-demand revalidate webhook after editing CMS, otherwise pages serve stale meta for hours

## References
- Google Search Central docs: https://developers.google.com/search
- Schema.org type catalog: https://schema.org/docs/full.html
- Open Graph protocol: https://ogp.me/
- web.dev Core Web Vitals: https://web.dev/vitals/
- Next.js Metadata API: https://nextjs.org/docs/app/building-your-application/optimizing/metadata
- Google Rich Results Test: https://search.google.com/test/rich-results
- `next-sitemap`: https://github.com/iamvishnusankar/next-sitemap
