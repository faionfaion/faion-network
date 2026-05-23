<!-- purpose: legacy template for ads-ab-testing-ads — test-results -->
<!-- consumes: per AGENTS.md Prerequisites -->
<!-- produces: artefact per content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml, content/06-decision-tree.xml -->
<!-- token-budget-impact: ~400-1200 tokens when loaded as context -->

# Test Results: [Test Name]

## Summary

- **Winner:** Control / Variant / Inconclusive
- **Confidence:** [X%]
- **Lift on primary metric:** [+/- X%]
- **Decision:** Implement winner / Extend test / Abandon and test next hypothesis

## Data

| Metric | Control | Variant | Difference |
|--------|---------|---------|------------|
| Impressions | X | X | — |
| Clicks | X | X | +X% |
| CTR | X% | X% | +X% |
| Conversions | X | X | +X% |
| CPA | $X | $X | -X% |

## Statistical Validity

- Confidence level: [X%]
- Method: [Bayesian / Frequentist]
- [Significant / Not significant / Test extended to reach significance]
- Sample size met: [Yes / No — state actual vs. required]

## Learnings

- What happened: [Factual description of outcome]
- Why we think this: [Hypothesis about mechanism]

## Next Steps

- [ ] Implement winner at scale (or note: inconclusive, test next hypothesis)
- [ ] Add to learning library: [One-sentence learning to carry forward]
- [ ] Next test hypothesis: [What to test next based on this result]
