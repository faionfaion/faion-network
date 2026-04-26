# Agent Integration — Solution Assessment (ba-core)

This integration takes the BABOK ba-core angle: Solution Evaluation as a knowledge
area, the canonical evaluation dimensions, and the pre-/post-launch fundamentals.
The companion `business-analyst/solution-assessment/agent-integration.md` covers
the full four-pass evidence pipeline; this file stays at the fundamentals layer
that any BA workflow can reuse.

## When to use
- Stage-gate of a BABOK Solution Evaluation knowledge area: when you need a
  documented answer to "does the solution deliver enterprise value?" against
  the original business need, not just against the spec.
- Design and Implementation Assessments inside the build phase, where the
  question is "are we still on the right path?" before any go-live signal exists.
  The ba-core templates are the lowest-overhead artifact for that question.
- Pre go-live deployment readiness review where multiple workstreams (QA,
  training, ops, support, security) must be reduced to one accept/reject row.
- 30 / 90 / 365-day post-implementation reviews where the BA is asked to score
  requirements compliance + benefit realization in a single report.
- Solution Limitations capture for compliance, audit, or vendor-renewal files —
  even when the solution is "fine", regulators expect a written limitation
  register with workarounds and a recommendation column.
- Lessons-learned input to the next iteration's Strategy Analysis (current state
  ⇒ future state). The Post-Implementation Review template feeds directly into
  the next discovery cycle.

## When NOT to use
- Continuous-discovery / pre-PMF startup work where requirements are still being
  invented every sprint. Run product analytics + retros; "REQ-001 met" is
  meaningless when REQ-001 was wrong.
- Throwaway prototypes, spikes, internal tools used by a handful of people.
  A 15-minute retro and a one-line decision log replace the whole template.
- Pure SRE / platform tuning (latency, cost, capacity). Use SLOs and error
  budgets — Solution Assessment evaluates business outcomes, not p99 graphs.
- When no baseline exists. Without a measured "before" the variance column is
  vibes; either back-fill the baseline first or downgrade scope to qualitative
  observations and label the report accordingly.
- When the assessor reports to the project sponsor whose bonus depends on the
  result. BABOK independence applies; route to a different chain or external
  reviewer.

## Where it fails / limitations
- **No baseline, no verdict.** The Step 3 variance column collapses to
  storytelling. Capture the baseline at requirements freeze, not at assessment
  time, otherwise it becomes a post-hoc rationalization.
- **Requirements drift over the build period.** REQ-014 written 9 months before
  go-live may be stale; scoring it Met / Not Met is the wrong axis. Add a
  fifth status — `deprecated` — explicitly.
- **Variance is correlation, not causation.** Revenue +18% post-launch may
  be the solution, market tailwind, a competitor's outage, or a comp-plan
  change. Without diff-in-diff or a control group, the report should say so.
- **Adoption ≠ value.** 95% adoption looks great, but if mandatory adoption
  replaced a 90%-efficient workflow with a 70%-efficient one, the solution
  destroyed value. Always cross-check adoption against productivity / cycle-time.
- **Survivorship bias in user feedback.** Surveys reach the still-active users.
  n=50 with a 4.2 score can hide 200 silent leavers; reconcile survey n
  against active-user count.
- **Single-snapshot assessments.** 30 days post-launch most users are in
  honeymoon mode; 12 months in the real friction shows. One-shot 30-day
  reports systematically overstate success.
- **Functional-only evaluation.** Listing "REQ-001 Met" without measuring the
  business benefit it was supposed to enable is the most common ba-core failure
  mode (README Common Mistake #3). Functional Met + benefit Not Realized = Not Met.

## Agentic workflow
At ba-core level, Solution Assessment is a five-step linear pipeline matching
the README (Define Criteria → Assess vs Requirements → Evaluate Value →
Identify Limitations → Recommend Actions). Drive it as five short subagent
calls, each emitting a structured fragment that the next step consumes; only
the Recommend step produces prose. The BA subagent stays the orchestrator and
the human signs the cover memo — agents never decide accept/reject alone.

### Recommended subagents
- `faion-improver` — natural home for cron-driven 30 / 60 / 90-day post-launch
  re-assessments; reads the prior report, deltas the metrics, and files the
  next version under `.aidocs/`.
- `faion-sdd-execution` — converts the Step 5 Recommendations list into SDD
  remediation tasks, one task per `Not Met` requirement or `Critical` issue,
  closing the loop back into delivery.
- `faion-feature-executor` — executes the bounded remediation tasks generated
  above (bug fixes, missing features, training rollout) under the
  accept-with-conditions verdict.
- `faion-brainstorm` — when the verdict is `Reject` or limitations are
  systemic, run diverge / converge before committing to a v2 design.

### Prompt pattern
```
You are a BA solution assessor. Inputs:
  assessment_type: design | implementation | deployment | post-implementation
  requirements[]:  [{id, statement, target_status}]
  success_criteria[]: [{name, baseline, target, source}]
  evidence[]:       [{ref, source_url, retrieved_at, sample_size, raw}]
Output JSON exactly matching:
{
  criteria_defined: [{category, criterion, target}],
  requirements_compliance: [
    {req_id, status: met|partial|not_met|deprecated,
     gap, evidence_ref, confidence}
  ],
  business_value: [
    {metric, baseline, target, actual, variance_pct,
     status: on_track|at_risk|off_track|exceeded, sample_size}
  ],
  limitations: [{issue, impact, workaround, severity}],
  recommendation: accept | accept_with_conditions | require_changes | reject,
  actions: {immediate[], short_term[], long_term[]}
}
Reject any field where evidence_ref is missing. Do not invent baselines.
```

```
You are a deployment readiness reviewer. Score each gate (QA, training,
ops, support, security, compliance) as ready | conditional | blocked with
one piece of evidence per gate. Output a single accept/conditional/reject
recommendation. Refuse if any gate has no evidence supplied.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Pull issues, PRs, release notes that feed the issues register | https://cli.github.com |
| `jira-cli` (ankitpokhrel) | Pull Jira tickets / epics for the requirements compliance matrix | https://github.com/ankitpokhrel/jira-cli |
| `linear-cli` | Same for teams on Linear | https://github.com/evangodon/lr |
| `pandoc` | Convert the assessment-report Markdown template to PDF / DOCX for sign-off | https://pandoc.org |
| `csvkit` (csvgrep, csvstat) | Slice survey / ticket exports without spinning up a notebook | https://csvkit.readthedocs.io |
| `duckdb` | One-binary SQL over CSV / Parquet exports for the variance and adoption math | https://duckdb.org |
| `mermaid-cli` (`mmdc`) | Render the assessment-flow / decision diagrams referenced from the report | https://github.com/mermaid-js/mermaid-cli |
| `ruff` (project lint gate) | Required for any helper scripts checked in alongside the report | https://docs.astral.sh/ruff |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira / Confluence (Atlassian) | SaaS | Yes — REST + JQL + OAuth | Source of truth for requirements compliance + the report's home page |
| Linear | SaaS | Yes — GraphQL + API key | Same role for product-led teams |
| GitHub Issues / Projects | SaaS / OSS | Yes — REST + GraphQL via `gh` | Issues register + remediation tracking |
| Mixpanel / Amplitude / PostHog | SaaS / OSS (PostHog self-host) | Yes — Query API | Adoption, feature usage, funnel metrics for Step 3 |
| GA4 + BigQuery export | SaaS | Yes — BigQuery SQL | Public-traffic value metrics |
| Tableau / Power BI / Metabase | SaaS / OSS | Partial — REST exists but data-prep is manual | Render the variance dashboards linked from the report |
| Qualtrics / SurveyMonkey / Typeform | SaaS | Yes — REST | User feedback ratings table; agent must reconcile n vs active users |
| Zendesk / Intercom / Freshdesk | SaaS | Yes — REST | Issues themes via topic clustering of tickets |
| Pendo / WalkMe | SaaS | Partial | Adoption + in-app NPS for usability score |
| Google Forms + Sheets API | SaaS | Yes — REST | Lightweight option for internal solutions |

## Templates & scripts
The README already ships the Solution Assessment Report and Post-Implementation
Review templates. Useful additions for agentic execution:

```bash
#!/usr/bin/env bash
# render-assessment.sh — turn the agent's JSON into the README report template.
# Usage: render-assessment.sh assessment.json report.md
set -euo pipefail
JSON=${1:?json input required}
OUT=${2:?markdown output required}

jq -r '
  "# Solution Assessment Report: \(.solution)\n",
  "**Date:** \(.date)  **Assessor:** \(.assessor)  **Type:** \(.assessment_type)\n",
  "## Requirements Compliance\n",
  "| Req ID | Status | Gap | Confidence |",
  "|---|---|---|---|",
  (.requirements_compliance[] |
     "| \(.req_id) | \(.status) | \(.gap // "-") | \(.confidence) |"),
  "\n## Business Value\n",
  "| Metric | Baseline | Target | Actual | Variance | Status |",
  "|---|---|---|---|---|---|",
  (.business_value[] |
     "| \(.metric) | \(.baseline) | \(.target) | \(.actual) | \(.variance_pct)% | \(.status) |"),
  "\n## Limitations\n",
  "| Issue | Severity | Impact | Workaround |",
  "|---|---|---|---|",
  (.limitations[] |
     "| \(.issue) | \(.severity) | \(.impact) | \(.workaround) |"),
  "\n## Recommendation: \(.recommendation)\n",
  "### Immediate\n", (.actions.immediate[] | "- \(.)"),
  "\n### Short-term\n", (.actions.short_term[] | "- \(.)"),
  "\n### Long-term\n", (.actions.long_term[] | "- \(.)")
' "$JSON" > "$OUT"
echo "wrote $OUT"
```

Pair with `pandoc -s report.md -o report.pdf` for the sign-off PDF.

## Best practices
- Lock metric definitions in the original business case and re-verify them at
  assessment time. Once the team knows the success number, the underlying
  definition will drift to make it land (Goodhart).
- Capture the baseline at requirements freeze. If you wait until assessment
  time, the "baseline" silently becomes "yesterday" and the variance is zero
  by construction.
- Run assessments at multiple horizons (30 / 90 / 365 days). One-shot 30-day
  reports systematically overstate success because users are still in
  honeymoon mode.
- Keep `deprecated` as a first-class requirement status. Forcing every legacy
  requirement into Met / Not Met inflates the Not Met count and wastes
  remediation tokens.
- Pull the issues register from the ticketing system over the full review
  window — never from team memory. Recency bias inflates whatever broke last
  week.
- Score functional + value separately. A solution can be 100% requirements-met
  and 0% value-realized; the report must surface that explicitly.
- Cross-check adoption with productivity. Mandatory rollouts always show
  high adoption; only paired cycle-time / output metrics show whether the
  adoption was beneficial.
- Independence: route the report through someone whose comp does not depend on
  the verdict. This is BABOK-explicit and the most-violated rule in practice.

## AI-agent gotchas
- LLMs will happily fill in `actual` values when evidence is missing. Force the
  prompt to refuse: every row needs an `evidence_ref` that resolves; otherwise
  the row is dropped, not invented.
- "Met / Partial / Not Met" is a four-state space once you add `deprecated`.
  Three-state prompts will silently miscategorize stale requirements as
  Not Met and inflate the remediation backlog.
- Survey-based satisfaction scores are mean-of-the-still-active. The agent must
  receive the active-user count alongside the survey n and refuse to compute
  satisfaction when n / active-users < a documented threshold (e.g., 10%).
- Variance is not causation. Prompt the agent to flag any metric where an
  obvious external factor (market move, comp change, competitor outage)
  overlapped the assessment window — and to mark `confidence: low`.
- Recommendation prose tends to hedge ("consider exploring"). Force a single
  enum value (`accept | accept_with_conditions | require_changes | reject`) and
  generate prose only as a derived field bound to that enum.
- Long evidence chains explode token budgets. Pre-summarize each evidence
  source to ≤ 200 tokens before the verdict pass; keep the raw URLs as
  references, not as inline payloads.
- Human-in-the-loop checkpoints: (a) sign-off on the criteria list before
  Step 2 runs, (b) review of `not_met` and `deprecated` rulings before
  recommendations are drafted, (c) human signature on the final
  accept / reject verdict. Agents never sign.

## References
- BABOK Guide v3 — Knowledge Area 6: Solution Evaluation
- IIBA — Measuring the Value of Business Analysis
- Kaplan & Norton — The Balanced Scorecard (evaluation dimensions)
- Goodhart, C. — "Goodhart's Law" (1975) on KPI gaming
- Companion file: `../../business-analyst/solution-assessment/agent-integration.md`
  for the four-pass evidence pipeline angle
