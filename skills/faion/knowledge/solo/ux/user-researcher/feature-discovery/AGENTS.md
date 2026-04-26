# Feature Discovery

## Summary

Six-step process for identifying, validating, and prioritizing product features: collect ideas from four source types (customer research, usage analytics, competitive analysis, market trends), categorize with Kano model (Must-have / Performance / Delight / Indifferent), score opportunity via Outcome Driven Innovation (Importance + max(Importance - Satisfaction, 0)), estimate effort (XS–XL), prioritize with RICE, then validate top candidates before building.

## Why

Feature decisions based on gut feeling or the loudest customer request produce features nobody uses and miss features that drive adoption. The six-step process separates discovery from prioritization — a critical distinction because collected feature requests describe symptoms, not jobs. RICE scoring forces explicit effort estimation before commitment; Kano categorization prevents building Delighters before Must-haves are solid.

## When To Use

- Quarterly roadmap planning when the backlog is full but priorities are unclear
- Post-launch: identifying what to build next based on usage data and support tickets
- Competitive gap analysis: discovering features rivals have but your product lacks
- Before running a user survey: generate a candidate feature list to score
- Synthesizing a large feature request log (50+ items) into actionable clusters

## When NOT To Use

- When the core product is not yet working — feature discovery before PMF is premature optimization
- Replacing direct customer conversations: analytics and ticket logs supplement but do not replace qualitative insight
- When only one vocal customer is requesting a feature — frequency matters; one loud voice is not signal
- When the team has already committed to a roadmap for the current quarter — discovery is for next cycle

## Content

| File | What's inside |
|------|---------------|
| `content/01-discovery-process.xml` | Four source types, Kano model, Opportunity Scoring, RICE, validation methods |
| `content/02-examples-and-antipatterns.xml` | SaaS dashboard and mobile app examples, six common mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/discovery-board.md` | Feature discovery board with collection, categorization, scoring, and validation plan |
| `templates/feature-request-log.md` | Per-feature request log with metadata, impact, validation, and decision fields |
| `templates/prompt-extract-features.txt` | LLM prompt to extract feature candidates from support tickets |
| `templates/prompt-opportunity-score.txt` | LLM prompt to compute Opportunity Scores from survey data |
| `templates/rice-scorer.py` | RICE score calculator for a feature candidate list |
