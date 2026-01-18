# Multilingual SEO Reference

## URL Structure Decision Matrix

| Structure | Example | Best For | Considerations |
|-----------|---------|----------|----------------|
| **Subdirectories** | `/uk/`, `/en/` | Most sites | ✅ Single domain authority, easy CDN |
| **Subdomains** | `uk.example.com` | Separate teams/servers | ⚠️ Treated as separate sites |
| **ccTLDs** | `example.ua` | Country-specific businesses | ⚠️ Expensive, complex, separate SEO |
| **Parameters** | `?lang=uk` | ❌ Avoid | Poor indexing, tracking issues |

### Recommended: Subdirectory Structure

```
https://faion.net/           → Default (English or language selector)
https://faion.net/en/        → English
https://faion.net/uk/        → Ukrainian
https://faion.net/de/        → German
https://faion.net/es/        → Spanish
https://faion.net/pt-br/     → Portuguese (Brazil)
```

---

## hreflang Implementation

### Method 1: HTML Head (Recommended for small sites)

```html
<head>
  <link rel="alternate" hreflang="en" href="https://faion.net/en/page/" />
  <link rel="alternate" hreflang="uk" href="https://faion.net/uk/page/" />
  <link rel="alternate" hreflang="de" href="https://faion.net/de/page/" />
  <link rel="alternate" hreflang="x-default" href="https://faion.net/page/" />
</head>
```

### Method 2: XML Sitemap (Recommended for large sites)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://faion.net/en/page/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://faion.net/en/page/" />
    <xhtml:link rel="alternate" hreflang="uk" href="https://faion.net/uk/page/" />
    <xhtml:link rel="alternate" hreflang="de" href="https://faion.net/de/page/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://faion.net/page/" />
  </url>
  <url>
    <loc>https://faion.net/uk/page/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://faion.net/en/page/" />
    <xhtml:link rel="alternate" hreflang="uk" href="https://faion.net/uk/page/" />
    <xhtml:link rel="alternate" hreflang="de" href="https://faion.net/de/page/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://faion.net/page/" />
  </url>
</urlset>
```

### Method 3: HTTP Headers (For non-HTML files like PDFs)

```
HTTP/1.1 200 OK
Link: <https://faion.net/en/doc.pdf>; rel="alternate"; hreflang="en",
      <https://faion.net/uk/doc.pdf>; rel="alternate"; hreflang="uk",
      <https://faion.net/doc.pdf>; rel="alternate"; hreflang="x-default"
```

---

## Language & Region Codes

### Language Codes (ISO 639-1)

| Code | Language |
|------|----------|
| en | English |
| uk | Ukrainian |
| de | German |
| fr | French |
| es | Spanish |
| pt | Portuguese |
| pl | Polish |
| hi | Hindi |
| zh | Chinese |
| ja | Japanese |

### Language + Region Codes

| Code | Target |
|------|--------|
| en-US | English (United States) |
| en-GB | English (United Kingdom) |
| en-AU | English (Australia) |
| pt-BR | Portuguese (Brazil) |
| pt-PT | Portuguese (Portugal) |
| zh-CN | Chinese (Simplified, China) |
| zh-TW | Chinese (Traditional, Taiwan) |
| es-ES | Spanish (Spain) |
| es-MX | Spanish (Mexico) |

### x-default Usage

```html
<!-- Option 1: Language selector page -->
<link rel="alternate" hreflang="x-default" href="https://faion.net/choose-language/" />

<!-- Option 2: Default language version -->
<link rel="alternate" hreflang="x-default" href="https://faion.net/en/" />

<!-- Option 3: Auto-detecting page -->
<link rel="alternate" hreflang="x-default" href="https://faion.net/" />
```

---

## Critical Rules

### Must Follow

1. **Self-referencing tags** - Every page must include hreflang pointing to itself
2. **Bidirectional linking** - If EN links to UK, UK must link back to EN
3. **Consistent URLs** - Same URLs in hreflang and sitemap
4. **Match canonical** - hreflang URL should be the canonical URL
5. **Complete set** - All language versions must have all hreflang tags

### Must Avoid

1. **hreflang + noindex** - Never combine (pick one)
2. **hreflang to redirected URLs** - Must point to final URL
3. **Country-only codes** - `hreflang="us"` is invalid (need language)
4. **Mixing methods** - Don't use HTML and sitemap for same page
5. **Broken reciprocal links** - Missing return links

---

## Localization Checklist

### Content

- [ ] **Translations** - Professional, not machine-only
- [ ] **Cultural adaptation** - Local examples, references
- [ ] **Local keywords** - Research per language
- [ ] **Date formats** - DD/MM/YYYY vs MM/DD/YYYY
- [ ] **Currency** - Local currency with proper formatting
- [ ] **Phone numbers** - Include country code
- [ ] **Addresses** - Local format

### Technical

- [ ] **Meta titles** - Translated, keyword-optimized
- [ ] **Meta descriptions** - Translated, locally relevant
- [ ] **Alt text** - Translated for images
- [ ] **Schema markup** - `inLanguage` property set
- [ ] **Open Graph** - `og:locale` and `og:locale:alternate`

### UX

- [ ] **Language switcher** - Visible, uses native language names
- [ ] **No auto-redirects** - Let users choose language
- [ ] **Remember preference** - Cookie/localStorage
- [ ] **Visible URL change** - Users see language in URL

---

## AI Search & Multilingual Sites (2025)

### Key Insight

> Sites with translated versions achieve up to **327% more visibility** in Google's AI Overviews for searches made in languages they did not originally serve.
> — Weglot 2025 Research (1.3M citations analyzed)

### Optimization for AI

1. **Translate key pages** - About, Products, FAQ
2. **Use hreflang** - Helps AI understand language relationships
3. **Schema `inLanguage`** - Add to Article, Product schemas
4. **llms.txt per language** - Consider language-specific versions

```json
{
  "@type": "Article",
  "inLanguage": "uk",
  "headline": "SDD Методологія",
  ...
}
```
