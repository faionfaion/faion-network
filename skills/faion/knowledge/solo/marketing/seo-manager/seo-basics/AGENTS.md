# SEO Basics

## Summary

Core technical SEO foundations: robots.txt configuration, XML sitemap structure, multilingual hreflang implementation, semantic HTML with accessibility (WCAG 2.2), and Core Web Vitals optimization (LCP, INP, CLS). These are the prerequisite building blocks before any on-page or off-page SEO work.

## Why

Search engines cannot rank pages they cannot crawl and index. Poor Core Web Vitals cause ranking demotions since 2021 (page experience update). Correct hreflang prevents duplicate content penalties for multilingual sites. Semantic HTML satisfies both accessibility requirements and Google's understanding of page structure — the same markup that helps screen readers helps crawlers.

## When To Use

- Setting up a new site's technical SEO foundation
- Auditing an existing site for crawlability and indexability issues
- Implementing multilingual SEO (hreflang + URL structure)
- Diagnosing Core Web Vitals failures (LCP, INP, CLS)
- Ensuring WCAG 2.2 accessibility compliance alongside SEO

## When NOT To Use

- When content quality and keyword strategy are the bottleneck — technical fixes alone won't improve rankings for thin content
- When the site has zero traffic and content — build content first
- For AEO/AI search optimization — use technical-seo-for-ai methodology instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-technical-foundation.xml` | robots.txt rules, sitemap.xml structure, HTTPS/redirect setup |
| `content/02-multilingual-hreflang.xml` | URL structure options, hreflang implementation rules, metadata localization |
| `content/03-semantic-html-accessibility.xml` | HTML structure, WCAG 2.2 checklist, ARIA landmarks |
| `content/04-core-web-vitals.xml` | LCP/INP/CLS targets and optimization checklists |

## Templates

| File | Purpose |
|------|---------|
| `templates/robots-txt.txt` | robots.txt with AI crawler rules and sitemap directive |
| `templates/sitemap-xml.xml` | XML sitemap template with hreflang alternates |
| `templates/hreflang-html.txt` | hreflang link tags for HTML head |
| `templates/semantic-html.txt` | Semantic HTML page structure with ARIA landmarks |
