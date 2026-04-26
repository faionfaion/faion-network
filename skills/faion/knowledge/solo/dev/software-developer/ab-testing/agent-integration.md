# Agent Integration — A/B Testing Implementation

## When to use
- You already have an experiment design (hypothesis, primary metric, MDE, sample size) and need the runtime: assignment, exposure logging, conversion tracking, sticky bucketing.
- Wiring a feature flag into a real experiment with stratified randomisation by `user_id` (or device id for logged-out).
- Multi-platform consistency: same user must get the same variant on web, iOS, app, and email — needs deterministic hashing, not random.
- Building an event pipeline that joins exposure → conversion within a stats engine (Snowflake / BigQuery / ClickHouse).

## When NOT to use
- Traffic too low to reach statistical power in a reasonable window (e.g., <1k weekly users on the surface) — use qualitative methods or holdouts instead.
- Changes that affect every user equally and irreversibly (DB schema migrations, pricing changes for existing customers without grandfathering).
- Cosmetic tweaks where the cost of running the test exceeds the cost of just shipping.
- Multi-armed scenarios with strong network effects (marketplace pricing, social ranking) — A/B is biased; use switchback or geo splits.
- Compliance-bound flows (KYC, payments) where variant differences create audit problems.

## Where it fails / limitations
- Sample Ratio Mismatch (SRM): exposure counts skew (e.g., 51/49 instead of 50/50) → invalid results. Almost always caused by bucketing bugs, redirects, or bot filters that hit one variant more.
- Peeking: stopping early on "significant" results inflates false-positive rate from 5% to 20–30%.
- Carry-over / contamination: same user crossing variants (logged-out → logged-in id swap), shared accounts, multi-device — sticky bucketing must survive both.
- Multiple-comparison inflation: tracking 20 metrics finds "significance" at random; pre-register the primary metric.
- Network effects in marketplaces: control sees fewer listings if treatment buys them up.
- Novelty / primacy bias in week 1 — first-week numbers are unreliable.

## Agentic workflow
Treat experimentation as a contract: agent reads `experiment.yaml` (id, variants, weights, eligibility, primary metric, MDE) and generates: (1) typed assigner with deterministic hash, (2) exposure + conversion event schema, (3) SQL or stats notebook for the readout. Separate agent runs SRM check before any p-value: if `chi2(observed_split, expected_split) > threshold`, abort. A reviewer agent re-derives sample-size and refuses to "call" results before the precomputed end date.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → flag → tracker → analysis pipeline.
- `faion-improver` — post-experiment retro: file pattern/mistake notes for next time (see `.aidocs/memory/`).
- A custom `experiment-srm-checker` agent that consumes daily exposure counts and only forwards results if SRM passes.

### Prompt pattern
```
Given experiment.yaml, generate:
1. assigner.py with deterministic SHA256(user_id || experiment_id) bucketing.
2. tracker.py wrapping exposure + conversion events; dedupe exposures per (exp_id,user_id).
3. readout.sql joining exposures and conversions on (user_id, experiment_id, variant)
   and computing per-variant rate + 95% CI (Wilson score).
4. srm_check.py: chi-square test against weights, fail if p < 0.001.
Constraints: no random.choice — must be deterministic; sticky across sessions.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| GrowthBook CLI | Open-source experimentation platform; flag + analysis | `npm i -g growthbook-cli` · growthbook.io |
| Statsig CLI | Statsig flags, experiments, analytics | npm |
| Eppo CLI | Eppo experiment platform | npm |
| jupytext + papermill | Parametrised stats notebooks for readouts | `pip install papermill` |
| tea-tasting (Python) | Pragmatic experiment statistics (Welch t-test, CI) | `pip install tea-tasting` |
| stats-can / scipy.stats | Underlying statistical tests | `pip install scipy` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GrowthBook | OSS + SaaS | Yes — REST + SDK + CLI | Self-host on Postgres/ClickHouse; agent can manage experiments via API. |
| Statsig | SaaS | Yes — REST + SDK | Strong CUPED + sequential testing. |
| Eppo | SaaS | Yes — Terraform + API | Warehouse-native (Snowflake/BigQuery), no event pipeline rebuild. |
| LaunchDarkly | SaaS | Yes — REST API | Flag-first; experimentation is a paid add-on. |
| PostHog | OSS + SaaS | Yes — REST API + SDK | Flags + product analytics + experiments in one. |
| Optimizely | SaaS | Partial | Heavier UI workflow; less agent-friendly. |
| Amplitude Experiment | SaaS | Yes | If you already use Amplitude analytics. |
| Segment + warehouse | SaaS | Yes | Useful as the event pipe feeding any of the above. |

## Templates & scripts
See `examples.md` and `templates.md` for assigner/tracker. Sample-size sanity check (binomial primary metric):

```python
# scripts/sample_size.py
from math import ceil
from statsmodels.stats.power import NormalIndPower

def sample_size_per_arm(p_baseline: float, mde_relative: float, alpha=0.05, power=0.8):
    p2 = p_baseline * (1 + mde_relative)
    effect = (p2 - p_baseline) / ((p_baseline * (1 - p_baseline)) ** 0.5)
    n = NormalIndPower().solve_power(effect_size=effect, alpha=alpha, power=power, ratio=1.0)
    return ceil(n)

if __name__ == "__main__":
    # baseline 5% conversion, want to detect +10% relative lift
    print(sample_size_per_arm(0.05, 0.10))
```

## Best practices
- Pre-register hypothesis, primary metric, MDE, sample size, and stop date. Treat any deviation as a new experiment.
- Deterministic hashing only: `hash(user_id || experiment_id)` mod 100. Never `random.choice` — breaks stickiness across processes.
- Salt per experiment so that successive experiments don't share buckets (correlated bias).
- Log exposure on every render, dedupe on `(exp_id, user_id, day)`. Without exposure log you can't filter to "actually saw it".
- Daily SRM check: chi-square exposure counts vs expected weights; pause experiment if `p < 0.001`.
- Report effect size + CI, not just p-value. Use Wilson CI for proportions, bootstrap for revenue per user (long-tailed).
- One primary metric, ≤3 secondaries, all guardrails (latency, error rate, churn) tracked but not stop-gated unless degraded.
- Run for full business cycles (≥1 week, often 2) to absorb day-of-week effects and novelty.

## AI-agent gotchas
- LLMs reach for `random.choice([A, B])` — destroys stickiness and reproducibility. Force a deterministic hash with `hashlib.sha256` mod weight buckets.
- Agents log conversions but forget exposures; readout becomes "users who converted while assigned to X" without denominator. Demand both events.
- Sample-size code generated by LLMs frequently confuses absolute and relative MDE; require explicit `mde_relative=0.05  # 5% lift over baseline` in the contract.
- Agents will compute p-value with `scipy.stats.ttest_ind` on a binary metric — wrong test. Use chi-square / two-proportion z-test for binomial, t-test only for continuous.
- "Stop the test, it's significant" pattern: peeking. Bake the stop date into the assigner config and refuse readouts before then unless using a sequential-test method (mSPRT, always-valid CIs).
- Bot/crawler traffic skews to the variant served on cold cache → SRM. Agent must filter `is_bot` before computing exposure ratios.
- Human-in-loop checkpoint: launch decision and shipping decision must be human; agent only produces readouts and recommendations, never auto-promotes a variant.

## References
- Trustworthy Online Controlled Experiments (Kohavi, Tang, Xu) — book, Microsoft / Airbnb / Booking practices.
- "Peeking at A/B tests" — Johari et al., Optimizely; foundational on sequential testing.
- Sample Ratio Mismatch — https://exp-platform.com/Documents/2018%20-%20DiagnosingSRM.pdf
- GrowthBook docs — https://docs.growthbook.io/
- Statsig stats engine — https://docs.statsig.com/
- Eppo statistics — https://docs.geteppo.com/statistics/
