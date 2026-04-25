# Agent Integration — A/B Testing Basics

## When to use
- Drafting an experiment spec from a hypothesis (variants, primary/secondary metrics, sample size, owner) — the `Experiment` dataclass is the contract.
- Adding deterministic bucketing to a service (hash-based assignment, override hooks for QA) — the `ExperimentAssigner` snippet is copy-pastable.
- Validating an experiment config before launch (allocations sum to 1, ≥ 2 variants, exactly 1 primary metric).
- Sketching the conceptual frame for a stakeholder doc (hypothesis → variants → metric → significance).

## When NOT to use
- Event tracking, exposure logging, sequential analysis, lift computation, dashboarding — see sibling `ab-testing-implementation`.
- Causal inference where randomisation isn't possible (rollouts you can't randomise) — switch to quasi-experimental methods (diff-in-diff, synthetic control), out of scope here.
- Bandit / multi-armed allocation — fixed-allocation A/B, not adaptive.
- High-throughput eventing pipelines for thousands of concurrent experiments — use a managed platform; this code is a teaching snippet.

## Where it fails / limitations
- `hashlib.md5` is fine for bucketing but flagged by some compliance scanners; agents may try to "fix" it to SHA-256, which silently changes everyone's bucket. Pin md5 explicitly.
- `bucket = (hash_value % 10000) / 10000.0` gives 4-decimal granularity; allocations like 0.001 (0.1%) round-trip to 0% sometimes. Agents launching 0.5% canaries get truncated.
- No sample-ratio mismatch (SRM) check — the assigner could drift from configured allocations if hash space isn't uniform on a small `user_id` distribution. Always run SRM in production.
- Override path (`override="treatment"`) is unauthenticated; agents copy as-is into prod and create a bypass for QA. Wrap in `if user.is_staff` or env check.
- `target_sample_size: int = 1000` is a placeholder, not statistically derived; agent treats it as the actual power calc. Always compute via baseline rate + MDE.
- No mutual-exclusion / experiment-cohort logic; if two experiments touch the same surface, results are confounded.

## Agentic workflow
The agent's job in basics is *design + safe assignment*, not analysis. Steps: (1) translate a PM hypothesis into the `Experiment` dataclass, (2) compute sample size via MDE/power (separate library: `statsmodels` or `evan-miller-style`), (3) wire `ExperimentAssigner` into the request handler, (4) emit an exposure event for downstream analysis (handled in `ab-testing-implementation`). Pair with a flag platform if you want runtime kill-switch independent of the bucketing.

### Recommended subagents
- `faion-sdd-executor-agent` — runs experiment-launch as an SDD task with a checklist (spec → assignment → exposure → kill-switch).
- `faion-brainstorm` — diverge/converge on hypothesis + metric tree before locking the spec.
- General code-writer for the assigner integration in app code.

### Prompt pattern
```
Design the A/B experiment for "checkout simplification".
Use solo/dev/automation-tooling/ab-testing-basics/README.md.
Inputs:
- baseline conversion = 6.2%
- minimum detectable effect = +0.5pp absolute (relative ~+8%)
- alpha = 0.05, power = 0.8
- two variants (control / treatment), 50/50
Output:
1. Filled Experiment(...) instance
2. Required sample size per variant (cite formula)
3. Exposure event schema (event name, properties)
4. Kill-switch plan
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `statsmodels` | Power / sample size (z-test for proportions) | `pip install statsmodels` |
| `scipy.stats` | Hypothesis tests | bundled with scipy |
| Evan Miller calculator (web) | Quick sample-size sanity check | https://www.evanmiller.org/ab-testing/ |
| `growthbook` CLI | Local SDK + experiment tooling | https://docs.growthbook.io |
| `optuna` (orthogonal) | Bayesian optimisation alternative — not A/B | only when bandits are appropriate |
| `dbt` + `metrics` | Define metrics for downstream analysis | https://docs.getdbt.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GrowthBook | OSS / SaaS | Yes — REST + SDKs | Define experiments in YAML/JSON; agents can flip variants via API. |
| Statsig | SaaS | Yes — REST + SDKs | Experiments + flags + analytics in one; generous free tier. |
| LaunchDarkly Experiments | SaaS | Yes — REST | Use if already on LD for flags. |
| PostHog | OSS / SaaS | Yes — REST | Self-hostable; experiments + product analytics. |
| Optimizely | SaaS | Yes — REST | Enterprise; mature Stats Engine (sequential testing). |
| Eppo | SaaS | Yes — REST | Warehouse-native; computes lifts in your dbt models. |
| Unleash | OSS | Limited | Has variants but weaker analysis layer. |
| AB Tasty / VWO | SaaS | Partial | Marketing-led; client-side bias. |

## Templates & scripts
Sample-size sanity check (z-test for two proportions) the agent can drop alongside the `Experiment`:

```python
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

def sample_size_per_variant(p_control: float, mde_abs: float,
                            alpha: float = 0.05, power: float = 0.8) -> int:
    es = proportion_effectsize(p_control + mde_abs, p_control)
    return int(NormalIndPower().solve_power(
        effect_size=es, alpha=alpha, power=power, ratio=1.0,
        alternative="two-sided"
    )) + 1

# e.g., sample_size_per_variant(0.062, 0.005)
```

Exposure event contract the agent should emit on first variant evaluation:

```json
{
  "event": "experiment_exposed",
  "experiment_id": "exp-checkout-v2-2024",
  "variant": "treatment",
  "user_id": "user-123",
  "ts": "2026-04-25T10:11:12Z",
  "context": {"surface": "checkout", "geo": "PT"}
}
```

## Best practices
- Lock the spec (variants, metrics, MDE, allocation) *before* writing assignment code — once the hash function ships, results bake the spec in.
- Use one primary metric. Secondary metrics are observational; promoting a secondary to primary mid-experiment is HARKing.
- Compute sample size from baseline + MDE + alpha + power; "1000 users" is not a stopping rule.
- Random units must be the same as analysis units — bucket by `user_id`, analyse by `user_id`. Bucketing by session and analysing by user under-powers and biases.
- Hold one variant pure ("control") even when shipping an obvious win; you need the counterfactual for diagnostics.
- Build kill-switches at two layers: (1) flag the experiment off (assigner returns `None`), (2) flag the *feature* off (LegacyPaymentProcessor still wired). Don't conflate the two.
- Record assignment + exposure separately. Assignment is "what would they get"; exposure is "did they actually see it". Analyses run on exposure, not assignment.

## AI-agent gotchas
- Peeking: agents asked to "check if winning early" silently inflate false-positive rate. Either mandate fixed-horizon test or use a sequential-testing library (e.g., `confidence-sequences`).
- Agent confuses relative vs absolute MDE — "+10% lift" on 6% baseline is +0.6pp, not +10pp. Always force units in the prompt.
- Agent writes the assignment hash as `hashlib.sha256(...).hexdigest()` "for security"; changing the hash post-launch reshuffles users. Pin algorithm + comment in source.
- Agent uses `random.random()` instead of deterministic hash — assignments are not stable across requests, breaking session continuity. Fail loud on `random.` imports inside the assigner.
- Agent forgets the override safety check; QA bypass leaks to prod. Always require an `is_staff`/env gate.
- Agent treats two simultaneous experiments as independent without checking surface overlap; results are confounded. Maintain an experiment registry the agent must consult.
- Multiple-comparison: when there are 5+ secondary metrics, agent reports each p-value at α=0.05 — false-positive rate balloons. Apply Bonferroni or report only confidence intervals.
- Human-in-loop checkpoint: launching at > 10% allocation, changing primary metric, or stopping early always requires human sign-off. The agent prepares the case; it does not pull the trigger.

## References
- Kohavi, Tang, Xu — *Trustworthy Online Controlled Experiments* (Cambridge) — https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59
- https://www.optimizely.com/optimization-glossary/statistical-significance/ — Stats Engine intro
- https://www.evanmiller.org/ab-testing/ — power + sample size calculators
- https://exp-platform.com/ — Microsoft Experimentation Platform papers
- https://docs.growthbook.io/statistics/overview — GrowthBook stats docs
- https://eng.uber.com/xp/ — Uber's experimentation infrastructure write-up
