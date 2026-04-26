# Agent Integration — Data-Driven Requirements Engineering

## When to use
- A backlog of feature requests with conflicting stakeholder priorities and existing telemetry/usage data — the matrix replaces "loudest voice wins" with usage- and revenue-weighted ranking.
- A regulated/audited product (fintech, healthtech) where every requirement must trace back to a measurable business question and baseline; auditors want a metric trail, not a slide.
- Performance / reliability work where the symptom (p95 latency, error rate, support ticket volume) is already measured but no one has translated it into requirement form with target deltas.
- A/B-testable surfaces (checkout, signup, pricing pages) where rolling out without a hypothesis + sample-size pre-calc is a waste of an experiment slot.
- AI/ML feature proposals where ROI must be defended in advance — the framework's four impact areas (operational, experience, financial, risk) prevent "we'll measure later" hand-waving.
- Roadmap quarter-planning when finance is asking for forecast impact per initiative — predictive analytics + cohort baselines turn "we think it'll help" into a numbered range.

## When NOT to use
- Pre-PMF / pre-launch products with no users and no telemetry. Instinct, qualitative discovery, and Wizard-of-Oz prototypes beat fake data. (Use `continuous-discovery` instead.)
- Discovery of a brand-new market segment — historical data of a different cohort actively misleads. Run interviews and persona work first.
- Compliance-mandatory features (GDPR, KYC, accessibility floor). Legal "must" overrides any score; don't pretend the matrix decided.
- Highly creative / brand / narrative work where the metric is downstream qualitative perception. Premature quantification kills the requirement.
- When the org has no data engineering capacity and the "data" is hand-cleaned spreadsheets shipped weekly. The veneer of rigor exceeds the actual rigor; document caveats or fall back to opinion-based prioritization with that flag visible.
- Two-week sprint micro-decisions where the cost of analysis exceeds the cost of just shipping the thing and rolling back.

## Where it fails / limitations
- **Survivorship bias in usage data**: heavily-used features look high-priority because users who hated them already churned. Add churn-cohort comparison or you'll over-invest in features your remaining base loves and your lost base rejected.
- **Vanity metric capture**: "page views" and "DAU" feel like business signal but are easy to game. Tie every requirement to a downstream conversion / retention / revenue metric, not a top-of-funnel proxy.
- **Baseline drift**: the "current value" cell ages out fast (seasonality, marketing campaigns, releases). Stamp every metric with `as_of_date` and a query/dashboard URL; reject baselines older than ~30 days for active surfaces.
- **Sample-size theater**: A/B plans that don't pre-calculate MDE (minimum detectable effect) and required N produce "no significant difference" results that are actually underpowered. Use a power calculator before, not after.
- **Simpson's paradox in cohort rollups**: aggregate metrics improve while every segment gets worse (or vice versa). Always slice by acquisition channel, plan tier, geo, and device class before declaring a baseline.
- **Privacy / consent boundaries**: PII or behavioral data may be unusable for product analytics under GDPR/CCPA without a lawful basis. Requirements built on data you cannot legally use will fail at the legal review gate.
- **Causal vs. correlational confusion**: "users who use feature X retain 2x" almost never means "shipping feature X for everyone doubles retention". Self-selection swallows the effect. Frame requirements around hypotheses to be tested, not foregone conclusions.
- **AI ROI fiction**: 95% of enterprise AI projects fail without a data strategy (cited in README). The framework asks for the four impact areas — most teams fill three with guesses; mark unknowns as "to be measured" not as point estimates.

## Agentic workflow
Drive this as a four-pass pipeline that turns telemetry into reviewable requirements. (1) **Question pass** — a sonnet agent reads the business context and emits `{business_question, hypothesis, kpi_owner, expected_direction}`; no data yet. (2) **Baseline pass** — agents query BI / warehouse / product analytics (BigQuery, Snowflake, Mixpanel, PostHog, GA4) and emit `{kpi, current_value, segment, as_of_date, source_url, n}`. Parallel agents per data source reduce blocking on slow warehouses. (3) **Requirement pass** — given baseline + hypothesis, an opus agent writes the structured requirement (the README template) and the success-metric table; a separate agent runs power calculation for the validation A/B. (4) **Review pass** — `faion-sdd-executor-agent` re-reads the requirement against constitution standards (no vanity metrics, has baseline + target + measurement method, validation plan defined). Humans own (a) the business question, (b) target setting (aggressive vs. realistic), (c) the go/no-go after the experiment.

### Recommended subagents
- `faion-brainstorm` — diverge on candidate hypotheses and KPI choices before locking the question. Skipping this gives you a beautifully-instrumented requirement for the wrong KPI.
- `faion-sdd-executor-agent` — gate-checks the requirement file: baseline cited, target numeric, measurement method named, validation plan present. Rejects requirements with "TBD" in success metrics.
- `faion-feature-executor` — once the requirement passes review, execute the implementation tasks bounded by the success criteria.
- `faion-improver` — quarterly meta-loop: read requirements shipped 1-2 quarters ago, compare predicted target vs. measured outcome, log calibration error per author and per domain (turn it into a "we systematically over-promise on conversion" pattern).
- A custom `metric-fetcher` worth creating: input `{warehouse, query, segment}`, output `{value, n, ci_95, query_hash, as_of}`. Caches results; refuses values older than `max_age_days`. Reuse across all data-driven requirements.
- A custom `power-calc-agent`: input `{baseline_rate, mde, alpha, power}`, output `{required_n_per_arm, runtime_estimate_days, runtime_at_traffic}`. Bolt onto the validation plan.

### Prompt pattern
```
You are a data-driven BA. Inputs: business_question, hypothesis, baseline[] (from warehouse),
constraints. Output JSON conforming to the README template:
{
  requirement_id, requirement_statement,
  business_context: {question, current_state_data[], target_state},
  evidence: {data_sources[{source, metric, current_value, n, as_of, confidence}], analysis_summary, supporting_links[]},
  success_metrics: [{name, baseline, target, direction, measurement_method, kpi_owner}],
  validation_plan: {ab_test: {hypothesis, primary_metric, mde_pct, alpha, power, required_n_per_arm, expected_runtime_days}, holdout_pct, guardrail_metrics[]},
  risks: [{risk, likelihood, mitigation}],
  data_caveats: [<= 3 bullets on segmentation, sample, recency>]
}
Constraints:
- Every current_value MUST cite source_url + as_of date. Reject "approx" / "~" without a query.
- Every target MUST have a measurement_method that is queryable (SQL / event name / dashboard URL).
- If baseline n < 100 or as_of > 30 days, mark confidence "low" and recommend re-baselining.
- Refuse to ship requirement if no guardrail metric is defined (regression detector).
- Distinguish correlational evidence from causal; never claim causation without an experiment slot.
```

```
You are a metric-fetcher for ONE KPI. Input: {warehouse, sql_or_event, segment, max_age_days}.
Output JSON:
{
  metric, value, n, confidence_interval_95, segment, as_of, query_hash, source_url,
  caveats: [<= 3 bullets: seasonality, sample, definition>],
  freshness_status: "fresh"|"stale"|"missing"
}
If as_of older than max_age_days, return freshness_status="stale" and refuse to be used as a baseline.
Never invent values; if the warehouse query errors, return value=null and surface the error.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Version-controlled SQL transformations; agents reference dbt models as the canonical KPI definitions | https://docs.getdbt.com |
| `bq` | BigQuery CLI; agents pull baselines as JSON, stamp `as_of` from query timestamp | `gcloud components install bq` |
| `snowsql` | Snowflake CLI equivalent for warehouse queries | https://docs.snowflake.com/en/user-guide/snowsql |
| `posthog` (REST) | Self-hosted/SaaS product analytics with first-class API; pull funnels and cohort retention as evidence | https://posthog.com/docs/api |
| `mixpanel` (REST/JQL) | Event analytics queryable from agents; cohort + funnel endpoints | https://developer.mixpanel.com |
| `metabase-cli` / Metabase API | Open-source BI; agents render baseline charts and embed in the requirement doc | https://www.metabase.com/docs/latest/api |
| `pwr` (R) / `statsmodels` (Python) | A/B power calculation; computes required N from baseline + MDE | `pip install statsmodels` |
| `numpy` + `pandas` + `scipy.stats` | Cohort segmentation, Simpson's-paradox checks, CI computation on baselines | `pip install numpy pandas scipy` |
| `pandas-profiling` / `ydata-profiling` | One-shot data quality report agents can attach to evidence section | `pip install ydata-profiling` |
| `gh` + `jq` | Pull product issue counts / churn signal from support repos as supplementary evidence | https://cli.github.com |
| `claude` CLI | Run the question / requirement / review passes against the JSON schema | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog | OSS / SaaS | Yes (REST + SQL) | Self-hostable; agents can run trends, funnels, cohort retention queries; ideal default for OSS-leaning teams |
| Mixpanel | SaaS | Yes (REST + JQL) | Strong for event-based KPI baselines; rate limits on free tier |
| Amplitude | SaaS | Yes (REST + Behavioral Graph API) | Cohort + retention + impact analysis exposed as API |
| GA4 | SaaS (free) | Yes (Data API) | Web-traffic baseline; agents fetch via google-analytics-data SDK |
| Segment / Rudderstack | SaaS / OSS | Yes (Tracking + Personas API) | Source of truth for event schema; agents validate that proposed metrics are actually emitted |
| Looker / Mode / Hex | SaaS | Yes (REST + LookML / Notebook API) | BI; agents reference saved Looks / models as canonical KPI definitions |
| Metabase | OSS | Yes (REST API) | Cheap default BI for small teams; agents read Q&A endpoints |
| Statsig / GrowthBook / Eppo / Optimizely | SaaS / OSS | Yes (SDK + REST) | A/B platforms; agents pre-register experiments with hypothesis, MDE, primary metric |
| Hightouch / Census | SaaS | Yes (REST) | Reverse-ETL — agents trigger sync of measured outcomes back into product DB once experiment ends |
| Atlan / DataHub / OpenMetadata | SaaS / OSS | Partial | Data catalogs; agents look up metric ownership, freshness SLA, lineage before citing a number |
| Great Expectations / dbt tests | OSS | Yes (CLI) | Data-quality checks the agent can run before trusting a baseline |
| Tableau / Power BI | SaaS | Limited (REST) | Read-only dashboard URLs are fine as evidence links; programmatic extraction is harder |

## Templates & scripts
See `templates.md` and `README.md` for the Data-Driven Requirements doc shell. Inline an A/B power-calculation helper that bolts onto the validation plan:

```python
# power_calc.py — usage: python power_calc.py 0.12 0.10 0.05 0.8 50000
# args: baseline_rate, mde_absolute, alpha, power, daily_traffic_per_arm
import sys, math
from statistics import NormalDist

def required_n(p1, mde, alpha=0.05, power=0.8):
    p2 = p1 + mde
    z_a = NormalDist().inv_cdf(1 - alpha / 2)
    z_b = NormalDist().inv_cdf(power)
    pbar = (p1 + p2) / 2
    num = (z_a * math.sqrt(2 * pbar * (1 - pbar)) +
           z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(num / (mde ** 2))

p1, mde, alpha, power, daily = (float(sys.argv[1]), float(sys.argv[2]),
                                float(sys.argv[3]), float(sys.argv[4]),
                                float(sys.argv[5]))
n = required_n(p1, mde, alpha, power)
days = math.ceil(n / daily)
print(f"required_n_per_arm: {n}")
print(f"runtime_days_at_{int(daily)}_per_arm: {days}")
print(f"verdict: {'feasible' if days <= 28 else 'too long; raise MDE or pool segments'}")
```
If runtime exceeds the experiment slot budget (typical: 14-28 days), the requirement should not promise an A/B-validated outcome — escalate to a holdout or skip experimentation.

## Best practices
- Pin the **business question** before touching data. Without it, agents mine for any metric that moves and call it a finding.
- Lock metric **definitions** in dbt / LookML / a metric layer before requirement writing. Reject any baseline that doesn't reference a versioned model.
- Always cite **n** alongside baseline values. A 12% conversion rate from 80 sessions is not the same number as from 80,000.
- Stamp `as_of` on every metric and refuse stale baselines (default 30 days; 7 days for fast-moving surfaces).
- Pre-register the A/B: hypothesis, primary metric, MDE, alpha, power, runtime, guardrails. Decisions made post-hoc on a peeked dashboard are not data-driven.
- Define **guardrail metrics** that must NOT regress (latency, error rate, support load) — every primary-metric win comes with a regression-check pass.
- Slice baselines by ≥ 2 dimensions (cohort × plan, channel × geo) to catch Simpson's paradox before it lands in a postmortem.
- Tie target setting to a **business-relevant delta** (e.g. "+€X ARR / quarter"), not a vanity percentage. Agents will happily promise +200% on tiny denominators.
- Archive the final requirement + post-hoc measurement in `.aidocs/` (or BI doc layer) so the next quarter's calibration loop can compare predictions to outcomes.
- Treat the BABOK competency table (statistical analysis, data viz, SQL, A/B, predictive) as agent-tool selection guidance, not as a hiring spec — assign each pass to the right tool, not the right human.

## AI-agent gotchas
- LLMs hallucinate plausible-looking metric values. Force every cell to cite either a query hash + warehouse + as_of, or a verifiable dashboard URL — and have a verifier agent re-run the query.
- Agents will collapse different metric definitions ("conversion", "checkout completion", "purchase rate") into one value. Resolve names against a metric layer; refuse to score a requirement whose KPI name isn't in the catalog.
- Agents over-fit to whichever segment has the largest sample and silently drop low-volume but high-revenue cohorts (enterprise tier). Require the requirement to either segment explicitly or justify the aggregate.
- Date drift: an agent that fetched a baseline yesterday will reuse it forever unless `as_of` is enforced. Add an automated "is this older than max_age_days" gate at requirement-finalization time.
- Vanity-metric capture: agents pick the metric that's easiest to query (page views) over the metric that matters (paid retention). Constrain the schema to require a downstream business KPI per requirement.
- Causal claims: agents will write "feature X drove +12% retention" from correlational data. Force a `causal_evidence_type ∈ {experiment, quasi-experiment, correlational}` field; correlational claims must caveat in the requirement statement.
- Multi-comparison inflation: an agent that ran 17 segment cuts and reports the one with p < 0.05 is doing p-hacking. Require the segments to be pre-specified or the alpha to be Bonferroni/BH-adjusted.
- Privacy leak: agents may pull PII columns into evidence. Restrict warehouse roles, and have a redaction-checker agent scan evidence blobs for emails, phone numbers, and customer IDs before commit.
- Anchoring on the proposer's hypothesis: agents are sycophantic and will find data supporting whatever the question implies. Add a counter-evidence pass: "find the strongest signal that this requirement should NOT be built."
- Human-in-the-loop checkpoints: (a) business question framing, (b) target value (ambition), (c) experiment go/no-go after baseline read, (d) post-experiment ship/rollback. Agent-only flow on any of these will eventually ship the wrong thing confidently.

## References
- Davenport & Harris — *Competing on Analytics* (canonical case for analytics-first decision-making in product orgs).
- Kohavi, Tang, Xu — *Trustworthy Online Controlled Experiments* (Microsoft / Airbnb experimentation playbook; gold standard for A/B rigor).
- Croll & Yoskovitz — *Lean Analytics* (one-metric-that-matters, stage-appropriate KPIs).
- BABOK Guide v3 — Strategy Analysis (§6) and Solution Evaluation (§8); industry-standard alignment between BA work and measured outcomes.
- DAMA-DMBOK 2 — *Data Management Body of Knowledge*; for the data-strategy half of "AI ROI requires data strategy".
- https://exp-platform.com — Microsoft Experimentation Platform research on power, MDE, peeking.
- https://posthog.com/docs/data — PostHog metrics + SQL data layer (OSS reference).
- https://docs.getdbt.com/docs/build/metrics — dbt semantic / metric layer for canonical KPI definitions.
- https://www.evanmiller.org/ab-testing/sample-size.html — practical sample-size calculator + commentary on common A/B mistakes.
