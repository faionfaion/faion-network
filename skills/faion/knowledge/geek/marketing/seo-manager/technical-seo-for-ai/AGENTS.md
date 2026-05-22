---
slug: technical-seo-for-ai
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Spec for the technical layer that lets AI crawlers (GPTBot, Claude-Web, PerplexityBot) discover, parse, and trust the site: llms.txt, Article+author schema, clean URLs, heading hierarchy, entity consistency, Core Web Vitals."
content_id: "78c5847137fd8339"
complexity: deep
produces: spec
est_tokens: 2900
tags: [seo, ai-crawlers, schema-markup, core-web-vitals, marketing, geek]
---

# Technical SEO for AI

## Summary

**One-sentence:** Spec for the technical layer that lets AI crawlers (GPTBot, Claude-Web, PerplexityBot) discover, parse, and trust the site: llms.txt, Article+author schema, clean URLs, heading hierarchy, entity consistency, Core Web Vitals.

**One-paragraph:** AI crawlers evaluate factual accuracy and authority, not just keyword density. This methodology specifies the technical layer: `llms.txt` for AI crawler guidance, Article schema with author credentials, clean URL structure, semantic heading hierarchy, entity consistency, Core Web Vitals on field data (LCP <2.5s, CLS <0.1), and explicit author authority signals (sameAs links, credentials). Output is the spec the engineering team implements and the SEO manager audits.

**Ефективно для:** engineering teams shipping content sites; SEO managers auditing technical readiness for AI; agencies validating client implementations.

## Applies If (ALL must hold)

- Setting up a new content site or blog that needs AI crawler visibility from launch
- Auditing an existing site for AI crawlability issues (missing schema, no llms.txt, ambiguous entities)
- Implementing author credential markup to improve E-E-A-T
- Optimising Core Web Vitals on field data for AI crawler accessibility

## Skip If (ANY kills it)

- Paywalled or premium content sites where AI crawling is undesirable — configure llms.txt to block
- Sites with no original content (pure aggregators) — technical layer cannot compensate for lack of authority
- Short-lived campaign landing pages with no long-term SEO value

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Site inventory with URL structure + canonical tags | Crawler export | engineering |
| Schema markup baseline (Article, FAQ, Person) | JSON-LD samples | engineering |
| Core Web Vitals field data (CrUX or PageSpeed Insights) | JSON / report | performance ops |
| Author profile inventory with credentials | YAML / sheet | content ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[google-ai-overviews-optimization]] | content-layer spec that sits on this technical layer |
| `solo/marketing/seo-manager` | operational SEO management context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit_robots_llms_txt` | haiku | Mechanical: file scan |
| `validate_schema_markup` | haiku | Mechanical: schema-validator pass |
| `write_remediation_spec` | sonnet | Bounded synthesis of findings into spec |
| `executive_summary` | opus | Cross-axis narrative for engineering lead |

## Templates

| File | Purpose |
|------|---------|
| `templates/article-schema.json` | Article schema JSON-LD template with author credentials |
| `templates/llms-txt.txt` | llms.txt template with crawler-allow rules |
| `templates/technical-seo-for-ai.md` | Spec skeleton with all six axes |
| `templates/_smoke-test.md` | Minimum-viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-technical-seo-for-ai.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[google-ai-overviews-optimization]]
- [[ai-overview-content-template]]
- [[ai-overview-monitoring]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether technical-seo-for-ai applies: root question — "Is the site public, content-driven, AND in scope for AI crawler visibility?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-llms-txt, r2-article-schema, r3-author-credentials, r4-clean-url-hierarchy, r5-cwv-field-data, r6-entity-consistency.
