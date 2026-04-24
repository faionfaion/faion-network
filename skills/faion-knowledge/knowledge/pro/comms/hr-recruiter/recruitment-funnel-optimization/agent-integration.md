# Agent Integration — Recruitment Funnel Optimization

How to drive recruitment-funnel-optimization with Claude subagents and ATS / analytics tooling. Pairs with `README.md` (stage benchmarks + dashboard template), `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.

## When to use

- Time-to-fill > 45 days or cost-per-hire > 4k USD with no clear bottleneck owner.
- Offer acceptance < 85% sustained over a quarter (not a single bad month).
- Diagnosing where a hiring slow-down lives (sourcing vs screening vs scheduling vs offer) without ATS dashboards covering all stages.
- Post-merger / ATS-migration baseline so the new platform's metrics aren't compared apples-to-oranges.
- Quarterly TA reviews where leadership wants a single-page funnel narrative grounded in real data.

## When NOT to use

- Volume < 30 applications per role per quarter — you have a sourcing problem, not a funnel problem; conversion math is too noisy.
- Roles with dedicated retainer search (executive search) — funnel mechanics are different and stage definitions don't transfer.
- Crisis hiring (fire / layoff backfill) where speed dominates and optimization burn is misallocated effort.
- One-off seasonal hires; the optimization investment doesn't amortize.

## Where it fails / limitations

- Benchmarks (8-12% application rate, 85-95% offer acceptance) are role-family-specific; LLMs cite them as universal.
- Conversion ratios mask quality of hire — a "tight" funnel may simply be filtering on the wrong criteria.
- Multi-source attribution: the candidate first saw you on LinkedIn, applied via Indeed, was sourced via referral. ATS attribution is single-touch by default and misleads investment decisions.
- Drop-off "root causes" produced by an LLM are pattern-matched ("compensation, speed, role clarity") regardless of actual data; force-feeding evidence is required.
- Survivorship bias: the funnel only reports candidates who applied. The biggest leak (people who *didn't* click apply) is invisible without ad analytics.
- Self-selection: candidate NPS surveys answered by the rejected-and-angry plus the hired-and-thrilled — middles ignored.

## Agentic workflow

Drive funnel optimization as a five-stage pipeline owned by `faion-recruiter-agent`. Stage 1 (data ingestion, sonnet) pulls ATS exports + ad spend + career-page analytics into a unified dataset. Stage 2 (anomaly detection, sonnet) compares this period vs trailing 4 against role-family benchmarks; flags only deltas with p < 0.05 or absolute swing > 5pp. Stage 3 (root-cause hypothesis, opus) — for each flag, generates 2-3 candidate causes with required evidence to confirm. Stage 4 (action recommendations, opus) — only proposes actions whose expected lift is computed against the hypothesis. Stage 5 (A/B plan, sonnet) — converts each action into a measurable test with sample-size math.

### Recommended subagents

- `faion-recruiter-agent` — primary; owns ingestion, anomaly detection, recommendations.
- `faion-research-agent (mode: market)` — competitive comp benchmarking when the leak is offer-stage.
- `faion-employer-brand-agent` — owns top-of-funnel actions (career page, employer-brand content).
- `general-purpose` reviewer (sonnet, fresh context) — challenges root-cause logic; rejects unfalsifiable hypotheses.

### Prompt pattern

Anomaly detection:
```
Inputs: this-period funnel JSON + trailing-4-period funnel JSON + role-family benchmarks (attached). For each stage, compute conversion + 4-period rolling mean + 95% CI. Flag only stages where this period is outside CI OR moves >5pp absolute. Output JSON of flags with stage, this_value, baseline, delta, direction. No interpretation.
```

Root-cause hypothesis:
```
For each flag in the input: produce 2-3 hypotheses ranked by likelihood. For each hypothesis: required evidence to confirm + required evidence to falsify + the cheapest data source. Do not recommend actions yet. Refuse to invent numbers.
```

A/B plan:
```
Convert each accepted action into an experiment: hypothesis, primary metric, secondary, MDE, sample-size n per arm at 80% power, randomization unit, duration estimate, kill switches. Output one row per action.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` + GitHub Pages / `markdown-it` | Version-control funnel reports as artefacts | cli.github.com |
| Greenhouse Harvest API | Stage-by-stage candidate exports | developers.greenhouse.io |
| Lever API v1 | Same for Lever | hire.lever.co/developer/documentation |
| Ashby API | Stage transitions with timestamps | developers.ashbyhq.com |
| `pandas` + `numpy` + `scipy.stats` | Conversion tests, CI math | pypi |
| `dbt` + `duckdb` | Light warehousing if pulling multiple ATSes | getdbt.com, duckdb.org |
| `metabase` (CLI / API) | Dashboards over the warehoused funnel | metabase.com |
| Google Analytics 4 / `bq` | Career-page top-of-funnel | developers.google.com/analytics |
| LinkedIn Recruiter API / Talent Insights | Source-effectiveness | learn.microsoft.com/linkedin/talent |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Greenhouse | SaaS ATS | Yes (Harvest REST + webhooks) | Strongest stage-transition logging. |
| Lever | SaaS ATS | Yes | Funnel reports out-of-box. |
| Ashby | SaaS ATS | Yes | Built-in funnel analytics; cleanest API. |
| Workable | SaaS ATS | Yes | SMB-friendly funnel views. |
| iCIMS / Workday | SaaS ATS (enterprise) | Partial | Heavy APIs; rate-limited. |
| Datapeople / Beamery | SaaS analytics | Yes (REST) | TA-specific funnel BI. |
| Gem / SeekOut | SaaS sourcing | Yes (REST) | Top-of-funnel sourcing intelligence. |
| Eightfold | SaaS AI | Yes (REST) | AI matching; bias audits required. |
| LinkedIn Talent Insights | SaaS | Limited (UI-heavy) | Market supply/demand. |
| Glassdoor / Indeed analytics | SaaS | Yes | Career-page traffic + apply rate. |
| Calendly / GoodTime | SaaS | Yes (REST) | Scheduling-stage data. |
| BrightHire | SaaS | Yes | Interview-stage drop-off + reason coding. |

## Templates & scripts

See `templates.md` for funnel dashboard, stage optimization checklist, drop-off analysis. `README.md` already includes a worked example of "diagnosing low offer acceptance".

Inline helper — funnel anomaly detector (deterministic gate before LLM root-cause):

```python
# funnel_anomaly.py — flag stages outside trailing-period CI
import sys, json, statistics, math

def ci95(xs):
    if len(xs) < 2: return (None, None)
    m = statistics.mean(xs); s = statistics.stdev(xs); n = len(xs)
    half = 1.96 * s / math.sqrt(n)
    return (m - half, m + half)

def flag(this_period, history):
    flags = []
    for stage, val in this_period.items():
        hist = [p[stage] for p in history if stage in p]
        lo, hi = ci95(hist)
        if lo is None: continue
        baseline = statistics.mean(hist)
        outside_ci = val < lo or val > hi
        big_swing = abs(val - baseline) >= 0.05
        if outside_ci or big_swing:
            flags.append({"stage": stage, "value": val, "baseline": round(baseline, 3),
                           "ci": [round(lo, 3), round(hi, 3)],
                           "delta": round(val - baseline, 3),
                           "direction": "down" if val < baseline else "up"})
    return flags

if __name__ == "__main__":
    data = json.load(sys.stdin)  # {"this": {stage: rate}, "history": [{stage: rate}, ...]}
    json.dump(flag(data["this"], data["history"]), sys.stdout, indent=2)
```

Pipe ATS export JSON in → only flagged stages get LLM root-cause analysis. Saves ~70% tokens vs sending the whole funnel.

## Best practices

- Segment funnel by role family (eng, sales, GA), level, and source. A blended funnel hides everything that matters.
- Always plot quality-of-hire (12-month performance) alongside conversion. Volume optimization at the cost of quality is a regression.
- Tag every reject reason at every stage with a controlled vocabulary (15-20 codes max). Free-text reasons are agent-uncodable in practice.
- Track time-in-stage, not just conversion. A 90% screen-to-interview that takes 21 days is worse than 70% in 4 days.
- Run a candidate experience survey at offer-decline and at hire — short, NPS plus 2 free-text. Sub-8-question surveys finish.
- For the 4 weeks after any process change, treat metrics as unstable. Pre-register the change and the expected lift in a doc the agent can later check.
- Compensation: keep a market-data refresh (Levels.fyi / Radford / Mercer) on a quarterly cadence. Offer-stage leaks are usually 6+ months stale data.
- Speed: time from final-interview to offer is the highest-leverage variable in offer acceptance for senior roles.
- Onboarding 90-day retention belongs in the funnel; if you optimize through offer-acceptance you're optimizing the wrong objective.

## AI-agent gotchas

- LLMs cite "industry benchmarks" with confidence regardless of role, geo, or level. Always pin the benchmark source in the prompt; reject any unsourced number in output.
- Agents will "explain" any drop-off with a comp/speed/clarity narrative. Force evidence-required prompting; reject unsupported narratives in review.
- Funnel data has stage-name drift across ATSes ("Phone Screen" vs "Recruiter Screen" vs "Initial"). Pre-normalize with a mapping file or the LLM will count duplicates as separate stages.
- Drop-off attribution is multi-causal; agents will pick a single cause. Require ranked hypotheses with evidence requirements, never one root cause.
- An agent computing CI on weekly samples without checking n will report "significant" deltas at n=4. Block if n < 8 per group.
- Action recommendations from LLMs default to "improve communication" and "review compensation" — both unmeasurable. Force every action into an A/B-testable form.
- Mandatory human-in-loop: (1) sign-off on the stage taxonomy, (2) approval of any compensation-band action (legal, equity, payroll cascade), (3) any change to JD or sourcing channel mix that touches budget.
- Career-page A/B tests must respect existing analytics consent banner; agents that auto-launch experiments without reading the privacy posture create GDPR liability.

## References

- LinkedIn Talent Solutions — "Recruiting Metrics That Matter".
- Greenhouse — "Recruiting Analytics" guide (greenhouse.com/blog/recruiting-analytics).
- SHRM — "Talent Acquisition Metrics" toolkit.
- Bersin / Deloitte — "High-Impact Talent Acquisition" research.
- Schmidt & Hunter (1998) — for quality-of-hire validity baseline.
- Datapeople reports — JD language and apply-rate effects (datapeople.io/research).
- Internal: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/recruiting-process/agent-integration.md`.
- Internal: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/retention-compliance/agent-integration.md`.
