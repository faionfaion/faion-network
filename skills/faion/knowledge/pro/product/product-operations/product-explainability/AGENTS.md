# Product Explainability

## Summary

Product explainability is how clearly a product communicates its purpose, value, behavior, and
limits to both humans and AI systems. As search, recommendations, and buying guidance become
AI-mediated, products need structured representation (llms.txt, schema.org JSON-LD, capability
KB) that AI crawlers can retrieve accurately. The canonical artifact is `product-kb.json` —
a structured source of truth for purpose, capabilities, limits, use cases, and audience — from
which all public surfaces are generated.

## Why

In 2026, AI answers mediate product discovery. ChatGPT, Claude, Perplexity, and Gemini surface
products from their training and retrieval corpora. A product without explicit capability and
limit documentation will be hallucinated or miscategorized. Keeping the KB aligned with the
actual product is now a product-quality requirement, not a marketing nicety. Limits are
first-class: a KB with no limits is a KB nobody trusts, and AI over-promises from it.

## When To Use

- Pre-launch: producing or auditing the product KB that will represent the product to AI systems
- Migrating from human-only marketing copy to AI-mediated discovery
- After a major model update or SEO/AEO shift when AI traffic displaces classical organic search
- When customers report wrong AI answers ("ChatGPT said your tool can do X but it can't")
- Integrating product into agent toolchains (MCP servers, OpenAI custom GPT actions, Claude skills)
- Compliance contexts (EU AI Act Art. 13, FTC AI guidance) where documented scope is required

## When NOT To Use

- Pre-PMF products with <100 users — fix the product, not its representation
- Internal-only tools that no AI will ever index or recommend
- One-page landing pages with a single CTA — standard Open Graph is sufficient
- Products whose purpose changes monthly — KB will be stale faster than it ships
- Hyper-niche enterprise sales reached only through human channels (RFP, channel partner)

## Content

| File | What's inside |
|------|---------------|
| `content/01-kb-structure.xml` | Explainability components, KB fields, four-stage pipeline, drift risks |
| `content/02-agent-usage.xml` | Extractor/generator/probe/drift agent workflow, prompt patterns, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/product-kb-validate.sh` | Validates product-kb.json against JSON Schema; wire into pre-commit |
