# Business Model Research (Market-Researcher Lens)

## Summary

Business model research at the market-researcher level produces a peer-benchmark table — not a single canvas. The methodology classifies 8-15 comparables (including failed and acquihired peers) into five revenue archetypes (subscription, one-time, transaction, advertising, marketplace), extracts P25/P50/P75 distributions for ARPU, gross margin, gross logo retention, NDR, and CAC payback, then overlays the founder's plan against the distribution. The core rule: always include at least 2 dead or acquihired comparables — without them, medians overstate viability by 20-40%.

## Why

Survivorship bias in comp sets is the primary failure mode: public-listed comps run higher gross margin (78-82%) than venture-stage privates (60-70%) because of scale. "Tiered subscription" is the default LLM answer for any SaaS, regardless of economics. NDR greater than 110% can hide gross logo churn greater than 25%. A distribution-first approach (P25/P50/P75 per archetype) prevents single-comp dominance and false precision, and explicitly separates the market-researcher deliverable (distributions) from the researcher sibling deliverable (a single canvas).

## When To Use

- Pre-spec market-side answer to "what model do peers in this category actually use?"
- Investor or board memo: produce an industry revenue-model distribution by archetype
- Pricing committee input: pull ARPU, gross margin, NDR, and rule-of-40 from a public-comp set
- Category entry decision: rank 5-15 candidate categories by median LTV:CAC and CAC payback
- M&A scoping: build a comps table mapping the target's model to nearest public proxy
- Cross-checking a researcher-mode canvas — verify the founder's chosen archetype against industry base rates

## When NOT To Use

- Single-product canvas and unit-economics design — that is the `researcher/business-model-research` sibling's scope
- Markets with fewer than 3 public or well-documented private comparables — table is statistically meaningless
- Hyper-local services where public comps do not transfer — use local-market survey instead
- Pre-revenue categories with no precedent — peer benchmarking is misleading; use analogous-markets or first-principles-pricing
- Regulated verticals where revenue model is dictated by law — research the regulation, not the comps

## Content

| File | What's inside |
|------|---------------|
| `content/01-comp-universe.xml` | Comp-universe construction rules: 8-15 comparables, archetype classification, survivorship-bias mitigation |
| `content/02-metric-harvest.xml` | Metric extraction from S-1/10-K/pricing pages, normalization rules (currency, period, line-item definitions) |
| `content/03-distribution-and-overlay.xml` | P25/P50/P75 distribution build, founder-plan overlay (green/yellow/red), trend annotation over quarters |
| `content/04-antipatterns.xml` | AI-agent gotchas: ARR/ARPU/ACV mix-up, hybrid model squashing, take-rate misread, NDR cherry-pick |

## Templates

| File | Purpose |
|------|---------|
| `templates/business-model-canvas.md` | Business Model Canvas template with nine building blocks and revenue stream table |
| `templates/unit-economics.md` | Unit economics calculator with LTV, CAC, payback, and break-even sections |
| `templates/bm-distribution.sh` | Bash script emitting P25/P50/P75 per archetype from a comps.csv with a missing-N warning |
