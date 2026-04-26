# SEO Techniques

## Summary

Advanced SEO tactics covering schema markup (JSON-LD), AI search optimization
(llms.txt, AEO-ready content structure), social meta tags (Open Graph, Twitter Cards),
pillar-cluster internal linking, and entity optimization for knowledge graph inclusion.
The core rule: validate all JSON-LD with Google Rich Results Test before deployment —
agents produce syntactically plausible but semantically incorrect schema.

## Why

Technical SEO signals (structured data, social meta, internal link equity) determine
whether content earns rich snippets, AI citations, and proper social previews.
Schema markup mistakes are silent — invalid JSON-LD passes the linter but produces
no rich results. A pillar-cluster internal link structure distributes authority from
high-value pages to long-tail clusters, improving ranking across the topic.

## When To Use

- Implementing or auditing schema markup on content-heavy pages (articles, FAQs, products)
- Publishing content that should be cited by AI engines (llms.txt + AEO structure)
- Adding social sharing meta tags (Open Graph, Twitter Cards) to a site
- Building or auditing a pillar-cluster internal link structure
- Optimizing for Google AI Overviews, featured snippets, or voice search

## When NOT To Use

- Site has no indexed content yet — schema on empty pages provides no benefit
- Technical SEO issues (crawl errors, indexing blocks, Core Web Vitals failures) are
  unresolved — fix fundamentals before adding schema
- Single-page apps without server-side rendering — schema injected client-side is
  not reliably parsed by crawlers; requires SSR

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema-markup.xml` | Article, Breadcrumb, FAQ, Organization JSON-LD patterns and validation workflow |
| `content/02-ai-optimization.xml` | llms.txt standard, AEO content structure, entity optimization for AI citation |
| `content/03-social-meta-and-linking.xml` | Open Graph, Twitter Cards, pillar-cluster internal linking, cannibalization fixes |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema-article.json` | Article schema JSON-LD template |
| `templates/schema-faq.json` | FAQPage schema JSON-LD template |
| `templates/schema-organization.json` | Organization + Person schema JSON-LD template |
| `templates/schema-breadcrumb.json` | BreadcrumbList schema JSON-LD template |
| `templates/llms-txt.txt` | llms.txt file template for AI crawlers |
| `templates/og-meta.html` | Open Graph + Twitter Card meta tag block |
