# Agent Integration — Project Integration Management

## When to use
- Programs with ≥2 workstreams whose decisions interact (e.g., scope ↔ schedule ↔ cost ↔ vendor) and need a single integrating role.
- Initiation phase: drafting the project charter to authorize work and bind sponsor commitment.
- Change-heavy environments where every CR has cross-area impact (scope + schedule + cost + risk simultaneously).
- Multi-team / multi-vendor delivery where each team optimizes locally and the program needs whole-system optimization.
- Closure: final integration, lessons learned, formal acceptance, contract closeout.
- Pairing with `change-control/`, `change-management/`, `lessons-learned/`, `scope-management/`, `schedule-development/`, `cost-estimation/`, `risk-register/`, `quality-management/`, `procurement-management/`, `communications-management/`, `stakeholder-engagement/`.

## When NOT to use
- Single-team / single-stream work with a stable backlog — Scrum or Kanban already integrates within the team.
- Short tactical engagements (<4 weeks) with no inter-area trade-offs — overhead exceeds value.
- Pure research / discovery phases with no committed scope — wait until charter signal is real.
- Solo-developer projects — the integrator is one person; the artifacts can be lightweight (one-page charter, README).

## Where it fails / limitations
- "Integration" is the easiest dimension to skip on paper — every plan claims integration; few enforce it. Without a single source of truth, integration degrades to status theatre.
- Charter rot: charters get signed and forgotten. If the charter does not change when scope/budget change, downstream teams use a stale "north star".
- Change control without integration becomes whack-a-mole — scope CR approved, schedule and cost not updated, baselines drift apart.
- Knowledge-area silos at the PMO produce inconsistent plans (schedule from MS Project, cost from Excel, risk in Confluence) that drift within weeks.
- "Single source of truth" claims fail in practice when humans edit derivatives instead of the source — locked workflows are mandatory.
- Solopreneurs treat integration as an afterthought; the README's solopreneur section is correct but rarely practiced.
- Status-report fatigue substitutes for actual integration decisions — colour codes without action are noise.

## Agentic workflow
Treat the program as a YAML "integrated plan" file (`integrated/plan.yaml`) referencing baselines for scope (WBS), schedule (gantt/critical path), cost (budget + EVM), risks, quality, resources, comms, procurement. A subagent maintains the integrated plan, runs cross-area impact analysis on every change request, drafts updated baselines as PRs, and emits the GREEN/YELLOW/RED status programmatically from baseline thresholds. The charter lives in the same repo (`charter.md`) and is amended via PR, not silently. Decisions log (`decisions/YYYY-MM-DD-slug.md`) is mandatory for every approved CR.

### Recommended subagents
- `faion-sdd-executor-agent` — drives integration setup as SDD tasks: TASK_charter, TASK_integrated_plan, TASK_change_control_process, TASK_status_dashboard, TASK_closure.
- A custom `charter-author-agent` (model: opus per README "Strategic decision"): drafts the charter from kickoff inputs, drives sponsor sign-off, captures assumptions, constraints, and high-level risks.
- A custom `change-impact-agent` (model: sonnet): given a CR, computes impact across scope/schedule/cost/quality/risk/resources from the integrated plan; emits a markdown impact memo with recommendation.
- A custom `baseline-curator-agent` (model: sonnet): keeps the integrated plan consistent — flags scope without schedule, schedule without cost, risks without owners.
- A custom `status-reporter-agent` (model: haiku per README "Apply established patterns"): renders the README "Project Status Report" template from numeric inputs only — colour follows thresholds, never tone.
- A custom `closure-agent` (model: sonnet): runs the README closure checklist, archives plans, captures lessons learned, generates final acceptance documentation.
- `password-scrubber-agent` — runs over charter/status/closure docs before distribution; integration artifacts are top leak paths.

### Prompt pattern
Two-step: charter authoring → integrated change analysis.

```
You are the change-impact agent. Inputs:
1. Approved change request (CR-NN.md): scope description, requestor, priority.
2. integrated/plan.yaml: scope (WBS), schedule, cost, risks, quality, resources.
3. Threshold table: GREEN/YELLOW/RED triggers per dimension.

Emit STRICT MARKDOWN:
## Impact Analysis CR-NN
| Area | Current | Proposed | Delta | Status | Notes |
|------|---------|----------|-------|--------|-------|

## Recommendation
- decision: approve | reject | conditional
- conditions: [ ... ]
- new_baseline_required: true|false
- communications: [ stakeholders to notify ]

Rules:
- Numbers come from inputs; never invent.
- Status follows threshold table verbatim.
- Recommend `reject` if any dimension goes RED without compensating
  trade-off elsewhere.
- Cite at least one risk-register entry if risk delta is non-zero.
```

Charter prompt: `Draft a charter using the README template. Every SMART objective must cite a measurable success criterion. Constraints and assumptions must be explicit; if unknown, list as "TO_CONFIRM". Sponsor signature line is mandatory.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + branch protection | Charter and integrated plan as code; PR gates sponsor sign-off | preinstalled |
| `gh` / `glab` | Drive change-request issues, link to PRs that update baselines | https://cli.github.com / https://gitlab.com/gitlab-org/cli |
| `yq` / `jq` | Read/patch `integrated/plan.yaml`; aggregate dependencies | `apt install yq jq` |
| `python-docx` / `python-pptx` / `pandoc` | Render charter, status reports, closure docs to org-required formats | `pip install python-docx python-pptx` / https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Render integration diagrams (scope ↔ schedule ↔ cost) and status dashboards | `npm i -g @mermaid-js/mermaid-cli` |
| `mpxj` | Read/write MS Project `.mpp` schedules from the integrated plan | https://www.mpxj.org |
| `taskjuggler` / `ganttproject-cli` | Compute critical path locally from YAML | http://taskjuggler.org |
| `dvc` / `lakeFS` | Version control for non-code deliverables (CAD, datasets) referenced from the plan | https://dvc.org |
| `pre-commit` | Block edits to `charter.md` or baselines without rationale and sponsor reviewer | https://pre-commit.com |
| `make` / `just` | Standardize "build status pack" / "render closure" tasks | https://github.com/casey/just |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Microsoft Project + Project for the Web | SaaS / desktop | Graph + REST | Dominant predictive tool; integrates with Teams + Power BI for status. |
| Smartsheet | SaaS | REST | Portfolio gantt + dashboards; common integration target. |
| Asana (Portfolios) / ClickUp (Goals) / Monday | SaaS | REST/GraphQL | Lightweight portfolio with built-in status fields; weak EVM. |
| Jira (with Plans / Advanced Roadmaps) | SaaS | REST + JQL | Common host; integrate via cross-project dashboards. |
| Azure DevOps | SaaS | REST | Hybrid host: portfolio Plans + team Boards + Pipelines. |
| GitLab Premium/Ultimate (Roadmaps + Boards + Iterations) | SaaS / OSS | REST + GraphQL | Single-pane integration alternative for engineering-heavy programs. |
| ServiceNow SPM (formerly ITBM) | SaaS | REST | Heavy enterprise PPM with full integration; required where governance is the constraint. |
| Planview / Clarity / Sciforma | SaaS | REST | Portfolio + EVM-grade tooling for large enterprises. |
| Confluence / Notion / Coda | SaaS | REST | Charter, decisions, status home; pair with the work-graph host. |
| OpenProject / Redmine / Tuleap | OSS | REST | Self-hosted hosts for regulated/airgapped orgs. |
| Power BI / Tableau / Looker | SaaS | REST/SDK | Status dashboards aggregating across tools. |
| Slack / MS Teams | SaaS | REST + Events | Status digest delivery; throttle to avoid noise. |
| DocuSign / Adobe Sign | SaaS | REST | Charter sign-off, formal acceptance. |
| Box / SharePoint / Drive | SaaS | REST | Repository for non-code deliverables; pair with `dvc` for versioning. |

## Templates & scripts
The README provides Project Charter and Project Status Report templates plus a solopreneur weekly check. Inline below: a script that validates the integrated plan and emits a colour-coded status snapshot.

```python
#!/usr/bin/env python3
"""integration_status.py — emit GREEN/YELLOW/RED per area from numeric inputs."""
from __future__ import annotations
import pathlib
import sys
import yaml

THRESHOLDS = {
    "schedule_slip_days":  [(0, "GREEN"), (5, "YELLOW"), (15, "RED")],
    "budget_overrun_pct":  [(0.00, "GREEN"), (0.05, "YELLOW"), (0.10, "RED")],
    "open_high_risks":     [(0, "GREEN"), (2, "YELLOW"), (5, "RED")],
    "scope_change_pct":    [(0.00, "GREEN"), (0.10, "YELLOW"), (0.20, "RED")],
    "defect_rate_pct":     [(0.00, "GREEN"), (0.05, "YELLOW"), (0.10, "RED")],
}

def status_for(value: float, ladder: list[tuple[float, str]]) -> str:
    label = ladder[0][1]
    for threshold, lbl in ladder:
        if value >= threshold:
            label = lbl
    return label

def main(path: str = "integrated/plan.yaml") -> int:
    plan = yaml.safe_load(pathlib.Path(path).read_text())
    metrics = plan.get("metrics", {})
    print(f"{'Area':<22} {'Value':>10}  Status")
    overall = "GREEN"
    rank = {"GREEN": 0, "YELLOW": 1, "RED": 2}
    for area, ladder in THRESHOLDS.items():
        if area not in metrics:
            print(f"{area:<22} {'MISSING':>10}  RED")
            overall = "RED"
            continue
        v = float(metrics[area])
        s = status_for(v, ladder)
        print(f"{area:<22} {v:>10.2f}  {s}")
        if rank[s] > rank[overall]:
            overall = s
    print(f"{'OVERALL':<22} {'':>10}  {overall}")
    return 0 if overall != "RED" else 1

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Wire to weekly CI; output feeds the status-reporter-agent draft.

## Best practices
- Single source of truth for the integrated plan (one YAML file, one repo). Derivatives (slides, docs, dashboards) are generated; never hand-edited.
- Charter as code: `charter.md` lives in the project repo, sponsor approves via PR review with signed commit. Amendments require a new PR, not a stealth edit.
- One decision log per project (`decisions/`), one ADR-style entry per integrated change. Search-first cultures depend on this.
- Status colour driven by numeric thresholds, never PM mood. Force the threshold table into the plan so the agent computes status, the human interprets it.
- Every change request triggers cross-area impact analysis before approval; the impact memo is committed alongside the CR.
- Re-baseline only when scope/budget/contract changes, not when velocity slips. Re-baselining for slip masks chronic delivery problems.
- Run an integration check weekly: scope without schedule? schedule without cost? risks without owners? — automate and open issues.
- For solopreneurs: keep the artifact lightweight (one-page charter, weekly integration check), but keep it. Skipping integration is the most common solopreneur failure.
- Closure is integration's last mile — formal acceptance + lessons learned + archive happens once, not after the team scatters.
- Pair integration with EVM (`earned-value-management/`) for predictive arms; with cycle-time / WIP for agile arms; never with both metric-sets uncritically combined.
- Keep change-control velocity moderate — too few CRs hides chaos; too many drown the integrator. Aim for batched weekly review.
- Train sponsors on what they sign — most integration failures are sponsor-driven (silent scope additions).

## AI-agent gotchas
- Agents over-summarize: an LLM declaring "GREEN — on track" without numeric backing is the dominant failure. Force colour from threshold arithmetic, not narrative.
- Charter generators hallucinate constraints and assumptions to look thorough. Force any unknown to be `TO_CONFIRM` and tracked as an open question.
- Change-impact analyses miss second-order effects (a 2-week delay shifts dependencies onto a holiday, breaking a vendor deadline). Force a critical-path recompute, not a delta on duration only.
- Cross-area trade-offs: agents propose "approve all CRs" by default. Force a budget-gate (cumulative scope-change cap) into the plan.
- Status report metric lifting: agents pull from the wrong source-of-truth (e.g., manager's spreadsheet vs. canonical YAML). Lock per-metric source.
- Charter sign-off automation is forbidden; the agent prepares the PR, the sponsor approves the merge.
- "Integrated" reports that secretly come from one knowledge area only — agents that only have access to Jira will produce schedule-blind reports. Force input audit.
- Long-context drift: integrated plans >500 lines blow context. Page by knowledge area; persist summaries, rehydrate.
- Confidentiality: charter and CR memos contain budgets, vendor names, customer info. Scrub before any third-party model call.
- Decision log entries get duplicated by parallel agents; force a unique-ID generator and lock.
- Closure shortcuts: agents skip lessons learned because there's no code change. Force the closure checklist to fail-close if lessons file is empty.
- Human-in-the-loop checkpoints (mandatory): charter approval, baseline changes, change-request approval, status colour shifts (especially RED), closure declaration.
- Stakeholder communication: integration outcomes belong to humans; agents draft status, humans deliver to executives and regulators.

## References
- PMI PMBOK 6e — Integration Management Knowledge Area (templates and processes still useful).
- PMI PMBOK 7e — Tailoring + Performance Domains (Planning, Project Work, Delivery, Measurement).
- ISO 21500 / 21502 — international guidance on integration and tailoring.
- Kotter "Leading Change" — change rollout principles applied to integrated change control.
- Reinertsen "The Principles of Product Development Flow" — queueing theory for integrated cadences.
- Sibling methodologies: `change-control/`, `lessons-learned/`, `scope-management/`, `schedule-development/`, `cost-estimation/`, `risk-register/`, `quality-management/`, `procurement-management/`, `communications-management/`, `stakeholder-engagement/`.
- BA `solution-assessment/` — closure-side evaluation pairing with project closure.
