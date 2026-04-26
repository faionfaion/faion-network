# Agent Integration — Experimentation at Scale

## When to use

- Product orgs running 50+ live A/B tests per quarter where central coordination, naming, and metric registry have outgrown spreadsheets.
- Maturity-Level transitions (ad-hoc → structured, structured → scaled): when the team is ready to formalize hypothesis intake, sample-size math, and guardrails.
- Feature-flag rollouts that must be tied to experiment readouts (LaunchDarkly/Statsig/GrowthBook) and need automated SRM (sample-ratio mismatch) checks.
- Warehouse-native shops (Snowflake/BigQuery/Databricks) wanting to drive Eppo/Statsig/GrowthBook from dbt models instead of an in-app SDK.
- Solopreneur or small product teams needing an LLM agent to generate hypotheses, write the experiment doc, monitor results, and emit a readout — replicating a central experimentation team of 1.
- After a launch when leadership asks "what did we learn?" — agentized synthesis across an experiment registry produces a quarterly learning memo.

## When NOT to use

- Pre-PMF zero-to-one with <1k weekly active users — sample-size math will demand months per test; switch to qualitative discovery (`continuous-discovery`, `customer-development`).
- Single-shot launches (marketing campaigns, regulatory cutovers) where a holdout is impossible or unethical.
- High-stakes irreversible decisions (pricing rebrand, contract terms, safety-critical UX) — use multi-method evidence, not a single A/B.
- Enterprise B2B with <50 accounts — switching cost and sample size make A/B impractical; use cohort analysis or switchback designs.
- Teams without a metrics governance owner — without a single source of truth for "what is conversion?" agents will compute four different numbers.
- Compliance-bound surfaces (HIPAA, payment flows, KYC) where any variant must clear legal review before it ships — agentic experiment authoring is too fast for the gating loop.

## Where it fails / limitations

- Sample Ratio Mismatch (SRM) is the silent killer; without an automated chi-square check on assignment counts, ~6% of experiments will report bogus winners.
- Peeking and early stopping inflate false-positive rate from 5% to 30%+; sequential tests (Always-Valid Inference, mSPRT) require careful framework support — most ad-hoc setups don't have it.
- Multiple-comparison explosion: 10 metrics × 50 variants/quarter ≈ 500 tests at α=0.05 ⇒ 25 false wins by chance. Need Bonferroni/BH or pre-registered primary metrics.
- Novelty + primacy effects: 7-day tests miss 4-week behavior change; agents that auto-call winners at day 7 will systematically misjudge habit-forming features.
- Metric definition drift: same name, different SQL, different tools — agents synthesizing across Amplitude + Snowflake will silently double-count.
- Network and interference effects (marketplaces, social features) break SUTVA; A/B becomes biased. Need cluster randomization or switchback designs that most tools don't support.
- LLMs hallucinate "statistical significance" from CI overlap or p-value misreads — never let an agent declare a winner without explicit framework output (lift, CI, p-value, power, SRM-check).
- Experimentation graveyards: 100k tests/year sounds heroic but most generate no learning; without a learning-extraction step the registry becomes write-only.

## Agentic workflow

```
Intake     → hypothesis-author (sonnet)        → experiment-doc.md + JSON spec
Pre-flight → sample-size-calculator (haiku)    → required N, runtime estimate, MDE
Pre-flight → guardrail-mapper (sonnet)         → guardrail metrics + thresholds
Launch     → flag-deployer (haiku, gated)      → LaunchDarkly/Statsig flag created
Monitor    → srm-watcher (haiku, hourly)       → SRM alert if chi-square p<0.001
Monitor    → metric-watcher (haiku, daily)     → primary/guardrail rolling readout
Readout    → analyst-agent (opus)              → readout.md, decision recommendation
Library    → learning-extractor (opus, weekly) → learnings-memo.md, registry update
Governance → metric-registry-keeper (sonnet)   → metric-catalog.yaml diff-checker
```

All agents read/write under `.aidocs/product_docs/experiments/` with a per-experiment folder (`exp_yyyy-NN-slug/`). Human-in-the-loop gates: hypothesis approval, flag deployment, decision sign-off.

### Recommended subagents

| Subagent | Model | Cadence | Inputs | Outputs |
|----------|-------|---------|--------|---------|
| `hypothesis-author` | sonnet | On intake | Opportunity-solution-tree node, prior data | `experiment-doc.md` (hypothesis, primary, guardrail, MDE) |
| `sample-size-calculator` | haiku | Pre-flight | Baseline rate, MDE, α, power | Required N, expected runtime, traffic-split |
| `guardrail-mapper` | sonnet | Pre-flight | Surface (checkout, signup, etc.), metric registry | Guardrail metrics + degradation thresholds |
| `flag-deployer` | haiku | On approval | Vendor (LaunchDarkly/Statsig/GrowthBook), variant config | API call result, flag URL |
| `srm-watcher` | haiku | Hourly | Assignment table, expected ratio | Pass/fail + chi-square p-value |
| `metric-watcher` | haiku | Daily | Warehouse query (dbt model), running window | Daily delta + CI; flags on guardrail breach |
| `analyst-agent` | opus | At decision point | All experiment data, segment cuts | Readout: ship/iterate/kill + caveats |
| `learning-extractor` | opus | Weekly | Closed experiments since last run | Cross-cutting learnings memo |
| `metric-registry-keeper` | sonnet | On metric change | dbt models, semantic layer | Diff alert if metric SQL changes mid-flight |

Cheap models (haiku) for collection, hourly checks, and flag operations. Sonnet for structured authoring (docs, mappings). Opus only for synthesis and decision recommendations. Never run opus on hourly SRM watch — it burns tokens for a chi-square test.

### Prompt pattern

```
<role>You are the {agent}. Experimentation at scale (Kohavi/Tang/Xu).</role>

<inputs>
  <experiment_id>{exp_yyyy-NN-slug}</experiment_id>
  <doc>{path to experiment-doc.md}</doc>
  <metrics>{path to metric-catalog.yaml}</metrics>
  <data>{warehouse SQL or vendor API result}</data>
  <prior>{related experiments registry slice}</prior>
</inputs>

<rules>
  - Never declare a winner without: lift, two-sided CI, p-value (or posterior), pre-registered primary metric, SRM-check passed.
  - Surface novelty risk: if runtime < 14 days or primary metric is engagement, flag "novelty likely".
  - Reject solution-shaped hypotheses ("we should add X"). Require behavioral prediction ("if X then metric M will move by Δ").
  - Never compute on >1 primary metric without Bonferroni correction in the verdict.
  - Output JSON to schema {schema_path}; markdown digest <= 80 lines.
  - If interference/cluster risk is plausible (marketplace, social, viral surface), flag and block decision until cluster-randomization is confirmed.
</rules>

<task>{cadence-specific instruction}</task>
```

Wire through Claude Agent SDK with structured outputs (Pydantic/Zod). Pin model output to vendor-emitted statistics — do not let the LLM compute p-values; have it read them from GrowthBook/Statsig/Eppo APIs.

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `growthbook` CLI (`@growthbook/cli`) | Manage experiments, features, definitions as code | `npm i -g @growthbook/cli` |
| `statsig` CLI / Console API | Feature gates, experiments, metrics via REST | docs.statsig.com/console-api |
| `ldcli` (LaunchDarkly) | Feature flags, segments, env management | docs.launchdarkly.com/home/getting-started/ldcli |
| `eppo` API (no first-class CLI) | Warehouse-native experiment readouts | docs.geteppo.com/reference/api |
| `optimizely` CLI/REST | Legacy A/B + flags | docs.developers.optimizely.com |
| `dbt` | Define metrics + experiment exposure tables once, reuse everywhere | getdbt.com |
| `cube` / `metricflow` | Semantic layer for metric governance | cube.dev / docs.getdbt.com/docs/build/about-metricflow |
| `posthog` CLI | OSS feature flags + experiments + analytics | posthog.com/docs/api |
| `amplitude-cli` | Pull cohort + funnel deltas as JSON | amplitude.com/docs/apis |
| `gh` | Treat experiment-doc.md as PR; review gate before launch | cli.github.com |
| `cron` / `systemd timers` | Drive hourly/daily watchers | system |
| `slack` webhook / `tg-send` | Alert SRM and guardrail breaches | NERO `~/bin/tg-send` |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GrowthBook | OSS + cloud | Yes (full REST + SDK) | Developer-first, OSS self-host, warehouse-native, supports CUPED + sequential testing |
| Statsig | SaaS | Yes (Console API) | Enterprise scale 1T+ events/day, generous free tier, built-in CUPED + Pulse readouts |
| Eppo | SaaS | Yes (REST) | Warehouse-native, statistical rigor, dbt-first, no in-app SDK overhead |
| Amplitude Experiment | SaaS | Yes (REST) | Tight coupling with Amplitude analytics; weak as standalone flag system |
| Optimizely | SaaS | Yes (REST) | Legacy enterprise; expensive; agent integration ok but verbose |
| LaunchDarkly | SaaS | Yes (REST + Terraform provider) | Best-in-class flag management; experimentation as add-on |
| PostHog | OSS + cloud | Yes (REST) | All-in-one OSS analytics + flags + experiments; weakest stats engine of the set |
| Split.io | SaaS | Yes (REST) | Enterprise flags + experimentation; data-streams to warehouse |
| Convert.com | SaaS | Partial | Marketing-A/B; weaker programmatic API |
| VWO | SaaS | Partial | Marketing-A/B; client-side bias |
| Mixpanel Experiments | SaaS | Yes (REST) | Tied to Mixpanel analytics |
| Snowflake / BigQuery / Databricks | DW | Yes (SQL) | Source of truth; warehouse-native tools (Eppo, Statsig Warehouse Native) read directly |
| dbt | Modeling | Yes (CLI + Cloud API) | Define `dim_experiment_exposure` + metric models once, reused by all agents |
| Cube / MetricFlow | Semantic layer | Yes (REST + GraphQL) | Single metric definition; agents query here, not raw warehouse |

## Templates & scripts

Experiment spec schema (`experiment-doc.yaml`):

```yaml
id: exp_2026-04-checkout-cta
status: draft  # draft | review | running | analyzing | shipped | killed
hypothesis: |
  If we replace "Buy now" with "Get yours" on checkout CTA,
  then conversion rate will increase by >=2% (relative)
  because of higher loss-aversion framing in cohort A/B prior.
primary_metric: checkout_completion_rate
guardrail_metrics:
  - name: checkout_p95_latency_ms
    threshold: "no degradation > 5%"
  - name: refund_rate_7d
    threshold: "no increase > 0.5pp"
secondary_metrics:
  - aov_usd
  - bounce_rate
mde_relative: 0.02
power: 0.8
alpha: 0.05
required_n_per_arm: 12450
expected_runtime_days: 14
traffic_split: {control: 0.5, variant: 0.5}
randomization_unit: user_id
exposure_event: viewed_checkout
exclusions: [bot_traffic, internal_ip]
segment_cuts: [device, country, paid_vs_organic]
sequential_test: false
cluster_randomization: false
related_experiments: [exp_2025-Q4-cta-color]
owner: pm@team.com
reviewer: data-science@team.com
```

Sample-size + runtime helper (`scripts/sample_size.py`, ~30 lines):

```python
import math
from statsmodels.stats.power import NormalIndPower

def required_n(baseline: float, mde_rel: float, alpha=0.05, power=0.8) -> int:
    """Two-proportion z-test sample size per arm."""
    p1 = baseline
    p2 = baseline * (1 + mde_rel)
    pooled = (p1 + p2) / 2
    es = (p2 - p1) / math.sqrt(pooled * (1 - pooled))
    n = NormalIndPower().solve_power(effect_size=es, alpha=alpha, power=power)
    return int(math.ceil(n))

def runtime_days(n_per_arm: int, daily_traffic: int, split: float = 0.5) -> int:
    return math.ceil(n_per_arm / (daily_traffic * split))

if __name__ == "__main__":
    import json, sys
    cfg = json.load(sys.stdin)
    n = required_n(cfg["baseline"], cfg["mde_rel"], cfg["alpha"], cfg["power"])
    days = runtime_days(n, cfg["daily_traffic"], cfg["split"])
    json.dump({"n_per_arm": n, "runtime_days": days}, sys.stdout)
```

SRM watcher (chi-square, ~20 lines, `scripts/srm_check.py`):

```python
from scipy.stats import chisquare
def srm(observed: list[int], expected_split: list[float]) -> dict:
    total = sum(observed)
    expected = [total * s for s in expected_split]
    stat, p = chisquare(observed, expected)
    return {"chi2": stat, "p": p, "pass": p > 0.001}
```

Cron schedule for the loop:

```
*/15 * * * *  /usr/local/bin/claude run /exp-srm-check
0 */6 * * *   /usr/local/bin/claude run /exp-metric-watch
0 8 * * 1     /usr/local/bin/claude run /exp-weekly-readout
0 9 1 * *     /usr/local/bin/claude run /exp-learning-memo
```

## Best practices

- Pre-register the primary metric, MDE, and decision rule before traffic flips — agents must reject any experiment-doc lacking these fields.
- Run an A/A test on the platform quarterly; if false-positive rate ≠ ~5%, fix the platform before shipping verdicts from it.
- Use CUPED (Controlled-experiment Using Pre-Existing Data) for variance reduction — cuts sample size 30–50% on heavy-tailed metrics; supported by GrowthBook, Statsig, Eppo.
- Always include latency, error rate, and a revenue/retention metric in guardrails — engineering wins that tank infra are common silent failures.
- Stratify randomization on known high-variance dimensions (device, country, plan tier) to control for imbalance.
- Use a metric registry (dbt + Cube/MetricFlow) so "conversion" has one SQL definition; agents must read from registry, never re-derive.
- Lock the analysis plan; freeze metrics + segments at launch; new cuts after launch are exploratory only and must be tagged as such.
- Treat sequential testing as opt-in and document the procedure (mSPRT, group-sequential); ad-hoc peeking is the dominant cause of bad ship decisions.
- After ship, leave a holdout (1–5%) on for 4–8 weeks to catch novelty decay.
- Quarterly: publish a "tests we got wrong" memo; tracking false ships is the single highest-leverage learning loop.
- Token budget: cap analyst-agent at 50k tokens per readout; if it needs more, the experiment has too many variants — split it.

## AI-agent gotchas

- LLMs will confidently misread CIs as "the variant has 95% chance of winning" — that's a Bayesian posterior, not a frequentist CI. Force the agent to copy the framework's verbatim output instead of paraphrasing.
- Agents synthesizing across vendors will silently double-count exposed users when the experiment runs in two SDKs (web + mobile). Require unique randomization-unit + dedup before stats.
- Hypothesis-author drifts to solution-shaped output ("we should redesign onboarding") when prompts allow narrative answers — constrain to a Hypothesis-If-Then-Because schema with a numeric MDE field.
- SRM is invisible without the chi-square check; agents will happily report a winner from an SRM-broken experiment. Make srm-watcher a hard gate on analyst-agent.
- Multiple-comparison correction is forgotten by default; always pass the metric count + α to the prompt and require Bonferroni or BH adjustment in the verdict.
- Peeking: hourly metric-watcher posts a "trending positive" message and humans interpret it as ship signal — make daily messages explicitly say "non-decisional, sequential test not enabled" until run completes.
- Novelty/primacy: agents shown 7-day data and asked "is this a winner" will say yes; require minimum-runtime gate (≥14 days for engagement metrics, ≥1 full business cycle for revenue).
- Vendor naming inconsistencies (LaunchDarkly "rule" vs Statsig "gate" vs GrowthBook "feature") trip up flag-deployer; encode the vocabulary mapping in the prompt.
- API keys for LaunchDarkly/Statsig leak through prompts when read from `.env`; route through the host environment, never inline in the model context.
- Idempotency: flag-deployer retries can create duplicate experiments — require an idempotency key (hash of experiment-id) on every vendor call.
- ZDR/PII: warehouse query results often contain user_ids/emails; agents must use Anthropic ZDR endpoints or aggregate before sending.
- Cluster/network interference (marketplaces, viral) is invisible to off-the-shelf tools — agent must check a "social-surface" flag on the experiment-doc and block decision-making if cluster-randomization is required but unavailable.
- Learning-extractor will hallucinate "we learned X" from a single null result; require N≥5 closed experiments with shared theme before emitting a learning bullet.
- Metric definition drift mid-flight (someone edits dbt model) silently changes the readout; metric-registry-keeper must hash the metric SQL at launch and re-hash at readout, blocking on mismatch.

## References

- Ron Kohavi, Diane Tang, Ya Xu — *Trustworthy Online Controlled Experiments* (2020), the canonical reference.
- Microsoft Experimentation Platform (ExP) — public papers on SRM, CUPED, organizational scaling.
- GrowthBook docs — `docs.growthbook.io` (CUPED, sequential testing, warehouse mode).
- Statsig Pulse + Warehouse Native — `docs.statsig.com`.
- Eppo — `docs.geteppo.com` (warehouse-native, dbt-first).
- LaunchDarkly Experimentation — `docs.launchdarkly.com/home/about-experimentation`.
- Booking.com, Airbnb, Spotify, LinkedIn experimentation engineering blogs (2022–2026).
- Sibling methodology: `../../../research/researcher/continuous-discovery/README.md` (feeds hypotheses).
- Sibling methodology: `../../../product/product-manager/` (decision frameworks consume readouts).
- Anthropic Claude Agent SDK — agents, structured outputs, scheduled triggers (`schedule` skill).
- "Always Valid Inference" (Optimizely 2015), "Peeking at A/B Tests" (Johari et al, 2017) — sequential-testing foundations.
