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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/metadata.ts`

```typescript
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next';

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: `https://example.com/blog/${post.slug}`,
      languages: { en: `/en/blog/${post.slug}`, uk: `/uk/blog/${post.slug}`, 'x-default': `/blog/${post.slug}` },
    },
    openGraph: { title: post.title, description: post.excerpt, type: 'article', images: [post.cover] },
  };
}

export default async function Page({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);
  const jsonLd = { '@context': 'https://schema.org', '@type': 'Article', headline: post.title, datePublished: post.date };
  return (<><script type='application/ld+json'>{JSON.stringify(jsonLd)}</script><article>{post.body}</article></>);
}

async function getPost(_slug: string) { return { slug: _slug, title: 'x', excerpt: 'y', date: '2026-01-01', body: 'z', cover: '/og.png' }; }
```

### `templates/sitemap.ts`

```typescript
import type { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await fetchAllPosts();
  return [
    { url: 'https://example.com/', lastModified: new Date(), changeFrequency: 'weekly', priority: 1 },
    ...posts.map((p) => ({ url: `https://example.com/blog/${p.slug}`, lastModified: p.updated })),
  ];
}

async function fetchAllPosts(): Promise<Array<{ slug: string; updated: Date }>> { return [{ slug: 'hello', updated: new Date() }]; }
```

### `templates/seo-component.tsx`

```tsx
// seo-component.tsx — Universal SEO component
// Supports Next.js (pages router via next/head) and non-Next React (react-helmet-async).
// All fields are required. og:image must be absolute URL 1200x630.

import Head from 'next/head'; // swap for Helmet from 'react-helmet-async' if not Next.js

interface SEOProps {
  title: string;            // 30-65 chars
  description: string;      // 120-160 chars
  canonicalUrl: string;     // absolute URL from env, never window.location
  ogImage: string;          // absolute URL, 1200x630 recommended
  ogType?: 'website' | 'article' | 'product';
  noIndex?: boolean;        // true only for admin/preview routes
}

export function SEO({
  title,
  description,
  canonicalUrl,
  ogImage,
  ogType = 'website',
  noIndex = false,
}: SEOProps) {
  const siteName = process.env.NEXT_PUBLIC_SITE_NAME ?? 'My Site';

  return (
    <Head>
      {/* Primary */}
      <title>{`${title} | ${siteName}`}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={canonicalUrl} />
      {noIndex && <meta name="robots" content="noindex, nofollow" />}

      {/* Open Graph */}
      <meta property="og:type" content={ogType} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={ogImage} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:url" content={canonicalUrl} />
      <meta property="og:site_name" content={siteName} />

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImage} />
    </Head>
  );
}

// JSON-LD injection helper (safe escaping)
interface JsonLdProps {
  data: object;
}

export function JsonLd({ data }: JsonLdProps) {
  // Escape </script> to prevent early tag close
  const safeJson = JSON.stringify(data).replace(/</g, '\\u003c');
  return (
    <Head>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: safeJson }}
      />
    </Head>
  );
}
```

### `templates/verify-seo.sh`

```bash
#!/usr/bin/env bash
# verify-seo.sh — Assert SEO essentials on each route via Googlebot curl
# Usage: ./verify-seo.sh http://localhost:3000 routes.txt
# routes.txt: one path per line (e.g. /products/widget-a)
# Exit 1 if any route is missing any required element.

set -euo pipefail

BASE="${1:-http://localhost:3000}"
ROUTES_FILE="${2:-routes.txt}"
FAIL=0

REQUIRED=(
  '<title>'
  'name="description"'
  'rel="canonical"'
  'property="og:image"'
  'property="og:title"'
  'property="og:url"'
  'twitter:card'
)

while IFS= read -r path; do
  [[ -z "$path" || "$path" == \#* ]] && continue
  html=$(curl -fsSL -A "Googlebot/2.1" "$BASE$path" 2>/dev/null) || {
    echo "FETCH_FAIL $path"
    FAIL=1
    continue
  }
  for sel in "${REQUIRED[@]}"; do
    grep -q "$sel" <<<"$html" || {
      echo "MISS [$sel] @ $path"
      FAIL=1
    }
  done
done < "$ROUTES_FILE"

if [[ $FAIL -eq 0 ]]; then
  echo "OK all routes passed SEO check"
fi
exit $FAIL
```

### `templates/_smoke-test.json`

```json
{
  "routes": [
    {
      "path": "/",
      "rendering_mode": "SSG"
    }
  ],
  "metadata_strategy": "per_route",
  "structured_data": {
    "enabled": true,
    "types": [
      "Article"
    ]
  },
  "sitemap": {
    "path": "/sitemap.xml",
    "auto_generated": true
  },
  "cwv_targets": {
    "lcp_ms": 2500,
    "inp_ms": 200,
    "cls": 0.1
  }
}
```
