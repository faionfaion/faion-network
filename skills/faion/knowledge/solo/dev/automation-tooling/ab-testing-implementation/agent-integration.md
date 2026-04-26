# Agent Integration — A/B Testing Implementation

## When to use
- Building the experiment plumbing in code: deterministic assignment by `hash(user_id + experiment_id)`, exposure tracking, conversion events.
- Adding a typed analytics layer (`ExperimentEvent`) so events land cleanly in Mixpanel / Amplitude / PostHog / a warehouse.
- Implementing significance, lift, confidence interval, and power calculations for shipped experiments.
- Generating an experiment summary endpoint or daily-metrics report for a dashboard.
- Migrating from raw "if user_id % 2 == 0" code to a structured assignment + tracking layer.

## When NOT to use
- For experiment design (hypothesis, MDE, sample size). That belongs in `ab-testing-basics`.
- When a managed platform (Statsig, Optimizely, GrowthBook, LaunchDarkly Experiments, PostHog) already runs assignment and stats — wiring them in is far cheaper than reimplementing.
- For multi-armed bandit / contextual bandits — the methodology is fixed-allocation A/B. Bandits need a different stack (Vowpal Wabbit, Thompson sampling).
- For tests that require sequential analysis (always-valid p-values, mSPRT). Naive z-test peeking gives false positives.
- For tiny user volumes where you'll never reach significance — switch to qualitative or holdout testing instead.

## Where it fails / limitations
- README's z-test assumes independence + binomial conversions. Doesn't cover ratio metrics (revenue / user), continuous metrics (latency p95), or clustered observations.
- "Wait for statistical significance" guidance ignores peeking; running the analyzer on a live dashboard inflates Type I error.
- Sample-size calc uses a 80%-power normal approximation; for very small/large baseline rates the formula drifts.
- `ExperimentTracker._exposures` is in-memory — won't dedupe across processes/replicas; an exposure is logged per pod restart.
- No SRM (sample-ratio mismatch) check — agents will ship traffic-imbalanced experiments and read garbage.
- No CUPED / variance reduction; results will appear underpowered vs what's possible.
- Bot/duplicate-user filtering is a sentence in "Best Practices"; the code doesn't implement it.
- Multiple-comparisons not handled (running 10 experiments in parallel without correction).

## Agentic workflow
Drive this with two cooperating agents: an `experiment-impl` agent that wires assignment, exposure, and conversion code into the service (and writes tests proving deterministic assignment + idempotent exposure), and an `experiment-analyzer` agent that runs the stats only on closed/locked datasets — never on live tables. Force a guardrail: the analyzer must refuse to compute p-values until (a) minimum runtime elapsed, (b) SRM check passes, (c) sample size ≥ pre-registered minimum. Output is always a structured report (JSON), never a "the variant is better" sentence — humans decide ship/no-ship.

### Recommended subagents
- `general-purpose` — wiring assignment + tracking into the service, writing tests.
- `faion-sdd-executor-agent` — when the experiment is a feature with SDD tasks.
- A narrow `srm-checker` task agent — runs only the chi-square SRM check and aborts the analysis if traffic split deviates from configured.
- A separate `stats-reviewer` agent (Opus only) — sanity-checks the analyzer's choices: metric type, test choice, multiple-comparisons correction, peeking guard.

### Prompt pattern
```
Read solo/dev/automation-tooling/ab-testing-implementation/README.md.
Wire experiment "<id>" into <service> at <surface>. Use the existing
ExperimentAssigner. Add: track_exposure on render, track_conversion on
<event>. Write pytest cases that (1) prove identical user_id always gets
the same variant, (2) exposures dedupe per (exp,user), (3) conversion is
recorded with correct variant.
```
```
Given a closed dataset for experiment <id>, run the analyzer. Refuse if
SRM > 1% (chi-square p<0.01) or sample size < pre-registered minimum.
Emit JSON: {control, treatment, lift, p_value, ci, power, srm_p,
duration_days, decision_ready: bool}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest --cov` + `hypothesis` | Property-test deterministic assignment | pip |
| `pandas` + `scipy.stats` | Local stats, sanity vs analyzer | pip |
| `statsmodels` | Robust two-proportion z, Welch's t, etc. | pip |
| `dbt test` | Validate the experiment data model in the warehouse | docs.getdbt.com |
| `growthbook` CLI | Self-host experiment platform; agent-friendly | docs.growthbook.io |
| `posthog-cli` | Manage feature flags + experiments via CLI | posthog.com/docs/cli |
| `statsig-cli` | Statsig config-as-code | docs.statsig.com |
| `expan` (Zalando) | Experiment analysis Python lib | github.com/zalando/expan |
| `evan` / `bayesian-testing` | Bayesian A/B Python libs | pypi |
| `srmcheck` (homegrown chi-square script) | SRM guard | n/a |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GrowthBook | OSS | Yes | Config-as-code (YAML), API + SDK; agents can author experiments in repo. |
| PostHog | OSS + SaaS | Yes | Feature flags + experiments + event store; one stack. |
| Statsig | SaaS | Yes | Strong API, automatic SRM, sequential testing. |
| Optimizely Feature Experimentation | SaaS | Partial | Powerful but enterprise auth makes agent automation friction. |
| LaunchDarkly Experimentation | SaaS | Yes | Pairs with existing LD flags; REST API. |
| Eppo | SaaS | Yes | Warehouse-native (BigQuery/Snowflake/Databricks) — no client SDK needed. |
| GrowthBook Cloud | SaaS | Yes | Hosted variant. |
| Mixpanel / Amplitude | SaaS | Partial | Good event store, weaker built-in stats. |
| Apache Druid / ClickHouse | OSS | Yes | Good event sinks for high-cardinality experiments. |
| BigQuery / Snowflake / Databricks | SaaS | Yes | Warehouse-side analysis is the durable pattern. |

## Templates & scripts
See `templates.md` and `examples.md` for full code. Minimum SRM guard the agent should always run before computing lift:

```python
# scripts/srm_check.py
import sys
from scipy.stats import chisquare

def srm(observed: dict[str, int], expected_split: dict[str, float], alpha=0.001) -> bool:
    total = sum(observed.values())
    expected = [expected_split[k] * total for k in observed]
    chi, p = chisquare(list(observed.values()), f_exp=expected)
    print(f"chi2={chi:.3f} p={p:.4f}")
    return p > alpha  # True = no SRM

if __name__ == "__main__":
    # observed = {'control': 49210, 'treatment': 50790}
    # expected_split = {'control': 0.5, 'treatment': 0.5}
    ok = srm(eval(sys.argv[1]), eval(sys.argv[2]))
    sys.exit(0 if ok else 1)
```

## Best practices
- Pre-register: hypothesis, primary metric, MDE, sample size, runtime, SRM threshold — store as YAML in repo before launch.
- Hash assignment with a stable, namespaced salt: `hash(f"{experiment_id}:{user_id}")` so re-running an experiment doesn't re-bucket the same user.
- Track exposures only when the variant is actually rendered/applied, not on assignment — otherwise lift dilutes.
- Persist exposures in a durable store (warehouse, event bus), not in-process — `_exposures` set is dev-only.
- Always check guardrail metrics (latency, error rate, churn) alongside the primary metric.
- Never peek with naive z-tests; if you must monitor live, use sequential testing (mSPRT) or a Bayesian framework.
- Bucket holdouts (5-10% never see any experiment) so long-term effects can be measured.
- Quarantine bots, internal users, and replays before analysis.
- Decision rule and stop date written down before launch — agents should refuse to compute "is it significant?" past arbitrary peeks.

## AI-agent gotchas
- Agents will happily compute a p-value on day 2 of a 14-day experiment. Block with a runtime/sample-size precondition.
- "Optimize the assigner" prompts can replace `hash(user_id + exp_id)` with a non-stable hash (`hash()` in Python 3 is salted per process). Use `hashlib.sha256` explicitly.
- Multiple comparisons: agents will analyze 6 secondary metrics and report the one with p<0.05 as a win. Force Bonferroni / Benjamini-Hochberg.
- Agents drop the SRM check when "the build is failing." Make it non-skippable.
- Lift formula: agents may flip control/treatment in `(treatment_rate - control_rate) / control_rate` after refactors. Add a property test.
- For revenue / continuous metrics, agents will reuse the binomial z-test pattern — wrong test. Force a typed metric registry: `binary | continuous | ratio | count` with a different analyzer per type.
- "Stop the experiment early because lift is huge" → almost always regression to mean from peeking. Agents must refuse early-stop without sequential method.
- Cross-experiment pollution: assigning the same user to two experiments touching the same surface invalidates both. Agents should detect overlapping experiments before launch.

## References
- Kohavi, Tang, Xu, Trustworthy Online Controlled Experiments (Cambridge).
- Microsoft ExP & SRM: https://exp-platform.com/Documents/2017-08KDDFabijan-SRM.pdf
- CUPED variance reduction: Deng et al., 2013.
- mSPRT / always-valid inference: Johari, Pekelis, Walsh.
- GrowthBook stats engine: https://docs.growthbook.io/statistics
- PostHog experiments: https://posthog.com/docs/experiments
- Sibling: `solo/dev/automation-tooling/ab-testing-basics/`, `feature-flags/`.
