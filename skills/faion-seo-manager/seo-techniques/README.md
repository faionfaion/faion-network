# SEO Techniques

**Advanced SEO tactics, schema markup, AI optimization, and content strategy.**

---

## AI Search Optimization (AEO)

### llms.txt Standard

```txt
# llms.txt - https://faion.net/llms.txt

# Faion Network
> AI-powered framework for solopreneurs with 282 methodologies and 43 AI agents

## Core Pages
- About: https://faion.net/about/
- Pricing: https://faion.net/pricing/
- Documentation: https://faion.net/docs/

## Products
- Ultimate Solopreneur Guide: https://faion.net/guide/
- SDD Methodology: https://faion.net/sdd/

## Contact
- Email: hello@faion.net
- Support: https://faion.net/support/

## Exclusions
- /premium/* (subscription required)
- /admin/*
```

**Purpose:**
- Provides AI crawlers with curated site structure
- Clarifies canonical sources
- Reduces hallucination risk
- Emerging standard (like robots.txt for AI)

### Structured Data for AI

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Faion Network",
  "description": "AI-powered framework for solopreneurs",
  "url": "https://faion.net",
  "founder": {
    "@type": "Person",
    "name": "Ruslan Faion"
  },
  "sameAs": [
    "https://twitter.com/faion",
    "https://linkedin.com/company/faion"
  ]
}
```

**Key Schema Types:**
- Organization, Person (brand/author)
- Article, BlogPosting (content)
- Product, Offer (e-commerce)
- FAQPage, HowTo (rich results + AI)
- BreadcrumbList (navigation)
- LocalBusiness (local SEO)

---

## Schema Markup (JSON-LD)

### Article Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "SDD Methodology: Complete Guide",
  "description": "Learn Specification-Driven Development...",
  "image": "https://faion.net/images/sdd-guide.jpg",
  "author": {
    "@type": "Person",
    "name": "Ruslan Faion",
    "url": "https://faion.net/about/"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Faion Network",
    "logo": {
      "@type": "ImageObject",
      "url": "https://faion.net/logo.png"
    }
  },
  "datePublished": "2026-01-15",
  "dateModified": "2026-01-18"
}
```

### Breadcrumb Schema

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://faion.net/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Guides",
      "item": "https://faion.net/guides/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "SDD Methodology"
    }
  ]
}
```

### FAQ Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is SDD?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SDD (Specification-Driven Development) is..."
      }
    }
  ]
}
```

---

## Social Meta Tags

### Open Graph (Facebook, LinkedIn)

```html
<meta property="og:type" content="article" />
<meta property="og:title" content="SDD Methodology Guide" />
<meta property="og:description" content="Learn how to build products faster..." />
<meta property="og:image" content="https://faion.net/og-image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:url" content="https://faion.net/guides/sdd/" />
<meta property="og:site_name" content="Faion Network" />
<meta property="og:locale" content="en_US" />
<meta property="og:locale:alternate" content="uk_UA" />
```

### Twitter Cards

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@faion" />
<meta name="twitter:creator" content="@ruslanfaion" />
<meta name="twitter:title" content="SDD Methodology Guide" />
<meta name="twitter:description" content="Learn how to build products faster..." />
<meta name="twitter:image" content="https://faion.net/twitter-image.jpg" />
```

**Image Requirements:**
- Minimum: 1200x630px (1.91:1 ratio)
- Max file size: 8MB
- Formats: JPG, PNG, GIF, WebP
- Always use absolute URLs

---

## Internal Linking Strategy

### Pillar-Cluster Model

```
             ┌─────────────────┐
             │  Pillar Page    │
             │ (Head Keyword)  │
             └────────┬────────┘
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ Cluster │  │ Cluster │  │ Cluster │
   │ (Long-  │  │ (Long-  │  │ (Long-  │
   │  tail)  │  │  tail)  │  │  tail)  │
   └─────────┘  └─────────┘  └─────────┘
```

### Avoiding Keyword Cannibalization

| Issue | Solution |
|-------|----------|
| Multiple pages targeting same keyword | Consolidate with 301 redirects |
| Similar content competing | Merge into comprehensive guide |
| Unclear primary page | Increase internal links to preferred page |
| Same anchor text for different pages | Use unique anchors per target page |

### Best Practices

1. **One primary keyword per page** → map keywords to URLs
2. **Internal links from high-authority pages** → pass link equity
3. **Contextual links within content** → better than footer/sidebar
4. **Descriptive anchor text** → tells Google what page is about
5. **Regular audits** → find orphan pages, broken links

---

## Breadcrumbs

### Implementation

```html
<nav aria-label="Breadcrumb">
  <ol itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="https://faion.net/">
        <span itemprop="name">Home</span>
      </a>
      <meta itemprop="position" content="1" />
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="https://faion.net/guides/">
        <span itemprop="name">Guides</span>
      </a>
      <meta itemprop="position" content="2" />
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <span itemprop="name">SDD Methodology</span>
      <meta itemprop="position" content="3" />
    </li>
  </ol>
</nav>
```

**Rules:**
- 3-5 levels maximum
- Reflect actual site hierarchy
- Last item = current page (no link)
- Include JSON-LD schema
- Visible on desktop (removed from mobile SERPs Jan 2025)

---

## AI/AEO Checklist

- [ ] llms.txt file created
- [ ] Organization schema
- [ ] FAQPage schema for Q&A content
- [ ] Clear, factual content structure
- [ ] Entity connections (author, organization)
- [ ] Recent publish/update dates

---

## References

- [references/technical-seo.md](references/technical-seo.md) - robots.txt, sitemaps, crawl budget
- [references/multilingual.md](references/multilingual.md) - hreflang, URL structure
- [references/schema.md](references/schema.md) - JSON-LD templates
- [references/aeo.md](references/aeo.md) - AI optimization, llms.txt
- [references/accessibility.md](references/accessibility.md) - WCAG, ARIA
- [references/performance.md](references/performance.md) - Core Web Vitals

---

## Sources

- [Yoast SEO Blog](https://yoast.com/seo-blog/)
- [Search Engine Land](https://searchengineland.com/)
- [Backlinko](https://backlinko.com/)
