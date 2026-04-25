# Agent Integration — Hybrid Delivery

## When to use
- Programs with hardware + software components (medical device, automotive, IoT) — physical milestones predictive, firmware iterative.
- Regulated software (FDA, FAA, ISO 26262, SOX, GDPR) needing stage gates / V-model evidence on top of agile execution.
- Enterprise transformation rollouts: portfolio level uses milestones + budget cycles, delivery teams use Scrum/Kanban.
- Vendor + internal team mixes where vendor work is fixed-bid (predictive) and internal teams iterate.
- Cloud platforms running DevOps + Agile for delivery while ops/finance/security gate quarterly.
- Pair with `agile-hybrid-approaches/`, `change-control/` (gate decisions), `pm-tools-overview/` (tool fit), `value-stream-management/` (flow metrics across both arms).

## When NOT to use
- Pure software product team with autonomous backlog and no compliance — full Scrum or Kanban is simpler.
- Tiny startup (<10 people) — ceremony overhead exceeds coordination value.
- Pure construction / fixed-scope build where iteration adds risk without value — stay predictive.
- Cargo-cult "we do hybrid" with no explicit boundary — that is incoherence; force a real method choice.

## Where it fails / limitations
- Boundary ambiguity is the dominant failure mode. If you cannot draw a literal line on the architecture or org chart between agile-here / predictive-there, the model collapses into status theatre.
- Two cadences = two definitions of "done". Without a translation layer (epic ↔ work package), reporting is incoherent at the steering committee level.
- Tool sprawl: backlog in Jira, gantt in MS Project, deliverables in SharePoint — agents waste tokens reconciling. One canonical work-graph required.
- Governance drift: predictive arm enforces a gate, agile arm flies through it; or agile gets gated to a quarterly cadence and dies. Match gate frequency to risk profile.
- Hybrid often hides a political compromise (PMO wants control, teams want autonomy). Failure here is organizational, not methodological.
- Earned-value on the agile arm is misleading — story points are not labour cost. Convert with care or do not.

## Agentic workflow
Model the program as a single work-graph (`program.yaml`): milestones (predictive) decompose into epics, epics into team backlogs (agile). A subagent maintains the graph, flags inconsistencies (epic past its milestone date with <50% issues done), and drafts gate-review packs from the underlying issue tracker. A "translation layer" agent keeps stage-gate vocabulary (deliverable, baseline, variance) reconciled with agile vocabulary (story, increment, velocity). Never let an agent unilaterally close a stage gate — gate decisions are sponsor calls.

### Recommended subagents
- `faion-sdd-executor-agent` — runs hybrid setup as SDD tasks (program charter, gate definitions, team cadence, translation layer).
- `program-graph-curator` (sonnet) — maintains `program.yaml`, syncs to Jira/Linear/MS Project, computes milestone-vs-epic alignment.
- `gate-review-pack` (sonnet) — one week before each gate, assembles deliverables list, evidence links, risk-register slice, EVM snapshot, drafts pack PR.
- `cadence-translator` (haiku) — converts agile cycle reports into predictive-arm vocabulary for steering-committee.
- `dual-rhythm-coach` (opus) — activated when team velocity diverges >25% from milestone burn; produces options memo (re-baseline, drop scope, add capacity, change cadence).
- `password-scrubber-agent` — runs over gate-review packs before distribution; predictive packs frequently leak credentials in screenshots.

### Prompt pattern
```
You are program-graph-curator. Inputs: program.yaml (milestones, epics, team
mappings) and a JQL pull of issues by epic. For each milestone, emit STRICT
JSON: { "milestone_id": "M-NN", "due": "YYYY-MM-DD", "epics": [...],
"issues_total": N, "issues_done": N, "pct_complete": 0.NN,
"burn_status": "ahead|on|behind|at_risk",
"gate_readiness": "ready|gaps|blocked", "gaps": [...], "evidence_links": [...] }
Rules: do not invent issues. burn_status is arithmetic only. Flag any epic
with no team owner or no issues as "ORPHAN".
```

```
Convert this cycle report into steering-committee predictive-arm vocabulary.
Map: story → deliverable, increment → milestone progress, velocity →
planned-vs-actual labour. Preserve dates and quantities exactly. No editorial.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + tags | Tag releases at gate decisions; git history = audit trail | preinstalled |
| `gh` / `glab` | Drive epic-level boards (predictive view) and issue boards (agile view) | https://cli.github.com / https://gitlab.com/gitlab-org/cli |
| `jira-cli` | JQL queries to pull cross-team status into program graph | https://github.com/ankitpokhrel/jira-cli |
| `python-pptx` / `pandoc` | Render gate-review packs from markdown into committee format | `pip install python-pptx` / https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Render gantts + dependency diagrams from `program.yaml` | `npm i -g @mermaid-js/mermaid-cli` |
| `taskjuggler` | Compute critical path on the predictive arm | http://taskjuggler.org |
| `mpxj` (Java) | Read/write MS Project `.mpp` for orgs that mandate them | https://www.mpxj.org |
| `pre-commit` | Block edits to `program.yaml` that change milestone dates without rationale | https://pre-commit.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira + Advanced Roadmaps / Plans | SaaS | REST v3 + JQL | Common hybrid host: epics+milestones in Plans, issues in team boards. |
| Microsoft Project + Project for the Web | SaaS | Graph + REST | Enterprise gantt + portfolio; predictive-arm SoT. |
| Azure DevOps | SaaS | REST | Native hybrid: portfolio Plans, team Boards, Pipelines for DevOps arm. |
| GitLab Premium/Ultimate (Roadmaps + Boards + Iterations) | SaaS/OSS | REST + GraphQL | Single-pane hybrid alternative. |
| Smartsheet | SaaS | REST | Portfolio gantts + dashboards. |
| Asana Portfolios | SaaS | REST | Portfolio-level milestones with team-level boards. |
| Planview / Clarity | SaaS | REST | Portfolio + EVM-grade tooling; expensive. |
| OpenProject / Redmine | OSS | REST | Self-hosted hybrid hosts for regulated/airgapped orgs. |
| Targetprocess (Apptio) | SaaS | REST | SAFe-aligned hybrid PPM. |
| Confluence / Notion | SaaS | REST | Charters, gate-review packs, decision records. |

## Templates & scripts
README provides decision tables and best-practices. Inline below: a Python script that flags milestone/epic misalignment.

```python
#!/usr/bin/env python3
"""hybrid_alignment.py — flag epics misaligned with their milestone."""
from __future__ import annotations
import datetime as dt, pathlib, sys, yaml

def main(path: str = "program.yaml") -> int:
    program = yaml.safe_load(pathlib.Path(path).read_text())
    today = dt.date.today()
    issues: list[str] = []
    for m in program.get("milestones", []):
        due = dt.date.fromisoformat(str(m["due"]))
        days_left = (due - today).days
        for epic in m.get("epics", []):
            done = epic.get("issues_done", 0)
            total = max(epic.get("issues_total", 0), 1)
            pct = done / total
            label = f"{m['id']}/{epic['id']}"
            if days_left < 0 and pct < 1:
                issues.append(f"{label}: PAST DUE ({-days_left}d, {pct:.0%})")
            elif days_left < 14 and pct < 0.5:
                issues.append(f"{label}: AT RISK ({days_left}d, {pct:.0%})")
            elif not epic.get("team"):
                issues.append(f"{label}: ORPHAN (no team)")
    if issues:
        sys.stderr.write("\n".join(issues) + "\n")
        return 1
    print("All epics aligned with milestones.")
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Run nightly; failure opens a triage issue assigned to the program PM.

## Best practices
- Draw the boundary in writing inside `program.yaml` — name which deliverables are predictive (charter, contracts, regulatory submissions, hardware BOMs) and which are agile (software increments, user research).
- Single backlog of epics, multiple team backlogs of stories — never two competing portfolios. Reconcile in code, not slides.
- Match tool count to boundary count: ideally one tool spans both arms (Azure DevOps, GitLab Ultimate, Jira+Plans). Two max with explicit sync; three+ is a smell.
- Gate cadence proportional to risk — monthly for regulated, quarterly for steady-state, never weekly (that is just a status meeting).
- Define one "translation table" (epic ↔ deliverable, story-points ↔ effort, velocity ↔ run rate) and use it for every steering report.
- Run agile teams on agile rituals, predictive workstreams on stage gates — do not force standups on regulatory submissions or gantt charts on user-research.
- DevOps arm: pair with `cicd-engineer/` and `infrastructure-engineer/` skills; ship on demand, do not let governance throttle deployment frequency.
- Re-baseline predictively only when scope or contract changes; do not re-baseline because velocity slipped.
- Train both PMs and Scrum Masters on the other side; the dominant cultural failure is "agile coach distrusts gantts" or "PM distrusts standups".

## AI-agent gotchas
- Agents over-summarize hybrid programs as "behind" because they conflate vocabulary; force agile metrics in agile units, predictive metrics in predictive units.
- LLMs auto-translate epics into "deliverables" and lose information (acceptance criteria collapse to one line). Keep both views; never destroy detail.
- Date arithmetic is unreliable across calendar conventions (work days vs. calendar days, fiscal vs. ISO weeks). Hard-code the convention in the prompt; have a tool, not the LLM, compute deltas.
- Stage-gate "go / no-go" must never be auto-emitted — flag readiness only, leave the call to the sponsor.
- EVM on agile arm is a trap: agents will compute SPI/CPI from story points × hourly rate. Refuse unless the conversion is explicitly accepted by finance.
- Cross-tool sync drift: if Jira and MS Project disagree, pin the system of record per field in `program.yaml`.
- Vocabulary leakage: predictive uses "milestone, deliverable, baseline"; agile uses "increment, story, velocity". Force terminology per audience.
- Bulk gate-pack generation is a leak risk — packs pull from confidential decks/screenshots. Run `password-scrubber-agent` and manual review before sharing.
- Long-context drift: program graphs >50 epics blow context. Page by milestone or workstream and operate on slices.
- Human-in-the-loop checkpoints (mandatory): boundary changes, gate decisions, re-baselining, cadence changes, vendor escalations.

## References
- PMI PMBOK 7e — Development Approach and Life Cycle Performance Domain.
- PMI Agile Practice Guide — hybrid life-cycle patterns.
- SAFe — Portfolio + Large Solution + Essential layers as a hybrid blueprint.
- Disciplined Agile Delivery (DAD, now part of PMI) — explicit hybrid life-cycle selection.
- ISO 21502 — guidance on tailoring development approach.
- Reinertsen, "The Principles of Product Development Flow".
- Sibling methodologies: `agile-hybrid-approaches/`, `change-control/`, `pm-tools-overview/`, `value-stream-management/`.
