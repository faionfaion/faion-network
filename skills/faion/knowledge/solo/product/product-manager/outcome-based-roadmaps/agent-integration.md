# Agent Integration — Outcome-Based Roadmaps

## When to use
- Replacing a feature-list roadmap that has shipped on time but moved no metrics.
- Communicating priority to engineers who keep asking "why this feature, not that one."
- Pre-PMF / post-PMF teams where the problem space is clearer than the solution space.
- Any team that wants room to discover the right solution without re-renegotiating the roadmap.

## When NOT to use
- Hard-deadline contractual obligations (regulatory, partner integration with launch date) — these need a feature roadmap.
- Pure execution phase of a well-validated initiative — outcome framing adds noise; "ship the redesign" is fine.
- Teams without metrics infrastructure — you cannot run an outcome roadmap if you cannot measure outcomes.
- Cultures that punish missed targets — outcome roadmaps require permission to report negative results.

## Where it fails / limitations
- "Reduce churn from 8% to 5%" sounds outcome-shaped but is meaningless without leading indicators that move on a quarterly cadence.
- Stakeholders read outcome roadmaps and silently translate them back to features anyway; you have to actively police the framing.
- Sales gets frustrated: prospects ask "when does the chat feature ship?" and outcome framing does not answer that question.
- Engineering gets frustrated when "options, not committed solution" leaves them unable to plan capacity.
- Outcomes without bounds (e.g. "improve activation") become moving targets — must specify "to X by Y date" or it is not an outcome.

## Agentic workflow
A translation agent ingests the existing feature roadmap and rewrites every line as "problem + outcome + candidate solutions" — flagging any item that does not have a clear outcome (those are typically infrastructure or pet features). A presenter agent generates two views: the engineering "options + sprint estimates" view and the leadership "outcome metric + confidence" view. A weekly metric-monitor agent reads dashboards and flags drift. Human PM owns the outcome decomposition, the kill criteria, and the conversation with sales.

### Recommended subagents
- A roadmap-translator agent (Opus) — converts feature lists to outcome statements; high-leverage strategic step.
- A view-generator agent (Sonnet) — formats one outcome roadmap into engineering vs leadership vs customer views.
- A metric-monitor agent — pulls leading-indicator data weekly, flags drift > threshold.
- `faion-mlp-impl-planner-agent` — once an outcome wins capacity, plans candidate experiments under it.

### Prompt pattern
```
For each row in the current feature roadmap:
- State the underlying problem (1 sentence).
- Restate as an outcome: "<metric> from <baseline> to <target> by <horizon>".
- List 2-3 candidate solutions (NOT a committed solution).
- Flag rows where you cannot identify an outcome — these are pet features or infrastructure.
Return the rewritten roadmap in markdown, sorted by outcome impact.
```

```
Given outcome roadmap <roadmap.md>, generate two views:
1. Engineering view: each outcome with 2-3 candidate solutions, rough effort per option, current confidence.
2. Leadership view: each outcome with metric, baseline, target, current value, confidence, kill criterion.
Both views must trace back to identical source rows.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Define and version the metric layer that powers outcome KPIs | https://docs.getdbt.com |
| `gh project` | Manage outcome roadmap as a GitHub Project with custom fields | https://cli.github.com/manual/gh_project |
| `metabase` API / `superset` API | Programmatic dashboard creation per outcome | https://www.metabase.com/docs/latest/api-documentation |
| `mermaid-cli` | Render goal → outcome → experiment trees | https://github.com/mermaid-js/mermaid-cli |
| `pandoc` | Convert source-of-truth markdown into multiple audience views | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ProdPad | SaaS | Yes (REST API) | "Now/Next/Later" outcome roadmap canon. |
| Productboard | SaaS | Yes (REST + webhooks) | Customer feedback links into outcomes. |
| Airfocus | SaaS | Yes (REST API) | Outcome-first board; multiple views per source. |
| Aha! Roadmaps | SaaS | Yes (REST API) | Strong audience-view support. |
| Notion + dbt + Hex | mixed | Yes | DIY outcome roadmap with a real metric layer. |
| Linear Initiatives | SaaS | Yes (GraphQL) | Initiatives are outcome-shaped; map cleanly. |
| OpenProject | OSS | Yes (REST API) | Self-host; custom outcome fields supported. |

## Templates & scripts
See `templates.md` and the advanced sibling methodology. Inline outcome-row validator:

```python
#!/usr/bin/env python3
"""validate-outcomes.py — every roadmap row must have outcome+baseline+target+horizon."""
import sys, yaml

REQ = {"problem", "outcome_metric", "baseline", "target", "horizon", "candidate_solutions"}

def lint(path):
    with open(path) as f:
        doc = yaml.safe_load(f)
    errs = []
    for row in doc.get("outcomes", []):
        missing = REQ - set(row.keys())
        if missing:
            errs.append(f"{row.get('id', '?')}: missing {sorted(missing)}")
        sols = row.get("candidate_solutions", [])
        if isinstance(sols, list) and len(sols) < 2:
            errs.append(f"{row.get('id', '?')}: needs at least 2 candidate solutions")
    return errs

errs = lint(sys.argv[1])
for e in errs: print(e)
sys.exit(1 if errs else 0)
```

## Best practices
- Every outcome row has metric + baseline + target + horizon. Drop any row missing those fields.
- Present 2-3 candidate solutions per outcome, never one. Single-solution rows are feature roadmaps in disguise.
- The customer-facing view stays at problem-statement level; never expose internal outcome metrics.
- Keep outcomes time-bounded (this quarter, next quarter). "Improve retention" with no horizon is a vibe, not a roadmap.
- Pair every outcome with a kill criterion: "if leading indicator does not move by week 6, drop this outcome."
- Reserve 20% of capacity for "unscheduled outcomes" — discoveries from the field that didn't exist when the quarter started.
- Sales objection management: maintain a "confirmed solutions" list that is a strict subset of the roadmap; only those get specific timing externally.

## AI-agent gotchas
- LLMs translate features to outcomes by simply rewording ("Build chat" → "Improve communication outcomes"). That is not an outcome. Force a measurable metric movement per row.
- Agents prefer 1 confident solution per outcome ("the obvious answer"). Force a minimum of 2 candidate solutions to preserve solution discovery.
- Vague outcome verbs (improve, enhance, optimize) creep in. Add a banned-verb instruction or require numeric movement per outcome.
- View-generator agents drift between leadership and engineering views — same row says different things. Require traceability ID per row across views.
- Agents hallucinate baselines. If the metric is not instrumented, the row must say "TO BE INSTRUMENTED, owner=X" — never invented numbers.
- Human-in-loop checkpoint: outcome decomposition (goal → outcomes) is strategic; humans must own the final tree before any view is generated.
- Human-in-loop checkpoint: kill criteria require human sign-off — agents are too quick to delete outcomes the moment metrics wobble.
- Don't let the agent re-rewrite the roadmap weekly. Cadence: weekly metric monitor, quarterly re-decomposition.

## References
- Marty Cagan — "Inspired" / "Empowered" — outcome-orientation foundation.
- Teresa Torres — "Continuous Discovery Habits", opportunity solution trees.
- ProdPad "Now/Next/Later" canon: https://www.prodpad.com/blog/now-next-later-roadmap/
- Lenny Rachitsky — outcome roadmap field guide: https://www.lennysnewsletter.com/p/the-ultimate-guide-to-product-roadmaps
- Reforge "Roadmap that scales": https://www.reforge.com/blog
- Sibling: `outcome-based-roadmaps-advanced/agent-integration.md`
