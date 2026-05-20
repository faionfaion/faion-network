---
slug: seo-techniques
tier: solo
group: marketing
domain: seo-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Advanced SEO tactics covering schema markup (JSON-LD), AI search optimization (llms.
content_id: "6e1d298802e4e2d8"
tags: [seo, schema-markup, json-ld, social-meta, internal-linking]
---
# SEO Techniques

## Summary

**One-sentence:** Advanced SEO tactics covering schema markup (JSON-LD), AI search optimization (llms.

**One-paragraph:** Advanced SEO tactics covering schema markup (JSON-LD), AI search optimization (llms.txt, AEO-ready content structure), social meta tags (Open Graph, Twitter Cards), pillar-cluster internal linking, and entity optimization for knowledge graph inclusion. The core rule: validate all JSON-LD with Google Rich Results Test before deployment — agents produce syntactically plausible but semantically incorrect schema.

## Applies If (ALL must hold)

- Implementing or auditing schema markup on content-heavy pages (articles, FAQs, products)
- Publishing content that should be cited by AI engines (llms.txt + AEO structure)
- Adding social sharing meta tags (Open Graph, Twitter Cards) to a site
- Building or auditing a pillar-cluster internal link structure
- Optimizing for Google AI Overviews, featured snippets, or voice search

## Skip If (ANY kills it)

- Site has no indexed content yet — schema on empty pages provides no benefit
- Technical SEO issues (crawl errors, indexing blocks, Core Web Vitals failures) are unresolved — fix fundamentals before adding schema
- Single-page apps without server-side rendering — schema injected client-side is not reliably parsed by crawlers; requires SSR

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/marketing/seo-manager/`
