# Technical SEO for AI

## Summary

Technical optimizations that make content accessible and trustworthy to AI crawlers (GPTBot, Claude-Web, PerplexityBot): creating `llms.txt` for AI crawler guidance, implementing Article schema with author credentials, clean URL structure, proper heading hierarchy, entity consistency, and explicit author authority signals. Different from traditional SEO — AI crawlers evaluate factual accuracy and authority, not just keyword density.

## Why

AI crawlers have different evaluation criteria than Google's crawler: they assess entity clarity, factual verifiability, author credentials, cross-platform consistency, and content freshness. Without `llms.txt`, AI crawlers may ingest premium/private content or ignore important pages. Without schema markup including author credentials, content appears unattributed. As AI-generated search results replace traditional SERPs, technical AI-readiness becomes a prerequisite for visibility.

## When To Use

- Setting up a new content site or blog that needs AI crawler visibility from launch.
- Auditing an existing site for AI crawlability issues (missing schema, no `llms.txt`, ambiguous entity naming).
- Implementing author credential markup to improve E-E-A-T signals for AI systems.
- Optimizing Core Web Vitals for AI crawler accessibility (LCP < 2.5s, CLS < 0.1).

## When NOT To Use

- Paywalled or premium content sites where AI crawling of content is undesirable — configure `llms.txt` to block rather than optimize.
- Sites with no original content (pure aggregators) — technical optimization cannot compensate for lack of authority.
- Short-lived campaign landing pages with no long-term SEO value.

## Content

| File | What's inside |
|------|---------------|
| `content/01-crawler-config.xml` | llms.txt format, robots.txt AI crawler rules, URL structure requirements for AI parsing. |
| `content/02-schema-authority.xml` | Article schema with author credentials, Organization schema, FAQSchema, entity markup rules. |
| `content/03-content-structure.xml` | Heading hierarchy, entity clarity, factual content structure, freshness strategy, authority signals. |

## Templates

| File | Purpose |
|------|---------|
| `templates/llms-txt.txt` | llms.txt template with crawler guidance, citation format, important page declarations. |
| `templates/article-schema.json` | Article schema JSON-LD with author credentials, datePublished, dateModified fields. |
