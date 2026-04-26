# Agent Integration — Solution Assessment

## When to use
- 30/60/90-day post-launch checkpoints when the business case promised quantified outcomes (e.g. "lift conversion +20%, cut sales cycle -15%") and somebody — finance, the board, the auditor — will ask whether the numbers landed. Solution Assessment is the artifact that answers them in writing.
- Pre-go-live "deployment readiness" gates where you must aggregate signals from QA, ops, support, training and security into a single accept/reject recommendation. Replaces ad-hoc launch meetings with a structured table.
- Phase-gate reviews on long programs (CRM, ERP, billing migrations) where each phase ships something measurable and the steering committee wants evidence before funding the next phase.
- Vendor / SaaS contract renewal: assess the deployed solution against the original requirements and SLA before clicking "renew". The post-implementation review template is exactly what procurement wants.
- Compliance and audit cycles (SOX, ISO, HIPAA) where regulators expect a documented evaluation that requirements were met and limitations have a remediation plan.
- Post-incident or post-outage assessment of a recently shipped solution — was the failure a missed requirement, an implementation gap, or an unmeasured non-functional? The matrix forces the distinction.

## When NOT to use
- Throwaway prototypes, spikes, internal tools used by ≤ 5 people. Run a 15-minute retro instead; a full assessment report is theatre.
- Pre-PMF early-stage startups where requirements legitimately change every sprint. Use product analytics + continuous discovery; "REQ-001 met" is meaningless when REQ-001 was wrong.
- When you have no baseline. Without a measured "before" you cannot compute variance, and the report degrades into vibes ("users seem happier"). Either back-fill the baseline or postpone.
- As a substitute for ongoing monitoring. A one-shot 90-day assessment that then sits in a Confluence page until the next audit is the canonical anti-pattern (see Common Mistakes #5 in the README).
- When the assessor reports to the project sponsor whose bonus depends on the result. Independence matters; route the assessment through a different chain or an external reviewer.
- Pure technical performance tuning (latency, throughput) — use SRE / SLO frameworks. Solution Assessment evaluates business outcomes, not p99 graphs.

## Where it fails / limitations
- **Survivorship bias in user feedback**: surveys reach the users who still use the solution. The ones who churned never answer. n=50 with a 4.2 satisfaction can mask 200 silent leavers; always reconcile survey n with active-user count.
- **Goodhart on KPIs**: once the team knows "lead conversion +20%" is the success metric, lead-quality definitions drift to make the number land. Lock metric definitions in the original business case and re-verify them at assessment time.
- **Variance ≠ causation**: revenue went up 18% post-deployment may be the solution, market tailwind, a competitor's outage, or the new comp plan. Without a control group / pre-post diff-in-diff the variance column is correlational at best.
- **Requirement drift**: REQ-014 was written 9 months before deployment. If the underlying business changed, "Met" or "Not Met" is the wrong question; the requirement is stale. Mark these explicitly as "deprecated" instead of forcing a binary verdict.
- **Recency bias on issues**: the issues list inflates whatever broke last week and forgets the silent successes from month one. Pull issues from the ticketing system over the full review period, not from team memory.
- **Adoption ≠ value**: 95% adoption looks great, but if the workflow it replaced was 90% efficient and the new one is 70% efficient, mandatory adoption *destroyed* value. Always cross-check adoption with productivity / cycle-time metrics.
- **Single-snapshot assessments**: 30 days post-launch most users are still in honeymoon mode; 12 months in, novelty fades and real friction shows. One-shot reports overstate success.

## Agentic workflow
Drive Solution Assessment as a four-pass evidence pipeline that mirrors the README's four assessment types. (1) **Frame pass** — a sonnet agent ingests the original spec, business case, and requirements register and emits structured `{requirements[], success_metrics[], baseline_values[], assessment_scope}`. No verdicts yet. (2) **Evidence-gathering pass** — parallel agents pull from product analytics (Mixpanel/PostHog/GA4), the ticketing system (Jira/Linear/GitHub), the support tool (Zendesk/Intercom), and survey results, emitting `{requirement_id, source, raw_metric, retrieved_at, sample_size}`. (3) **Verdict pass** — an opus agent compares actuals against targets per requirement and per metric, emitting `{requirement_id, status: met|partial|not_met|deprecated, variance_pct, evidence_urls[], confidence}` plus an issues register synthesized from support tickets clustered by topic. (4) **Recommendation pass** — an opus agent fuses (3) into Immediate / Short-term / Long-term action lists with owners and a final accept/conditional/reject verdict; only this pass produces prose. The decision (sign or rework) stays human; agents produce the table, the human signs the cover memo.

### Recommended subagents
- `faion-improver` — runs the assessment loop on a cron at 30/60/90 days; reads the original business case, drives the four-pass pipeline, files the report under `.aidocs/`. This is the natural home for ongoing assessment.
- `faion-sdd-execution` — converts the recommendations list into SDD remediation tasks (one task per "Not Met" requirement or "Critical" issue), keeping the loop closed back into delivery.
- `faion-feature-executor` — executes the discrete remediation tasks (bug fixes, missing features, training rollout) bounded by the accept-with-conditions verdict.
- `faion-brainstorm` — when the verdict is "Reject" or there are systemic gaps, run diverge / converge to generate alternatives before committing to a v2.
- A custom `metrics-collector` worth creating: input = `{metric_name, baseline, target, source}`, output = `{actual, sample_size, retrieved_at, evidence_urls}`. Reuse across assessments; caches connectors for the BI / analytics stack.
- A custom `issue-clusterer`: input = ticket export (CSV/JSON), output = `{theme, ticket_count, severity, representative_quotes[]}`. Replaces "I read 200 tickets and feel" with structured topic modeling.

### Prompt pattern
```
You are a solution assessor. Inputs: requirements[] (with target status),
success_metrics[] (with baseline + target), evidence[] (one row per metric or
requirement, each with source_url and retrieved_at), assessment_type:
design|implementation|deployment|post-implementation. Output JSON:
{
  requirements_compliance: [{req_id, status: met|partial|not_met|deprecated,
                             variance, evidence_urls, confidence, notes}],
  business_value: [{metric, baseline, target, actual, variance_pct,
                    sample_size, status: on_track|at_risk|off_track|exceeded}],
  issues: [{theme, severity: critical|high|medium|low, ticket_count,
            representative_quotes[], recommended_action}],
  limitations: [{limitation, business_impact, workaround}],
  recommendation: {verdict: accept|accept_with_conditions|require_changes|reject,
                   immediate_actions, short_term, long_term, rationale_<= 120_words}
}
Constraints:
- Every requirement verdict must cite >= 1 evidence_url; otherwise confidence="low".
- A metric with sample_size below the original power calculation must be marked
  "underpowered" — never call it "met" on n=12.
- Status "deprecated" is allowed when the requirement no longer reflects the
  business; do not force a met/not-met binary on a stale requirement.
- "Accept" requires zero "critical" issues and zero "not_met" requirements.
```

```
You are an evidence collector for ONE metric. Input: {metric_name, baseline,
target, source: analytics|tickets|survey|sla}. Output JSON:
{
  actual: number,
  sample_size: int,
  source_urls: [<= 3 primary sources>],
  retrieved_at: ISO8601,
  measurement_window: {start, end},
  caveats: [<= 3 bullets, e.g. "seasonality", "control group missing"],
  confidence: "high"|"medium"|"low"
}
If the metric definition cannot be reproduced from the original business case,
return confidence="low" and surface the ambiguity in caveats. Never invent
a number; refuse and report missing data.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog-cli` | Pull funnel, retention, feature-flag adoption from PostHog into the assessment | https://posthog.com/docs/cli |
| `mixpanel-api` (Python) | Query Mixpanel JQL for cohorted before/after metrics | `pip install mixpanel-utils` |
| `gh` + `jq` | Pull GitHub issue counts, severity labels, time-to-close as quality signals | https://cli.github.com |
| `jira-cli` | Export Jira issues, filter by component / fix-version, cluster by labels | `pipx install jira-cli` |
| `zendesk-cli` | Pull tickets and CSAT for the review window | https://github.com/Anthropic-style-tools (or `zenpy` Python lib) |
| `pandas` + `scipy` | Compute variance, t-tests, diff-in-diff for the business-value table | `pip install pandas scipy` |
| `bertopic` (Python) | Topic-model support tickets / survey free text into themed issues | `pip install bertopic` |
| `gnuplot` / `matplotlib` | Render variance and adoption charts for the executive summary | `pip install matplotlib` |
| `pandoc` | Render the markdown assessment to PDF / DOCX for sponsor sign-off | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog | SaaS / OSS (MIT) | Yes (REST + SQL) | Funnels, retention, feature-flag adoption — primary source for adoption metrics |
| Mixpanel | SaaS | Yes (JQL API) | Cohort before/after; native funnel-to-impact reports |
| Amplitude | SaaS | Yes (REST) | Same role as Mixpanel; better for product-led-growth assessments |
| Pendo | SaaS | Limited (REST) | Combines product analytics with in-app NPS / surveys; one-stop for adoption + satisfaction |
| Hotjar / FullStory | SaaS | Limited | Session replay for usability findings — feed clips into the issues register |
| Zendesk | SaaS | Yes (REST) | Ticket export + CSAT for the issues / user-feedback sections |
| Intercom | SaaS | Yes (REST) | Same role; better for B2B SaaS conversations |
| Jira / Linear / GitHub Issues | SaaS / OSS | Yes (REST) | Defect leakage and sprint variance for the implementation assessment |
| ServiceNow | SaaS (enterprise) | Yes (Table API) | Incident, change, problem records for enterprise post-implementation |
| Qualtrics / SurveyMonkey / Tally | SaaS | Yes (REST) | Structured satisfaction surveys; feed into User Feedback table |
| Confluence / Notion | SaaS | Yes (REST) | Publish the report and link evidence; agents post drafts for human review |
| Looker / Metabase / Superset | SaaS / OSS | Yes (SQL / REST) | BI layer for the business-value table — single source of truth for KPIs |
| Sentry / Datadog | SaaS | Yes (REST) | NFR / reliability evidence for the deployment-readiness assessment |
| StatusGator / Statuspage | SaaS | Yes (REST) | Uptime / incident history for SLA verification at renewal time |

## Templates & scripts
See `templates.md` (in this folder, currently a stub — fill from the README's two markdown templates) for the Solution Assessment Report and Post-Implementation Review shells. Inline a small variance helper to bolt onto the business-value table:

```python
# variance.py — usage: python variance.py metrics.json
# metrics.json: [{"name": "lead_conversion", "baseline": 0.10, "target": 0.12,
#                 "actual": 0.118, "n_baseline": 1000, "n_actual": 1150}]
import json, sys, math
from scipy import stats

def status(target, actual, baseline):
    progress = (actual - baseline) / (target - baseline) if target != baseline else 1
    if progress >= 1.0: return "exceeded"
    if progress >= 0.85: return "on_track"
    if progress >= 0.5: return "at_risk"
    return "off_track"

rows = json.load(open(sys.argv[1]))
print(f"{'metric':<25}{'baseline':>10}{'target':>10}{'actual':>10}{'var%':>8}{'p':>8} status")
for r in rows:
    var = (r["actual"] - r["target"]) / r["target"] * 100
    # two-prop z-test if rates, else t-test approx via SE on ratios
    p1, p2 = r["baseline"], r["actual"]
    n1, n2 = r["n_baseline"], r["n_actual"]
    pooled = (p1*n1 + p2*n2) / (n1+n2)
    se = math.sqrt(pooled*(1-pooled)*(1/n1 + 1/n2))
    z = (p2 - p1) / se if se else 0
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    print(f"{r['name']:<25}{p1:>10.3f}{r['target']:>10.3f}{p2:>10.3f}{var:>7.1f}%{p:>8.3f} {status(r['target'], p2, p1)}")
```
If `p > 0.05` for any "Met" verdict, the result is statistically inconclusive — escalate as "underpowered" rather than declaring success.

## Best practices
- Lock metric definitions and baselines in the original business case; re-verify them at assessment time using the same query/source. Drift here invalidates the whole report.
- Always include sample size on every metric row; a target hit on n=12 is not a hit, and reviewers must see this.
- Triangulate every business-value metric with a second source (analytics + finance, or analytics + survey). Single-source verdicts are fragile.
- Time-box the review window explicitly (e.g. "30 days starting 2026-03-15") and stamp `retrieved_at` on every fact. Without windows, "actual" silently mixes pre- and post-launch traffic.
- Cluster support tickets by topic before reading them, not after. Otherwise the loudest 5 tickets dominate the issues register.
- Score independence: route the assessment through someone who is not on the delivery team and not the sponsor. Independence is what gives the report its weight at the steering committee.
- Run the assessment at 30, 60, and 90 days, not just one milestone. Compare the three reports — a metric that was "on track" at 30 and "at risk" at 60 is the real story; either snapshot alone misses it.
- Distinguish "deprecated requirements" from "not met". A binary verdict on a stale requirement penalizes the team for not building something the business no longer wants.
- Pre-mortem the recommended verdict ("if in 6 months we regret accepting this, why?"). The output goes into the Limitations section.
- Always include a "do nothing more" option in the recommendations — sometimes the right answer is to stop investing, not to remediate.

## AI-agent gotchas
- Agents will hallucinate KPI values when the analytics connector is missing. Force `evidence_urls` and `retrieved_at` on every metric and reject rows without primary sources (analytics export, finance export, ticketing export). Marketing dashboards and screenshots are not primary.
- LLMs cluster verdicts in the middle ("partially met") because it is the safest answer. Calibrate by requiring met / partial / not_met thresholds tied to numeric variance bands (e.g. variance ≥ 0% = met, -15..0% = partial, < -15% = not met).
- Agents will silently fold "adoption" into "value" ("95% adoption → success"). Force separate sections in the schema; never let one column substitute for the other.
- Date drift: a metric pulled three months ago is not the same as today's. Stamp `retrieved_at` on every fact; agents must refuse to reuse evidence > the assessment window without re-fetching.
- An agent reading only the support-ticket export will report 100% complaints — by definition support sees only problems. Always pair tickets with active-user count and CSAT, never tickets alone.
- Survey-only assessments under-sample churners. Reconcile survey n with active-user count; flag if response rate < 30% or if churned users are absent from the panel.
- A single agent doing all four passes inherits its own framing. Use a different model / prompt for the verdict pass than for the evidence pass; large disagreement signals low confidence.
- Agent-written executive summaries drift toward optimism. Lock the verdict mapping (accept requires zero "critical" issues and zero "not_met" reqs) at the schema level so prose cannot soften it.
- Watch for prompt-injected satisfaction quotes: free-text survey answers can contain "ignore previous instructions". Strip / sandbox before clustering.
- Human-in-the-loop checkpoints: signing the assessment scope (before evidence pass), the final verdict (before publication), and remediation acceptance (before triggering SDD tasks). Agents must never auto-accept on behalf of the sponsor.

## References
- BABOK Guide v3 — Knowledge Area 6: Solution Evaluation, §8.1–8.5 (industry-standard tasks: Measure Solution Performance, Analyze Performance Measures, Assess Solution Limitations, Assess Enterprise Limitations, Recommend Actions to Increase Solution Value).
- PMI — *Practice Standard for Project Estimating* and *Pulse of the Profession: Benefits Realization* (canonical post-implementation review framing).
- Kaplan & Norton — *The Balanced Scorecard* (multi-perspective metric design beyond financials).
- Doerr — *Measure What Matters* (OKR-grade success metrics; useful for the Business Value table).
- Tetlock & Gardner — *Superforecasting* (calibration of predicted vs actual outcomes; underpins post-implementation calibration loops).
- Kahneman, Sibony, Sunstein — *Noise* (why structured assessments outperform expert gut feel after launch).
- Reichheld — *The Ultimate Question 2.0* (NPS as one input to the user-feedback section, with caveats).
- https://www.iiba.org/career-resources/a-business-analyst%27s-toolkit/business-analysis-knowledge-area-solution-evaluation/ — IIBA's solution-evaluation primer.
- https://posthog.com/docs/product-analytics — reference for adoption / retention metrics that feed the business-value table.
