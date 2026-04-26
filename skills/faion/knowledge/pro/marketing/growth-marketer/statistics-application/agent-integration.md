# Agent Integration — Statistical Significance: Application

## When to use
- You're analyzing a finished A/B test and need a defensible significance + confidence-interval verdict.
- You're sizing an experiment up-front (power analysis) so you don't waste traffic.
- You suspect an "underpowered" win and need an agent to compute actual achieved power.
- You want to standardize stat reporting across many small tests so results are comparable over time.

## When NOT to use
- Causal inference from observational data (no random assignment) — significance tests over-claim here; use diff-in-diff or matching instead.
- Multi-armed / sequential / bandit experiments — z-tests inflate false positives; use SPRT, group sequential, or Bayesian.
- Tiny samples (<30 per variant) — switch to Fisher's exact, not z-test.
- Highly skewed continuous metrics (revenue per user, session length) — proportions math doesn't apply; bootstrap or t-test on log-transformed data.

## Where it fails / limitations
- Two-proportion z-test assumes independence; clustered users (multiple sessions) violate this and inflate significance.
- Peeking + early stopping silently breaks p-values; agents must refuse to compute on incomplete tests unless explicitly told it's a sequential design.
- Multiple comparisons (10 metrics, 5 segments) need Bonferroni or FDR; default `scipy.stats.proportions_ztest` doesn't correct.
- Frequentist p-values get mistaken for "probability B is better"; agents should report Bayesian posterior or CI alongside.
- MDE is relative-vs-absolute confusion is the #1 source of wrong sample sizes.

## Agentic workflow
A `sonnet` analyst agent ingests raw counts (n1, x1, n2, x2), runs the test, and emits a structured verdict (p, CI, power, decision). For sizing, it accepts (baseline, MDE, alpha, power) and returns sample-per-variant + duration estimate. An `opus` reviewer agent sanity-checks the test design before launch (correct primary metric, no peeking plan, no proxy metric). A `haiku` agent can pull counts daily for monitoring but must NOT report significance until pre-registered sample size is hit.

### Recommended subagents
- `faion-growth-agent` (sonnet for analysis, opus for design review).
- Generic stats subagent with scipy / statsmodels access.
- Review subagent (opus) for pre-launch hypothesis + metric audit.

### Prompt pattern
```
Run two-proportion z-test on:
A: n1=15000, x1=450
B: n2=15000, x2=525
Return JSON: {p_value, z, ci_lower, ci_upper, lift_abs, lift_rel,
significant_at_0.05, recommendation}. Two-tailed.
```

```
Power analysis: baseline=0.10, MDE_relative=0.05, alpha=0.05, power=0.80.
Return n_per_variant and explain MDE conversion to absolute.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Python `scipy.stats` | `proportions_ztest`, `chi2_contingency`, `fisher_exact` | `pip install scipy statsmodels` |
| `statsmodels` | Power analysis: `NormalIndPower().solve_power()` | `pip install statsmodels` |
| `R` `pwr` package | Reference power calcs | `install.packages("pwr")` |
| Evan Miller calculators | Web UI sanity-check | https://www.evanmiller.org/ab-testing/ |
| `abracadabra` (Square OSS) | Bayesian + frequentist A/B in Python | `pip install abracadabra` |
| `expan` (Zalando OSS) | Experimentation analysis | `pip install expan` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Statsig | SaaS | Yes (REST + SDK) | Sequential testing, CUPED variance reduction |
| Eppo | SaaS | Yes (REST) | Warehouse-native, strong stats engine |
| GrowthBook | OSS | Yes (REST + self-host) | Bayesian by default |
| Optimizely Stats Engine | SaaS | Partial | Sequential testing built-in |
| VWO SmartStats | SaaS | Partial | Bayesian, agent reads results via API |

## Templates & scripts
See `templates.md` for raw-data and power-analysis blocks. Inline calculator:

```python
# stat_check.py — agent's significance helper
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
from statsmodels.stats.power import NormalIndPower
import math

def check(n1, x1, n2, x2, alpha=0.05):
    z, p = proportions_ztest([x1, x2], [n1, n2])
    p1, p2 = x1/n1, x2/n2
    se = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    diff = p2 - p1
    ci = (diff - 1.96*se, diff + 1.96*se)
    return {
        "p_value": round(p, 4), "z": round(z, 3),
        "lift_abs": round(diff, 4), "lift_rel": round(diff/p1, 4),
        "ci_95": [round(ci[0], 4), round(ci[1], 4)],
        "significant": p < alpha,
    }

def sample_size(baseline, mde_rel, alpha=0.05, power=0.8):
    mde_abs = baseline * mde_rel
    effect = mde_abs / math.sqrt(baseline*(1-baseline))
    return math.ceil(NormalIndPower().solve_power(
        effect_size=effect, alpha=alpha, power=power, alternative="two-sided"))
```

## Best practices
- Pre-register the primary metric, sample size, and end date BEFORE launch; agents should refuse to analyze tests where these weren't fixed.
- Always report CI alongside p-value; "significant" with CI [0.01%, 4%] is barely actionable.
- Convert MDE to absolute terms in the prompt explicitly to dodge the relative/absolute trap.
- Use one-sided tests only when a regression would never be shipped — otherwise default to two-sided.
- For revenue/AOV use bootstrapping (10k resamples) — proportions math is wrong.
- Apply Bonferroni when checking >3 metrics; better, pick one primary and treat the rest as guardrails.

## AI-agent gotchas
- LLMs confidently compute p-values from headline percentages without raw counts; always force `n1, x1, n2, x2`.
- Agents will report "p=0.06, almost significant" — no, it isn't. Force a binary `significant_at_alpha` field.
- "95% CI doesn't cross 0" is the right plain-English summary, not "95% chance B is better" (that's Bayesian).
- For sample-size prompts, agents drop the alpha/power assumptions silently — require them in output.
- Asymmetric traffic split (90/10) breaks the simplified `16 × p(1-p)/MDE²` formula; use `statsmodels` or `evan-miller` calculator instead.
- When test has 0 conversions in one variant, z-test breaks; fall back to Fisher's exact and tell the agent to detect this case.

## References
- Ron Kohavi, Diane Tang, Ya Xu, *Trustworthy Online Controlled Experiments* (the canonical reference)
- Georgi Georgiev, *Statistical Methods in Online A/B Testing*
- Evan Miller's blog — https://www.evanmiller.org/
- Microsoft ExP team papers — https://www.exp-platform.com/
- Statsig docs on sequential testing — https://docs.statsig.com/
