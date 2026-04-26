# Agent Integration — Agile and Hybrid Approaches

## When to use
- Project kickoff where the right delivery model is genuinely unclear (mixed-experience team, semi-defined scope).
- Fixed-price contracts that need agile execution under predictive governance (Water-Scrum-Fall).
- Regulated environments where parts must be predictive (compliance, validation) and parts must be agile (UI, integrations).
- Coaching engagements moving from waterfall to agile, where pure-agile-from-day-one would fail change-management.
- Solopreneur / small-team work where lightweight Kanban + monthly review is right-sized.

## When NOT to use
- A team already running stable Scrum or Kanban; switching to a hybrid often loses cadence without recovering certainty.
- Pure exploration / research where any delivery framework is overhead.
- Single-person product owner running freeform — formalizing into a hybrid adds ceremony with no payoff.
- Teams whose dysfunction is cultural, not methodological — a hybrid won't fix accountability gaps.
- Crisis / incident response — switch to incident-response playbooks (`error-handling`, runbooks), not delivery framework.

## Where it fails / limitations
- "Hybrid" becomes "we cherry-pick whatever each role likes" — no actual coherence.
- Phase-gate funding combined with sprint planning leads to sprint commitments that can't survive funding cuts.
- Scrum events without empowerment ("Agile in name only") produce theater, not improvement.
- Fixed scope + agile execution = scope creep masked as "discovery" — eventually busts the contract.
- Stakeholders demand both burn-down charts AND traditional Gantt; teams burn cycles maintaining both.
- Discovery → Implementation handoff bakes in a translation tax (agile→waterfall) that's hard to remove later.

## Agentic workflow
A selection agent runs the decision-framework checklist (requirements clarity, customer availability, risk, team experience, contract type) against project inputs and outputs a recommendation with rationale. A scaffolding agent generates the ceremony cadence + artifact set tailored to the chosen approach (sprint plan templates for agile parts, milestone plan for predictive parts). A weekly governance agent reconciles status across approaches into one stakeholder-facing summary.

### Recommended subagents
- `approach-selector` — runs the 5-question decision framework, outputs Predictive / Agile / Hybrid recommendation with rationale.
- `hybrid-scaffolder` — given chosen approach, emits ceremony calendar, artifact list, RACI per phase.
- `governance-reconciler` — merges sprint reports + phase-gate updates into one weekly stakeholder summary.
- `faion-feature-executor` — already in repo; runs the agile execution loop once features are scoped.
- `dual-track-coach` — for discovery+delivery splits, ensures discovery feeds delivery without blocking.

### Prompt pattern
```
You are approach-selector. Inputs: 5 answers (requirements_clarity, stakeholder_availability,
risk_tolerance, team_experience, contract_type) on 3-point scale. Output JSON
{recommendation: "Predictive"|"Agile"|"Hybrid", rationale: "...",
caveats: ["..."], minimum_ceremonies: ["..."], required_artifacts: ["..."]}.
Prefer Hybrid only when at least two answers point to Predictive AND two to Agile.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gantty` / `mermaid` Gantt blocks | Render predictive timelines from YAML | https://mermaid.js.org/syntax/gantt.html |
| `mkdocs-material` | Project site combining sprint reports + phase-gate docs | https://squidfunk.github.io/mkdocs-material/ |
| `monte-carlo-throughput` (community Python) | Forecast end dates from agile throughput | `pip install fcboard` (or similar) |
| `confluence-cli` (community) | Push hybrid status pages back into Confluence | https://github.com/topics/confluence-cli |
| `pandoc` | Convert hybrid reports into PDF for steering committees | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira + Advanced Roadmaps | SaaS | Yes — REST | Native hybrid: agile teams + initiative-level roadmaps. |
| Azure DevOps | SaaS | Yes — REST | CMMI process for predictive parts, Scrum for agile parts in same project. |
| ClickUp | SaaS | Yes — REST | Hybrid views (Gantt + sprints) in one workspace. |
| Smartsheet | SaaS | Yes — REST | Strong predictive scheduling, lighter agile, good for hybrids led by PMOs. |
| Asana | SaaS | Yes — REST | Timeline + boards; reasonable hybrid. |
| Wrike | SaaS | Yes — REST | Hybrid PMO features baked in. |
| Linear + Notion | SaaS | Yes — GraphQL/REST | Linear for agile delivery, Notion for predictive plan & governance. |

## Templates & scripts
See `templates.md` for sprint planning + Kanban + decision checklist. Inline script: pick approach from a YAML answer file (`scripts/pick_approach.py`):

```python
#!/usr/bin/env python3
"""Pick Predictive/Agile/Hybrid from a YAML decision file."""
import sys, yaml
ans = yaml.safe_load(open(sys.argv[1]))
score = {"P": 0, "A": 0}
for k in ["requirements_clarity", "stakeholder_availability",
          "risk_tolerance", "team_experience", "contract_type"]:
    v = ans[k]  # one of "P", "H", "A"
    if v == "P": score["P"] += 1
    if v == "A": score["A"] += 1
if score["P"] >= 4: rec = "Predictive"
elif score["A"] >= 4: rec = "Agile"
else: rec = "Hybrid"
print(yaml.safe_dump({"recommendation": rec, "scores": score}))
```

## Best practices
- Pick one approach per phase, not per ceremony. "Discovery is agile, build is agile, deploy is predictive" beats "we do daily standups but also Gantt charts in parallel".
- Translate between approaches at explicit boundaries: a sprint review at the end of agile build feeds the predictive deploy plan as input artifacts.
- Burn-up > burn-down for hybrid stakeholder reporting; burn-down hides scope additions.
- Keep ceremonies minimal: one planning, one daily, one demo, one retro per cycle. Add governance gates as separate, named events.
- Define "Done" once per phase. Hybrid teams that share a single Definition of Done across modes get sloppy.
- Calibrate forecasts with Monte Carlo + throughput; deterministic estimates lie.
- Document the chosen mix as an ADR — future contributors need to know why.

## AI-agent gotchas
- LLMs default to "Hybrid" because it sounds safe; force calibration with explicit thresholds.
- Agents conflate Scrum and Kanban concepts (sprints vs. WIP, velocity vs. throughput) — pin definitions.
- Generated sprint plans from incomplete inputs over-commit; require capacity inputs and enforce ≤80% utilization.
- Status reports that mix agile and predictive metrics confuse stakeholders; have the agent emit two sections, clearly labeled.
- "Self-organizing team" in prompts is a magic phrase that makes agents skip explicit ownership; require Accountable per work item.
- For solopreneur use, agents over-engineer ceremonies; cap at one weekly review unless asked.

## References
- PMBOK Guide 7/8 — Development Approach Performance Domain
- "Disciplined Agile Delivery" (Scott Ambler / Mark Lines)
- https://www.scrum.org/resources/blog/scrum-and-pmbok
- "Lean Enterprise" (Humble, Molesky, O'Reilly)
- https://www.scaledagileframework.com/agile-product-delivery/
