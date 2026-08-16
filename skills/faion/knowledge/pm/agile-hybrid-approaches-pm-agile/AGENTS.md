# Agile and Hybrid Approaches

## Summary

**One-sentence:** Decision framework + ADR selecting Predictive / Agile / Hybrid delivery from five factors (clarity, stakeholder availability, risk, team experience, contract).

**One-paragraph:** Agile and Hybrid Approaches defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Project kickoff where the right delivery model is genuinely unclear.
- Fixed-price contracts needing agile execution under predictive governance.
- Regulated environments where parts must be predictive (validation) and parts agile (UI).
- Coaching engagement migrating from waterfall to agile; default-to-hybrid is the wrong move.

## Applies If (ALL must hold)

- Initiation phase of a project that has not yet committed to a delivery model.
- At least 2 of the 5 decision factors (clarity, stakeholders, risk, experience, contract) are answerable.
- A decision owner exists who can ratify the recommendation as an ADR.
- Project lifetime >=4 weeks (shorter scope: pick any approach, overhead not worth it).

## Skip If (ANY kills it)

- Team is already running stable Scrum or Kanban — switching to hybrid loses cadence.
- Pure exploration / research where any delivery framework is overhead.
- Crisis or incident response — use incident-response runbooks, not delivery selection.
- Cultural dysfunction is the real problem — hybrid won't fix accountability gaps.

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
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `agile-hybrid-approaches_template_fill` | haiku | Bounded template fill, no judgement. |
| `agile-hybrid-approaches_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `agile-hybrid-approaches_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the approach-selection ADR artefact. |
| `templates/sprint-plan.md.j2` | Sprint planning template: goal, capacity, backlog, dependencies, risks. |
| `templates/sprint-plan.md` | Sprint planning template: goal, capacity, backlog, dependencies, risks. Generated from `templates/sprint-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/kanban-board.md.j2` | Kanban board template with WIP limits and explicit policies. |
| `templates/kanban-board.md` | Kanban board template with WIP limits and explicit policies. Generated from `templates/kanban-board.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pick_approach.py` | YAML decision script that reads factor scores and recommends Predictive / Agile / Hybrid. |

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
  "$id": "https://faion.net/schemas/agile-hybrid-approaches.json",
  "type": "object",
  "required": [
    "adr_id",
    "project_id",
    "factor_scores",
    "recommendation",
    "decision_owner"
  ],
  "properties": {
    "adr_id": {
      "type": "string"
    },
    "project_id": {
      "type": "string"
    },
    "factor_scores": {
      "type": "object",
      "required": [
        "requirements_clarity",
        "stakeholder_availability",
        "risk_tolerance",
        "team_experience",
        "contract_type"
      ],
      "additionalProperties": {
        "type": "object",
        "required": [
          "score",
          "evidence"
        ],
        "properties": {
          "score": {
            "enum": [
              "P",
              "H",
              "A"
            ]
          },
          "evidence": {
            "type": "array",
            "minItems": 1
          }
        }
      }
    },
    "recommendation": {
      "type": "object",
      "required": [
        "approach",
        "rationale"
      ],
      "properties": {
        "approach": {
          "enum": [
            "Predictive",
            "Agile",
            "Hybrid"
          ]
        }
      }
    },
    "decision_owner": {
      "type": "string"
    },
    "phases": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "approach",
          "definition_of_done"
        ]
      }
    }
  }
}
```

### `templates/pick_approach.py`

```python
"""


"""Pick Predictive/Agile/Hybrid from a YAML decision file.

Usage:
    python pick_approach.py answers.yaml

answers.yaml format:
    requirements_clarity: P   # P | H | A
    stakeholder_availability: A
    risk_tolerance: H
    team_experience: A
    contract_type: H

Output: YAML with recommendation and per-factor scores.
"""
import sys

import yaml

FACTORS = [
    "requirements_clarity",
    "stakeholder_availability",
    "risk_tolerance",
    "team_experience",
    "contract_type",
]

ans = yaml.safe_load(open(sys.argv[1]))
score = {"P": 0, "A": 0, "H": 0}

for k in FACTORS:
    v = ans.get(k, "H")
    if v in score:
        score[v] += 1

if score["P"] >= 4:
    rec = "Predictive"
elif score["A"] >= 4:
    rec = "Agile"
else:
    rec = "Hybrid"

print(
    yaml.safe_dump(
        {"recommendation": rec, "scores": score},
        default_flow_style=False,
    )
)
```
