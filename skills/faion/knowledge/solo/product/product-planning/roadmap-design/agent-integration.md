# Agent Integration — Roadmap Design

## When to use
- Quarterly planning where strategy must be communicated to a team / stakeholders / customers in a single artifact.
- After RICE/MoSCoW prioritization — the roadmap is the consumable form of those rankings.
- Multiple audiences (eng, sales, customers) need different slices of the same plan.
- Strategic alignment check: does the planned work actually drive the stated objectives?

## When NOT to use
- < 4 weeks of work ahead — a sprint plan or kanban suffices.
- Pre-PMF discovery phase — use opportunity solution trees and continuous-discovery instead.
- High-uncertainty research projects with no shippable outcome — write a research charter instead.
- One-person, one-week feature — overkill.

## Where it fails / limitations
- Timeline format with hard dates always slips and erodes trust; Now-Next-Later rarely does.
- Roadmap-as-feature-list disconnects from outcomes; theme-based + outcome-based roadmaps avoid it.
- Single artifact for all audiences leaks too much detail to customers or too little to eng.
- "Later" rots — items pile up with no review and the section becomes meaningless.
- Customer-shared roadmaps can get treated as legal commitments. Footer disclaimer + abstraction level matter.

## Agentic workflow
A strategy subagent collects vision, OKRs, and constraints into a roadmap context blob. A theme subagent groups prioritized initiatives (from the RICE/MoSCoW outputs) into 3–5 themes per period. A formatter subagent emits two markdown artifacts from the same source: an internal Now-Next-Later with confidence levels, and an external customer-facing Coming-Soon with abstracted capabilities. A reviewer subagent checks every initiative links to a stated objective and every theme has a measurable success metric. Update cadence: monthly review, quarterly rewrite — automate the diff between versions.

### Recommended subagents
- `faion-mlp-impl-planner-agent` — roadmap planner named in this methodology's metadata.
- `faion-mlp-feature-proposer-agent` — feeds candidates into themes.
- `faion-mvp-scope-analyzer-agent` — checks "Now" items are actually scoped.
- `faion-spec-reviewer-agent` — validates each "Now" initiative has a spec or a discovery brief.

### Prompt pattern
```
Given vision=<v>, objectives=[{id, name, kr}], prioritized_items=[{id, name, score, theme}]:
Output a roadmap JSON:
{
  "vision": "<sentence>",
  "now": [{theme, items: [{id, status, confidence}], drives_objective}],
  "next": [{theme, items: [{id, confidence}], depends_on}],
  "later": {exploring: [], watching: [], not_doing: [{item, reason}]},
  "metrics": [{objective_id, metric, target}],
  "audience": "internal|external"
}
Constraints: every initiative MUST cite a drives_objective; every theme MUST have ≤5 initiatives.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` CLI + Projects v2 | Roadmap as a Project with iteration / theme fields | https://cli.github.com |
| Linear API | Roadmap, cycles, project objectives | https://developers.linear.app |
| Productboard API | Roadmap views (now-next-later, timeline, swimlane) | https://developer.productboard.com |
| Aha! API | Strategy → release timeline | https://www.aha.io/api |
| Notion API | Embedded roadmap pages with database views | https://developers.notion.com |
| `mermaid-cli` | Render Gantt/timeline diagrams | https://github.com/mermaid-js/mermaid-cli |
| `pandoc` | Convert internal MD roadmap to stakeholder PDF | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | Yes (REST) | Multiple roadmap views, customer portal share |
| Aha! Roadmaps | SaaS | Yes (REST) | Best-in-class for outcome roadmaps |
| Roadmunk | SaaS | Yes (REST) | Lightweight, swimlane focus |
| ProductPlan | SaaS | Yes (REST) | Strong external sharing/portal |
| Linear | SaaS | Yes (GraphQL) | Cycles + projects = native Now-Next-Later |
| Trello + Roadmap power-up | SaaS | Yes (REST) | Cheap option |
| Public-roadmap (faionfaion/roadmap.faion.net) | OSS-internal | Yes (file-based) | This repo's own pattern |

## Templates & scripts
See `templates.md` for Now-Next-Later, quarterly outcome, and external customer roadmap layouts. Diff helper for monthly review (≤ 30 lines):

```python
# roadmap_diff.py — show what moved between two roadmap snapshots
import json, sys
prev, curr = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))

def index(rm): return {i["id"]: bucket for bucket in ("now","next") for i in rm.get(bucket, [])}

p, c = index(prev), index(curr)
moved = {k: (p[k], c[k]) for k in c if k in p and p[k] != c[k]}
added = [k for k in c if k not in p]
dropped = [k for k in p if k not in c]

print(json.dumps({"moved": moved, "added": added, "dropped": dropped}, indent=2))
```

## Best practices
- Pick the format that matches your uncertainty: low → timeline, medium → Now-Next-Later, high → outcome-themed.
- Always include "Not Doing" — it's the cheapest scope-creep prevention.
- Tag each initiative with confidence (high/medium/low). Stakeholders read "high" as commitment; downgrade aggressively.
- Tie every initiative to one stated objective; if it doesn't drive an OKR, ask why it's on the roadmap.
- Keep two artifacts from one source: internal (with confidence + dependencies) and external (with capability descriptions). Generate, don't maintain in parallel.
- Review monthly, rewrite quarterly. Add a "last updated" date prominently — stale roadmaps lose trust faster than missing ones.
- For solo / small teams, use 3 themes max per period; more is aspirational.

## AI-agent gotchas
- LLMs over-promise dates. Default to Now-Next-Later unless data justifies a timeline.
- Agents copy-paste initiatives across periods without re-evaluating; force a re-justification when an item moves from Next to Now.
- "Later" becomes a dumping ground; cap at 8 items, force one quarterly cull pass.
- Customer-shared roadmaps need legal-style disclaimer; auto-append a "subject to change, no commitment" footer.
- Confidence inflation — every initiative ends up "high". Calibrate against past quarter delivery to set a realistic mix.
- Human-in-loop checkpoints: (a) theme selection, (b) Now-bucket lock per cycle, (c) any external publish, (d) any item promoted from Later straight to Now.

## References
- Roman Pichler, "Strategize" — outcome-based roadmaps.
- Janna Bastow / ProdPad — Now-Next-Later format origin https://www.prodpad.com/blog/the-now-next-later-roadmap/
- Bruce McCarthy, "Product Roadmaps Relaunched" (O'Reilly).
- Marty Cagan SVPG — "Roadmaps are dead" essay https://www.svpg.com/revisiting-product-roadmaps/
- Teresa Torres — connecting roadmaps to opportunity solution trees https://www.producttalk.org/
