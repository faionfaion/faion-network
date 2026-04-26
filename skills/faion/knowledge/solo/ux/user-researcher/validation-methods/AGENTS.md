# Validation Methods

## Summary

A reference combining three validation lenses: Problem Validation (evidence hierarchy + 5-step process + PROCEED/PIVOT/KILL decision), Pain Point Mining (tiered source strategy + Pain Intensity Matrix scoring), and Niche Viability Scoring (5-criteria weighted model: market size 25%, competition 20%, barriers 20%, profitability 20%, your fit 15%). All three are pre-build tools; none apply after product-market fit.

## Why

Early-stage discovery requires multiple simultaneous lenses: a problem may be real (validation) and painful (pain mining) but in a market too small or crowded to sustain a business (niche viability). Running only one lens produces an incomplete picture. The 5-criteria niche model adds a dimension not present in the other methodologies: the researcher's own fit, which affects execution risk independently of market attractiveness.

## When To Use

- Early discovery phase: before any code or design work begins
- Deciding whether to pivot a product idea or kill it
- Evaluating a new niche against a portfolio of opportunities
- After user complaints surface — checking if a recurring pain is widespread
- Pre-sprint: confirming a feature addresses a real problem before scoping

## When NOT To Use

- When you already have paying customers validating with their wallets — move to retention analysis
- When iterating on an existing shipped feature — switch to analytics and usage data
- When the hypothesis is too vague to score against the 5-criteria model
- For internal tooling with a captive user base who must use the product

## Content

| File | What's inside |
|------|---------------|
| `content/01-problem-validation.xml` | Evidence types by strength, 5-step validation process, scoring criteria |
| `content/02-pain-mining-and-niche.xml` | Pain mining source strategy and search patterns, niche viability 5-criteria model and thresholds |

## Templates

| File | Purpose |
|------|---------|
| `templates/validation-report.md` | Problem Validation Report with evidence table and decision |
| `templates/niche-scorecard.md` | 5-criteria weighted niche viability scorecard |
| `templates/prompt-validate.txt` | LLM prompt to score evidence and output a filled report |
| `templates/prompt-niche-score.txt` | LLM prompt to return raw niche scores as JSON |
| `templates/pain-miner.py` | PRAW-based Reddit pain aggregator by keyword theme |
