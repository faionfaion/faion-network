# Product Development Trends 2026

## Summary

A research lens for the 2026 product-development landscape: four primary trends (AI-augmented ideation, continuous customer feedback, rapid pivots, cross-functional teams) with evidence-collection and signal-scoring methodology. Produces a trend brief grounded in URL-cited primary sources with a 90-day recency gate.

## Why

Generic trend lists decay within one quarter and agents hallucinate vendor capabilities from stale training data. This methodology enforces a two-pass pipeline — broad signal collection, then scored triage — and separates process trends (how teams work) from consumer trends (what users want), preventing the conflation that produces unfocused roadmap inputs.

## When To Use

- Quarterly product strategy review needing an external view of where development practice is moving.
- Drafting a product pivot brief requiring a defensible answer to "what is industry-standard in 2026".
- Onboarding a new PM or research lead who must align on the modern Agile + Data-Driven + Cross-Functional model.
- Adding a "trends" section to `.aidocs/product_docs/market-research.md` or `executive-summary.md`.
- Selecting which methodology folders in `pro/research/researcher/` to activate next.

## When NOT To Use

- Pure tactical execution (sprint planning, story splitting) — use `pm-agile` or `sdd-planning`.
- Single-feature validation answerable by one customer interview — use `user-researcher/problem-validation`.
- Pricing tear-down or TAM/SAM/SOM math — use `market-researcher/pricing-research` and `market-researcher/tam-sam-som`.
- Engineering-practice changes (CI, testing) — use `cicd-engineer` and `code-quality` skills.
- Less than 6 weeks since the last trends pass with no triggering event.

## Content

| File | What's inside |
|------|---------------|
| `content/01-trends.xml` | Four 2026 trend axes with impact table and AI-Human ideation flow |
| `content/02-methodology.xml` | Two-pass pipeline: signal collection → scored triage; recency/evidence/applicability scoring rules |
| `content/03-gotchas.xml` | LLM training-cutoff bias, hallucinated cross-functional claims, SEO-ranked search results, human-in-the-loop gates |

## Templates

| File | Purpose |
|------|---------|
| `templates/collect-trends.py` | Exa.ai API collector: fetches 2025+ evidence per trend axis, outputs JSONL |
| `templates/score-signals.py` | Signal scoring pass: recency × evidence × applicability, drops below threshold 5 |
