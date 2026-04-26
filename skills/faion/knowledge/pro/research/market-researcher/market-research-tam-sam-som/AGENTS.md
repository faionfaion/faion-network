# Market Research — TAM/SAM/SOM

## Summary

TAM/SAM/SOM sizing quantifies market opportunity through three nested estimates — total addressable market, serviceable available market, and realistically obtainable market — using top-down, bottom-up, and competitor-based methods. The core rule: always triangulate with both top-down and bottom-up; if the two diverge more than 2x, flag it as a research gap rather than averaging the numbers. The market-researcher lens produces three audience-specific cuts from the same canonical base: an investor cut (one slide, three numbers, three sources), a GTM cut (SAM split per acquisition channel), and a pricing cut (TAM/SAM/SOM decomposed per tier).

## Why

Entrepreneurs either overestimate markets (citing billion-dollar TAMs with no grounding) or underestimate them (ignoring the bottom-up path to $1M ARR). Investor partners spot the gap between the slide number and the financial model in 90 seconds. GTM channel budgets that lack per-channel SAM ceilings routinely double-count customers. A rigorous three-cut methodology forces each view to derive from the same canonical base and flags the moment they diverge.

## When To Use

- Seed/Series-A pitch deck market slide needs three numbers, three sources, one chart
- GTM segmentation kickoff: SAM split per channel so the marketer can allocate CAC budget
- Pricing-tier sizing: each tier needs its own ARPU × addressable-count math
- Re-sizing after a pivot, geography expansion, or new pricing page
- Board update comparing SOM-actual vs. SOM-plan for the trailing quarter

## When NOT To Use

- Hobby projects, internal tooling, free OSS — investor audience absent, sizing is theatre
- Two-sided marketplaces pre-launch — supply liquidity dominates raw market size
- Replacement for win/loss interviews — TAM/SAM/SOM does not explain why deals close
- Already-shipping products where bottom-up cohort revenue forecasts are stronger
- Solo freemium-with-no-paid-plan — SAM × ARPU collapses to zero

## Content

| File | What's inside |
|------|---------------|
| `content/01-sizing-methods.xml` | TAM/SAM/SOM definitions, three calculation methods (top-down, bottom-up, competitor-based), and validation checks |
| `content/02-three-cuts.xml` | Investor cut, GTM cut, and pricing-tier cut conventions; how each derives from the canonical base; hygiene rules |
| `content/03-antipatterns.xml` | Common mistakes and AI-agent gotchas (TAM anchoring, tier-mix bias, currency soup, slide-text bloat) |

## Templates

| File | Purpose |
|------|---------|
| `templates/market-sizing-report.md` | Full market sizing report with TAM/SAM/SOM calculations, bottom-up funnel, and validation table |
| `templates/quick-market-check.md` | 15-minute rough market check for early-stage screening |
| `templates/tier-som.sh` | Bash script that decomposes SAM/SOM per pricing tier with LTV/CAC sanity check from a CSV of tier data |
