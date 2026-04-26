# Agent Integration — Kanban and Scaled Agile Ceremonies

## When to use
- Continuous-flow teams (support, ops, data engineering) with no natural sprint boundary.
- Multi-team programs (>3 Scrum teams) needing PI Planning and Scrum-of-Scrums coordination.
- Teams with high mid-sprint volatility (incident-heavy ops, content production) — sprint commitments break weekly.
- Platform teams serving many internal customers — replenishment + service-delivery review fits better than Scrum.
- Hybrid ScrumBan setups: sprint planning kept for steering, WIP limits enforced for flow.

## When NOT to use
- A single team of <8 people with stable feature work — Scrum's lightweight ceremonies suffice.
- Pure project work with a fixed end date and known scope — predictive cadences fit better.
- Organizations already drowning in ceremonies; adding SAFe events without removing existing ones causes revolt.
- Discovery-heavy product work where dual-track agile (Discovery + Delivery) maps better than SAFe.
- Solopreneur or 2-person teams — overhead exceeds value; a personal Kanban board is enough.

## Where it fails / limitations
- WIP limits without leadership backing become aspirational; teams blow past them under pressure.
- Service-delivery review devolves into status theater unless metrics drive concrete policy changes.
- PI Planning quality drops sharply when run remote-only with poor tooling (Miro lag, audio chaos).
- Scrum-of-Scrums turns into a status round-robin instead of a dependency-resolution forum.
- Inspect-and-Adapt actions don't survive into the next PI without an owner + tracking artifact.
- Kanban metrics (cycle time, throughput) need ≥6 weeks of clean data before they're trustworthy.

## Agentic workflow
A "ceremony-prep" subagent ingests the team's board state (via Jira/Linear API) and generates the agenda + pre-read for the next ceremony — replenishment list, SDR metrics deck, retro themes from cycle-time outliers. A "ceremony-scribe" agent attends (transcript or summary input) and produces structured outputs: action items with owners, policy changes, WIP-limit adjustments. A third "ceremony-tracker" agent posts unresolved items to the next ceremony's input automatically.

### Recommended subagents
- `kanban-flow-analyst` — pulls cycle/lead time, throughput, WIP from API; flags outliers, aging items.
- `replenishment-prepper` — orders the "Ready" queue by priority × age × dependency, returns top-N picks.
- `pi-planning-facilitator` — generates the PI agenda, capacity sheet, dependency board template per team.
- `inspect-adapt-tracker` — captures I&A action items into the program backlog with owners + due dates.
- `faion-feature-executor` — already in repo; can be invoked to walk SDD tasks once they're committed in PI plan.

### Prompt pattern
```
You are kanban-flow-analyst. Inputs: JSON list of issues with state, entered_state_at,
exited_state_at, wip_limit per column. Output: Markdown brief with throughput
(items/week, last 4 weeks), avg cycle time per state, WIP vs limit, list of items aged > 2x
median cycle time. Do not infer reasons — only report numbers.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` | Pull board state, JQL queries for cycle time | https://github.com/ankitpokhrel/jira-cli |
| Linear GraphQL via `gh`-style script | Fetch cycle times for Linear teams | https://developers.linear.app |
| `actionable-agile` data export | Cycle-time scatter, CFD export → CSV → agent | https://www.actionableagile.com/ |
| `pandas` + `matplotlib` | Render flow metrics for SDR | `pip install pandas matplotlib` |
| Miro REST API | Generate PI Planning board scaffolds programmatically | https://developers.miro.com |
| Mural REST API | Same, for Mural-based PI Planning | https://developers.mural.co |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira + Advanced Roadmaps | SaaS | Yes — REST API | Native SAFe support; PI plans live as initiatives. |
| Azure DevOps + Boards | SaaS | Yes — REST API | Built-in delivery plans; suits SAFe ART structure. |
| Atlassian Jira Align | SaaS | Partial — REST API | Purpose-built SAFe tool, expensive, agent integration limited. |
| Targetprocess / Apptio | SaaS | Yes — REST API | Strong SAFe portfolio views, agent-driven dashboards possible. |
| Kanbanize / Businessmap | SaaS | Yes — REST API | First-class Kanban metrics, SLA, flow analytics. |
| LeanKit (Planview) | SaaS | Yes — REST API | Multi-team Kanban with portfolio views. |
| Miro / Mural | SaaS | Yes — REST API | PI Planning board orchestration; agents can pre-build sticky-note layouts. |
| Linear | SaaS | Yes — GraphQL | Cycles map to iterations; weak SAFe support. |

## Templates & scripts
See `templates.md` for the SDR dashboard layout and PI Planning board scaffold. Inline cycle-time stats (`scripts/cycle_stats.py`):

```python
#!/usr/bin/env python3
"""Compute throughput and cycle-time stats from JSONL of issues."""
import json, sys, statistics
from datetime import datetime, timedelta, timezone

issues = [json.loads(l) for l in sys.stdin]
now = datetime.now(timezone.utc)
done = [i for i in issues if i["state"] == "Done"
        and datetime.fromisoformat(i["resolved_at"]) > now - timedelta(days=28)]
cycle = [(datetime.fromisoformat(i["resolved_at"])
         - datetime.fromisoformat(i["started_at"])).total_seconds() / 86400
         for i in done if i.get("started_at")]
print(f"throughput_28d={len(done)}  weekly={len(done)/4:.1f}")
if cycle:
    print(f"cycle_p50={statistics.median(cycle):.1f}d  "
          f"cycle_p85={statistics.quantiles(cycle, n=20)[16]:.1f}d  "
          f"max={max(cycle):.1f}d")
```

## Best practices
- Throughput + 85th-percentile cycle time beats velocity for forecasting; use Monte Carlo on these for date predictions.
- For PI Planning, lock the agenda exactly; teams that "tweak" it lose 30 minutes per ceremony to confusion.
- Run replenishment with the PO + tech lead only; opening it to "anyone interested" turns a 30-min meeting into 90.
- Make WIP limits a first-class column setting with a hard block (Jira Premium / Linear Cycles) — soft warnings get ignored.
- Track I&A actions in the same backlog as features; otherwise they get prioritized to zero.
- For remote PI Planning, pre-build the program board the day before; live-creation kills momentum.

## AI-agent gotchas
- Agents trained on Scrum default to sprint-thinking; explicitly tell them "this team uses Kanban, no sprints, WIP-limited."
- Cycle-time math: define "started" precisely (entered "In Progress" vs. assignee set). LLMs guess inconsistently.
- SAFe terminology overlap (PI vs. Iteration, Feature vs. Story) — pin definitions in the system prompt or get garbage outputs.
- An agent generating retro themes from comments often surfaces venting, not actionable signal — filter for verbs.
- Confidence-vote scores look like data but are social signals; do not feed raw to forecasting models.
- Time-zone math for distributed PI Planning: pass explicit IANA TZ strings, never "PST" / "EST".

## References
- https://www.kanban.university/kanban-guide/
- https://scaledagileframework.com/pi-planning/
- "Actionable Agile Metrics for Predictability" (Daniel S. Vacanti)
- https://www.atlassian.com/agile/kanban/metrics
- "Kanban: Successful Evolutionary Change for Your Technology Business" (David J. Anderson)
