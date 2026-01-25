# SEO Basics

**Core SEO principles, technical setup, and fundamentals.**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Technical** | robots.txt, sitemap.xml, crawl budget, Core Web Vitals |
| **On-Page** | Semantic HTML, schema markup, headings, meta tags |
| **Multilingual** | hreflang, URL structure, x-default |
| **AI/AEO** | llms.txt, structured data, entity optimization |
| **Social** | Open Graph, Twitter Cards, LinkedIn |
| **Accessibility** | WCAG 2.2, ARIA, screen readers, semantic markup |
| **Performance** | LCP < 2.5s, INP < 200ms, CLS < 0.1 |

---

## Core Principles

### 1. Dual Optimization Strategy

```
Traditional SEO (Google, Bing)
        ↓
    Your Content
        ↓
AI Search (ChatGPT, Perplexity, Claude)
```

**Both need:** Clear structure, authoritative content, proper markup, fast loading.

### 2. E-E-A-T Framework

- **Experience** → First-hand knowledge, case studies
- **Expertise** → Author credentials, depth of content
- **Authoritativeness** → Backlinks, citations, brand mentions
- **Trustworthiness** → HTTPS, contact info, privacy policy

---

## Technical SEO Fundamentals

### robots.txt Best Practices

```txt
# robots.txt - faion.net

User-agent: *
Disallow: /admin/
Disallow: /api/internal/
Disallow: /*?sessionid=
Disallow: /*?utm_
Allow: /api/public/

# AI Crawlers (manage separately)
User-agent: GPTBot
Disallow: /premium/
Allow: /

User-agent: Claude-Web
Disallow: /premium/
Allow: /

User-agent: PerplexityBot
Allow: /

# Sitemaps
Sitemap: https://faion.net/sitemap.xml
Sitemap: https://faion.net/sitemap-articles.xml
```

**Key Rules:**
- Block admin, session URLs, internal APIs
- Manage AI crawlers separately from search crawlers
- Always include Sitemap directive
- Never block CSS/JS files
- Test in Google Search Console before deploying

### sitemap.xml Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://faion.net/guides/sdd-methodology/</loc>
    <lastmod>2026-01-18</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <!-- Multilingual alternates -->
    <xhtml:link rel="alternate" hreflang="en" href="https://faion.net/en/guides/sdd-methodology/" />
    <xhtml:link rel="alternate" hreflang="uk" href="https://faion.net/uk/guides/sdd-methodology/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://faion.net/guides/sdd-methodology/" />
  </url>
</urlset>
```

**Best Practices:**
- Max 50,000 URLs per sitemap (use sitemap index for more)
- Update `lastmod` only when content changes
- Include in sitemap ONLY indexable pages
- Don't include URLs blocked in robots.txt

---

## Multilingual SEO & hreflang

### URL Structure Options

| Pattern | Example | Pros | Cons |
|---------|---------|------|------|
| **Subdirectories** (recommended) | `/uk/`, `/en/` | Easy to manage, shared domain authority | None significant |
| **Subdomains** | `uk.faion.net` | Separate hosting possible | Split domain authority |
| **ccTLDs** | `faion.ua` | Strong geo-signal | Expensive, complex management |
| **Parameters** ❌ | `?lang=uk` | Easy to implement | Poor SEO, indexing issues |

### hreflang Implementation

```html
<head>
  <!-- Self-referencing required -->
  <link rel="alternate" hreflang="en" href="https://faion.net/en/article/" />
  <link rel="alternate" hreflang="uk" href="https://faion.net/uk/article/" />
  <link rel="alternate" hreflang="de" href="https://faion.net/de/article/" />
  <link rel="alternate" hreflang="x-default" href="https://faion.net/article/" />
</head>
```

**Critical Rules:**
1. Self-referencing tag required on every page
2. Bidirectional linking (if A → B, then B → A)
3. Use ISO 639-1 language codes (en, uk, de)
4. Use ISO 3166-1 Alpha 2 for regions (en-US, en-GB)
5. x-default for language selector or global page
6. Metadata (title, description) MUST match page language
7. Never combine hreflang with noindex

---

## Semantic HTML & Accessibility

### Correct Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title | Site Name</title>
</head>
<body>
  <header role="banner">
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/">Home</a></li>
      </ul>
    </nav>
  </header>

  <main id="main-content">
    <article>
      <h1>Single H1 Per Page</h1>
      <p>Introduction...</p>

      <section aria-labelledby="section1">
        <h2 id="section1">Section Title</h2>
        <p>Content...</p>

        <h3>Subsection</h3>
        <p>More content...</p>
      </section>
    </article>

    <aside aria-label="Related content">
      <h2>Related Articles</h2>
    </aside>
  </main>

  <footer role="contentinfo">
    <p>&copy; 2026 Faion Network</p>
  </footer>
</body>
</html>
```

### Accessibility Checklist

- [ ] **Headings:** Logical hierarchy (H1 → H2 → H3), single H1
- [ ] **Images:** Descriptive alt text, decorative images: `alt=""`
- [ ] **Links:** Descriptive text (not "click here")
- [ ] **Forms:** Labels associated with inputs
- [ ] **Color:** Sufficient contrast (4.5:1 minimum)
- [ ] **Keyboard:** All interactive elements focusable
- [ ] **ARIA:** Use landmarks (banner, main, navigation, contentinfo)

---

## Core Web Vitals (2025)

### Target Metrics

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5s - 4s | > 4s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

### Optimization Checklist

**LCP:**
- [ ] Preload largest image: `<link rel="preload" as="image" href="...">`
- [ ] Use WebP/AVIF formats (25-35% smaller)
- [ ] Implement lazy loading for below-fold images
- [ ] Optimize server response time (TTFB < 800ms)
- [ ] Use CDN for static assets

**INP:**
- [ ] Minimize main thread blocking
- [ ] Break up long JavaScript tasks (< 50ms chunks)
- [ ] Defer non-critical JS
- [ ] Use `requestIdleCallback` for low-priority work

**CLS:**
- [ ] Always include width/height on images
- [ ] Reserve space for ads and embeds
- [ ] Avoid inserting content above existing content
- [ ] Use `font-display: swap` with font preload

---

## Quick Audits

### Technical SEO Checklist

- [ ] robots.txt configured correctly
- [ ] XML sitemap submitted to Search Console
- [ ] No duplicate content (canonical tags)
- [ ] HTTPS everywhere
- [ ] Mobile-friendly (responsive)
- [ ] Core Web Vitals passing
- [ ] No 4xx/5xx errors
- [ ] Proper redirects (301, not chains)

### On-Page SEO Checklist

- [ ] Unique title tag (50-60 chars)
- [ ] Meta description (120-160 chars)
- [ ] Single H1 with primary keyword
- [ ] Logical heading hierarchy
- [ ] Internal links to related content
- [ ] External links to authoritative sources
- [ ] Image alt text
- [ ] Schema markup

---

## Tools

| Tool | Purpose |
|------|---------|
| [Google Search Console](https://search.google.com/search-console) | Indexing, Core Web Vitals, errors |
| [PageSpeed Insights](https://pagespeed.web.dev/) | Performance analysis |
| [Rich Results Test](https://search.google.com/test/rich-results) | Schema validation |
| [Schema Validator](https://validator.schema.org/) | Schema.org validation |
| [Ahrefs/Semrush](https://ahrefs.com) | Backlinks, keywords, audits |
| [Screaming Frog](https://www.screamingfrog.co.uk/) | Technical crawling |
| [WAVE](https://wave.webaim.org/) | Accessibility testing |

---

## Sources

- [Google Search Central](https://developers.google.com/search)
- [Schema.org](https://schema.org/)
- [Web.dev](https://web.dev/)
- [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/)
