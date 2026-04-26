# Risk Assessment (Market-Researcher Lens)

## Summary

Market-risk assessment identifies, scores, and mitigates demand, competition, pricing, trend, and channel risks before committing to a segment or pricing strategy. The core rule: every risk row must cite a paragraph or table from an existing market research file — no row may rely on general knowledge. This ensures the register stays grounded in evidence and can be automatically validated.

## Why

Entrepreneurs either ignore risks until they materialize or paralyze themselves without structure. Standard H/M/L scoring collapses four distinct pricing failure modes into one row and anchors demand risk on TAM rather than the validated wedge. A citation-enforced register surfaces these hidden exposures and connects each High-priority row to a concrete trigger metric already in the company's dashboard.

## When To Use

- Pre-entry go/no-go on a new market segment when TAM/SAM/SOM exists but demand evidence is thin
- Pricing strategy decision: before locking a price point, score demand-elasticity and anchor-competitor risk
- Launch-readiness review for a positioning or category bet
- After a competitor raises a Series B or ships a copycat: re-score competitive-displacement and pricing-pressure rows
- Channel-dependence audit when more than 40% of pipeline comes from one channel
- Pivot evaluation: comparing two segment options requires a structured market-risk delta

## When NOT To Use

- Pure technical, team, financial, or operational risk — use the generic `researcher/risk-assessment` variant or `pro/pm/pm-traditional/risk-management/`
- Idea stage with fewer than 5 problem interviews — demand-risk score is uncalibrated; run continuous discovery first
- B2B deals where risk is per-account, not per-market — use account-level deal-risk frameworks
- Solo side projects under $1k of committed spend — overhead exceeds expected loss

## Content

| File | What's inside |
|------|---------------|
| `content/01-risk-categories.xml` | Five risk categories (demand, competition, pricing, trend, channel) with sub-types and scoring rules |
| `content/02-process-and-antipatterns.xml` | Five-step assessment process, pre-mortem technique, common mistakes, and AI-agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-register.md` | Risk register template with high/medium/low priority tables and contingency plan format |
| `templates/pre-mortem.md` | Pre-mortem facilitation template with failure-mode consolidation and risk conversion table |
| `templates/market-risk-lint.sh` | Bash script that enforces citations from market-research files on every register row |
