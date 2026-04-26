# Market Research TAM/SAM/SOM

## Summary

Three nested market size calculations (TAM = total addressable, SAM = serviceable
available, SOM = realistically obtainable) computed via three independent methods
(top-down from reports, bottom-up from customer counts, competitor-based from
revenue proxies) and triangulated. Lock the ICP definition before any number is
fetched. Round aggressively — two significant figures max. Express SOM as a customer
count first, dollars second. Output to .aidocs/product_docs/market-research.md.

## Why

Entrepreneurs either overestimate markets ("It's a billion dollar opportunity!") or
underestimate them because there is no practical method to size markets for solo
products. The root failure is using top-down numbers without grounding: a Statista
headline TAM without a bottom-up customer count is a guess dressed as data. Running
three methods and triangulating forces the agent to reconcile contradictions before
the estimate enters a deliverable.

## When To Use

- Pre-spec phase: sanity check whether a niche clears a revenue floor (e.g. SOM > $1M ARR in 3 years)
- Pitch decks, investor memos, grant applications requiring a numerical market frame
- Pricing or positioning decisions where segment economics matter (SAM × ARPU sets the envelope)
- Comparing two adjacent niches before committing to MVP scope
- Annual roadmap review as market segment shifts (new geography, new tier, post-funding)

## When NOT To Use

- Hobby projects, internal tools, free OSS — sizing adds zero signal
- Replacement for actual customer interviews — TAM/SAM/SOM is not problem validation
- Already-shipping products with real ARR — extrapolate from cohorts, not market reports
- Two-sided marketplaces in pre-launch — supply/demand dynamics dominate raw market size
- Deep-tech with a 10-year horizon — the market category may not exist yet
- Regulated markets pre-license (medical, fintech) — addressable share depends on regulator decisions

## Content

| File | What's inside |
|------|---------------|
| `content/01-definitions.xml` | TAM/SAM/SOM definitions, formulas, calculation methods with examples |
| `content/02-agentic-pipeline.xml` | 7-step agent pipeline, prompt patterns, ICP lock rule, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/market-sizing-report.md` | Full market sizing report structure with all required sections |
| `templates/quick-market-check.md` | 15-minute rough market check template |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/tam-triangulate.sh` | Flags divergence across three sizing methods; exits 1 if spread > 2x |
