# Agent Integration — Schedule Development

## When to use
- Programs with hard external deadlines (regulatory, market, contractual) requiring critical-path defense.
- Multi-team / multi-vendor work with cross-team dependencies (FS / SS / FF links).
- Fixed-bid bids where the schedule baseline drives the price.
- Resource-constrained programs needing leveling and conflict detection.

## When NOT to use
- Pure-Scrum cadence with empowered PO (sprint plan replaces schedule).
- Continuous-flow / Kanban product teams.
- Projects shorter than ~2 weeks; a checklist beats a Gantt.
- Discovery / R&D where activity duration is fundamentally unknowable.

## Where it fails / limitations
- "Single-point" estimates create false precision; without three-point or Monte Carlo, dates lie.
- Critical path drifts as work progresses; schedules not refreshed weekly stop reflecting reality.
- Resource conflicts hide when the plan ignores per-resource capacity (parallel tasks, same person).
- Padding hidden inside individual estimates → invisible buffers no one can manage.
- "Optimistic by 30%" base rate — humans systematically underestimate; agents inherit this if seeded with human estimates only.

## Agentic workflow
A subagent is well-suited to: convert a WBS into an activity list, propose dependencies (FS/SS/FF/SF) by analyzing leaf descriptions, generate three-point estimates against analogous projects, identify the critical path, recommend feeding/project buffers (CCPM-style), and run weekly schedule-vs-actual variance reports. Humans own duration commitments, resource assignments, and stakeholder-facing date communications. Pair the agent with EVM (separate methodology) for performance tracking once execution starts.

### Recommended subagents
- `faion-pm-agent` — owns schedule baseline, runs CPM, drafts variance reports.
- `faion-business-analyst` — strong for activity-vs-deliverable mapping and dependency identification.
- `faion-sdd-execution` — gate that PRs reference activity IDs, helping schedule actuals stay accurate.

### Prompt pattern
```
Given this WBS (YAML), produce an activity list:
[{id, wbs_ref, name, predecessors:[{id, type:FS|SS|FF|SF, lag}],
  est_o, est_m, est_p, pert_mean, resource}]
Constraints: every leaf maps to >=1 activity; PERT = (O+4M+P)/6.
Flag activities lacking analogous estimation source as needs_calibration.
```

```
Compute the critical path. Output:
- forward pass: [{id, ES, EF}]
- backward pass: [{id, LS, LF, total_float}]
- critical_path: [id,...]
- project_duration: <days>
- recommended_buffers: project_buffer (15-25% of CP), feeding_buffers per non-critical merge.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mpxj` (Java/CLI) | Read/write MS Project (.mpp/.xml) files | https://www.mpxj.org |
| `python-mpxj` / `pyp6xer` | Python access to Project / Primavera XER | https://github.com/p6xer |
| `gantt` (npm `gantt-task-react` CLI) | JSON → Gantt SVG | https://www.npmjs.com/package/gantt |
| `mermaid-cli` | Render `gantt` blocks to SVG/PNG | https://mermaid.js.org |
| `frappe-gantt` | Lightweight HTML Gantt from JSON | https://frappe.io/gantt |
| `taskjuggler` | Full open-source CPM/CCPM scheduler | https://taskjuggler.org |
| `plan` (Python `plan` CLI) | YAML schedules with dependency math | https://pypi.org/project/plan/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| MS Project / Project for the Web | SaaS | Yes — Graph API | Industry default; full CPM, leveling. |
| Primavera P6 (Oracle) | Enterprise | Yes — XER/REST | Construction / megaproject standard. |
| Smartsheet | SaaS | Yes — REST API | Hierarchical Gantt with predecessors. |
| OpenProject | OSS / SaaS | Yes — REST API | Free CPM + Gantt + baselines. |
| TaskJuggler | OSS | Yes — text DSL | Programmable, agent-friendly. |
| LiquidPlanner | SaaS | Yes — REST API | Probabilistic three-point baked in. |
| Asana / Monday timeline | SaaS | Yes — REST/GraphQL | Lightweight, no true CPM. |

## Templates & scripts
See `templates.md` for activity list and Gantt outline. Minimal CPM in Python:

```python
# cpm.py — usage: python cpm.py activities.yaml
import sys, yaml
acts = {a["id"]: a for a in yaml.safe_load(open(sys.argv[1]))}
# forward pass
def es(a):
    if "_es" in a: return a["_es"]
    a["_es"] = max((es(acts[p["id"]]) + acts[p["id"]]["dur"] + p.get("lag",0)
                    for p in a.get("preds",[])), default=0)
    a["_ef"] = a["_es"] + a["dur"]
    return a["_es"]
for a in acts.values(): es(a)
end = max(a["_ef"] for a in acts.values())
# backward pass
def lf(a):
    if "_lf" in a: return a["_lf"]
    succ = [s for s in acts.values() if any(p["id"]==a["id"] for p in s.get("preds",[]))]
    a["_lf"] = min((lf(s) - s["dur"] - next(p for p in s["preds"] if p["id"]==a["id"]).get("lag",0)
                    for s in succ), default=end)
    a["_ls"] = a["_lf"] - a["dur"]
    a["_float"] = a["_ls"] - a["_es"]
    return a["_lf"]
for a in acts.values(): lf(a)
crit = [a["id"] for a in acts.values() if a["_float"]==0]
print({"duration":end, "critical_path":crit})
```

## Best practices
- Use three-point estimates (PERT) for any activity > 5 days; single-point only for trivial work.
- Make buffers explicit (CCPM-style project + feeding buffers); never hide them in task estimates.
- Re-baseline when accumulated changes exceed 10% of duration; otherwise actuals lose meaning.
- Keep per-resource capacity inputs; without them parallel tasks are fiction.
- Flag any activity with float < 2 days as "near-critical" — these become the next critical path.
- Track milestone slip rate (count of milestones slipped / total) as a leading indicator.
- For agile-hybrid: schedule at the epic/release level, run sprint cadence inside; do not Gantt every story.

## AI-agent gotchas
- LLMs default to optimistic estimates (M ≈ O); explicitly request a P that is 1.5-2× M.
- Auto-detected dependencies miss soft / resource dependencies; require human review of the dependency graph.
- Critical path computed by an LLM in prose is error-prone — use a deterministic CPM script and pass the JSON to the LLM only for narrative.
- Schedules > 100 activities exceed comfortable context; chunk by phase or summary task and pass detail on demand.
- Don't let the agent commit to dates with stakeholders; dates require sponsor signoff.
- Human-in-loop checkpoints: (1) baseline approval, (2) any critical-path change, (3) re-baseline events, (4) milestone-slip communications.

## References
- PMI, *PMBOK Guide* 7th ed., Planning Performance Domain.
- PMI, *Practice Standard for Scheduling*, 3rd ed.
- E. Goldratt, *Critical Chain* (1997) — CCPM and buffers.
- AACE International Recommended Practice 27R-03 — schedule classification.
