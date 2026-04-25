# Agent Integration — Hybrid Delivery

## When to use
- Programs combining hardware + software, or firmware + cloud (medical device, automotive, IoT) where physical-world milestones are predictive and digital iteration is agile.
- Regulated software (FDA, FAA, ISO 26262, SOX, GDPR) needing stage gates / V-model evidence on top of agile execution.
- Enterprise transformation rollouts: portfolio level uses milestones + budget cycles, delivery teams use Scrum/Kanban.
- Vendor + internal team mixes where vendor contracts are fixed-bid (predictive) and internal teams iterate.
- Cloud-platform programs running DevOps + Agile for delivery while ops/finance/security gate on monthly/quarterly reviews.
- Pairing with `agile-hybrid-approaches/` (deeper hybrid taxonomy), `change-control/` (gate decisions), `pm-tool-selection/` (tool fit), `earned-value-management/` (predictive arm metrics), `agile-ceremonies-setup/` (agile arm rituals).

## When NOT to use
- Pure software-only product team with autonomous backlog and no compliance gates — full Scrum or Kanban is simpler.
- Tiny startup (<10 people) where ceremony overhead exceeds coordination value — pick one mode and stick.
- Pure construction / fixed-scope delivery where iteration adds risk without value — stay predictive.
- Cargo-cult adoption "we do hybrid" without explicit boundaries — that is incoherence, not hybrid; refuse and force a real method choice.

## Where it fails / limitations
- Boundary ambiguity is the dominant failure mode. If you cannot draw a literal line between "agile here, predictive there" on an architecture or org diagram, the model collapses into status theatre.
- Two cadences = two rhythms = two definitions of "done". Without a translation layer (e.g., epic ↔ work package), reporting is incoherent at the steering committee level.
- Tool sprawl: backlog in Jira, gantt in MS Project, deliverables in SharePoint — agents spend more tokens reconciling than executing. One canonical work-graph is required.
- Governance drift: the predictive arm enforces a stage gate, the agile arm flies through it; or vice versa, agile is gated to a quarterly cadence and dies. Gate frequency must match risk profile, not legacy habit.
- Hybrid often hides a political compromise (PMO wants control, teams want autonomy). Failure here is organizational, not methodological.
- Earned-value metrics on the agile arm are misleading — story points are not labour cost. Convert with care or do not.

## Agentic workflow
Model the program as a single work-graph (`program.yaml`): top-level milestones (predictive arm) decompose into epics, epics into team backlogs (agile arm). A subagent maintains the graph, flags inconsistencies (e.g., epic past its milestone date with <50% issues done), and drafts gate-review packs from the underlying issue tracker. The "translation layer" is owned by a custom agent that keeps stage-gate vocabulary (deliverable, baseline, variance) reconciled with agile vocabulary (story, increment, velocity). Never let the agent unilaterally close a stage gate — gate decisions are sponsor calls.

### Recommended subagents
- `faion-sdd-executor-agent` — executes hybrid setup as SDD tasks: TASK_program_charter, TASK_gate_definitions, TASK_team_cadence_setup, TASK_translation_layer_setup.
- A custom `program-graph-curator-agent` (model: sonnet per README Agent Selection): maintains `program.yaml`, syncs to Jira/Linear/MS Project, computes milestone-vs-epic-vs-issue alignment.
- A custom `gate-review-pack-agent` (model: sonnet): one week before each gate, assembles deliverables list, evidence links, risk register slice, EVM snapshot, and produces a draft pack PR.
- A custom `cadence-translator-agent` (model: haiku): converts agile cycle reports into predictive-arm vocabulary for steering-committee consumption.
- A custom `dual-rhythm-coach-agent` (model: opus): activated when team velocity diverges >25% from milestone burn; produces options memo (re-baseline, drop scope, add capacity, change cadence).
- `password-scrubber-agent` — runs over gate-review packs before distribution; predictive-arm packs frequently leak credentials in screenshots.

### Prompt pattern
Two-step: graph integrity check → translation.

```
You are the program-graph-curator agent. Inputs: program.yaml (milestones,
epics, team mappings) and a JQL/GraphQL pull of issues by epic.

For each milestone, emit STRICT JSON:
{ "milestone_id": "M-NN", "due": "YYYY-MM-DD", "epics": [...],
  "issues_total": N, "issues_done": N, "pct_complete": 0.NN,
  "burn_status": "ahead|on|behind|at_risk",
  "gate_readiness": "ready|gaps|blocked",
  "gaps": ["..."], "evidence_links": ["..."] }

Rules: do not invent issues. burn_status comes from arithmetic only. gate_readiness
must cite specific gaps if not "ready". Flag any epic with no team owner or no
linked issues as "ORPHAN".
```

Translation prompt: `Convert this cycle report into steering-committee predictive-arm vocabulary. Map: story → deliverable, increment → milestone progress, velocity → planned-vs-actual labour. Preserve dates and quantities exactly. Do not editorialize.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + tags | Tag releases at gate decisions; git history = audit trail of gate outcomes | preinstalled |
| `gh` / `glab` | Drive epic-level boards (predictive view) and issue-level boards (agile view) | https://cli.github.com / https://gitlab.com/gitlab-org/cli |
| `jira-cli` | JQL queries to pull cross-team status into program graph | https://github.com/ankitpokhrel/jira-cli |
| `python-pptx` / `pandoc` | Render gate-review packs from markdown into the format the steering committee will accept | `pip install python-pptx` / https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Render gantts + dependency diagrams from `program.yaml` | `npm i -g @mermaid-js/mermaid-cli` |
| `ganttproject-cli` / `taskjuggler` | Compute critical path and forecast on the predictive arm | http://taskjuggler.org |
| `mpxj` (Java) | Read/write MS Project `.mpp` files for orgs that mandate them | https://www.mpxj.org |
| `dvc` / `lakeFS` | Version control for non-code deliverables (CAD, datasets) on the predictive arm | https://dvc.org / https://lakefs.io |
| `pre-commit` | Block edits to `program.yaml` that change milestone dates without rationale | https://pre-commit.com |
| `yq` / `jq` | Read/patch the program graph and JSON exports | `apt install yq jq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (+ Advanced Roadmaps / Plans) | SaaS | REST v3 + JQL | Common hybrid host: epics+milestones in Plans, issues in team boards. |
| Microsoft Project + Project for the Web | SaaS | Graph + REST | Enterprise gantt + portfolio; predictive-arm SoT. Pair with Azure DevOps for agile arm. |
| Azure DevOps | SaaS | REST API | Native hybrid: portfolio Plans, team Boards, Pipelines for DevOps arm. |
| GitLab Premium/Ultimate (Roadmaps + Boards + Iterations) | SaaS/OSS | REST + GraphQL | Single-pane hybrid alternative; agent-friendly via GraphQL. |
| Smartsheet | SaaS | REST API | Portfolio gantts + dashboards for orgs already on Smartsheet. |
| Asana (Portfolios) | SaaS | REST API | Portfolio-level milestones with team-level boards underneath. |
| ClickUp | SaaS | REST API | All-in-one with goals + sprints; reporting depth limited at scale. |
| Monday.com | SaaS | GraphQL | Portfolio + agile boards; weak EVM. |
| ServiceNow SPM (formerly ITBM) | SaaS | REST + ScriptedREST | Heavy enterprise PPM; required where governance is the constraint. |
| Planview / Clarity | SaaS | REST | Portfolio + EVM-grade tooling; expensive; agent integration via REST. |
| Confluence / Notion | SaaS | REST API | Charters, gate-review packs, decision records — pair with the work-graph host. |
| OpenProject / Redmine / Tuleap | OSS | REST API | Self-hosted hybrid hosts for regulated/airgapped orgs. |
| Targetprocess (Apptio) | SaaS | REST | SAFe-aligned hybrid PPM. |
| Hansoft (Perforce) | SaaS/on-prem | REST | Game/aerospace heritage; backlog + gantt in one. |

## Templates & scripts
The README provides hybrid-pattern decision tables and best-practices. Inline below: a Python script that reads `program.yaml` and prints alignment between milestones (predictive) and epic completion (agile).

```python
#!/usr/bin/env python3
"""hybrid_alignment.py — flag epics misaligned with their milestone."""
from __future__ import annotations
import datetime as dt
import pathlib
import sys
import yaml

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
                issues.append(f"{label}: AT RISK ({days_left}d left, {pct:.0%})")
            elif not epic.get("team"):
                issues.append(f"{label}: ORPHAN (no team)")
    if issues:
        sys.stderr.write("\n".join(issues) + "\n")
        return 1
    sys.stdout.write("All epics aligned with milestones.\n")
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Run nightly; failure opens a triage issue assigned to the program PM.

## Best practices
- Draw the boundary explicitly: name in writing which deliverables are predictive (charter, contracts, regulatory submissions, hardware BOMs) and which are agile (software increments, user research, internal services). Boundary in `program.yaml`.
- Single backlog of epics, multiple team backlogs of stories — never two competing portfolios. Reconcile in code, not in slides.
- Choose tool count to match boundary count: ideally one tool spans both arms (Azure DevOps, GitLab Ultimate, Jira+Plans). Two tools max with explicit sync; three or more is a smell.
- Make the gate cadence proportional to risk — monthly for regulated, quarterly for steady-state, never weekly (that is just a status meeting).
- Define one "translation table" (epic ↔ deliverable, story-points ↔ effort estimate, velocity ↔ run rate) and use it for every steering report.
- Run agile teams on agile rituals, predictive workstreams on stage gates — do not force standups onto regulatory submissions or gantt charts onto user-research.
- DevOps + Agile arm: pair with `cicd-engineer/` and `infrastructure-engineer/` skills; ship on demand, do not let governance throttle deployment frequency.
- Re-baseline predictively only when scope or contract changes; do not re-baseline because velocity slipped — that is for retros.
- Train both PMs and Scrum Masters on the other side; the dominant cultural failure is "agile coach distrusts gantts" or "PM distrusts standups".
- Budget for change-management explicitly — hybrid programs fail more on org change than on method.

## AI-agent gotchas
- Agents over-summarize hybrid programs as "behind" because they conflate vocabulary; force the agent to report agile metrics in agile units and predictive metrics in predictive units.
- LLMs auto-translate epics into "deliverables" and lose information (acceptance criteria collapse to one line). Keep both views; never destroy the agile detail.
- Date arithmetic is unreliable across calendar conventions (work days vs. calendar days, fiscal vs. ISO weeks). Hard-code the convention in the prompt and have a tool, not the LLM, compute deltas.
- Stage-gate "go / no-go" decisions must never be auto-emitted — flag readiness only, leave the call to the sponsor.
- EVM on agile arm is a trap: agents will earnestly compute SPI/CPI from story points × hourly rate. Refuse unless the conversion is explicitly defined and accepted by finance.
- Cross-tool sync drift: if Jira and MS Project disagree, the agent will pick the latest; pick the system of record per field instead and pin it in `program.yaml`.
- Vocabulary leakage: predictive arm uses "milestone", "deliverable", "baseline"; agile arm uses "increment", "story", "velocity". Force terminology per audience or executives lose trust.
- Bulk gate-pack generation is a leak risk — every pack often pulls from confidential decks/screenshots. Run `password-scrubber-agent` and a manual review before sharing.
- Long-context drift: program graphs >50 epics blow context. Page by milestone or workstream and operate on slices.
- Human-in-the-loop checkpoints (mandatory): boundary changes, gate decisions, re-baselining, cadence changes for any team, vendor escalations.

## References
- PMI PMBOK 7e — Development Approach and Life Cycle Performance Domain.
- PMI Agile Practice Guide — hybrid life cycle patterns (incremental, iterative, hybrid).
- SAFe (Scaled Agile Framework) — Portfolio + Large Solution + Essential layers as a hybrid blueprint.
- Disciplined Agile Delivery (DAD, now part of PMI) — explicit hybrid life cycle selection.
- ISO 21502 — guidance on tailoring development approach.
- Reinertsen, "The Principles of Product Development Flow" — queueing rationale for hybrid cadences.
- Sibling methodologies in this repo: `agile-hybrid-approaches/`, `change-control/`, `pm-tool-selection/`, `earned-value-management/`, `agile-ceremonies-setup/`.
