# Cost Estimation

## Summary

A bottom-up cost estimation process: decompose the WBS into work packages, apply three-point PERT estimation per package, load labor with a fully-loaded multiplier (1.3-2.0x depending on region and benefits), add tools and infrastructure costs, calculate risk-driven contingency (sum of probability x cost-exposure per open risk), separate contingency reserve from management reserve, and produce a cost baseline (BAC = Cost Baseline + Management Reserve). The agent is a calculator and auditor, not a decision-maker; humans approve all numbers before they enter the budget.

## Why

Projects fail financially because they underestimate true costs, forget indirect costs, use flat-percentage contingencies that ignore actual risk exposure, and do not update the baseline when scope changes. Risk-driven contingency calibrates to actual exposure. Tracking P80 rather than P50 means the budget is breached only 20% of the time rather than 50%. Citing sources on every rate prevents hallucinated benchmarks from corrupting the baseline.

## When To Use

- Producing the initial budget from an approved WBS before kickoff
- Bottom-up cost roll-up for an RFP response requiring a defensible cost baseline
- Build-vs-buy / build-vs-SaaS decisions where opportunity cost matters
- Updating the cost baseline after an approved change-control event
- Solopreneur "true cost" analysis pricing own time at market rate

## When NOT To Use

- Agile teams that fund team capacity by time-box, not by feature — use team-month run-rate, not bottom-up sum
- Pre-discovery with requirements &lt;30% defined — output will have false precision; use ROM (±50%) instead
- Already-negotiated fixed-fee contracts — re-estimating internally has no contractual force
- Tasks under 1 week where estimate cost exceeds work cost

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Five-step cost estimation process: categories, bottom-up, three-point PERT, contingency, cost baseline |
| `content/02-rules.xml` | Rules for rate citation, burden multiplier, risk-driven vs flat contingency, P80 tracking; antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-worksheet.md` | Full cost estimation table: direct / indirect / reserves / total budget |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/risk-contingency.py` | Risk-driven contingency via Monte Carlo over Bernoulli risk events; outputs expected, P50, P80, P95 |
