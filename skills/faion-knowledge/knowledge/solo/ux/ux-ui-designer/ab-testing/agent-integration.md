# Agent Integration — A/B Testing

## When to use
- Generating a statistically sound test plan from a design change hypothesis
- Calculating required sample size given baseline conversion rate and target MDE (minimum detectable effect)
- Reviewing a completed test's raw results and determining whether to ship, hold, or extend
- Synthesizing segment-level analysis (mobile vs. desktop, new vs. returning users) from result data
- Writing the post-test report for stakeholder communication

## When NOT to use
- Traffic is under ~1,000 conversions/month — insufficient sample size makes results meaningless
- The change is a major redesign (not an isolated variant) — too many confounding variables
- You need to understand *why* users behave differently — A/B testing tells you *what* happened, not why; use user interviews for causation
- Early-stage product where the primary metric itself is unclear
- Regulatory or safety-critical features where split exposure carries risk

## Where it fails / limitations
- Agent cannot run the test — it can only plan, analyze data provided to it, and report
- Sample size calculations are sensitive to baseline conversion rate; agent output is only as accurate as the baseline you provide
- Agent analysis of segment data without statistical significance per segment leads to false conclusions (multiple comparisons problem)
- Novelty effect: agent cannot detect whether an uplift is short-term curiosity or durable improvement — human judgment on test duration is required
- Agent has no access to your testing platform (Optimizely, VWO, GA4 experiments) without manual data export

## Agentic workflow
A Claude subagent takes a design change description, baseline metric, and desired improvement threshold and outputs a complete A/B Test Plan document (hypothesis, metrics, guardrails, sample size, duration estimate, risk flags). After the test runs, a second agent pass receives the results table and returns a structured analysis: statistical significance assessment, segment breakdown, guardrail check, and a clear ship/hold/extend recommendation.

### Recommended subagents
- `faion-sdd-executor-agent` — produce the test plan as a structured SDD artifact
- General Claude subagent with analyst role — analyze results CSV and produce the decision report

### Prompt pattern
```
You are a CRO analyst. Given:
- Change: [describe variant vs. control]
- Primary metric: [metric name, current baseline %]
- Minimum detectable effect: [%]
- Statistical power: 80%, significance level: 95%

Output:
1. Hypothesis statement (If/Then/Because format)
2. Required sample size per variant (show calculation)
3. Estimated test duration at [N] daily visitors
4. Three guardrail metrics to monitor
5. Risks and confounds to watch for
```

```
You are a CRO analyst reviewing A/B test results.
Input: [results table with control/variant metrics, confidence intervals, p-values, segment breakdown]

Output:
1. Was statistical significance reached? (yes/no, confidence level)
2. Practical significance: is the lift meaningful for the business?
3. Segment analysis: does the effect hold across key segments?
4. Guardrail metrics: did any worsen?
5. Recommendation: Ship / Hold / Extend test — with rationale
6. Key learning for future tests
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| scipy (Python) | Statistical significance calculations, t-tests, chi-squared | `pip install scipy` / https://docs.scipy.org/doc/scipy/reference/stats.html |
| statsmodels (Python) | Sample size calculation (`statsmodels.stats.power`) | `pip install statsmodels` / https://www.statsmodels.org |
| R (base stats) | Full frequentist and Bayesian A/B analysis | `R -e "prop.test(c(conv_a, conv_b), c(n_a, n_b))"` |
| abba (Node.js) | CLI A/B test significance calculator | `npm install -g abba` / https://github.com/thumbtack/abba |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimizely | SaaS | Yes (REST API) | Results, experiments, and audiences accessible via REST; agent can pull result data programmatically |
| VWO | SaaS | Yes (REST API) | Similar to Optimizely; report export via API |
| Google Analytics 4 | SaaS | Yes (Data API) | A/B test results via GA4 experiments exported through Data API |
| PostHog | OSS/SaaS | Yes (REST API) | Open-source experimentation with full API access; self-hostable |
| GrowthBook | OSS/SaaS | Yes (REST API) | Open-source A/B testing platform; agent-friendly REST API for feature flags and results |
| Statsig | SaaS | Yes (REST API) | Experimentation platform with Bayesian and frequentist modes; REST API for results |
| Evan Miller's Sample Size Calculator | Web tool | No API | Reference for manual calculations; use scipy/statsmodels for programmatic equivalent |

## Templates & scripts
See `templates.md` for the full A/B Test Plan and Results templates. Below is a Python snippet for sample size and significance:

```python
#!/usr/bin/env python3
"""ab_stats.py — A/B test sample size and significance calculator"""
from scipy import stats
from statsmodels.stats.power import NormalIndPower
import math

def sample_size(baseline_rate, mde, power=0.8, alpha=0.05):
    """Calculate required sample size per variant."""
    effect_size = (mde) / math.sqrt(baseline_rate * (1 - baseline_rate))
    analysis = NormalIndPower()
    n = analysis.solve_power(effect_size=effect_size, power=power, alpha=alpha)
    return math.ceil(n)

def significance(conv_a, n_a, conv_b, n_b):
    """Chi-squared test for two proportions."""
    table = [[conv_a, n_a - conv_a], [conv_b, n_b - conv_b]]
    chi2, p, dof, expected = stats.chi2_contingency(table)
    lift = (conv_b / n_b - conv_a / n_a) / (conv_a / n_a) * 100
    return {"p_value": round(p, 4), "lift_pct": round(lift, 2), "significant": p < 0.05}

if __name__ == "__main__":
    # Example: baseline 5%, detect 1% absolute improvement (MDE=0.01)
    n = sample_size(baseline_rate=0.05, mde=0.01)
    print(f"Required n per variant: {n}")
    result = significance(conv_a=150, n_a=3000, conv_b=180, n_b=3000)
    print(f"Results: {result}")
```

## Best practices
- Always pre-register the hypothesis, primary metric, and minimum sample size before launching — prevents peeking and moving goalposts
- Run tests for full business cycles (minimum 2 weeks) to capture weekday/weekend variation
- Test one thing at a time in the variant; multiple simultaneous changes make attribution impossible
- Compute segment results only for pre-specified segments — post-hoc segment fishing inflates false-positive risk
- When there is no clear winner, default to keeping the control — simpler is better, and a null result is still a valid learning
- Document every test result, including null results, in a shared experiment log — prevents re-running the same tests

## AI-agent gotchas
- Agent cannot detect test contamination (users switching between control and variant devices) in the data — flag this risk in the test plan
- Agent significance analysis using just "p < 0.05" is fragile; require agent to also assess practical significance (effect size in business terms) and confidence intervals
- Human-in-loop checkpoint: "ship" decisions based on agent analysis must be confirmed by a PM or analyst before implementation — agent output is advisory
- Agent may misinterpret segment uplift as a universal win; always check whether the primary metric is significant across the full population, not just one segment
- Sequential testing (peeking) invalidates standard p-values; if results are checked mid-test, agent should note this caveat explicitly

## References
- https://experimentguide.com/ (*Trustworthy Online Controlled Experiments* by Kohavi, Tang & Xu)
- https://www.nngroup.com/articles/ab-testing-usability-engineering/
- https://www.optimizely.com/optimization-glossary/statistical-significance/
- https://vwo.com/ab-testing/
- https://www.statsmodels.org/stable/stats.html
