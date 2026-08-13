# Scrum Ceremonies

## Summary

**One-sentence:** Defines the five Scrum events (Sprint Planning, Daily Standup, Sprint Review, Sprint Retrospective, Backlog Refinement) with time-boxes, facilitation patterns, and quality gates per sprint length.

**One-paragraph:** Defines the five Scrum events (Sprint Planning, Daily Standup, Sprint Review, Sprint Retrospective, Backlog Refinement) with time-boxes, facilitation patterns, and quality gates per sprint length. The methodology applies in pm-agile contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-scrum-ceremonies.py` enforces the output contract.

**Ефективно для:**

- Bootstrapping Scrum for a new team and wiring ceremonies into a PM tool (Jira, Linear, GitHub Projects).
- Replacing free-form standups with structured cadence after onboarding or merging teams.
- Remote/distributed Scrum optimisation — async standups, retro tools, recorded reviews.
- Evidence collection for transformations (sprint-goal achievement, retro-action follow-through, velocity stability).

## Applies If (ALL must hold)

- Cross-functional team of 3-9 delivering in 1-4 week iterations.
- Sprint goal must be falsifiable in one sentence.
- Retro actions must have an owner and a linked issue or they do not exist.

## Skip If (ANY kills it)

- Solo developer or pair — Scrum overhead exceeds value; use Kanban with lightweight reviews.
- Pure research or discovery teams with no incremental delivery.
- Crisis or incident periods — break-glass first.
- Hardware-heavy programs where 2-week sprints do not match material lead times.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product backlog (refined ≥1.5x capacity) | Markdown/Jira | Product Owner |
| Sprint length | int weeks | team agreement |
| Definition of Done | Markdown | team |
| PM tool credentials | API token | team admin |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[team-development]] | team must reach Norming before retros yield signal |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-sprint` | sonnet | Light judgement: backlog ready check + capacity arithmetic. |
| `score-retro` | haiku | Mechanical: count owned + linked actions vs un-owned. |
| `review-readiness` | haiku | Boolean checks on completion ratio, environment, invitees. |

## Templates

| File | Purpose |
|------|---------|
| `templates/retrospective.md` | Retro structure with metrics, formats (Start-Stop-Continue, 4Ls, Mad-Sad-Glad, Sailboat) and action table |
| `templates/sprint-planning.md` | Sprint Planning notes template with sprint goal box, top items, capacity, and Part-1/Part-2 split |
| `templates/sprint-review-readiness.py` | Pre-review gate script: completion ratio, demoable items, environment, invited stakeholders |
| `templates/standup-bot.yaml` | Geekbot async standup configuration with 3-question template and blocker SLA |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-scrum-ceremonies.py` | Validate the playbook-step artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[team-development]]
- [[tool-migration-basics]]
- [[value-stream-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/sprint-review-readiness.py`

```python
#!/usr/bin/env python3
"""sprint-review-readiness.py — gate for "is this sprint ready to demo?"

Usage: python sprint-review-readiness.py sprint.json
Input JSON: {committed_points, completed_points, committed: [{status, demoable}],
             demo_environment, invited_stakeholders, escaped_bugs}
Exit 0 = ready, exit 1 = not ready (reasons printed).
"""
from __future__ import annotations
import json
import sys


def main(path: str) -> int:
    s = json.load(open(path))
    issues = []
    ratio = s["completed_points"] / max(s["committed_points"], 1)
    if ratio < 0.6:
        issues.append(f"low completion ratio ({ratio:.0%}, threshold 60%)")
    if any(i["status"] != "Done" for i in s["committed"] if i.get("demoable")):
        issues.append("undone demoable items present")
    if not s.get("demo_environment"):
        issues.append("no demo environment URL specified")
    if not s.get("invited_stakeholders"):
        issues.append("no stakeholders invited")
    if s.get("escaped_bugs", 0) > 3:
        issues.append(f"too many escaped bugs to demo cleanly ({s['escaped_bugs']})")
    if issues:
        print("NOT READY:")
        for i in issues:
            print(f"  - {i}")
        return 1
    print("Sprint review ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
```

### `templates/standup-bot.yaml`

```yaml
# Geekbot Async Standup Configuration
standup:
  name: "Daily Standup"
  channel: "#team-standups"
  time: "09:00"
  timezone: "Europe/Kyiv"
  days:
    - monday
    - tuesday
    - wednesday
    - thursday
    - friday

  questions:
    - text: "What did you accomplish yesterday?"
      required: true

    - text: "What are you working on today?"
      required: true

    - text: "Any blockers or help needed?"
      required: true

    - text: "How are you feeling? (optional)"
      required: false

  settings:
    send_to_channel: true
    allow_edits: true
    remind_after_minutes: 30
    skip_on_absence: true

  escalation:
    # Blocker older than this triggers sync or SM escalation
    blocker_max_age_hours: 24
```
