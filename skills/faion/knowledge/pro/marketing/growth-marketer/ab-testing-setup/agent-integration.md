# Agent Integration — A/B Testing Setup

## When to use
- Pre-launch sample-size and duration calculation, so you don't run underpowered tests.
- Configuring traffic split, randomization, and SRM monitoring in a feature-flag/experiment platform.
- Generating test-plan and test-result templates that an analyst agent fills in deterministically.
- Auditing a draft test against a checklist (hypothesis, primary metric, MDE, guardrails, end date) before traffic flows.

## When NOT to use
- Network-effect surfaces (chat, marketplace, multiplayer) — independent randomization breaks; need cluster or switchback designs.
- Heavy personalization where every user already sees a unique variant; plain A/B math doesn't apply.
- Single-shot critical decisions (pricing model, brand) — too few decisions, blast radius too large.
- Pre-instrumentation: if your primary metric isn't tracked end-to-end yet, don't compute sample size; instrument first.
- Continuous-metric heavy-tailed outcomes (revenue) without log-transform/bootstrap — proportion math is misleading.

## Where it fails / limitations
- Simplified `n ≈ 16 × p × (1-p) / MDE²` formula assumes 95% sig + 80% power + 50/50 split + two-sided test; deviations break it.
- MDE relative vs absolute confusion is the single biggest sample-size error agents make.
- Daily-traffic estimates don't account for weekend dips; agent-predicted durations can be 30-50% too short.
- "Required sample" is per-variant — agents drop the doubling and report half the real total.
- Sequential / always-valid designs require entirely different math; using fixed-horizon n with sequential analysis inflates false positives.
- Variance reduction (CUPED, stratification) reduces required n by 30-50%; agent should suggest if pre-experiment data exists.

## Agentic workflow
An `opus` design agent runs the pre-launch checklist (hypothesis, primary, secondaries, guardrails, MDE) and computes sample size + duration with explicit alpha/power/split. A `sonnet` config agent translates the plan into the experiment platform's API call (Statsig/GrowthBook/LaunchDarkly). A `haiku` monitor watches SRM and traffic-allocation health daily. The same `opus` agent reads results at the pre-committed end date and writes the learning into the experiment log.

### Recommended subagents
- `faion-growth-agent` (opus) — design review + power analysis.
- Stats/sonnet subagent — sample size, CI, SRM, post-test analysis.
- Platform/sonnet subagent — Statsig/GrowthBook/LaunchDarkly REST calls.
- Logger/haiku subagent — append to `experiments.md` log.

### Prompt pattern
```
Compute sample size: baseline=8.2%, MDE_relative=10%, alpha=0.05, power=0.80,
split=50/50, two-sided. Daily traffic on test surface = 12,400. Output:
n_per_variant, total_n, days, and a sanity-check note if days > 28 or
< 7. Convert MDE to absolute explicitly.
```

```
Audit this test plan against pre-launch checklist: {plan_json}.
Return pass/fail per item and refuse to launch if any of [hypothesis,
primary, MDE, sample, end_date, guardrails] is missing.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `statsmodels.stats.power.NormalIndPower` | Accurate power analysis (handles split, one/two-sided) | `pip install statsmodels` |
| `scipy.stats` | Tests + chi-square SRM | `pip install scipy` |
| Evan Miller calculator | UI cross-check on agent math | https://www.evanmiller.org/ab-testing/sample-size.html |
| `statsig` Python SDK | Programmatic experiment creation | `pip install statsig` |
| `growthbook` Python SDK | Same, OSS | `pip install growthbook` |
| `launchdarkly-server-sdk` | Feature flags + experiments | `pip install launchdarkly-server-sdk` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Statsig | SaaS | Yes (REST + SDK) | Sequential testing, CUPED, full API |
| GrowthBook | OSS | Yes (REST + self-host) | Best fit for warehouse-native, agent-driven setup |
| Eppo | SaaS | Yes (REST) | Warehouse-native (BQ/Snowflake/Redshift) |
| LaunchDarkly | SaaS | Yes (REST) | Strong flag platform, experiments add-on |
| Split.io | SaaS | Yes (REST) | Mature for engineering teams |
| Optimizely Full Stack | SaaS | Partial | Console-heavy |
| VWO | SaaS | Partial | Bayesian engine + REST |
| PostHog Experiments | OSS | Yes (REST) | Bundled with product analytics |

## Templates & scripts
See `templates.md` for the full plan and result blocks. Inline accurate sample-size helper:

```python
# sample_size.py — agent uses statsmodels for honest math
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
import math

def n_per_variant(baseline: float, mde_rel: float,
                  alpha: float = 0.05, power: float = 0.80,
                  ratio: float = 1.0, alternative: str = "two-sided") -> int:
    p2 = baseline * (1 + mde_rel)
    effect = proportion_effectsize(p2, baseline)
    n = NormalIndPower().solve_power(
        effect_size=abs(effect), alpha=alpha, power=power,
        ratio=ratio, alternative=alternative)
    return math.ceil(n)

def duration_days(n_per_variant: int, daily_users: int,
                  variants: int = 2) -> int:
    return math.ceil((n_per_variant * variants) / max(daily_users, 1))

# Example: baseline=0.10, mde=10% → ~16k/variant
```

## Best practices
- Always use `statsmodels` (or Evan Miller) for the real number — the simplified formula is a teaching aid, not a planning tool.
- Pre-commit to the end date in writing; never let "we'll see how it looks" change the stop condition.
- Configure SRM check (chi-square on observed split vs expected) on day 1 and alert on p < 0.001.
- Test the randomization itself before launch: A/A test for 1-2 days and confirm no false positive on primary.
- Reserve one bucket (e.g. 5% holdout) outside any experiments for clean baseline measurement.
- Use feature flags with deterministic-hash bucketing (user_id + experiment_id) so users stay in the same arm across sessions.
- For platforms with sequential testing engines (Statsig, Optimizely), opt in — peeking becomes safe.

## AI-agent gotchas
- Agent reports "duration: 7 days" without checking whether traffic includes a weekend; weekend traffic dips by 30-50%.
- The simplified formula uses two-sided alpha=0.05 implicitly; agents on one-sided tests under-size by ~25%.
- Asymmetric splits (90/10 to limit blast radius) blow up the sample requirement on the small arm; agent must apply the ratio correctly.
- SRM check is often skipped in templates — wire it into the pre-launch checklist explicitly.
- Sample-size answers in "users" can confuse a per-session metric — agent should declare the unit of randomization.
- Experiment-platform API agents that auto-create experiments without the analytical-plan attachment break audit trails.
- Prompt agents to refuse the test if MDE is missing rather than picking a default; a "default 10%" silently misleads.

## References
- Ron Kohavi, Diane Tang, Ya Xu, *Trustworthy Online Controlled Experiments*
- Statsmodels power docs — https://www.statsmodels.org/stable/stats.html
- Statsig sequential-testing primer — https://statsig.com/blog/sequential-testing
- Microsoft ExP papers — https://www.exp-platform.com/Pages/papers.aspx
- Georgi Georgiev, *Statistical Methods in Online A/B Testing*
- Evan Miller, "Sample Size Calculator" — https://www.evanmiller.org/ab-testing/sample-size.html
