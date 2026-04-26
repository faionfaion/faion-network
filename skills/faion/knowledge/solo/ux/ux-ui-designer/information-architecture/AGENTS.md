# Information Architecture

## Summary

Organize and label content so users can find what they need. Produces a category
structure (L1/L2 navigation), taxonomy document (content types, tags, naming rules),
and sitemap skeleton. Always validate the proposed IA with card sorting and tree testing
before building — agent-generated IA reflects feature lists, not user mental models.

## Why

Navigation organized around internal product logic or org charts fails users who search
by task or topic. A structured IA process (research → organize → validate) prevents the
most common failure: building navigation that makes sense to the team but not to the
user. 4-7 top-level categories is the validated sweet spot for scannability.

## When To Use

- Generating a sitemap or taxonomy from a product spec, feature list, or content inventory
- Auditing an existing IA against card sort or tree test data to identify mismatches
- Drafting an IA strategy document from user research findings and business requirements
- Proposing navigation label alternatives when current labels test poorly with users

## When NOT To Use

- Validating a proposed IA — agents draft structure but cannot replace card sorting and tree testing with real users
- Real-time search relevance tuning — IA shapes browse; search ranking is a separate discipline
- Micro-level layout decisions — IA governs content organization, not component placement within a page

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Organization schemes, navigation types, labeling rules, scalability principles |
| `content/02-patterns.xml` | IA patterns: mega menu, hub-and-spoke, flat structure; when each applies |
| `content/03-examples.xml` | E-commerce IA (task-based); SaaS IA (user-journey-based); agentic workflow with prompt patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/ia-strategy.md` | Strategy document: research summary, organization approach, navigation design, labeling, search, validation plan |
| `templates/sitemap.md` | Sitemap skeleton with page inventory table |
| `templates/taxonomy.md` | Taxonomy document: content types, categories, tags, naming conventions |
| `templates/sitemap-generator.py` | Python: generate Mermaid diagram from a structured IA definition dict |
| `templates/prompt-ia.txt` | LLM prompt for generating an IA structure from a product spec |
