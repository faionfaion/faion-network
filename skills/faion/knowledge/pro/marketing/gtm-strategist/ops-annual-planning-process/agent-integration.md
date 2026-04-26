# Agent Integration — Annual Planning Process

## When to use
- Driving the year-end planning ritual: pull metrics from the past year, generate the year-in-review, surface candidate priorities, and structure the planning doc.
- Maintaining quarterly OKR drafts: agent proposes KRs based on the annual goal + current trajectory; humans choose and lock.
- Running monthly check-ins as scheduled prompts: agent reads dashboards, summarizes drift vs goal, queues a 30-min review with concrete questions.
- Decomposing a quarterly goal into a monthly+weekly task tree, slotting tasks into the project tracker (Linear / Todoist / Notion / GitHub).
- Producing the quarterly review packet: actuals vs targets, win/loss themes from CRM notes, suggested adjustments to annual plan.

## When NOT to use
- Setting the founder's vision. Vision-setting is a deeply human act; agents produce regression-to-mean prose. Founders write vision; agents critique and operationalize.
- Strategic pivots based on new market signal or single-customer breakthrough — qualitative, narrative, requires founder ownership.
- Personal goals (energy, satisfaction, burnout). Agents have no telemetry on these and should not propose them.
- Salary, equity, or capital-allocation decisions inside the plan. Treat as financial planning under separate human-only governance.

## Where it fails / limitations
- LLM-generated OKRs are vague ("improve customer experience") and uncalibrated. Without explicit targets + measurement plan, they are decoration.
- Year-in-review summaries selectively pick wins, mirror founder bias, and miss negative signals (rising churn, declining cohort retention).
- Cascading goals (annual → quarterly → monthly → weekly) becomes a rigid Gantt chart that ignores Q1 learnings affecting Q3-4. The methodology says "build in flexibility" — agents tend to over-specify.
- Prioritization to ≤3 priorities is hard for LLMs — they list 7. Force-rank constraint must be enforced in prompts.
- Cadence drift: monthly check-ins skip, quarterly reviews compress into Slack messages. Agent reminders help; agent decisions don't.
- Metric definitions drift over the year (what counted as a "customer" in Jan ≠ Dec). Goal tracking against shifting denominators is misleading.

## Agentic workflow
A cron-driven planning subagent runs: (1) annually in early December — pulls full-year metrics, drafts year-in-review, opens a planning doc with template; (2) quarterly — produces a review packet 1 week before quarter-end; (3) monthly — runs a 30-min check-in script with goal-progress diff; (4) weekly — prepares a "this week vs this quarter" snapshot. Each output is a draft for human review, never an autonomous decision. A separate "guardrail" pass red-teams the plan: flags too-many-priorities, missing kill-switches, undefined metrics.

### Recommended subagents
- `faion-growth-agent` (methodology frontmatter) — operational owner of the planning doc, dashboards, cadence triggers.
- `faion-sdd-executor-agent` — runs annual planning as an SDD feature: spec (vision), design (priorities + cadence), test-plan (KRs and how measured), implementation-plan (quarter-month decomposition with token budgets).
- `faion-brainstorm` — diverges on possible priorities + risks before convergence; useful pre-Q1 + at any quarterly review.
- `faion-improver` — runs the December reflection session as an audit-improve loop, pulling patterns from the year's mistakes / decisions logs.

### Prompt pattern
```
Goal: produce year-in-review draft for [Year].
Inputs: monthly metric exports (revenue, customers, churn, MRR, ARPU); CRM win/loss notes; sprint retros.
Method: compute YoY deltas; surface 3 wins, 3 challenges, 3 surprises with CITED data; flag any metric definition that changed mid-year.
Constraints: no more than 1 page; every claim sourced; mark "ASSUMPTION" when data missing.
```

```
Goal: red-team annual plan v1.
Method: enumerate 5 ways this plan fails by Q3. For each, name the leading indicator, the kill-switch, and the alternative.
Refuse: if priorities > 3, refuse and ask user to drop one; do not silently accept.
Output: risk register; do not edit the plan.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `notion-sdk-py` / `notion-cli` | Read/write planning doc + OKR DB in Notion | https://developers.notion.com |
| `linear-sdk` | Cycle planning, projects, milestones | https://developers.linear.app |
| `gh` | GitHub Projects + milestones if planning lives in repo | https://cli.github.com |
| `metabase-api` / `evidence` | Pull dashboard data for review packets | https://www.metabase.com/docs |
| `dbt` | Define metric layer (semantic layer) so definitions don't drift | https://docs.getdbt.com |
| `cube.dev` | Headless metric API for OKR scoring | https://cube.dev/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion | SaaS | Yes (API) | Common home for V/TO + OKRs. |
| Linear | SaaS | Yes (API) | Cycles + projects map cleanly to quarter+month. |
| Lattice / 15Five / Mooncamp | SaaS OKR | Yes | Purpose-built OKR tooling with API. |
| Tability / Weekdone | SaaS OKR | Yes | Lightweight OKR tracking. |
| Mixpanel / Amplitude / PostHog | SaaS analytics | Yes | Source-of-truth for product KRs. |
| Stripe / ChartMogul / ProfitWell | SaaS | Yes | Source-of-truth for revenue KRs. |
| EOS Worldwide V/TO templates | Template | N/A | Methodology framework reference. |
| Reclaim / Motion / Sunsama | SaaS | Yes | Auto-scheduling weekly tasks aligned to goals. |

## Templates & scripts
Inline: monthly check-in packet. Reads metrics, computes drift vs quarterly target, lists actions due.

```python
from datetime import date

def monthly_checkin(quarter_targets: dict, actuals: dict, today: date) -> dict:
    items = []
    quarter_progress = (today.month - 1) % 3 / 3 + (today.day / 30) / 3
    for kr, target in quarter_targets.items():
        actual = actuals.get(kr, 0)
        expected = target * quarter_progress
        delta = actual - expected
        status = "on_track" if delta >= -0.05 * target else ("at_risk" if delta >= -0.15 * target else "off_track")
        items.append({"kr": kr, "actual": actual, "expected": expected, "target": target, "status": status})
    return {
        "as_of": today.isoformat(),
        "quarter_progress_pct": round(quarter_progress * 100, 1),
        "items": items,
        "off_track": [i["kr"] for i in items if i["status"] == "off_track"],
    }
```

See `templates.md` for the OKR template, year-review template, and quarterly cadence checklist.

## Best practices
- Lock the metric layer (dbt / Cube semantic layer / spreadsheet of definitions) at the start of the year. Goal scoring fails when definitions drift.
- Cap priorities to ≤3 annual, ≤3 per quarter. Codify the limit in the planning prompt.
- Pair every KR with a kill-switch (when do we stop?) and a leading indicator (what changes first if we are wrong?).
- Schedule reviews on the calendar before the year starts; agent can hold the slot but humans must show up.
- Keep the annual doc a living artifact: monthly delta entries instead of rewrites. History is the asset.
- Separate quantitative goals (revenue, customers) from systems goals (e.g. "launch retention dashboard") — methodology blends them; agents should tag.
- Always include a "stop doing" list. The methodology's "what should you stop doing?" is the easiest to skip; force the agent to surface candidates.

## AI-agent gotchas
- LLMs auto-hedge: "increase revenue meaningfully". Force quantification (number + unit + date) or reject the KR.
- Year-in-review pulls survivorship bias — winners loud, losers buried. Always include lost-deal + churned-customer themes.
- Cascading too far. Daily tasks generated by an LLM in January are stale by March. Cascade only to month; let weekly/daily emerge.
- "Stretch goals" become anchors; teams hit ~70% of stretch and feel like they failed. Use 1.0 = ambitious-but-credible, not 0.7.
- Multi-year compounding: agent sets unrealistic Y2/Y3 trajectory based on Y1 outlier. Check growth assumptions against industry benchmarks (OpenView SaaS, Bessemer Cloud Index).
- Calendar-driven reminders work; calendar-driven decisions don't. Agent should never skip a human review even if metrics look fine.
- Be wary of the agent generating "vision" prose — it converges on bland mission-statement style. Vision is a founder artifact; agent is editor not author.
- Don't let agent close objectives early. Closure is a human decision tied to evidence + retro; auto-closing on metric hit hides drift in inputs.

## References
- *Traction* by Gino Wickman + EOS V/TO: https://www.eosworldwide.com/vision-traction-organizer
- *Measure What Matters* — John Doerr (OKRs)
- *Good Strategy Bad Strategy* — Richard Rumelt
- *Scaling Up* — Verne Harnish
- WhatMatters OKR guide: https://www.whatmatters.com/resources/okrs-ultimate-guide
- *The Great CEO Within* — Matt Mochary (operating cadence)
- High Output Management — Andy Grove (review rhythm)
