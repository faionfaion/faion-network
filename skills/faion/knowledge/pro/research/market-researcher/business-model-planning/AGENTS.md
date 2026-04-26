# Business Model Planning

## Summary

Business model planning covers four linked frameworks for evaluating whether a niche is worth pursuing and how to monetize it: niche-viability scoring (5-criteria weighted), Blue Ocean / Four Actions (market space creation), Value Proposition Canvas (pain-gain fit), and pricing-model selection. The core rule: score 3-5 niches in parallel — the framework's value is comparative ranking across niches, not an absolute go/no-go on a single one.

## Why

Entrepreneurs enter crowded niches based on gut feel or build products without a viable revenue model. Subjective niche scores feel imprecise without a structured rubric. Blue Ocean analysis on a single case suffers from survivorship bias. LLMs default to "tiered subscription" pricing regardless of the product economics. Parallel scoring with citation-required inputs and explicit model rejection reasons disciplines these failure modes.

## When To Use

- Pre-spec phase of a new product where TAM/SAM/SOM exists but no model decision yet
- Niche short-list that needs ranking before writing a spec.md
- Re-pricing an existing SaaS after churn spikes or competitor shift
- Pivoting into an adjacency — must justify which factors to eliminate or raise
- Founder needs a number ("is this niche worth pursuing?"), not an opinion

## When NOT To Use

- Pure market sizing — use `market-research-tam-sam-som` first; pipe its output here
- Competitor feature/pricing scrape — use `competitor-analysis` first
- Already-priced product with PMF — use `conversion-optimizer`, not a canvas
- B2C consumer apps with ad-only revenue — pricing-research framework assumes paid value capture
- Internal tools, hobby projects, or commissioned client work with fixed scope/budget

## Content

| File | What's inside |
|------|---------------|
| `content/01-niche-viability.xml` | 5-criteria scoring model (market size, competition, barriers, profitability, fit) with decision thresholds |
| `content/02-blue-ocean.xml` | Four Actions framework (eliminate/reduce/raise/create), Strategy Canvas, and when NOT to use Cirque-du-Soleil examples |
| `content/03-value-proposition.xml` | Customer Profile (jobs/pains/gains) and Value Map (pain relievers/gain creators), FIT scoring, decay warning |
| `content/04-pricing-models.xml` | Six pricing models with selection criteria, Van Westendorp rules, and LLM bias mitigations |

## Templates

| File | Purpose |
|------|---------|
| `templates/niche-scorecard.md` | Weighted niche viability scorecard with justification and decision columns |
| `templates/blue-ocean-canvas.md` | Blue Ocean Four Actions canvas template |
| `templates/value-proposition-canvas.md` | VPC template with customer profile and value map sections |
| `templates/pricing-strategy.md` | Pricing strategy document with competitor table and tier definitions |
| `templates/score-niche.sh` | Bash/jq script that validates weights sum to 1.0 and recomputes weighted total from a JSON sidecar |
