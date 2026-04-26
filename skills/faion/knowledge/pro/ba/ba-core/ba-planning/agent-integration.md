# Agent Integration — BA Planning (BABOK KA1 Fundamentals)

Scope: this file covers the **fundamentals** of BABOK Knowledge Area 1
("Business Analysis Planning and Monitoring"). It treats the methodology as
the umbrella that owns the **5 BABOK tasks** — plan BA approach, plan
stakeholder engagement, plan BA governance, plan BA information management,
identify BA performance improvements — and shows how to wire each task into
agent workflows. The sibling `business-analyst/ba-planning/agent-integration.md`
covers the broader agentic plan-as-code pattern; this file complements it by
focusing on KA1 mechanics and the **monitoring** half that the README
under-specifies.

## When to use

- A new initiative crosses the boundary from discovery to planned delivery and
  needs an explicit BA approach, stakeholder map, governance, information
  management, and performance plan — the 5 BABOK KA1 outputs.
- Programs that must demonstrate BABOK conformance to certifying bodies or
  internal QA (CCBA / CBAP audits, IIBA-aligned PMOs).
- Hybrid plan-driven + change-driven engagements where you need to declare per
  KA1 task which artifacts are baselined vs. living, and pair the plan with a
  monitoring loop.
- When activating sibling ba-core methodologies (`stakeholder-analysis/`,
  `ba-governance/`, `requirements-lifecycle/`, `elicitation-techniques/`) —
  KA1 is the seeding ceremony for all of them.
- When introducing the **performance improvement** discipline: capturing BA
  metrics (rework rate, requirement defect density, elicitation throughput)
  and feeding them back into the next plan cycle.

## When NOT to use

- Solo MVP, prototype, or research spike — KA1's five tasks are heavier than
  the work itself. Use a one-page lean canvas.
- Pure backlog-driven Scrum where the Definition of Ready already encodes the
  BA approach and the team rejects ceremony beyond it.
- Continuous-discovery contexts where requirements churn weekly; KA1 baselines
  go stale faster than they can be reviewed.
- When the sponsor will not name a governance approver — without a named
  approver, KA1 governance and information management become decorative.

## Where it fails / limitations

- The 5 KA1 tasks are presented as parallel; in practice they have ordering
  constraints (governance before information management before performance).
  Treating them as independent produces an incoherent plan.
- BABOK calls for "BA Performance Assessment" but most teams skip it because
  there are no defaults for which metrics to collect. Without metric defaults
  baked in, the monitoring loop never starts.
- Information management (where artifacts live, retention, access) is the most
  common skip; agents inherit a default of "all in Notion" which breaks
  traceability and audit.
- KA1 outputs reference each other (stakeholder list ↔ governance ↔ info
  management); duplicating instead of linking causes drift within days.
- LLMs collapse the 5 tasks into a single "BA plan" deliverable and lose the
  monitoring/performance task entirely. Force task-level outputs.
- Performance improvements need a baseline. First-time KA1 cannot measure
  improvement; budget two cycles before deriving signal.

## Agentic workflow

Model KA1 as **5 task-scoped artifacts** in a single git directory under the
project's `.product/` or `.aidocs/` tree, one Markdown file per BABOK task,
each with YAML frontmatter (`task_id`, `version`, `approver`, `last_reviewed`,
`baselined`). A planning subagent runs once at engagement kickoff producing
v0.1 of all five; a monitoring subagent runs on a fixed cadence (weekly for
performance, fortnightly for stakeholder/governance/info-management drift)
diffing the artifact set against actuals (commits, sessions held, CRs merged,
defects logged) and emitting CR patches. Replan triggers are deterministic and
encoded in `triggers.yml`: stakeholder added, scope CR merged, two missed
elicitation sessions, performance metric breach, or `last_reviewed` older than
the cadence threshold. Every CR is reviewed by the named approver via PR;
agents never push to the baseline branch.

### Recommended subagents

- `faion-sdd-executor-agent` — drives the 5 KA1 tasks as 5 SDD tasks
  (TASK-01..05) with their own commits, lifecycle (todo → in-progress → done)
  and execution reports. Plan reviews are PRs reviewed by the approver named
  in governance frontmatter.
- `faion-brainstorm` — diverge/converge for two specific KA1 decisions:
  approach selection (Plan-Driven / Change-Driven / Hybrid) and stakeholder
  engagement technique mix. Both benefit from explicit alternative generation.
- `faion-sdd-execution` (skill) — quality gates per KA1 task: did the
  approach task name an approver? does information management declare a
  retention policy? does performance plan list at least 3 measurable metrics?
- A custom `ba-kickoff-agent` (sonnet) — owns one-shot generation of all 5
  KA1 artifacts from an initiative brief plus org chart.
- A custom `ba-monitor-agent` (haiku) — runs weekly via cron, computes the
  monitoring metrics, emits a status JSON and CR patches when triggers fire.
- A custom `ba-performance-agent` (opus) — runs at engagement boundaries
  (sprint, phase, milestone) to compute BA performance KPIs from git history
  and elicitation logs, and propose process improvements for the next cycle.

### Prompt pattern

Single planner prompt that emits all 5 KA1 artifacts as separate JSON sections
keyed by task, allowing strict schema validation:

```
You are the BABOK KA1 planner. For initiative {brief}, produce the 5
artifacts of BA Planning and Monitoring:
  T1 plan_ba_approach
  T2 plan_stakeholder_engagement
  T3 plan_ba_governance
  T4 plan_ba_information_management
  T5 identify_ba_performance_improvements

Constraints:
- Constrain stakeholders to {stakeholder_seed}; flag gaps as TODO(reason).
- T5 must list >=3 measurable metrics with baseline=null and target=null on
  first cycle; do not invent baselines.
- T3 must name a single human approver; reject "leadership" or roles only.
- T4 must declare repo path, retention policy, access list.
Return JSON {T1, T2, T3, T4, T5}; each task is the frontmatter+body of its
Markdown artifact.
```

Monitoring prompt: `Given the 5 KA1 artifacts (attached) and this week's
events (commits, sessions, CRs, defects), compute drift per task and return
CR patches keyed by task_id. Cap at 5 changes per task.`

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git log --follow` | Version history of each KA1 artifact; replaces manual revision tables. | preinstalled |
| `pre-commit` | Block commits that drop required frontmatter fields per task. | https://pre-commit.com |
| `yq` | Read/update YAML frontmatter (`yq '.last_reviewed' T3-governance.md`) in cron. | `apt install yq` / `brew install yq` |
| `jq` | Validate planner JSON against the 5-task schema before persisting. | `apt install jq` |
| `gh issue` / `gh pr` | Mirror KA1 deliverables and governance gates as issues. | https://cli.github.com |
| `mermaid-cli` (`mmdc`) | Render embedded Mermaid Gantt of the engagement plan to PNG. | `npm i -g @mermaid-js/mermaid-cli` |
| `graphviz` (`dot`) | Render stakeholder map and KA1 artifact dependency graph. | `apt install graphviz` |
| `pandoc` | Convert Markdown plan to PDF/DOCX for stakeholders and auditors. | https://pandoc.org |
| `csvkit` | Aggregate metric CSVs (rework rate, defect density) for the performance task. | `pip install csvkit` |
| `taskwarrior` | CLI todo store agents read/write deterministically for activity plans. | https://taskwarrior.org |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Jira (Cloud) | SaaS | REST v3 + JQL | Each KA1 task = an Epic; deliverables = sub-tasks; performance metrics via JQL aggregations. |
| Linear | SaaS | GraphQL API | KA1 = a Project; the 5 tasks = milestones; agents transition states via `issueUpdate`. |
| Azure DevOps | SaaS | REST API | Use "Iteration Plan" + custom `ba_task` field for KA1 task tagging. |
| Confluence + Requirements blueprint | SaaS | REST API | Common enterprise default; pair with a state plugin or governance becomes free-text. |
| Notion | SaaS | REST API | OK for the human view of KA1; weak typing makes governance fields fragile — gate writes via wrapper. |
| Jama Connect | SaaS | REST + webhooks | Enterprise-grade; KA1 fits as a "project profile" item agents can update. |
| Polarion ALM | SaaS / on-prem | REST + Webservices | Strong workflow engine; map governance to Polarion workflows for regulated programs. |
| StrictDoc | OSS | CLI + plain-text | Best fit for agent flows: text-first, git-native, plan and requirements share a repo. |
| Doorstop | OSS | Python API | Markdown + YAML, scriptable from agents; good for KA1 artifact storage. |
| Smartsheet | SaaS | REST API | PMO-heavy orgs; the activity plan as a sheet, agents drive via row updates. |
| dbt + a metrics warehouse | OSS | CLI | For KA1 task 5 (performance): turn elicitation logs and git history into BA KPIs. |

## Templates & scripts

The README ships BA Approach Document and BA Activity Plan templates. Inline
below is a Python script that validates the **set of 5 KA1 artifacts** is
complete and coherent — wire into pre-commit and the weekly monitor agent.

```python
#!/usr/bin/env python3
"""ka1_check.py — verify the 5 BABOK KA1 artifacts are present and coherent."""
from __future__ import annotations
import sys, json, datetime as dt, pathlib, yaml

TASKS = {
    "T1": "plan_ba_approach",
    "T2": "plan_stakeholder_engagement",
    "T3": "plan_ba_governance",
    "T4": "plan_ba_information_management",
    "T5": "identify_ba_performance_improvements",
}
REQUIRED = {"task_id", "version", "approver", "last_reviewed", "baselined"}
CADENCE_DAYS = {"T1": 30, "T2": 14, "T3": 30, "T4": 30, "T5": 7}

def load_fm(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing frontmatter")
    return yaml.safe_load(text.split("---", 2)[1]) or {}

def main(root_str: str) -> int:
    root = pathlib.Path(root_str)
    errors: list[str] = []
    found: dict[str, dict] = {}
    for tid, slug in TASKS.items():
        candidates = list(root.glob(f"{tid}-*.md"))
        if not candidates:
            errors.append(f"{tid} ({slug}): no artifact found")
            continue
        fm = load_fm(candidates[0])
        missing = REQUIRED - set(fm)
        if missing:
            errors.append(f"{tid}: missing fields {sorted(missing)}")
        last = fm.get("last_reviewed")
        if isinstance(last, (dt.date, dt.datetime)):
            last_d = last if isinstance(last, dt.date) else last.date()
            age = (dt.date.today() - last_d).days
            if age > CADENCE_DAYS[tid]:
                errors.append(f"{tid} stale: {age}d > {CADENCE_DAYS[tid]}d")
        found[tid] = fm
    print(json.dumps({"errors": errors, "ok": not errors,
                      "tasks_found": sorted(found)}, indent=2, default=str))
    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
```

## Best practices

- Treat KA1 as **5 artifacts, not 1**. One file per BABOK task, each with its
  own approver, cadence, and lifecycle. Collapsing them into a single doc
  loses the monitoring half.
- Order the kickoff sequence: T1 approach → T2 stakeholders → T3 governance →
  T4 information management → T5 performance. Dependencies flow forward; out
  of order produces incoherent plans.
- Cadence-per-task (not one global review): performance weekly, stakeholder
  fortnightly, approach/governance/info-mgmt monthly. Encode in `triggers.yml`.
- T5 (performance) must list metrics on day one even if baselines are null.
  First cycle measures; second cycle improves. Skipping T5 = no monitoring.
- Reference, do not duplicate: the stakeholder list lives in
  `stakeholder-analysis/`, governance in `ba-governance/`, requirements
  architecture in `ba-requirements-mgmt/`. KA1 holds links and IDs only.
- Encode replan triggers as YAML the monitor agent reads, not prose. "Replan
  if X" only fires automatically if it's machine-readable.
- For regulated programs, `pandoc` each KA1 artifact to PDF and `gpg
  --detach-sign` it; auditors accept the signed bundle.
- Drive the BABOK conformance check from `ka1_check.py` in CI so the plan set
  cannot regress unnoticed.
- Use complexity tiers (S/M/L) instead of hours/days for elicitation effort —
  per repo policy, no time estimates in SDD docs.
- Pair each KA1 task with one and only one approver; CODEOWNERS by directory
  (e.g. `T3-governance.md` owned by sponsor email) makes this enforceable.

## AI-agent gotchas

- Task collapse: LLMs merge the 5 BABOK tasks into one document and silently
  drop T4 and T5. Validate output keys against the 5-task schema; reject if
  any task is missing.
- Stakeholder hallucination: agents invent plausible stakeholders ("Director
  of UX") that do not exist. Constrain to a `stakeholder_seed`; flag every
  gap as `TODO(reason)`.
- Governance dilution: agents produce vague approvers ("leadership",
  "product team"). Require an email or @-handle; reject role-only outputs.
- Performance metric confabulation: agents invent baselines for T5 on first
  cycle. Force `baseline: null` and `target: null` until two cycles of data
  exist; only the human approver may set them.
- Monitoring drift: the monitor agent silently rewrites artifacts when the
  approver is offline. Force unified diffs / CR patches, never full-doc
  overwrites; cap CRs at 5 changes per run.
- Information-management default leakage: agents default T4 to "all in
  Notion" regardless of org policy. Pass the org's storage/retention policy in
  the system prompt and reject Notion if not allowed.
- BABOK / PMBOK confusion: agents borrow PMBOK schedule language and produce
  Gantt charts for everything. KA1 governs analysis, not delivery; defer
  schedule integration to `project-manager`.
- Plan-Driven / Change-Driven binary: real programs are 70/30 hybrids. Force
  per-artifact baselined/living flags; reject pure-binary outputs.
- Frontmatter parse failures on smart-quote / em-dash injection from copy-
  paste. Pre-commit hook must reject non-ASCII in YAML keys.
- Token budget: at >50 stakeholders or >5 sibling methodology refs, do not
  load the whole KA1 set into context. Index frontmatter via `yq` and load
  full sections on demand.
- Human-in-the-loop checkpoints (mandatory): all 5 artifacts at v1.0 sign-off,
  every approach change, every governance/approver change, every CR adding or
  removing a stakeholder, every change to T5 baselines and targets.

## References

- IIBA BABOK Guide v3, ch. 3 "Business Analysis Planning and Monitoring" —
  https://www.iiba.org/standards-and-resources/babok/
- IIBA Agile Extension to the BABOK Guide v2 — https://www.iiba.org/career-resources/agile-extension/
- PMI-PBA Practice Guide on Business Analysis — https://www.pmi.org/pmbok-guide-standards/practice-guides/business-analysis
- ISO/IEC/IEEE 29148:2018 Requirements Engineering — https://www.iso.org/standard/72089.html
- StrictDoc requirements-as-code toolkit — https://strictdoc.readthedocs.io
- Sibling: `business-analyst/ba-planning/agent-integration.md` (broader agent pattern)
- Sibling ba-core methodologies: `stakeholder-analysis/`, `ba-governance/`,
  `ba-requirements-mgmt/`, `elicitation-techniques/`, `requirements-lifecycle/`.
