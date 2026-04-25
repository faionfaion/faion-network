# Agent Integration — Annual Planning Templates

## When to use
- End-of-year planning cycle: produce annual plan, OKRs, quarterly breakdown, budget table.
- Quarterly/monthly review cycles: assemble results-vs-goals, wins, misses, learnings into the standard template.
- Generating a year-in-review artifact for personal reflection or stakeholder communication.
- Aligning multiple workstreams (product, marketing, ops) onto shared OKRs with consistent format.
- Scaffolding a planning document for a brainstorm session — agent fills the template skeleton, human fills the strategic content.

## When NOT to use
- Strategic ideation phase — the templates assume strategy already exists; for upstream brainstorming use `faion-brainstorm`.
- Daily / weekly task management — overkill; use Linear/Asana/Notion native tooling.
- Detailed financial modeling — use `ops-financial-planning` for cohort projections, scenarios, sensitivity analysis.
- Crisis / pivot replanning — annual templates assume baseline stability; pivots need a different playbook.
- Org-wide planning at >20 people — needs PM-traditional or PM-agile methodologies, not solopreneur templates.

## Where it fails / limitations
- Templates are content-empty scaffolds; agents tend to fill them with truisms ("focus on growth, deliver value") unless given strong upstream context.
- OKR template is correct shape but doesn't enforce OKR rigor (ambitious + measurable + outcome-not-output) — agents need a separate validator pass.
- "Not Doing This Year" section is the most valuable and most often left blank; methodology doesn't push hard enough on it.
- Calendar-year framing assumes Jan-Dec; many businesses run on fiscal years or product-cycle-driven planning.
- No retrospective-formality — assumes the planner is honest with themselves; agents can amplify motivated reasoning.

## Agentic workflow
Use the agent as a structured-content scribe, not a strategist. Feed it: prior-year metrics, current state, draft strategic priorities (from human), competitor moves, budget envelope. Agent emits the filled template. Pair with `ops-annual-planning-process` (the framework that *generates* the inputs) and `growth-gtm-strategy` (strategic context). Quarterly, run a review-template-fill agent that pulls metrics from analytics/Stripe and drafts the Q[X] Review automatically, then a human edits the wins/learnings sections.

### Recommended subagents
- `faion-growth-agent` (source README) — owns the planning template fill.
- `faion-brainstorm` — upstream divergence on possible priorities before consolidation.
- `faion-improver` — generates "what didn't work / what to change" inputs from the year's improvement log.
- `faion-feature-executor` — converts annual priorities → quarterly initiatives → SDD features.
- General-purpose Claude subagent for OKR validator pass: checks each KR is measurable, time-bound, outcome-not-activity.

### Prompt pattern
```
You are filling the Annual Plan template (see templates.md). Inputs:
- vision_oneliner: <text>
- prior_year_metrics: {revenue, customers, mrr, ...}
- strategic_priorities: 3 bullet list from human
- budget_total: $X
Output: filled markdown matching the template exactly. Leave any field you cannot
ground in inputs as "[NEEDS HUMAN INPUT: <reason>]". Do not invent metrics.
```

```
OKR validator: for each KR in <list>, check (a) measurable with current data sources?
(b) outcome vs activity? (c) ambitious (50/50 confidence)? Output table with pass/fail
+ suggested rewrite for failures.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert filled markdown templates to PDF / docx for stakeholders | pandoc.org |
| `gh` | Track plan in repo; PR-driven quarterly amendments | cli.github.com |
| `linear` | Push initiatives → Linear projects/cycles | developers.linear.app |
| `notion-cli` (community) | Sync filled template to Notion workspace | github search |
| `obsidian` plugins | Local PKM ingestion of plans + reviews | obsidian.md |
| `dbt` (overkill but possible) | If metrics live in warehouse, build a YoY-results table | docs.getdbt.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion | SaaS | Yes | Most flexible; templates render natively. |
| Asana / Monday / ClickUp | SaaS | Yes | All have annual-planning template galleries + APIs. |
| Linear | SaaS | Yes | Cycles/projects map well to quarters/initiatives. |
| Lattice / 15Five / Quantive (Gtmhub) | SaaS | Yes | Dedicated OKR platforms with APIs. |
| Mooncamp | SaaS | Yes | Lightweight OKR tool; solo-friendly pricing. |
| Tability | SaaS | Yes | OKR-focused, API + Slack integration. |
| Coda | SaaS | Yes | Mix of doc + sheet + automation; planning-friendly. |
| Google Sheets | SaaS | Yes | Budget table; agent fills via Sheets API. |
| Obsidian (local) | OSS | Yes | Markdown-native; agent writes files directly. |

## Templates & scripts
See `templates.md` for the full set (annual, quarterly, monthly, OKR, year-in-review). Inline OKR validator stub:

```python
# OKR sanity check
def validate_okr(objective, key_results):
    issues = []
    for kr in key_results:
        text = kr["text"].lower()
        # outcome not activity
        if any(w in text for w in ["launch", "build", "ship", "publish", "create"]):
            issues.append(f"KR '{kr['text']}' looks like an activity, not an outcome")
        # measurable
        if not any(c.isdigit() for c in kr["text"]):
            issues.append(f"KR '{kr['text']}' has no numeric target")
        # current vs target present?
        if "current" not in kr or "target" not in kr:
            issues.append(f"KR '{kr['text']}' missing baseline or target")
    return {"objective": objective, "issues": issues, "ok": not issues}
```

## Best practices
- Strategy first, template later. The template should never be the place where strategy gets invented.
- Always fill "Not Doing This Year" with at least three concrete items. Without it, the plan is a wishlist.
- Pick 3 annual goals max. More than 3 means none are real.
- Make every Key Result reportable from existing data sources. If you can't measure it weekly, it's not a KR.
- Run quarterly reviews on a fixed date; calendar-driven, not motivation-driven. Skipping is the failure mode.
- Keep a "decisions log" alongside the plan — what changed mid-year and why. The plan is a snapshot; decisions are the truth.
- Pair the annual plan with an explicit budget table; goals without budget shape are aspirations.
- Force a "personal reflection" pass for solopreneurs (energy, satisfaction, growth). Burning out a founder kills the plan.

## AI-agent gotchas
- Filling templates with plausible-sounding goals is exactly what LLMs are good at and exactly what hurts planning quality. Require every goal to be grounded in input data; fail loudly if not.
- Quarterly review templates encourage post-hoc rationalization ("we missed because of market conditions"); push the agent to identify behavioral causes ("we deprioritized X for Y").
- OKR generators tend to produce activity KRs ("launch 5 features") instead of outcome KRs ("increase activation rate to 40%"); always run the validator.
- Annual plans frozen in markdown go stale within a quarter; design the workflow so amendments are first-class (PR + decision log).
- Don't auto-publish the year-in-review; it's a vulnerability artifact (failures, finances, energy). Human gate before any public version.
- Agent-generated "wins" tend to overstate; cross-reference against quantitative metrics from financial-basics.
- Budget tables filled by agents will round to round numbers and lose category granularity; use the actual prior-year P&L as input.
- For multi-stakeholder reviews, agent-summarized "what didn't work" risks blaming individuals; force structural framings.

## References
- Notion annual planning gallery — https://www.notion.so/templates/annual-planning
- "Measure What Matters" by John Doerr (OKR canonical) — https://www.whatmatters.com/
- Atlassian planning playbooks — https://www.atlassian.com/team-playbook
- SaaStr annual planning — https://www.saastr.com/annual-planning/
- Sibling methodology: `ops-annual-planning-process/README.md`
- Sibling methodology: `ops-financial-planning/README.md`
- Sibling methodology: `growth-gtm-strategy/README.md`
