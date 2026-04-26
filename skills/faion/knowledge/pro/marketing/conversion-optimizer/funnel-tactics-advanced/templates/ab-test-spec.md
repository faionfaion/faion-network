# A/B Test Spec: [Hypothesis Name]

## Hypothesis
If we [change what], then [expected outcome] because [diagnosis-based reason].

## Control vs. Variant
- **Control:** [Current version description]
- **Variant:** [New version description]
- **Only change:** [Single variable — enforce this strictly]

## Success Metrics
- **Primary:** [Main KPI]
- **Secondary:** [Supporting metrics]
- **Target lift:** [Expected improvement %]

## Sample Size and Duration
- **Min sample per variant:** [Calculate with power calculator at 80% power, p=0.05]
- **Minimum duration:** [Days — run at least 7 days for weekly patterns]
- **Statistical significance threshold:** p &lt; 0.05

## Decision Criteria
- **Win if:** variant outperforms control by [X%] with p &lt; 0.05
- **Loss if:** control outperforms variant by [X%]
- **Inconclusive:** run additional 7 days, then call it

## Post-Test
- [ ] Document result and statistical confidence
- [ ] Implement winner if criteria met
- [ ] Archive learnings in team wiki
- [ ] Define next hypothesis based on findings
