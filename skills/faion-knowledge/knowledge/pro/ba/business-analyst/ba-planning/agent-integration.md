# Agent Integration — Business Analysis Planning

## When to use

- Kicking off a multi-stakeholder initiative (>3 stakeholder groups) where elicitation, deliverables, and approval flow must be agreed before requirements work starts.
- Regulated programs (medical, fintech, gov, ISO 9001 / SOX) where auditors expect a documented BA approach with named approvers and a fixed deliverable list.
- Hybrid plan-driven + change-driven engagements where you must declare upfront which artifacts are baselined vs. living, so the team does not silently default to one extreme.
- Spinning up a new BA capability inside a delivery team that previously had none — the BA Approach Document plus weekly Activity Plan become the operating contract.
- Pairing with `stakeholder-analysis/`, `elicitation-techniques/`, and `requirements-lifecycle/` to seed their inputs (stakeholder list, technique selection, governance gates).

## When NOT to use

- Solo founder building an MVP — the planning ceremony is overhead; one-page lean canvas plus `continuous-discovery` covers it.
- Pure XP / Scrum teams running on a refined backlog where the Definition of Ready already encodes the BA approach.
- Initiatives smaller than ~2 weeks of effort with one stakeholder — the plan costs more than the work it organises.
- When the sponsor refuses to commit to a governance model in writing — without an approver the plan becomes shelfware.
- Throwaway prototypes, spikes, or research probes where the goal is learning, not delivery.

## Where it fails / limitations

- Plans drift from reality once execution starts; the BA Approach Document is rarely updated mid-flight, so by week 4 it lies. Treat it as a versioned artifact with a review cadence, not a one-shot deliverable.
- Stakeholder lists captured at plan time miss the real decision makers who only surface during elicitation. Every elicitation session must trigger a stakeholder-list diff.
- Estimating elicitation effort is notoriously inaccurate; "1 workshop" hides 4 hours of pre-work, 2 hours of facilitation, and 6 hours of synthesis. Track actuals to recalibrate.
- Plan-Driven vs. Change-Driven is a false binary in practice. Most real programs are 70/30 hybrids, and the README's three-row table over-simplifies — explicitly document which artifacts are baselined and which are living.
- LLMs anchor on whichever sample plan they last saw and propose plan-driven defaults even for agile contexts. Always pass the engagement model in the system prompt.
- Governance section is the most common skip — no approver named, no escalation path. Without these the rest of the plan is decorative.

## Agentic workflow

Treat the BA Approach Document as a Markdown file with YAML frontmatter (`engagement_id`, `approach`, `version`, `approver`, `last_reviewed`) committed to git alongside the project's `.aidocs/` or `.product/` tree. A planning subagent ingests context (initiative brief, org chart, prior post-mortems), proposes a draft plan, and emits the document as a patch — never overwriting an approved baseline without a CR. A weekly cron-driven activity-plan agent diffs the BA Approach against the live `stakeholder-analysis` register and the elicitation backlog, produces the next week's `BA Activity Plan`, and posts it for human approval. Replan triggers are deterministic: stakeholder added/removed, scope change merged, two missed elicitation sessions, or `last_reviewed` older than 14 days.

### Recommended subagents

- `faion-sdd-executor-agent` — drives the BA plan as SDD tasks. Each section (stakeholders, elicitation, deliverables, governance) becomes a `TASK-NN` with its own commit, execution report, and lifecycle (todo → in-progress → done). Plan reviews become PRs reviewed by the named approver.
- `faion-brainstorm` — diverge/converge cycle for picking the elicitation technique mix (interviews vs. workshops vs. observation) given stakeholder availability and culture; outputs a ranked technique list per stakeholder group.
- `faion-sdd-execution` (skill) — quality gates on the plan itself: did we name an approver? does each deliverable have a target? are technique choices justified?
- A custom `ba-planner-agent` (model: sonnet, per the README's Agent Selection table for "Gather and analyze requirements"): owns Steps 1–5 of the README — context, approach selection, stakeholder list seed, elicitation plan, deliverable list.
- A custom `ba-governance-agent` (model: opus): owns Step 6 — picks approvers, change process, escalation path; uses the stakeholder register and org chart, not LLM recall.
- A custom `ba-replanner-agent` (model: haiku): runs weekly via cron, diffs the plan against actuals, and emits a CR if drift exceeds a threshold (e.g. >2 stakeholders added, >1 missed sprint of elicitation).

### Prompt pattern

Two-shot pattern: context read → plan draft.

```
You are the BA planner. Produce a BA Approach Document v0.1 using the
template in ba-planning/README.md (sections 1–8). Engagement context:
{initiative_brief}. Org culture: {formal|informal|mixed}. Constraints:
{time_budget, stakeholder_availability, regulatory}.

Decision rules:
- If requirements clarity high AND change frequency low -> Plan-Driven.
- If clarity low OR continuous discovery active -> Change-Driven.
- Else Hybrid; declare per-artifact which is baselined vs. living.

Return strict JSON matching the template's section keys; do not invent
stakeholders not in {stakeholder_seed}; flag every gap as TODO(reason).
```

For weekly replan: `Diff the current BA Approach Document (attached) against
this week's stakeholder register and elicitation log. Return a CR-XXX patch
in the format from requirements-lifecycle/templates.md. Cap at 5 changes.`

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git log --follow` | Version history of the BA Approach Document; replaces the manual revision table. | preinstalled |
| `pre-commit` + custom hook | Block commits to `ba-plan.md` that drop the `approver` or `last_reviewed` field. | https://pre-commit.com |
| `yq` | Read/update YAML frontmatter (`yq -i '.last_reviewed = now' ba-plan.md`) in cron jobs. | `brew install yq` / `apt install yq` |
| `gh issue` / `gh pr` | Mirror plan deliverables and governance gates as issues so non-BA stakeholders see them in their tool. | https://cli.github.com |
| `dot` (Graphviz) | Render the stakeholder map and elicitation schedule from the YAML so the plan is self-documenting. | `apt install graphviz` |
| `pandoc` | Convert the Markdown plan to PDF/DOCX for stakeholders who refuse Markdown. | https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Render embedded Mermaid Gantt of the elicitation plan into PNG/SVG for status reports. | `npm i -g @mermaid-js/mermaid-cli` |
| `taskwarrior` / `todo.txt` | Track BA Activity Plan items in a CLI-driven todo store agents can read/write deterministically. | https://taskwarrior.org |
| `dateutil` (Python) / `gdate` | Compute review-cadence triggers (`last_reviewed + 14d`) without timezone bugs. | `pip install python-dateutil` |
| `csvkit` (`csvlook`, `csvsql`) | Aggregate stakeholder CSV exports from HRIS into the plan's stakeholder table. | `pip install csvkit` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (Cloud) | SaaS | REST v3 + JQL | Encode the plan as an Epic with sub-tasks per deliverable; elicitation sessions as Calendar issues. |
| Linear | SaaS | GraphQL API | Treat the plan as a Project with milestones for governance gates; agents transition states via `issueUpdate`. |
| Azure DevOps | SaaS | REST API | Plan = Iteration Plan; deliverables = Work Items with custom `ba_phase` field. |
| Notion | SaaS | REST API | Good for the human-readable plan; weak typing on state fields, easy for agents to corrupt — gate writes through a wrapper. |
| Confluence + Requirements blueprint | SaaS | REST API | Common enterprise default; pair with a state plugin so governance fields are not free-text. |
| Smartsheet | SaaS | REST API | Heavy in PMO orgs; plan as a sheet, agents drive via row updates. |
| Microsoft Planner / Project for the Web | SaaS | Graph API | Lightweight task plan; OK for activity plan, weak for governance. |
| Aha! / Productboard | SaaS | REST API | Roadmap-flavoured plans; better for product-led BA than enterprise BA. |
| StrictDoc | OSS | CLI + plain-text store | Best fit for agent workflows: text-first, git-native, lets the plan and the requirements share a repo. |
| Doorstop | OSS | Python API | Markdown + YAML, git-native, scriptable from agents. |
| Jama Connect | SaaS | REST API + webhooks | Enterprise; the BA approach lives as a "project profile" item agents can update. |
| Polarion ALM | SaaS/on-prem | REST + Webservices | Strong workflow engine; map the plan's governance to Polarion workflows. |
| Trello | SaaS | REST API | Acceptable for the weekly Activity Plan only; too thin for the BA Approach Document. |

## Templates & scripts

The README provides BA Approach Document and BA Activity Plan templates. Inline below is a Python script that validates a `ba-plan.md` frontmatter, checks the review cadence, and emits a JSON status — wire into pre-commit or cron.

```python
#!/usr/bin/env python3
"""ba_plan_check.py — validate BA Approach Document and emit status."""
from __future__ import annotations
import sys, json, datetime as dt, pathlib, yaml

REQUIRED = {"engagement_id","approach","version","approver","last_reviewed"}
APPROACHES = {"Plan-Driven","Change-Driven","Hybrid"}
MAX_AGE_DAYS = 14

def load_frontmatter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing frontmatter")
    fm = text.split("---", 2)[1]
    return yaml.safe_load(fm) or {}

def main(path_str: str) -> int:
    path = pathlib.Path(path_str)
    fm = load_frontmatter(path)
    errors: list[str] = []
    missing = REQUIRED - set(fm)
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    if fm.get("approach") not in APPROACHES:
        errors.append(f"approach must be one of {sorted(APPROACHES)}")
    age_days = None
    last = fm.get("last_reviewed")
    if isinstance(last, (dt.date, dt.datetime)):
        last_d = last if isinstance(last, dt.date) else last.date()
        age_days = (dt.date.today() - last_d).days
        if age_days > MAX_AGE_DAYS:
            errors.append(f"plan stale: {age_days}d > {MAX_AGE_DAYS}d")
    status = {"file": str(path), "errors": errors, "age_days": age_days,
              "ok": not errors}
    print(json.dumps(status, indent=2, default=str))
    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "ba-plan.md"))
```

## Best practices

- Keep the BA Approach Document in git as Markdown + YAML frontmatter; diffs become the change log, `git blame` is the audit trail, branches model proposed plan revisions.
- Name a single human approver in the frontmatter (`approver: ruslan@faion.net`) and gate updates with CODEOWNERS — no approver = no plan.
- Set `last_reviewed` and enforce a 14-day cadence via cron + `ba_plan_check.py`; staleness is the leading indicator of plan-reality drift.
- Declare per-artifact whether it is baselined or living (e.g. "stakeholder list: living, BRD: baselined v1.0") — kills the false Plan-Driven vs. Change-Driven binary.
- Tie every BA activity to a deliverable ID (`DEL-03`) and every deliverable to a requirement set; plug into `requirements-traceability/` so the plan is queryable.
- Track actual vs. planned elicitation effort in a CSV next to the plan; recalibrate every 2 weeks. The first plan is always wrong; the second is usually fine.
- Stakeholder list lives in `stakeholder-analysis/` and is referenced by ID, not duplicated. Single source of truth or it diverges within days.
- Use Mermaid Gantt embedded in the plan for the elicitation schedule; render to PNG with `mmdc` for executives who refuse Markdown.
- Bake replan triggers into the document itself ("replan if X happens") so agents can fire automatically rather than relying on a human noticing drift.
- For regulated contexts, sign the plan PDF (`pandoc -o plan.pdf`, then `gpg --detach-sign`) and store the signature in git; auditors accept this in lieu of paper.

## AI-agent gotchas

- Anchoring bias: LLMs default to whatever sample plan they last produced, usually plan-driven and over-formal. Always pass the engagement model and culture flags in the system prompt; reject outputs that ignore them.
- Stakeholder hallucination: agents will invent plausible-sounding stakeholders ("Director of UX") that do not exist. Constrain to a `stakeholder_seed` list and forbid additions outside it; flag gaps as `TODO(reason)`.
- Governance is the section LLMs skim. They produce vague text ("approval by leadership") instead of named roles. Validate that `approver` resolves to a real identity.
- Effort estimates are confabulated. Strip any time estimates from agent output and replace with complexity tiers (S/M/L); per repo policy, no time estimates in SDD docs.
- LLMs conflate Plan-Driven with Waterfall and Change-Driven with Scrum. Define both terms in the system prompt with the README's table; otherwise the plan inherits a process that does not match the team.
- Bulk replanning is dangerous. Cap any agent-driven plan update to N changes per run (e.g. 5) and require human review on the diff. A runaway replanner that rewrites half the deliverables is hard to undo.
- Frontmatter parsing fails silently when stakeholders paste smart quotes or em-dashes into YAML. Add a pre-commit hook that rejects non-ASCII in keys.
- When the agent revises the plan, force it to emit a unified diff or a CR patch, not the full new document — easier to review and preserves history.
- Token budget: at >50 stakeholders or >20 deliverables, do not load the whole plan into context. Index frontmatter only via `yq` and load full sections on demand.
- Human-in-the-loop checkpoints (mandatory): plan v1.0 sign-off, every approach change (Plan-Driven ↔ Change-Driven ↔ Hybrid), every CR that touches governance, every replan that adds/removes a stakeholder. The agent prepares the artifact; a human approves.
- Confusing BA Planning with Project Planning: agents borrow PMBOK schedule language and produce Gantt charts for everything. Keep the BA plan focused on analysis activities; defer schedule integration to `project-manager`.

## References

- IIBA BABOK Guide v3, ch. 3 "Business Analysis Planning and Monitoring" — https://www.iiba.org/standards-and-resources/babok/
- PMI-PBA Practice Guide on Business Analysis — https://www.pmi.org/pmbok-guide-standards/practice-guides/business-analysis
- ISO/IEC/IEEE 29148:2018 Requirements Engineering — https://www.iso.org/standard/72089.html
- StrictDoc requirements-as-code toolkit — https://strictdoc.readthedocs.io
- Mermaid Gantt syntax — https://mermaid.js.org/syntax/gantt.html
- Sibling methodologies in this repo: `stakeholder-analysis/`, `elicitation-techniques/`, `requirements-lifecycle/`, `requirements-traceability/`, `requirements-prioritization/`.
