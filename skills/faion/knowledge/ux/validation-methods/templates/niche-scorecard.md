<!-- purpose: Weighted 5-criteria niche viability score with a GO/caution/pass decision -->
<!-- consumes: opportunity list, market/competition/profitability evidence -->
<!-- produces: filled niche viability scorecard markdown (Niche Viability lens) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~190 tokens filled -->

# Niche Viability Scorecard: <niche_name>

| Criterion | Score | Weight | Weighted | Justification |
|-----------|-------|--------|----------|---------------|
| Market Size | {1-10} | 25% | {score x 0.25} | {evidence} |
| Competition | {1-10} | 20% | {score x 0.20} | {evidence} |
| Barriers | {1-10} | 20% | {score x 0.20} | {evidence} |
| Profitability | {1-10} | 20% | {score x 0.20} | {evidence} |
| Your Fit | {1-10} | 15% | {score x 0.15} | {evidence} |
| **Total** | | | **<sum>** | |

## Decision
- 7.5-10: Strong opportunity
- 5.5-7.4: Proceed with caution
- 3.5-5.4: Significant risks
- &lt;3.5: Pass

**Decision: <threshold_label>** — {one-sentence rationale}

## Risk Mitigation
- <risk_1>: <mitigation>
- <risk_2>: <mitigation>
