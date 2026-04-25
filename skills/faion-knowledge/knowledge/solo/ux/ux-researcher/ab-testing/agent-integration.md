# Agent Integration — A/B Testing

## When to use
- When you have a specific conversion metric (sign-ups, click-through, checkout completion) and enough traffic to reach statistical significance within a reasonable run time
- When a design debate cannot be resolved by expert judgment and a quantitative answer is needed
- When iterating on a proven flow to optimize incrementally — not when redesigning from scratch
- When validating that a design change does not harm secondary or guardrail metrics even if it helps the primary metric

## When NOT to use
- On low-traffic pages where reaching statistical significance would take months
- During major product redesigns — test users' understanding and mental models first with qualitative research
- When you need to understand why users behave differently, not just whether they do — use session recordings and interviews
- For complex multi-step flows where the winning variant on step 1 may harm completion on step 5 — funnel analysis with holdout groups is needed instead
- On pages with high seasonal variance (e.g., holiday e-commerce) without adjusting for the cycle

## Where it fails / limitations
- Novelty effect: new UI elements get clicks simply because they are new; watch for lift that decays after week 1
- Simpson's paradox: aggregate results can hide segment reversals (mobile users prefer A while desktop users prefer B)
- Interaction effects: running two simultaneous tests on overlapping user populations creates confounding
- Statistical significance is not the same as practical significance; a 0.1% lift at 99% confidence may not be worth implementing
- Tests run too short surface false positives; stopping at "significance" without reaching the pre-calculated sample size is p-hacking

## Agentic workflow
An agent handles the mechanical phases: sample size calculation given baseline conversion, MDE, and power; generating test configuration parameters; monitoring a running test for early stopping conditions; and producing a results summary with statistical details. A human approves the hypothesis, validates the variant design, and makes the ship/no-ship decision from the results.

Do not let an agent make the ship decision — the combination of statistical output, business context, and segment analysis requires human judgment.

### Recommended subagents
- `faion-sdd-executor-agent` — create A/B test plan document from a hypothesis, set up tracking spec, generate results report from raw metrics
- General Claude subagent — calculate required sample size, interpret p-values and confidence intervals, flag early stopping risks

### Prompt pattern
```
Calculate the required sample size for this A/B test:
- Baseline conversion rate: [X]%
- Minimum detectable effect: [Y]%
- Statistical power: 80%
- Significance level: 95% (two-tailed)

Also calculate expected run time given [N] daily visitors split 50/50.
```

```
Here are the results of an A/B test:
Control: [N] users, [X] conversions ([rate]%)
Variant: [N] users, [X] conversions ([rate]%)
Run duration: [X] days

Calculate: p-value, confidence interval for the difference, and state whether the result is statistically significant at 95%.
Flag any concerns about the test validity (too short, sample ratio mismatch, etc.).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `scipy` (Python) | Statistical significance calculations (t-test, chi-square, z-test) | `pip install scipy` / scipy.org |
| `statsmodels` (Python) | Power analysis, sample size calculation, proportion tests | `pip install statsmodels` / statsmodels.org |
| `evan-miller/abba` | JavaScript A/B test stats library | `npm i abba` / github.com/evan-miller/abba |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimizely | SaaS | Yes (REST API) | Full-featured A/B platform; results and experiment config via API |
| VWO | SaaS | Yes (REST API) | A/B, MVT, heatmaps; results export via API |
| GrowthBook | OSS | Yes (REST API + SDK) | Open-source experimentation platform; self-hostable; agent-friendly |
| PostHog | OSS/SaaS | Yes (REST API) | Feature flags + A/B testing; strong API for agent integration |
| Google Analytics 4 | SaaS | Yes (Data API) | Segment analysis for running tests; no built-in test management |
| LaunchDarkly | SaaS | Yes (REST API) | Feature flag platform with experimentation layer |

## Templates & scripts
See `templates.md` for A/B test plan template and A/B test results template.

Inline: sample size and run-time calculator:
```python
from math import ceil
from scipy.stats import norm

def ab_sample_size(
    baseline_rate: float,
    mde: float,
    power: float = 0.80,
    alpha: float = 0.05,
) -> dict:
    """
    baseline_rate: current conversion rate (0.0 - 1.0)
    mde: minimum detectable effect as relative lift (e.g., 0.10 for +10%)
    Returns required sample size per variant.
    """
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)
    p_bar = (p1 + p2) / 2
    n = ceil(
        (z_alpha * (2 * p_bar * (1 - p_bar)) ** 0.5
         + z_beta * (p1 * (1 - p1) + p2 * (1 - p2)) ** 0.5) ** 2
        / (p2 - p1) ** 2
    )
    return {"n_per_variant": n, "total_n": n * 2}
```

## Best practices
- Write the hypothesis and success criteria before implementation — post-hoc rationalization of results is widespread and produces bad decisions
- Pre-register the primary metric; adding metrics after seeing results inflates false positive rate
- Run for at least one full business cycle (typically 7-14 days) regardless of when significance is reached — day-of-week effects are real
- Always check for sample ratio mismatch (SRM) first: if control and variant have significantly different sample sizes despite 50/50 split, the randomization is broken
- Analyze key segments (new vs. returning, mobile vs. desktop, geographic) before concluding; aggregate results hide important reversals
- Document and share learnings from losing tests — null results and negative results are valuable; they prevent future teams from retesting the same ideas

## AI-agent gotchas
- Agents can compute p-values correctly but cannot detect test integrity issues (cookie leakage, bot traffic, SRM) without access to raw assignment logs — always check SRM before interpreting results
- "Statistically significant" answers from an agent should always include the confidence interval, not just a yes/no — small effects at large sample sizes are statistically significant but practically meaningless
- Agents will not flag seasonal confounding or competitor-driven traffic spikes unless you include date and traffic context in the prompt
- Do not ask an agent to recommend ship/no-ship based on numbers alone; it will answer based on the numbers, ignoring business context (cost of implementation, engineering debt, support load)
- For multivariate tests (2+ changes), agents must account for multiple comparison correction (Bonferroni or FDR) — prompt explicitly for this

## References
- Kohavi, R., Tang, D., Xu, Y. "Trustworthy Online Controlled Experiments." Cambridge University Press, 2020. https://experimentguide.com/
- NNg A/B testing perspective: https://www.nngroup.com/articles/ab-testing-usability-engineering/
- Optimizely stats engine: https://www.optimizely.com/optimization-glossary/statistical-significance/
- GrowthBook docs: https://docs.growthbook.io/
- VWO A/B testing guide: https://vwo.com/ab-testing/
