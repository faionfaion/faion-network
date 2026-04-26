# Agent Integration — Schedule Development

## When to use
- Building the initial schedule from a WBS once work packages exist (activity definition → sequencing → CPM).
- Establishing a critical-path baseline before kickoff so management focus targets the right tasks.
- Re-baselining after a change-control event (scope add, vendor slip, milestone shift).
- Producing a PERT 3-point duration estimate for stakeholder communications when point estimates are not credible.
- Solopreneur weekly capacity planning where one resource works on multiple parallel projects with handoffs.

## When NOT to use
- Pure agile teams running fixed-cadence sprints — schedule is replaced by velocity + roadmap; CPM is overhead.
- Highly creative / R&D work where activity duration is unknowable (scope is the variable, not time). Use rolling-wave or Kanban.
- Sub-2-week tasks: CPM overhead exceeds value; a checklist suffices.
- Fixed-deadline work (regulatory cutover, conference launch) where you back-plan from end date — use reverse-pass / time-boxed scope.

## Where it fails / limitations
- LLMs default to wildly optimistic durations because training data emphasises happy paths; pessimistic values must be hand-injected.
- PERT mean assumes a beta distribution but software task duration is heavy-tailed lognormal — P50 schedule will slip ~70% of the time.
- Critical path "longest chain" is brittle: a near-critical path 1 day shorter becomes critical after one slip and is invisible without slack analysis.
- Resource leveling is NOT part of CPM — same person on parallel critical-path tasks blows the schedule silently.
- Multi-project portfolios with shared resources need RCPSP, not CPM; agents almost never solve this correctly.
- Buffer placement (Critical Chain / Goldratt) gives better statistical protection than padding each task; most agent outputs pad tasks instead, hiding slack.

## Agentic workflow
The agent is a deterministic schedule compiler. Feed it WBS work packages with effort + role + dependency edges; it emits an activity-on-node graph, runs forward + backward pass for ES/EF/LS/LF, computes total/free float, identifies critical path, and outputs Gantt-renderable JSON. A second agent runs Monte Carlo over 3-point durations to produce P50/P80/P95 finish dates. Humans approve buffer sizing and resource constraints before the schedule becomes the baseline.

### Recommended subagents
- `schedule-builder` — ingests `wbs.yaml` + `dependencies.yaml`, outputs CPM JSON with float per activity.
- `monte-carlo-scheduler` — runs N=10000 simulations over PERT triples, outputs date distribution + sensitivity (per-activity criticality index).
- `resource-leveler` — checks no resource is double-booked; flags conflicts with proposed re-sequencing.
- `faion-sdd-executor` — once the schedule baseline is approved, drives task-by-task execution under quality gates.

### Prompt pattern
```
Inputs:
- wbs.yaml: [{id, name, effort_hours, role, predecessors:[{id, type:FS|FF|SS|SF, lag_days}]}]
- calendar.yaml: working days/holidays per resource
- start_date: YYYY-MM-DD

Output JSON:
{ "activities": [{id, ES, EF, LS, LF, total_float, free_float, critical:bool}],
  "critical_path": [id...],
  "project_finish_p50": "...", "p80": "...", "p95": "...",
  "near_critical_paths": [[id...]],     # within 2 days of critical
  "resource_conflicts": [...] }

Rules:
- No invented durations; if missing, return error not guess.
- Lag in business days, never calendar days unless calendar.yaml says otherwise.
- Reject WBS containing cycles; report the cycle.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `taskjuggler` | Text-based PM with CPM, resource leveling, Monte Carlo | https://taskjuggler.org/ |
| `plan` (`plantuml-gantt`) | Gantt + critical path from text DSL | https://plantuml.com/gantt-diagram |
| `mermaid-cli` (`mmdc`) | Render `gantt` Mermaid blocks to SVG/PNG in CI | https://github.com/mermaid-js/mermaid-cli |
| `gh project` / `jira-cli` | Pull dependencies / activities from issue trackers | https://cli.github.com/ , https://github.com/ankitpokhrel/jira-cli |
| `gantt` (Python `python-gantt`) | Programmatic Gantt + critical path | https://pypi.org/project/python-gantt/ |
| `networkx` (Python) | Graph algorithms — CPM, topological sort, cycle detection | https://networkx.org/ |
| `simpy` / `numpy` | Monte Carlo simulation over PERT triples | https://simpy.readthedocs.io/ |
| `omniplan-cli` (macOS) | OmniPlan headless export | https://www.omnigroup.com/omniplan/ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Microsoft Project (Project Online) | SaaS | Partial — Graph API for read; rich CPM | Enterprise PMO standard |
| Smartsheet | SaaS | Yes — REST | Gantt, dependencies, automation; popular agent target |
| Asana Timeline | SaaS | Yes — REST | Dependency-aware; not full CPM |
| Monday.com | SaaS | Yes — GraphQL | Timelines, dependencies; weak CPM |
| ClickUp Gantt | SaaS | Yes — REST | Critical path view available |
| Jira + Advanced Roadmaps | SaaS | Yes — REST | Cross-team scheduling |
| LiquidPlanner | SaaS | Yes — REST | Probabilistic ranged scheduling |
| TeamGantt | SaaS | Yes — REST | Lightweight Gantt |
| Notion + Timeline DB | SaaS | Yes — REST | Lightweight, not real CPM |
| ProjectLibre / GanttProject | OSS | Yes — XML import/export | MS Project-compatible offline |

## Templates & scripts
See `templates.md` for the activity list and Gantt skeleton. Critical-path snippet (Python, ~30 lines):

```python
import networkx as nx
def critical_path(activities):
    G = nx.DiGraph()
    for a in activities:
        G.add_node(a["id"], dur=a["effort_days"])
        for p in a.get("predecessors", []):
            G.add_edge(p["id"], a["id"], lag=p.get("lag_days", 0))
    if not nx.is_directed_acyclic_graph(G):
        raise ValueError(f"cycle: {list(nx.find_cycle(G))}")
    es = {n: 0 for n in G}
    for n in nx.topological_sort(G):
        for s in G.successors(n):
            es[s] = max(es[s], es[n] + G.nodes[n]["dur"] + G[n][s]["lag"])
    finish = max(es[n] + G.nodes[n]["dur"] for n in G)
    lf = {n: finish for n in G}
    for n in reversed(list(nx.topological_sort(G))):
        for p in G.predecessors(n):
            lf[p] = min(lf[p], lf[n] - G.nodes[n]["dur"] - G[p][n]["lag"])
    crit = [n for n in G if es[n] == lf[n] - G.nodes[n]["dur"]]
    return finish, crit
```

## Best practices
- Use Critical Chain buffering (one project buffer at end, feeding buffers at merge points) — not per-task padding. Hidden slack always gets used (Parkinson's Law).
- Track schedule performance index (SPI from EVM) weekly, not just milestone hits — reveals slip earlier.
- Lock the baseline once; re-baselining hides slip from stakeholders. Track variance against the original.
- Keep the WBS-to-activity ratio at ~3-7 activities per work package; finer creates a fake-precision schedule, coarser hides risk.
- Identify near-critical paths (float < 2 days) explicitly; one slip promotes them. Without this you only see issues post-mortem.
- Use FS dependencies by default; SS/FF/SF only when truly required and document why. Most "we can parallelize" claims fail integration.

## AI-agent gotchas
- Effort vs duration confusion: 40 effort-hours is NOT 5 working days for a 50%-loaded resource (it's 10). Always model availability.
- LLMs hallucinate dependencies they cannot verify; require explicit `predecessors:` in input, never let agent infer them from prose.
- "How long does X take?" prompts return median industry numbers; force a 3-point with sources or refuse.
- Calendar arithmetic is a frequent agent bug (skipping weekends, public holidays, half-days). Use `business_calendar` libraries, never raw date math.
- Recursive/automatic re-scheduling on every standup creates instability — humans need a stable plan to commit against. Re-baseline only on change-control events.
- Critical path agents often miss multi-path criticality (two paths tie at the same finish); print all paths whose float ≤ 0, not "the" path.
- Resource calendars in different timezones are a silent slip generator; always assert tz on every date.

## References
- PMI PMBOK Guide 6th Ed., Chapter 6 — Project Schedule Management.
- Goldratt, *Critical Chain* (1997) — buffering and Parkinson/student-syndrome.
- Hulett, *Practical Schedule Risk Analysis* (2009) — Monte Carlo schedule sensitivity.
- DOD PARCA Generally Accepted Scheduling Practices (GASP).
- AACE International Recommended Practice 27R-03 (schedule risk analysis).
- networkx CPM example: https://networkx.org/documentation/stable/reference/algorithms/dag.html
