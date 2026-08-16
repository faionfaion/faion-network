# Communications Management

## Summary

**One-sentence:** Plan, execute, and monitor stakeholder communications so the right people receive the right information at the right time via comms plan + status reports + action extraction.

**One-paragraph:** Plan, execute, and monitor stakeholder communications so the right people receive the right information at the right time via comms plan + status reports + action extraction. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-communications-management.py` enforces the output contract.

**Ефективно для:**

- Multi-stakeholder programs with varied information needs (exec, ops, dev, vendor).
- Distributed teams with timezone-driven async-first comms.
- Crisis comms during incidents or scope escalations.
- Programs where status fatigue erodes stakeholder engagement.

## Applies If (ALL must hold)

- Stakeholder register exists with ≥3 segments.
- Comms plan can be authored before delivery starts.
- Tooling exists for status distribution (email, Slack, dashboard).

## Skip If (ANY kills it)

- Single-stakeholder side project.
- Team < 3 with co-located workspace and verbal sync.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder register | CSV/YAML | PM |
| Comms channels inventory | list | PM + IT |
| Status report cadence | weekly/biweekly | Sponsor |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[seven-performance-domains]] | comms lives within Stakeholders domain |

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
| `draft-comms-plan` | sonnet | Judgement: channel + cadence per segment. |
| `extract-actions` | haiku | Mechanical: regex/heuristic on transcript. |
| `score-engagement` | haiku | Roll-up of opens/replies/attendance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/comms-plan.md.j2` | Comms plan template: segment × channel × cadence × content × owner |
| `templates/comms-plan.md` | Comms plan template: segment × channel × cadence × content × owner Generated from `templates/comms-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/action-extractor.py` | Action extraction from meeting transcript → owner + due + linked issue |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[seven-performance-domains]]
- [[change-control]]
- [[project-integration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/action-extractor.py`

```python
"""action_extractor.py — extract action items from markdown meeting notes.

Matches lines like:
  - [ ] Deploy to staging @alice by 2026-05-01
  * [ ] Review SOW @bob due 2026-05-03
  - [x] Done item @carol by 2026-04-28

Usage:
  notes = open("meeting-notes.md").read()
  for action in extract(notes):
      print(action)
"""

import re

ACTION_RE = re.compile(
    r"(?:^|\n)\s*[-*]\s*\[\s*(?P<done>[xX ])?\s*\]\s*(?P<text>.+?)"
    r"(?:\s+@(?P<owner>\w[\w.-]*))?"
    r"(?:\s+(?:by|due)\s+(?P<due>\d{4}-\d{2}-\d{2}))?\s*(?=\n|$)",
    re.IGNORECASE | re.MULTILINE,
)


def extract(notes: str) -> list[dict]:
    """Return list of action items; items without owner or due date are flagged."""
    results = []
    for m in ACTION_RE.finditer(notes):
        text = m.group("text").strip()
        if not text:
            continue
        item = {
            "text": text,
            "owner": m.group("owner"),
            "due": m.group("due"),
            "complete": m.group("done") in ("x", "X"),
            "warnings": [],
        }
        if not item["owner"]:
            item["warnings"].append("no owner — add @name")
        if not item["due"]:
            item["warnings"].append("no due date — add 'by YYYY-MM-DD'")
        results.append(item)
    return results
```
