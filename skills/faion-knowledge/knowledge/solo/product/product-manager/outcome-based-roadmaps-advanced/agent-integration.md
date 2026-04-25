# Agent Integration — Outcome-Based Roadmaps Advanced

## When to use
- Stakeholders keep demanding feature timelines despite an outcome-first culture; you need an audience-tailored view per cohort (board, sales, eng, customers).
- Translating a top-line business goal (revenue, retention, NPS) into a tree of product outcomes with leading indicators.
- Quarterly re-planning where confidence levels shift and "the same roadmap" must be re-presented to 4 different audiences with different commitment levels.
- A PM transitioning from "feature owner" to "architect of impact" who needs scaffolding for the new role.

## When NOT to use
- Early-stage product (pre-PMF) where outcomes are unstable and discovery dominates — use a simpler outcome roadmap or a "now/next/later" theme list.
- Single-stakeholder context (just you and your co-founder) — the audience-matrix overhead has zero ROI.
- Enterprise with hard-deadline contractual commitments — you need a hybrid (outcome theme + dated milestones).
- Org with no metrics infrastructure — you cannot operate confidence levels and leading indicators if you cannot measure.

## Where it fails / limitations
- "Confidence level" is itself an opinion; without calibration data it becomes another HiPPO axis.
- Decomposing a business goal into product outcomes is creative work, not deterministic — two PMs produce different trees from the same goal.
- The audience matrix can drift into 4 different roadmaps that disagree; you need a single source of truth with views, not 4 documents.
- Sales pressure is hardest: "give me a date" is a political problem, not a roadmap-format problem; outcome framing reduces but does not eliminate it.
- Boards often skim metrics, miss the experiment narrative, and ask "where's the chat feature" anyway.

## Agentic workflow
A decomposition agent takes one business goal and produces 2-4 candidate product outcomes with leading indicators and an experiment menu, plus an honest "we don't know" branch when evidence is weak. A second agent generates the audience views (theme-based for customers, outcome-metric for board, options-with-confidence for engineering, problem-solution for sales) from the same source. A third agent monitors the leading indicators on a weekly cadence and proposes "promote/demote/replace" actions to the human PM. Human owns final decomposition and audience-view sign-off.

### Recommended subagents
- An outcome-decomposition agent (Opus) — strategy work; needs the highest reasoning model.
- An audience-rewriter agent (Sonnet) — reformats one source-of-truth into 4 views without losing fidelity.
- A leading-indicator monitor agent — pulls metrics weekly, flags drift > 10%.
- `faion-mlp-impl-planner-agent` — once an outcome is committed, plans experiments under it.

### Prompt pattern
```
Business goal: <goal with current baseline and target>
Decompose into 2-4 product outcomes. Each outcome must have:
- A leading indicator measurable within 4 weeks
- A target movement size with stated confidence (low/med/high)
- 2-3 candidate experiments (not committed solutions)
- An "evidence we have" line and a "what we still need to learn" line.
Reject decompositions where any outcome has confidence=high but no shipped data.
```

```
Given source-of-truth roadmap <roadmap.md>, generate 4 audience views:
1. Customer (theme-based, no dates, no internal metrics)
2. Board (outcome metrics, quarterly targets, confidence column)
3. Engineering (outcome + 2-3 solution options + sprint-level breakdown when known)
4. Sales (problem -> solution narrative; only "confirmed" items get specific timing)
Each view must trace every line back to a row in source-of-truth.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Define and version leading-indicator metrics with lineage | https://docs.getdbt.com |
| `metabase` API / `superset` API | Programmatic dashboard creation per audience view | https://www.metabase.com/docs/latest/api-documentation |
| `mermaid-cli` | Render outcome-tree diagrams (goal → outcome → experiment) | https://github.com/mermaid-js/mermaid-cli |
| `pandoc` | Convert one source markdown into 4 audience PDFs/HTML | https://pandoc.org |
| `gh project` | Manage outcome roadmap as GitHub Projects with custom fields | https://cli.github.com/manual/gh_project |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ProdPad | SaaS | Yes (REST API) | Outcome-roadmap UX is best-in-class; "now/next/later" with confidence. |
| Airfocus | SaaS | Yes (REST API) | Configurable view per audience from one source. |
| Productboard | SaaS | Yes (REST + webhooks) | Strong customer-feedback linkage; audience-specific portals. |
| Aha! Roadmaps | SaaS | Yes (REST API) | Multiple "views" per roadmap is native. |
| Jira Plans / Advanced Roadmaps | SaaS | Yes (REST API) | Engineering-execution audience view; weak for outcome semantics. |
| Notion + dbt + Hex | mixed | Yes (APIs) | DIY outcome roadmap that integrates metric layer; cheap and flexible. |
| OpenProject | OSS | Yes (REST API) | Self-hostable; supports custom outcome fields. |

## Templates & scripts
See `templates.md` and `examples.md`. Inline outcome-tree validator:

```python
#!/usr/bin/env python3
"""validate-outcome-tree.py — fail on outcomes without leading indicators."""
import sys, yaml

def check(node, path=""):
    errs = []
    for outcome in node.get("outcomes", []):
        p = f"{path}/{outcome['name']}"
        if not outcome.get("leading_indicator"):
            errs.append(f"{p}: missing leading_indicator")
        if outcome.get("confidence") == "high" and not outcome.get("evidence"):
            errs.append(f"{p}: confidence=high requires evidence")
        if not outcome.get("experiments"):
            errs.append(f"{p}: must list 2-3 candidate experiments")
    return errs

with open(sys.argv[1]) as f:
    tree = yaml.safe_load(f)
errs = check(tree)
for e in errs: print(e)
sys.exit(1 if errs else 0)
```

## Best practices
- Source-of-truth in one place; everything else is a view. Never edit views directly.
- Confidence has 3 levels max (low/med/high). More levels create false precision.
- Every outcome has a leading indicator that moves within ≤4 weeks; otherwise you cannot learn fast enough.
- Pair every roadmap presentation with a kill criterion: "if X does not move by Y, we drop this outcome." Forces honest stakes.
- Sales gets the only audience view that mentions specific solutions, and only for items at high confidence — protects you from over-commitment everywhere else.
- Customer-facing roadmap stays at theme level ("better collaboration", not "real-time presence v2") for at least 2 quarters out.
- Board-facing roadmap leads with the metric movement, not the activity list.

## AI-agent gotchas
- LLMs love to invent plausible-but-wrong leading indicators. Require that every metric has a query/dashboard URL or a flag of "TO BE INSTRUMENTED".
- Outcome decomposition tends toward 6-8 outcomes per goal; force the agent to a hard cap of 4. More than 4 = lack of focus.
- Audience-rewriter agents drift from source over time; run a daily diff job that flags lines in views without traceability.
- Confidence inflation: agents default to "medium" because it sounds safe. Force evidence-based justification per confidence assertion.
- Human-in-loop checkpoint: outcome trees are strategic; a human PM owns the final decomposition before any audience view is generated.
- Human-in-loop checkpoint: customer-facing view requires human edit before publication — agent-generated phrasing leaks internal jargon.
- Do not let the agent rewrite the roadmap on every metric blip. Cadence: weekly metric monitor, quarterly re-decomposition, only re-version on real signal.

## References
- Marty Cagan, "Inspired" and "Empowered" — outcome thinking foundation.
- Teresa Torres, "Continuous Discovery Habits" — opportunity solution trees feed outcome roadmaps.
- ProdPad — "Now/Next/Later" outcome roadmap canon: https://www.prodpad.com/blog/now-next-later-roadmap/
- Reforge — "Roadmap that scales": https://www.reforge.com/blog/roadmap
- Lenny Rachitsky — outcome roadmaps in the wild: https://www.lennysnewsletter.com/p/the-ultimate-guide-to-product-roadmaps
