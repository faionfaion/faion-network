# Hybrid Delivery

## Summary

**One-sentence:** ADR for a hybrid delivery model that assigns predictive (stage-gate) or agile method per component by risk profile, with explicit translation boundaries.

**One-paragraph:** Hybrid Delivery defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 5 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Programs spanning regulated (compliance) and non-regulated (UI / integrations) components.
- Fixed-price contracts that require agile execution under predictive governance.
- Organisations migrating from pure waterfall and unable to flip the whole portfolio at once.
- Multi-vendor delivery where vendors run different methods.

## Applies If (ALL must hold)

- Program comprises >=2 components with materially different risk profiles.
- Stage-gate funding model is in effect at the program level.
- An execution PMO can enforce translation boundaries between methods.
- Components can be enumerated and tagged with risk profile.

## Skip If (ANY kills it)

- Single-component project — pure agile or pure predictive is the right call.
- Risk profile is uniform across components — hybrid adds overhead without benefit.
- No PMO authority to enforce translation boundaries — hybrid will collapse into mixed-mode chaos.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `hybrid-delivery_template_fill` | haiku | Bounded template fill, no judgement. |
| `hybrid-delivery_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `hybrid-delivery_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the hybrid-delivery ADR artefact. |
| `templates/hybrid-alignment.py` | Reference script aligning component method assignment with risk profile. |
| `templates/component-map.md` | Markdown skeleton listing components with method + risk profile + boundary contracts. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/hybrid-delivery.json",
  "type": "object",
  "required": [
    "adr_id",
    "program_id",
    "components",
    "translation_boundaries",
    "governance_cadence"
  ],
  "properties": {
    "adr_id": {
      "type": "string"
    },
    "program_id": {
      "type": "string"
    },
    "components": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "object",
        "required": [
          "name",
          "method",
          "risk_profile",
          "evidence"
        ],
        "properties": {
          "method": {
            "enum": [
              "Predictive",
              "Agile",
              "Hybrid"
            ]
          },
          "risk_profile": {
            "enum": [
              "compliance",
              "novel-tech",
              "vendor-driven",
              "low-risk-iterative"
            ]
          },
          "evidence": {
            "type": "array",
            "minItems": 1
          }
        }
      }
    },
    "translation_boundaries": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "from_component",
          "to_component",
          "artefact",
          "contract"
        ]
      }
    },
    "governance_cadence": {
      "type": "object",
      "required": [
        "stage_gates"
      ]
    }
  }
}
```

### `templates/hybrid-alignment.py`

```python
"""


"""hybrid-alignment.py — flag epics misaligned with their milestone from program.yaml.

Usage: python hybrid-alignment.py program.yaml
Input: YAML with milestones[]{id, due, epics[]{id, issues_done, issues_total, team}}
Exit 0 = aligned, exit 1 = issues found (written to stderr).
"""
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
                issues.append(f"{label}: PAST_DUE ({-days_left}d overdue, {pct:.0%} complete)")
            elif days_left < 14 and pct < 0.5:
                issues.append(f"{label}: AT_RISK ({days_left}d left, {pct:.0%} complete)")
            elif not epic.get("team"):
                issues.append(f"{label}: ORPHAN (no team assigned)")
    if issues:
        sys.stderr.write("\n".join(issues) + "\n")
        return 1
    print("All epics aligned with milestones.")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```
